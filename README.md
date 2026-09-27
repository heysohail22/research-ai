# Autonomous AI Research Agent

An AI agent that gathers live web information, filters out noise and duplicate content, and generates a structured, actionable research summary with citations.

---

## ⚡ How It Works

```
User Query ──► Tavily Web Search ──► Relevance Filter & Deduplication ──► Gemini 3.5 Flash Synthesis ──► Structured Report
```

1. **Search**: Fetches live web results using Tavily Search API.
2. **Filter & Deduplicate**: Rejects low-relevance results (`score < 0.72`), normalizes URLs, and discards duplicate text using lexical overlap.
3. **Structured Synthesis**: Uses Gemini 3.5 Flash Lite to produce:
   - 📌 **Key points** (executive takeaways)
   - 🔍 **Important findings** (with inline citations `[1]`, `[2]`)
   - ⚡ **Actionable insights** (practical next steps)
   - 📚 **References & Sources** (clickable URLs and descriptions)

---

## 🚀 Quickstart

### 1. Backend Setup

```bash
cd backend
cp .env.example .env
# Add your TAVILY_API_KEY and GEMINI_API_KEY in .env

uv sync
uv run uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

*Or run via CLI:*
```bash
uv run python main.py "Recent breakthroughs in autonomous AI agents"
```

### 2. Frontend Setup

```bash
cd frontend
pnpm install
pnpm dev
```

Open **`http://localhost:3000`** in your browser.

---

## 📂 Project Structure

```
research-ai/
├── backend/
│   ├── app/
│   │   ├── config.py       # API keys & client initialization
│   │   ├── search.py       # Tavily search tool
│   │   ├── filter.py       # Relevance filter & lexical deduplicator
│   │   └── synthesizer.py  # Gemini structured report generator
│   ├── outputs/            # Saved markdown reports
│   ├── main.py             # CLI runner
│   └── server.py           # FastAPI server
└── frontend/               # Next.js web dashboard
```
