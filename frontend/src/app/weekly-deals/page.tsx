"use client";

import React, { useEffect, useState } from "react";
import { apiFetch, Product } from "@/lib/api";
import { ProductCard } from "@/components/ProductCard";

export default function WeeklyDealsPage() {
  const [data, setData] = useState<{ pareto_front: Product[]; tiers: { economic: Product[]; balanced: Product[]; luxury: Product[] } } | null>(null);

  useEffect(() => {
    apiFetch<any>("/api/v1/optimize/pareto").then(setData).catch(() => {});
  }, []);

  if (!data) return <div className="p-8 text-center">جاري حساب الحد الأمثل لباريتو (Pareto Front)...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">أفضل العروض الأسبوعية ونتائج Pareto Front (AGENT 13)</h1>
        <p className="text-xs opacity-75">العروض التي لا يتفوق عليها أي عرض آخر في السعر والجودة والموثوقية معاً.</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {data.pareto_front.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}
