import os
import re
from datetime import datetime
from typing import List, Dict, Any
from app.config import get_gemini_client, DEFAULT_MODEL

def generate_structured_summary(
    query: str, 
    sources: List[Dict[str, Any]], 
    save_to_file: bool = True,
    model_name: str = DEFAULT_MODEL
) -> str:
    """
    Uses Gemini LLM to synthesize research sources into a structured report:
    1. Key points
    2. Important findings (with inline citations [1], [2])
    3. Actionable insights
    4. References/Sources
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

    print(f"🤖 Synthesizing structured summary with Gemini ({model_name})...")
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    
    summary_markdown = response.text
    
    # Optionally save to outputs folder
    if save_to_file:
        os.makedirs("outputs", exist_ok=True)
        slug = re.sub(r"[^\w\s-]", "", query.lower()).strip().replace(" ", "_")[:40]
        filename = f"outputs/research_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(summary_markdown)
        print(f"💾 Summary saved to: {filename}")
        
    return summary_markdown
