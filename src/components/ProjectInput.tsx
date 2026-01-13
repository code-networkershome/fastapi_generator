"use client";

import { useState } from "react";

export default function ProjectInput({ onAnalyze, loading }: { onAnalyze: (text: string) => void, loading: boolean }) {
    const [text, setText] = useState("");

    return (
        <div className="glass p-6 rounded-xl space-y-4">
            <textarea
                className="w-full h-64 bg-transparent border border-white/10 rounded-lg p-4 focus:outline-none focus:border-blue-500 transition resize-none font-mono text-sm"
                placeholder="Describe your FastAPI project... e.g., 'A chat app with RAG using OpenAI, streaming enabled, and a POST endpoint at /ask'"
                value={text}
                onChange={(e) => setText(e.target.value)}
            />
            <button
                onClick={() => onAnalyze(text)}
                disabled={loading || !text}
                className="w-full py-3 bg-blue-600 disabled:bg-blue-600/50 rounded-lg font-bold hover:bg-blue-700 transition"
            >
                {loading ? "Analyzing..." : "Analyze Idea"}
            </button>
        </div>
    );
}
