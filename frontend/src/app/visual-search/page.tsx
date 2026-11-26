"use client";

import React, { useState } from "react";
import { Image as ImageIcon } from "lucide-react";
import { apiFetch, Product } from "@/lib/api";
import { ProductCard } from "@/components/ProductCard";

export default function VisualSearchPage() {
  const [sofaType, setSofaType] = useState("l_shape");
  const [color, setColor] = useState("كحلي");
  const [seatsCount, setSeatsCount] = useState(6);
  const [filename, setFilename] = useState("");
  const [matches, setMatches] = useState<{ similarity_percent: number; product: Product }[]>([]);
  const [note, setNote] = useState("");

  const runSearch = async () => {
    const res = await apiFetch<any>("/api/v1/visual-search", {
      method: "POST",
      body: JSON.stringify({ sofa_type: sofaType, color, seats_count: seatsCount, image_filename: filename }),
    });
    setMatches(res.matches || []);
    setNote(res.guardrail_note || "");
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <ImageIcon className="w-6 h-6 text-emerald-500" />
        البحث عن أريكة باستخدام صورة
      </h1>
      <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFilename(e.target.files?.[0]?.name || "")}
          className="rounded-lg border border-wood-500/30 p-2"
        />
        <select value={sofaType} onChange={(e) => setSofaType(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2">
          <option value="l_shape">زاوية L</option>
          <option value="u_shape">صالون U</option>
          <option value="turkish">صالون تركي</option>
          <option value="modular">معياري Modular</option>
          <option value="sofa_bed">سرير Sofa Bed</option>
        </select>
        <input value={color} onChange={(e) => setColor(e.target.value)} placeholder="اللون الظاهر..." className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2" />
        <button onClick={runSearch} className="rounded-lg bg-emerald-500 text-navy-950 font-bold px-4 py-2">
          بحث بصري
        </button>
      </div>
      {note && <div className="text-xs p-3 rounded-xl bg-amber-500/10 border border-amber-500/30">{note}</div>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {matches.map((m) => (
          <div key={m.product.id} className="space-y-1">
            <div className="text-xs font-bold text-emerald-600">التشابه البصري: {m.similarity_percent}%</div>
            <ProductCard product={m.product} />
          </div>
        ))}
      </div>
    </div>
  );
}
