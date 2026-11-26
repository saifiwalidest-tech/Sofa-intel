"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function AdminPage() {
  const [adapters, setAdapters] = useState<any[]>([]);
  const [agents, setAgents] = useState<any[]>([]);

  useEffect(() => {
    apiFetch<{ adapters: any[] }>("/api/v1/adapters/status").then((d) => setAdapters(d.adapters)).catch(() => {});
    apiFetch<{ agents: any[] }>("/api/v1/agents/status").then((d) => setAgents(d.agents)).catch(() => {});
  }, []);

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">لوحة إدارة المنصة — حالة المصادر والوكلاء الـ 18</h1>

      <section className="space-y-3">
        <h2 className="font-bold text-lg">حالة محولات المصادر (Source Adapters)</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {adapters.map((a) => (
            <div key={a.id} className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4 text-xs space-y-1.5">
              <div className="flex justify-between items-center">
                <strong className="text-sm">{a.name}</strong>
                <span className={`px-2.5 py-0.5 rounded-full font-bold ${
                  a.status === "connected" ? "bg-emerald-500/20 text-emerald-600" :
                  a.status === "limited" ? "bg-amber-500/20 text-amber-600" : "bg-red-500/20 text-red-600"
                }`}>
                  {a.status}
                </span>
              </div>
              <div className="opacity-80">الوسيلة: {a.access_method}</div>
              <div className="opacity-70">{a.notes}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="font-bold text-lg">حالة الوكلاء الـ 18 (Multi-Agent System)</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          {agents.map((ag) => (
            <div key={ag.id} className="rounded-xl border border-wood-500/20 bg-white dark:bg-navy-900 p-3 flex justify-between items-center">
              <div>
                <div className="font-bold">{ag.id} — {ag.name}</div>
                <div className="opacity-75">{ag.role_ar}</div>
              </div>
              <span className="px-2 py-0.5 rounded bg-ivory-100 dark:bg-navy-800 font-mono text-[10px]">{ag.status}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
