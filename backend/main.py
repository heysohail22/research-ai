import os
import sys
from dotenv import load_dotenv
from tavily import TavilyClient

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

def search_tavily(query: str, max_results: int = 5, include_raw_content: bool = True):
    client = get_tavily_client()
    
    print(f"\n🔍 Searching Tavily for: '{query}'...")
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_raw_content=include_raw_content,
    )
    
    results = response.get("results", [])
    print(f"\n✅ Found {len(results)} results:\n")
    print("=" * 80)
    
    for idx, item in enumerate(results, 1):
        title = item.get("title", "No Title")
        url = item.get("url", "")
        score = item.get("score", 0.0)
        content = item.get("content", "")
        raw_content = item.get("raw_content", "")
        
        print(f"[{idx}] {title}")
        print(f"    🔗 URL:   {url}")
        print(f"    📊 Score: {score:.3f}")
        print(f"    📝 Summary / Snippet:")
        print(f"       {content}\n")
        
        if raw_content:
            preview = raw_content[:400].replace("\n", " ").strip()
            print(f"    📄 Raw Content Preview ({len(raw_content)} chars):")
            print(f"       {preview}...\n")
        print("-" * 80)
        
    return results

if __name__ == "__main__":
    # Check if a query was passed as a command-line argument, or prompt the user
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Enter your search query (or press Enter for default): ").strip()
        if not user_query:
            user_query = "Recent developments in autonomous AI agents"
            
    search_tavily(user_query)
