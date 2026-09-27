from typing import List, Dict, Any
from app.config import get_tavily_client

def search_web(
    query: str, 
    max_results: int = 8, 
    search_depth: str = "advanced",
    include_raw_content: bool = False
) -> List[Dict[str, Any]]:
    """
    Executes an external web search using Tavily.
    Returns cleaned raw results list with title, url, score, and content.
    """
    client = get_tavily_client()
    print(f"\n🔍 Searching Tavily for: '{query}' (requesting up to {max_results} results)...")
    
    response = client.search(
        query=query,
        search_depth=search_depth,
        max_results=max_results,
        include_raw_content=include_raw_content,
    )
    
    results = response.get("results", [])
    print(f"📥 Tavily returned {len(results)} raw results.")
    return results
