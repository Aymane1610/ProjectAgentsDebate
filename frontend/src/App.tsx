import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send,
  Upload,
  Shield,
  Search,
  CheckCircle,
  XCircle,
  Scale,
  Zap,
  FileText,
  RefreshCw,
  MoreHorizontal
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

interface DebateRound {
  agent: string;
  content: string;
}

interface QueryResponse {
  query: string;
  debate_rounds: DebateRound[];
  sources: string[];
}

interface Status {
  index_ready: boolean;
  chunk_count: number;
  files_indexed: string[];
}

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<QueryResponse | null>(null);
  const [status, setStatus] = useState<Status | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Poll status
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/status`);
      setStatus(res.data);
    } catch (err) {
      console.error("Failed to fetch status", err);
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResults(null);
    setError(null);
    try {
      const res = await axios.post(`${API_BASE}/query`, { query });
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setResults(res.data);
      }
    } catch (err) {
      setError("The backend is not responding. Please check if the terminal is running.");
      console.error("Query failed", err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${API_BASE}/upload`, formData);
      await fetchStatus();
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setUploading(false);
    }
  };

  const getAgentIcon = (agent: string) => {
    switch (agent) {
      case 'Agent_Pro': return <CheckCircle className="text-black" size={20} />;
      case 'Agent_Contra': return <Shield className="text-black" size={20} />;
      case 'Agent_Judge': return <Scale className="text-black" size={20} />;
      case 'Agent_Synthesizer': return <Zap className="text-black" size={20} />;
      default: return <MoreHorizontal className="text-black" size={20} />;
    }
  };

  return (
    <div className="min-h-screen font-sans bg-white selection:bg-zinc-100 selection:text-black">

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <header className="flex justify-between items-end mb-16 pb-6 border-b-2 border-black">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col gap-1"
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-zinc-900 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">D</span>
              </div>
              <h1 className="text-xl font-semibold tracking-tight text-zinc-900">Debate Core</h1>
            </div>
            <span className="text-xs text-zinc-400 font-medium tracking-widest pl-11">ADVANCED RAG SYSTEM</span>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-6 text-sm"
          >
            <div className="flex items-center gap-2 text-zinc-500 bg-zinc-50 px-3 py-1.5 rounded-full border border-zinc-100">
              <div className={`w-1.5 h-1.5 rounded-full ${status?.index_ready ? 'bg-zinc-900' : 'bg-zinc-300'}`} />
              <span className="font-medium text-xs tracking-wide">{status?.index_ready ? 'SYSTEM ACTIVE' : 'OFFLINE'}</span>
            </div>

            <label className="cursor-pointer group">
              <input type="file" className="hidden" onChange={handleFileUpload} accept=".pdf" disabled={uploading} />
              <div className="flex items-center gap-2 text-zinc-500 hover:text-black transition-colors">
                {uploading ? <RefreshCw className="animate-spin" size={14} /> : <Upload size={14} />}
                <span className="text-xs font-semibold uppercase tracking-wider">Upload Source</span>
              </div>
            </label>
          </motion.div>
        </header>

        {/* Hero Section */}
        {!results && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h2 className="text-5xl font-bold mb-6 tracking-tight">
              High-Fidelity RAG <br />
              <span className="text-muted italic">Multi-Agent Debate</span>
            </h2>
            <p className="text-muted max-w-lg mx-auto mb-8">
              A precise data extraction system powered by competing AI agents.
              Zero hallucination, full traceability.
            </p>
          </motion.div>
        )}

        {/* Search Bar */}
        <form onSubmit={handleQuery} className="mb-12">
          <div className="relative group">
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
              <Search className="text-black" size={24} />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question..."
              className="w-full bg-white border-2 border-black rounded-xl py-5 pl-14 pr-20 text-xl text-black placeholder:text-zinc-400 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] focus:outline-none focus:translate-x-[2px] focus:translate-y-[2px] focus:shadow-none transition-all font-bold"
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-4 top-1/2 -translate-y-1/2 p-2 bg-black text-white rounded-lg hover:scale-105 transition-transform disabled:opacity-50"
            >
              {loading ? <RefreshCw className="animate-spin" size={20} /> : <Send size={20} />}
            </button>
          </div>
          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-6 p-4 border border-zinc-800 bg-zinc-900/50 text-zinc-300 text-sm font-mono flex items-center gap-3"
            >
              <XCircle size={16} className="text-white" />
              {error}
            </motion.div>
          )}
        </form>

        {/* Results Area */}
        <div ref={scrollRef}>
          {loading && (
            <div className="flex flex-col items-center justify-center py-20 gap-6">
              <div className="w-12 h-12 border-4 border-zinc-200 border-t-black rounded-full animate-spin"></div>
              <p className="text-black text-lg font-bold animate-pulse tracking-widest">DEBATING...</p>
            </div>
          )}

          <AnimatePresence>
            {results && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-16 pb-24"
              >
                <div className="grid gap-8">
                  {results.debate_rounds.map((round, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.1 }}
                      className={`relative border-2 border-black rounded-xl p-8 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] ${round.agent === 'Agent_Synthesizer' ? 'bg-zinc-50' : 'bg-white'
                        }`}
                    >
                      <div className="flex items-center gap-3 mb-6 border-b-2 border-black/5 pb-4">
                        {getAgentIcon(round.agent)}
                        <span className="font-black text-sm tracking-widest uppercase text-black">
                          {round.agent.replace('_', ' ')}
                        </span>
                        {round.agent === 'Agent_Synthesizer' && (
                          <span className="ml-auto bg-black text-white text-[10px] font-bold px-2 py-1 rounded">FINAL VERDICT</span>
                        )}
                      </div>

                      <div className={`prose prose-zinc max-w-none whitespace-pre-wrap leading-8 ${round.agent === 'Agent_Synthesizer'
                        ? 'text-black font-medium text-lg'
                        : 'text-zinc-700 font-normal'
                        }`}>
                        {round.content}
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* Sources Footer */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1 }}
                  className="pt-10 border-t-2 border-dashed border-zinc-300"
                >
                  <span className="text-xs font-black text-black uppercase tracking-widest block mb-4">Verified Evidence</span>
                  <div className="flex flex-wrap gap-3">
                    {results.sources.map((src, i) => (
                      <div key={i} className="flex items-center gap-2 text-xs font-bold border-2 border-black bg-white px-4 py-2 rounded-lg shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:translate-y-[1px] hover:translate-x-[1px] hover:shadow-none transition-all cursor-default">
                        <FileText size={14} className="text-black" />
                        {src}
                      </div>
                    ))}
                  </div>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

export default App;
