"use client";

import React, { useEffect, useState } from "react";
import { apiFetch, formatDZD } from "@/lib/api";

export default function PriceObservatoryPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    apiFetch("/api/v1/price-observatory").then(setData).catch(() => {});
  }, []);

  if (!data) return <div className="p-8 text-center">جاري تحميل مرصد الأسعار...</div>;
  const st = data.market_stats;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">مرصد الأسعار (بالدينار الجزائري)</h1>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4">
          <div className="text-xs opacity-70">الوسيط السعري</div>
          <div className="text-xl font-black text-emerald-600">{formatDZD(st.median_dzd)}</div>
        </div>
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4">
          <div className="text-xs opacity-70">النطاق العادل</div>
          <div className="text-sm font-bold">{formatDZD(st.fair_min_dzd)} – {formatDZD(st.fair_max_dzd)}</div>
        </div>
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4">
          <div className="text-xs opacity-70">أدنى سعر</div>
          <div className="text-xl font-bold">{formatDZD(st.min_dzd)}</div>
        </div>
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4">
          <div className="text-xs opacity-70">أعلى سعر</div>
          <div className="text-xl font-bold">{formatDZD(st.max_dzd)}</div>
        </div>
      </div>

      <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5">
        <h2 className="font-bold mb-3">متوسط السعر حسب نوع الصالون</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
          {Object.entries(data.average_by_type_dzd).map(([k, v]) => (
            <div key={k} className="p-3 rounded-xl bg-ivory-100 dark:bg-navy-800 flex justify-between">
              <span className="font-semibold">{k}</span>
              <strong>{formatDZD(Number(v))}</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
