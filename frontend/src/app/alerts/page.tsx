"use client";

import React, { useEffect, useState } from "react";
import { Bell } from "lucide-react";
import { apiFetch, formatDZD } from "@/lib/api";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [label, setLabel] = useState("تنبيه صالون L برغوة D36 في البليدة");
  const [maxPrice, setMaxPrice] = useState("130000");

  const load = () => apiFetch<{ items: any[] }>("/api/v1/alerts").then((d) => setAlerts(d.items)).catch(() => {});
  useEffect(() => { load(); }, []);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    await apiFetch("/api/v1/alerts", {
      method: "POST",
      body: JSON.stringify({ label, max_price_dzd: Number(maxPrice) || null, wilaya_code: "09", min_foam_density: "D36" }),
    });
    load();
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold flex items-center gap-2"><Bell className="w-6 h-6 text-emerald-500" /> التنبيهات الذكية (AGENT 16)</h1>
      <form onSubmit={create} className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 flex flex-col sm:flex-row gap-3 text-xs">
        <input value={label} onChange={(e) => setLabel(e.target.value)} className="flex-1 rounded-lg border border-wood-500/30 bg-transparent px-3 py-2" />
        <input type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2" placeholder="أقصى سعر دج" />
        <button type="submit" className="rounded-lg bg-emerald-500 text-navy-950 font-bold px-5 py-2">إنشاء تنبيه</button>
      </form>
      <div className="space-y-2">
        {alerts.map((a) => (
          <div key={a.id} className="rounded-xl border border-wood-500/20 bg-white dark:bg-navy-900 p-4 flex justify-between text-xs">
            <span className="font-bold">{a.label}</span>
            <span>الحد الأقصى: {formatDZD(a.max_price_dzd)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
