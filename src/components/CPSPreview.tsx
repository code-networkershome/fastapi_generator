"use client";

export default function CPSPreview({ cps, onGenerate, loading }: { cps: any, onGenerate: () => void, loading: boolean }) {
    if (!cps) {
        return (
            <div className="glass p-6 rounded-xl h-64 flex items-center justify-center text-white/40 italic">
                Extract a specification first...
            </div>
        );
    }

    return (
        <div className="glass p-6 rounded-xl space-y-4 flex flex-col h-full">
            <pre className="flex-1 overflow-auto bg-black/40 p-4 rounded border border-white/10 text-xs font-mono">
                {JSON.stringify(cps, null, 2)}
            </pre>
            <button
                onClick={onGenerate}
                disabled={loading}
                className="w-full py-3 bg-green-600 disabled:bg-green-600/50 rounded-lg font-bold hover:bg-green-700 transition"
            >
                {loading ? "Generating..." : "Generate FastAPI Code"}
            </button>
        </div>
    );
}
