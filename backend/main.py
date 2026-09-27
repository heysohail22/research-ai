import sys
from app import search_web, filter_and_deduplicate, generate_structured_summary

def run_research(query: str, max_results: int = 8, min_score: float = 0.72) -> str:
    """
    Executes the research agent pipeline:
    1. Search external sources (Tavily)
    2. Relevance Filter & Deduplication
    3. Structured Report Synthesis (Gemini)
    """
    # 1. Search
    raw_results = search_web(query, max_results=max_results)
    
    # 2. Filter & Deduplicate
    filtered_results = filter_and_deduplicate(raw_results, min_score=min_score)
    
    # 3. Structured Summary
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
        
    run_research(user_query, max_results=8, min_score=0.72)
