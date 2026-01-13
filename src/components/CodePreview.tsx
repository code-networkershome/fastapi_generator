"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { Folder, FileCode } from "lucide-react";

const Editor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export default function CodePreview({ files, onUpdateFile }: { files: Record<string, string>, onUpdateFile: (path: string, content: string) => void }) {
    const [selectedPath, setSelectedPath] = useState(Object.keys(files)[0]);

    const paths = Object.keys(files).sort();

    return (
        <div className="flex-1 flex border border-white/10 rounded-xl overflow-hidden glass">
            {/* Sidebar / File Tree */}
            <div className="w-64 border-r border-white/10 bg-black/20 overflow-y-auto">
                <div className="p-4 uppercase text-xs font-bold text-white/40 tracking-widest">Files</div>
                <div className="space-y-1 p-2">
                    {paths.map(path => (
                        <button
                            key={path}
                            onClick={() => setSelectedPath(path)}
                            className={`w-full text-left px-3 py-2 rounded text-sm flex items-center space-x-2 transition ${selectedPath === path ? "bg-blue-600/20 text-blue-400" : "hover:bg-white/5"
                                }`}
                        >
                            <FileCode className="w-4 h-4" />
                            <span className="truncate">{path.split("/").pop()}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Editor */}
            <div className="flex-1 bg-[#1e1e1e]">
                <div className="p-2 bg-black/40 text-xs font-mono text-white/60 border-b border-white/5 px-4 flex justify-between items-center">
                    <span>{selectedPath}</span>
                </div>
                <Editor
                    height="100%"
                    theme="vs-dark"
                    path={selectedPath}
                    defaultLanguage="python"
                    value={files[selectedPath]}
                    onChange={(val) => onUpdateFile(selectedPath, val || "")}
                    options={{
                        minimap: { enabled: false },
                        fontSize: 14,
                        padding: { top: 16 }
                    }}
                />
            </div>
        </div>
    );
}
