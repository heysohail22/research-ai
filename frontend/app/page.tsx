"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { 
  Search, 
  Sparkles, 
  BookOpen, 
  ExternalLink, 
  CheckCircle2, 
  Clock, 
  Copy, 
  Check, 
  AlertCircle,
  Cpu,
  Layers,
  FileText
} from "lucide-react";

interface ResearchSource {
  title: string;
  url: string;
  score: number;
  content: string;
}

interface ResearchData {
  query: string;
  summary: string;
  sources_count: number;
  sources: ResearchSource[];
}

const SUGGESTIONS = [
  "Recent breakthroughs in autonomous AI agents",
  "Solid-state battery commercial viability for EVs",
  "Quantum computing applications in drug discovery",
  "Next-generation nuclear SMR reactors",
];

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<ResearchData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [currentStep, setCurrentStep] = useState<string>("");

  const handleResearch = async (searchTopic?: string) => {
    const topicToSearch = searchTopic || query;
    if (!topicToSearch.trim()) return;

    setLoading(true);
    setError(null);
    setData(null);
    setCurrentStep("Searching Tavily for relevant web sources...");

    try {
      // Simulate real-time progress steps for better UX
      const stepTimer1 = setTimeout(() => {
        setCurrentStep("Applying relevance filter & lexical deduplication...");
      }, 1800);

      const stepTimer2 = setTimeout(() => {
        setCurrentStep("Synthesizing structured findings with Gemini 2.5...");
      }, 3500);

      const res = await fetch("http://localhost:8000/api/research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: topicToSearch, max_results: 8, min_score: 0.72 }),
      });

      clearTimeout(stepTimer1);
      clearTimeout(stepTimer2);

      if (!res.ok) {
        const errJson = await res.json().catch(() => ({ detail: "Failed to fetch" }));
        throw new Error(errJson.detail || "Error running research agent");
      }

      const result: ResearchData = await res.json();
      setData(result);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setLoading(false);
      setCurrentStep("");
    }
  };

  const handleCopy = () => {
    if (!data?.summary) return;
    navigator.clipboard.writeText(data.summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navigation */}
      <header className="border-b border-slate-800/80 bg-slate-900/50 backdrop-blur-md sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Cpu className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                ResearchAI Agent
              </span>
              <span className="ml-2.5 px-2 py-0.5 text-xs font-medium rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                Core Engine
              </span>
            </div>
          </div>
          <div className="text-xs text-slate-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Backend: <span className="text-slate-200 font-mono">FastAPI :8000</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8 flex flex-col gap-8">
        {/* Search Hero Area */}
        <section className="flex flex-col items-center text-center max-w-3xl mx-auto w-full pt-4">
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white mb-3">
            Autonomous Research Assistant
          </h1>
          <p className="text-slate-400 text-sm sm:text-base mb-6">
            Accepts any research topic, fetches external sources via Tavily, deduplicates &amp; filters noise, and produces a grounded 4-part structured executive summary.
          </p>

          {/* Search Box */}
          <div className="w-full relative shadow-2xl rounded-2xl bg-slate-900/80 border border-slate-700/80 p-2">
            <div className="flex items-center gap-2">
              <Search className="w-5 h-5 text-slate-400 ml-3 shrink-0" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !loading && handleResearch()}
                placeholder="Enter any research topic (e.g. Autonomous AI Agents)..."
                disabled={loading}
                className="w-full bg-transparent border-0 px-2 py-3 text-sm sm:text-base text-white placeholder-slate-500 focus:outline-none focus:ring-0 disabled:opacity-50"
              />
              <button
                onClick={() => handleResearch()}
                disabled={loading || !query.trim()}
                className="px-5 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-medium text-sm transition-all shadow-md shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shrink-0 cursor-pointer"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>Researching...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>Run Agent</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Quick Suggestions */}
          <div className="flex flex-wrap items-center justify-center gap-2 mt-4 text-xs">
            <span className="text-slate-500">Try asking:</span>
            {SUGGESTIONS.map((s, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setQuery(s);
                  handleResearch(s);
                }}
                disabled={loading}
                className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-800/80 transition-all cursor-pointer"
              >
                {s}
              </button>
            ))}
          </div>
        </section>

        {/* Loading Progress State */}
        {loading && (
          <div className="max-w-2xl mx-auto w-full bg-slate-900/60 border border-cyan-500/30 rounded-2xl p-6 shadow-xl backdrop-blur-sm animate-pulse">
            <div className="flex items-center space-x-4">
              <div className="w-8 h-8 rounded-full bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400">
                <Clock className="w-4 h-4 animate-spin" />
              </div>
              <div className="flex-1">
                <div className="text-sm font-semibold text-cyan-300">{currentStep}</div>
                <div className="text-xs text-slate-400 mt-1">
                  1. Search Web ➔ 2. Deduplicate &amp; Filter ➔ 3. Gemini Report Synthesis
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="max-w-2xl mx-auto w-full bg-rose-950/40 border border-rose-500/40 rounded-2xl p-5 flex items-start gap-3 text-rose-200">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div>
              <div className="font-semibold text-sm">Research Agent Error</div>
              <div className="text-xs text-rose-300/90 mt-1">{error}</div>
            </div>
          </div>
        )}

        {/* Results Area */}
        {data && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
            {/* Left 2 Cols: Report */}
            <div className="lg:col-span-2 bg-slate-900/70 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl">
              <div className="flex items-center justify-between pb-6 border-b border-slate-800 mb-6">
                <div>
                  <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                    <FileText className="w-3.5 h-3.5" /> Generated Report
                  </span>
                  <h2 className="text-xl sm:text-2xl font-bold text-white mt-1">
                    {data.query}
                  </h2>
                </div>
                <button
                  onClick={handleCopy}
                  className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 transition-all text-xs flex items-center gap-1.5 cursor-pointer"
                >
                  {copied ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Copied</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      <span>Copy Markdown</span>
                    </>
                  )}
                </button>
              </div>

              {/* Markdown Content */}
              <div className="prose prose-invert prose-cyan max-w-none text-slate-300 space-y-4 leading-relaxed text-sm sm:text-base">
                <ReactMarkdown
                  components={{
                    h1: ({ ...props }) => (
                      <h1 className="text-2xl font-extrabold text-white mt-4 mb-2 pb-2 border-b border-slate-800" {...props} />
                    ),
                    h2: ({ ...props }) => (
                      <h2 className="text-lg font-bold text-cyan-300 mt-6 mb-3 flex items-center gap-2" {...props} />
                    ),
                    h3: ({ ...props }) => (
                      <h3 className="text-base font-semibold text-slate-200 mt-4 mb-2" {...props} />
                    ),
                    ul: ({ ...props }) => (
                      <ul className="space-y-2 my-3 list-disc pl-5 text-slate-300" {...props} />
                    ),
                    ol: ({ ...props }) => (
                      <ol className="space-y-2 my-3 list-decimal pl-5 text-slate-300" {...props} />
                    ),
                    li: ({ ...props }) => (
                      <li className="text-slate-300 leading-normal" {...props} />
                    ),
                    strong: ({ ...props }) => (
                      <strong className="font-semibold text-white" {...props} />
                    ),
                    a: ({ ...props }) => (
                      <a className="text-cyan-400 hover:underline inline-flex items-center gap-0.5" target="_blank" rel="noreferrer" {...props} />
                    ),
                  }}
                >
                  {data.summary}
                </ReactMarkdown>
              </div>
            </div>

            {/* Right 1 Col: Verified Sources */}
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl sticky top-24">
              <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
                <div className="flex items-center gap-2">
                  <Layers className="w-4 h-4 text-cyan-400" />
                  <h3 className="font-semibold text-white text-sm">
                    Filtered Sources ({data.sources_count})
                  </h3>
                </div>
                <span className="text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">
                  Deduplicated
                </span>
              </div>

              <p className="text-xs text-slate-400 mb-4">
                Retained high-signal sources after relevance thresholding and lexical similarity checks:
              </p>

              <div className="space-y-3 max-h-[500px] overflow-y-auto pr-1">
                {data.sources.map((src, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 transition-all text-xs"
                  >
                    <div className="flex items-start justify-between gap-2 mb-1.5">
                      <span className="font-medium text-slate-200 line-clamp-1">
                        [{i + 1}] {src.title}
                      </span>
                      <a
                        href={src.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-cyan-400 hover:text-cyan-300 shrink-0"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    </div>
                    <p className="text-slate-400 line-clamp-3 leading-relaxed mb-2">
                      {src.content}
                    </p>
                    <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1.5 border-t border-slate-800/60">
                      <span>Score: <strong className="text-cyan-400">{src.score.toFixed(3)}</strong></span>
                      <span className="truncate max-w-[140px] text-slate-500">
                        {new URL(src.url).hostname.replace("www.", "")}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
