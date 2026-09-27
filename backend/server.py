import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import run_research, filter_and_deduplicate, get_tavily_client, generate_structured_summary

app = FastAPI(title="Autonomous Research Agent API", version="1.0.0")

# Allow requests from frontend (Next.js typically runs on port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str
    max_results: int = 8
    min_score: float = 0.75

class ResearchResponse(BaseModel):
    query: str
    summary: str
    sources_count: int
    sources: list

@app.get("/api/health")
def health_check():
    return {"status": "ok", "agent": "Autonomous Research Agent"}

@app.post("/api/research", response_model=ResearchResponse)
def conduct_research(request: ResearchRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        client = get_tavily_client()
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=request.max_results,
            include_raw_content=False,
        )
        raw_results = response.get("results", [])
        
        # 1. Relevance Filter & Deduplication
        filtered = filter_and_deduplicate(raw_results, min_score=request.min_score)
        
        # 2. Gemini Structured Summary
        summary = generate_structured_summary(query, filtered)
        
        return ResearchResponse(
            query=query,
            summary=summary,
            sources_count=len(filtered),
            sources=filtered
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
