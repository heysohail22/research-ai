from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app import search_web, filter_and_deduplicate, generate_structured_summary

app = FastAPI(title="Autonomous Research Agent API", version="1.0.0")

# CORS middleware for frontend access
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
    min_score: float = 0.72

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
        # 1. Search
        raw_results = search_web(query, max_results=request.max_results)
        
        # 2. Filter & Deduplicate
        filtered = filter_and_deduplicate(raw_results, min_score=request.min_score)
        
        # 3. Gemini Structured Summary
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
