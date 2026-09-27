import os
import sys
import re
from datetime import datetime
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai

# Load environment variables from .env
load_dotenv()

def get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key or api_key == "set the api":
        print("\n❌ Error: TAVILY_API_KEY is not set!")
        print("Please update backend/.env with your valid Tavily API key:")
        print('    TAVILY_API_KEY="tvly-xxxx..."\n')
        sys.exit(1)
    return TavilyClient(api_key=api_key)

def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("\n❌ Error: GEMINI_API_KEY is not set!")
        print("Please update backend/.env with your Gemini API key:")
        print('    GEMINI_API_KEY="AIzaSy..."\n')
        sys.exit(1)
    return genai.Client(api_key=api_key)

def normalize_url(url: str) -> str:
    """Normalize URL by stripping query parameters, fragments, and trailing slashes."""
    try:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", "", ""))
    except Exception:
        return url.strip().rstrip("/")

def get_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""

def filter_and_deduplicate(
    results: list, 
    min_score: float = 0.70, 
    min_content_length: int = 80,
    max_per_domain: int = 2,
    similarity_threshold: float = 0.70
) -> list:
    """
    Filters irrelevant results and removes duplicates:
    1. Relevance Filter: checks Tavily score threshold & minimum content length.
    2. URL Deduplication: detects duplicate or tracking-tagged links.
    3. Domain Diversity: avoids single-domain saturation.
    4. Content Deduplication: calculates lexical word overlap (Jaccard similarity).
    """
    cleaned = []
    seen_urls = set()
    domain_counts = {}
    
    print("\n🧹 --- Applying Relevance Filter & Deduplication ---")
    
    for item in results:
        title = item.get("title", "Untitled")
        raw_url = item.get("url", "")
        score = item.get("score", 0.0)
        content = item.get("content", "").strip()
        
        # 1. Relevance Score Filter
        if score < min_score:
            print(f"  🔻 [REJECTED - LOW RELEVANCE] ({score:.3f} < {min_score}): {title[:50]}...")
            continue
            
        # 2. Content Quality / Length Filter
        if len(content) < min_content_length:
            print(f"  🔻 [REJECTED - SHORT/NOISE] ({len(content)} chars): {title[:50]}...")
            continue
            
        # 3. URL Deduplication
        norm_url = normalize_url(raw_url)
        if norm_url in seen_urls:
            print(f"  🔻 [REJECTED - DUPLICATE URL]: {raw_url}")
            continue
            
        # 4. Domain Diversity Check
        domain = get_domain(norm_url)
        if domain_counts.get(domain, 0) >= max_per_domain:
            print(f"  🔻 [REJECTED - DOMAIN CAP]: Max {max_per_domain} reached for '{domain}'")
            continue
            
        # 5. Content Similarity (Lexical Overlap)
        current_words = set(content.lower().split())
        is_duplicate_content = False
        for accepted in cleaned:
            accepted_words = set(accepted.get("content", "").lower().split())
            intersection = len(current_words & accepted_words)
            min_size = min(len(current_words), len(accepted_words))
            
            if min_size > 0:
                overlap_ratio = intersection / min_size
                if overlap_ratio >= similarity_threshold:
                    print(f"  🔻 [REJECTED - DUPLICATE CONTENT] ({overlap_ratio:.1%} overlap with '{accepted.get('title')[:30]}...'): {title[:40]}...")
                    is_duplicate_content = True
                    break
                    
        if is_duplicate_content:
            continue
            
        # Passed all filters!
        seen_urls.add(norm_url)
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
        cleaned.append(item)
        print(f"  ✅ [ACCEPTED] ({score:.3f}): {title[:60]}")
        
    print(f"--- Filter complete: Retained {len(cleaned)} of {len(results)} items ---\n")
    return cleaned

def generate_structured_summary(query: str, sources: list) -> str:
    """
    Uses Gemini LLM to synthesize research sources into a structured report:
    - Key points
    - Important findings (with inline citations [1], [2])
    - References/Sources
    - Actionable insights
    """
    if not sources:
        return "No relevant sources found to generate summary."
        
    client = get_gemini_client()
    
    # Format sources for context window
    sources_text = ""
    for idx, item in enumerate(sources, 1):
        sources_text += f"[{idx}] Title: {item.get('title')}\n"
        sources_text += f"    URL: {item.get('url')}\n"
        sources_text += f"    Content Excerpt: {item.get('content')}\n\n"
        
    prompt = f"""You are an autonomous research intelligence agent.
Your task is to analyze the collected and deduplicated research findings below and produce a comprehensive, well-structured, actionable summary.

USER TOPIC / QUERY:
"{query}"

RESEARCH SOURCES:
{sources_text}

INSTRUCTIONS:
You MUST structure your response into the following 4 distinct sections:

# Research Report: {query}

## 1. 📌 Key Points
- Provide 3 to 5 concise executive bullet points summarizing the core takeaways.

## 2. 🔍 Important Findings
- Provide an in-depth analysis synthesized from the sources.
- Ground every claim with inline bracketed citations referencing the source numbers, e.g., [1], [2].
- Group related insights with subheadings if helpful.

## 3. ⚡ Actionable Insights
- Provide 3 to 5 concrete recommendations, real-world applications, or strategic next steps based on the findings.

## 4. 📚 References & Sources
- List each reference using the exact source numbers, formatted as:
  [#] [Title](URL) - Brief description of what this source contributed.

Maintain a professional, objective, and analytical tone. Do not fabricate information outside the provided sources."""

    print("🤖 Synthesizing structured summary with Gemini (gemini-2.5-flash)...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    summary_markdown = response.text
    
    # Save the markdown report to outputs directory
    os.makedirs("outputs", exist_ok=True)
    slug = re.sub(r"[^\w\s-]", "", query.lower()).strip().replace(" ", "_")[:40]
    filename = f"outputs/research_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary_markdown)
        
    print(f"\n💾 Summary saved to: {filename}")
    return summary_markdown

def run_research(query: str, max_results: int = 8, min_score: float = 0.70):
    client = get_tavily_client()
    
    print(f"\n🔍 Searching Tavily for: '{query}'...")
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_raw_content=False,
    )
    
    raw_results = response.get("results", [])
    print(f"📥 Tavily returned {len(raw_results)} raw results.")
    
    # 1. Relevance Filter & Deduplication
    filtered_results = filter_and_deduplicate(raw_results, min_score=min_score)
    
    # 2. Structured Summary Generation via Gemini LLM
    summary = generate_structured_summary(query, filtered_results)
    
    print("\n" + "=" * 80)
    print("📄 GENERATED STRUCTURED RESEARCH SUMMARY")
    print("=" * 80 + "\n")
    print(summary)
    print("\n" + "=" * 80)
    
    return summary

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = "Recent developments in autonomous AI agents"
        
    run_research(user_query, max_results=8, min_score=0.75)
