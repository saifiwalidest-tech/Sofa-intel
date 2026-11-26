"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Bot, Search } from "lucide-react";

export default function SmartSearchPage() {
  const router = useRouter();
  const [query, setQuery] = useState("صالون زاوية رغوة D36 خشب الزان");
  const [logs, setLogs] = useState<{ agent: string; progress: number; message: string }[]>([]);
  const [running, setRunning] = useState(false);

  const startOrchestratedSearch = () => {
    setRunning(true);
    setLogs([]);
    const wsBase = (process.env.NEXT_PUBLIC_WS_URL || "ws://127.0.0.1:8001").replace(/^http/, "ws");
    const ws = new WebSocket(`${wsBase}/ws/search/${Date.now()}`);
    ws.onmessage = (evt) => {
      const data = JSON.parse(evt.data);
      setLogs((prev) => [...prev, data]);
      if (data.progress >= 100) {
        setRunning(false);
        setTimeout(() => router.push(`/results?q=${encodeURIComponent(query)}`), 500);
      }
    };
    ws.onerror = () => {
      setRunning(false);
      router.push(`/results?q=${encodeURIComponent(query)}`);
    };
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">محرك البحث الذكي متعدد اللغات</h1>
      <p className="text-sm opacity-80">
        يفهم المرادفات الجزائرية (كنبة، صالون، موس 36، خشب الزان، salon en L، anti-tache) ويشغّل الوكلاء عبر WebSocket.
      </p>

      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 rounded-xl border border-wood-500/30 bg-white dark:bg-navy-900 px-4 py-3 text-sm"
          placeholder="اكتب مواصفات الصالون..."
        />
        <button
          onClick={startOrchestratedSearch}
          disabled={running}
          className="rounded-xl bg-emerald-500 text-navy-950 font-bold px-6 py-3 text-sm inline-flex items-center gap-2"
        >
          <Search className="w-4 h-4" />
          {running ? "جاري التحليل..." : "تشغيل الوكلاء"}
        </button>
      </div>

      {logs.length > 0 && (
        <div className="rounded-2xl border border-wood-500/25 bg-navy-900 text-ivory-50 p-5 space-y-3">
          <div className="font-bold text-sm flex items-center gap-2 text-emerald-400">
            <Bot className="w-4 h-4" />
            تقدم الوكلاء المباشر (WebSocket)
          </div>
          {logs.map((l, i) => (
            <div key={i} className="text-xs flex items-center justify-between border-b border-white/10 pb-2">
              <span>
                <strong className="text-wood-300">{l.agent}</strong>: {l.message}
              </span>
              <span className="text-emerald-400 font-mono">{l.progress}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
