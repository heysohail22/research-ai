from urllib.parse import urlparse, urlunparse
from typing import List, Dict, Any

def normalize_url(url: str) -> str:
    """Normalize URL by stripping query parameters, fragments, and trailing slashes."""
    try:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", "", ""))
    except Exception:
        return url.strip().rstrip("/")

def get_domain(url: str) -> str:
    """Extract base domain from a URL."""
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""

def filter_and_deduplicate(
    results: List[Dict[str, Any]], 
    min_score: float = 0.72, 
    min_content_length: int = 80,
    max_per_domain: int = 2,
    similarity_threshold: float = 0.70
) -> List[Dict[str, Any]]:
    """
    Filters irrelevant results and removes duplicates:
    1. Relevance Filter: checks Tavily score threshold & minimum content length.
    2. URL Deduplication: detects duplicate or tracking-tagged links.
    3. Domain Diversity: avoids single-domain saturation.
    4. Content Deduplication: calculates lexical word overlap (Jaccard similarity).
    """
    cleaned: List[Dict[str, Any]] = []
    seen_urls = set()
    domain_counts: Dict[str, int] = {}
    
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
