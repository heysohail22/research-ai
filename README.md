# Autonomous AI Research Agent

An autonomous research intelligence agent capable of collecting information from external live web sources, filtering noise and duplicates, and generating a structured, actionable executive summary with grounded citations.

Built for **Assessment Option 1: Autonomous Research Agent**.

---

## 🚀 Key Features

* **Live Web Intelligence**: Leverages the **Tavily Search API** with advanced search depth to retrieve high-signal web sources.
* **4-Stage Filtering & Deduplication**:
  1. **Neural Relevance Thresholding**: Automatically filters out lower-confidence results (`score < 0.72`).
  2. **Content Quality & Noise Removal**: Discards ultra-short snippets, cookie notices, and empty fragments (`< 80 characters`).
  3. **URL Normalization**: Strips tracking tags (`?utm_...`, `#fragments`) and normalizes paths to prevent duplicate sources.
  4. **Domain Diversity Capping**: Limits results per domain to prevent single-source bias.
  5. **Lexical Jaccard Deduplication**: Calculates word-level overlap and discards syndicated/duplicate articles.
* **Structured Report Generation**: Uses **Gemini 3.5 Flash Lite** to synthesize a comprehensive research dossier containing:
  * 📌 **Key Points**: 3 to 5 executive-level bullet takeaways.
  * 🔍 **Important Findings**: In-depth analysis with grounded inline citations (`[1]`, `[2]`).
  * ⚡ **Actionable Insights**: Concrete recommendations, strategic applications, or next steps.
  * 📚 **References & Sources**: Complete bibliography with clickable URLs and source contributions.
* **Dual Interface**:
  * **Interactive Web UI**: Modern Next.js + React 19 interface with real-time status steps, markdown rendering, and a filtered sources inspector.
  * **Clean CLI Runner**: Fast command-line execution for automated scripting.
* **Automatic File Export**: Automatically timestamps and saves every generated report as a clean Markdown file in `backend/outputs/`.

---

## 🏛 Architecture

```mermaid
graph TD
    User([User Query / Topic]) --> Search[1. External Web Search (Tavily API)]
    Search --> Filter[2. Relevance & Length Filter]
    Filter --> URLDedupe[3. URL Normalization & Domain Capping]
    URLDedupe --> ContentDedupe[4. Lexical Content Deduplication]
    ContentDedupe --> Synthesizer[5. Gemini 3.5 Flash Lite Synthesis]
    Synthesizer --> OutputMD[Saved to outputs/*.md]
    Synthesizer --> UI[Web UI / CLI Display]
```

---

## 📂 Project Structure

```
research-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # Exposes search_web, filter, synthesizer
│   │   ├── config.py          # Environment loading & client initializations
│   │   ├── search.py          # Tavily search wrapper
│   │   ├── filter.py          # 4-stage relevance & deduplication pipeline
│   │   └── synthesizer.py     # Gemini structured synthesis prompt & file saving
│   ├── outputs/               # Automatically generated .md research dossiers
│   ├── main.py                # Lightweight CLI runner
│   ├── server.py              # FastAPI REST backend (runs on :8000)
│   ├── pyproject.toml         # Python dependencies (managed via uv)
│   └── .env                   # API keys (Tavily & Gemini)
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # Interactive Next.js research dashboard
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Tailwind CSS styles
│   ├── package.json           # Frontend dependencies (managed via pnpm)
│   └── tsconfig.json          # TypeScript configuration
└── README.md
```

---

## 🛠️ Setup & Installation

### Prerequisites
* [Python 3.12+](https://www.python.org/) & [`uv`](https://github.com/astral-sh/uv) (fast Python package manager)
* [Node.js 18+](https://nodejs.org/) & [`pnpm`](https://pnpm.io/)
* [Tavily API Key](https://app.tavily.com)
* [Google Gemini API Key](https://aistudio.google.com/app/apikey)

---

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Open `backend/.env` and add your keys:
   ```env
   TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxx"
   GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere..."
   GEMINI_MODEL="gemini-3.5-flash-lite"
   ```

4. Install backend dependencies:
   ```bash
   uv sync
   ```

---

### 2. Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

---

## 💻 Running the Application

### Option A: Using the Web UI (Recommended)

1. **Start the FastAPI Backend** (from `backend/`):
   ```bash
   uv run uvicorn server:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the Next.js Frontend** (from `frontend/`):
   ```bash
   pnpm dev
   ```

3. Open **`http://localhost:3000`** in your browser.
4. Enter any topic (or click a suggestion), and click **"Run Agent"**.

---

### Option B: Using the CLI

Run the research agent directly from your terminal:

```bash
cd backend
uv run python main.py "Quantum computing applications in drug discovery"
```

The CLI will:
1. Fetch live sources from Tavily.
2. Display a log of accepted vs. rejected sources (with reasons).
3. Synthesize the 4-part executive report.
4. Save the report to `backend/outputs/` and print it to your terminal.

---

## 🧪 Sample Queries to Test

Try running these topics to test various research domains:
* `Recent breakthroughs in autonomous AI agent orchestration and tool use in 2026`
* `Commercial viability and production challenges of solid-state EV batteries`
* `Quantum computing applications in molecular simulation and drug discovery`
* `Cybersecurity implications of post-quantum cryptography transition`
