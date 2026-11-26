"use client";

import React, { useEffect, useState } from "react";
import { Factory, CheckCircle2 } from "lucide-react";
import { apiFetch, Seller } from "@/lib/api";

export default function ManufacturersPage() {
  const [sellers, setSellers] = useState<Seller[]>([]);

  useEffect(() => {
    apiFetch<{ items: Seller[] }>("/api/v1/manufacturers")
      .then((d) => setSellers(d.items))
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">دليل المصانع والحرفيين في الجزائر (AGENT 06)</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sellers.map((s) => (
          <div key={s.id} className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-2">
            <div className="flex items-center justify-between">
              <div className="font-bold flex items-center gap-2">
                <Factory className="w-4 h-4 text-emerald-500" />
                {s.name}
              </div>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-wood-500/20 text-wood-700 dark:text-wood-300 font-semibold">
                {s.seller_type}
              </span>
            </div>
            <div className="text-xs opacity-80">{s.wilaya_name} — {s.commune} | {s.business_address || "العنوان غير محدد"}</div>
            <div className="flex flex-wrap gap-2 text-[11px] pt-2">
              {s.custom_orders_supported && <span className="inline-flex items-center gap-1 text-emerald-600"><CheckCircle2 className="w-3 h-3" /> تفصيل حسب الطلب</span>}
              {s.has_written_warranty && <span className="inline-flex items-center gap-1 text-emerald-600"><CheckCircle2 className="w-3 h-3" /> ضمان مكتوب</span>}
              {s.cash_on_delivery && <span className="inline-flex items-center gap-1 text-emerald-600"><CheckCircle2 className="w-3 h-3" /> الدفع عند الاستلام</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
