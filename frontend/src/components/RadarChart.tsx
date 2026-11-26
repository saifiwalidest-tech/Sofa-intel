"use client";

import React from "react";
import { Product } from "@/lib/api";

const AXES = [
  { key: "quality_score_midpoint", label: "الجودة" },
  { key: "value_for_money_score", label: "القيمة/السعر" },
  { key: "evidence_confidence_score", label: "الموثوقية" },
  { key: "data_completeness_score", label: "اكتمال البيانات" },
  { key: "comfort_suitability_score", label: "الراحة" },
  { key: "delivery_cost_score", label: "التوصيل" },
] as const;

const COLORS = ["#10B981", "#C89B6E", "#3B82F6", "#F59E0B", "#EC4899", "#8B5CF6"];

export function RadarChart({ products }: { products: Product[] }) {
  const cx = 170;
  const cy = 155;
  const radius = 105;
  const n = AXES.length;

  const pointAt = (idx: number, val: number) => {
    const angle = (Math.PI * 2 * idx) / n - Math.PI / 2;
    const r = (Math.max(0, Math.min(100, val)) / 100) * radius;
    return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
  };

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 340 310" className="w-full max-w-md">
        {[25, 50, 75, 100].map((ring) => {
          const pts = AXES.map((_, i) => pointAt(i, ring).join(",")).join(" ");
          return <polygon key={ring} points={pts} fill="none" stroke="currentColor" strokeOpacity={0.15} />;
        })}
        {AXES.map((ax, i) => {
          const [x2, y2] = pointAt(i, 100);
          const [lx, ly] = pointAt(i, 120);
          return (
            <g key={ax.key}>
              <line x1={cx} y1={cy} x2={x2} y2={y2} stroke="currentColor" strokeOpacity={0.2} />
              <text x={lx} y={ly} textAnchor="middle" fontSize="10" fill="currentColor">
                {ax.label}
              </text>
            </g>
          );
        })}
        {products.map((p, idx) => {
          const pts = AXES.map((ax, i) => pointAt(i, Number(p[ax.key] ?? 0)).join(",")).join(" ");
          const col = COLORS[idx % COLORS.length];
          return (
            <polygon
              key={p.id}
              points={pts}
              fill={col}
              fillOpacity={0.16}
              stroke={col}
              strokeWidth={2}
            />
          );
        })}
      </svg>
      <div className="flex flex-wrap justify-center gap-3 text-xs mt-2">
        {products.map((p, idx) => (
          <span key={p.id} className="inline-flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[idx % COLORS.length] }} />
            <span className="truncate max-w-[160px]">{p.title}</span>
          </span>
        ))}
      </div>
    </div>
  );
}
