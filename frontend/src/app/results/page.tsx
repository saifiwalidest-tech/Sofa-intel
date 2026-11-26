"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Bookmark, SlidersHorizontal } from "lucide-react";
import { apiFetch, Product } from "@/lib/api";
import { ProductCard } from "@/components/ProductCard";

function ResultsInner() {
  const sp = useSearchParams();
  const [items, setItems] = useState<Product[]>([]);
  const [tokens, setTokens] = useState<string[]>([]);
  const [q, setQ] = useState(sp.get("q") || "");
  const [wilayaCode, setWilayaCode] = useState("");
  const [sofaType, setSofaType] = useState("");
  const [foamDensity, setFoamDensity] = useState("");
  const [woodType, setWoodType] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [documentedOnly, setDocumentedOnly] = useState(false);
  const [savedMsg, setSavedMsg] = useState("");

  const fetchResults = async () => {
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (wilayaCode) params.set("wilaya_code", wilayaCode);
    if (sofaType) params.set("sofa_type", sofaType);
    if (foamDensity) params.set("foam_density", foamDensity);
    if (woodType) params.set("wood_type", woodType);
    if (maxPrice) params.set("max_price", maxPrice);
    if (documentedOnly) params.set("documented_only", "true");

    const data = await apiFetch<{ items: Product[]; expanded_tokens: string[] }>(`/api/v1/products?${params.toString()}`);
    setItems(data.items);
    setTokens(data.expanded_tokens || []);
  };

  useEffect(() => {
    fetchResults().catch(() => {});
  }, []);

  const saveCurrentSearch = async () => {
    await apiFetch("/api/v1/saved-searches", {
      method: "POST",
      body: JSON.stringify({
        name: q || `بحث مخصص (${wilayaCode || "كل الجزائر"})`,
        filters_json: { q, wilayaCode, sofaType, foamDensity, woodType, maxPrice, documentedOnly },
      }),
    });
    setSavedMsg("تم حفظ البحث بنجاح!");
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">نتائج البحث المتقدمة ({items.length})</h1>
        <button
          onClick={saveCurrentSearch}
          className="inline-flex items-center gap-1.5 rounded-xl bg-wood-500 text-white px-4 py-2 text-xs font-bold"
        >
          <Bookmark className="w-4 h-4" />
          حفظ الفلاتر كبحث دائم
        </button>
      </div>

      {savedMsg && <div className="text-xs text-emerald-600 font-semibold">{savedMsg}</div>}

      <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4 grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-xs">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="كلمة مفتاحية..."
          className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2"
        />
        <select value={wilayaCode} onChange={(e) => setWilayaCode(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2">
          <option value="">كل الولايات</option>
          <option value="09">09 - البليدة</option>
          <option value="16">16 - الجزائر</option>
          <option value="19">19 - سطيف</option>
          <option value="31">31 - وهران</option>
          <option value="15">15 - تيزي وزو</option>
        </select>
        <select value={sofaType} onChange={(e) => setSofaType(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2">
          <option value="">كل الأشكال</option>
          <option value="l_shape">زاوية L</option>
          <option value="u_shape">صالون U</option>
          <option value="turkish">صالون تركي</option>
          <option value="modular">معياري Modular</option>
          <option value="sofa_bed">سرير Sofa Bed</option>
        </select>
        <select value={foamDensity} onChange={(e) => setFoamDensity(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2">
          <option value="">كل كثافات الرغوة</option>
          <option value="D36">D36</option>
          <option value="D40">D40</option>
          <option value="HR">HR</option>
          <option value="D35">D35</option>
        </select>
        <input
          type="number"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          placeholder="أقصى سعر (دج)..."
          className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2"
        />
        <button
          onClick={fetchResults}
          className="rounded-lg bg-emerald-500 text-navy-950 font-bold px-4 py-2 inline-flex items-center justify-center gap-1"
        >
          <SlidersHorizontal className="w-3.5 h-3.5" />
          تطبيق الفلاتر
        </button>

        <label className="col-span-full flex items-center gap-2 cursor-pointer">
          <input type="checkbox" checked={documentedOnly} onChange={(e) => setDocumentedOnly(e.target.checked)} />
          <span>إظهار العروض ذات كثافة الرغوة الموثقة بشهادة فقط</span>
        </label>
      </div>

      {tokens.length > 0 && (
        <div className="text-xs opacity-75">
          توسيع المرادفات متعددة اللغات: {tokens.slice(0, 10).join(" · ")}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {items.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}

export default function ResultsPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">جاري التحميل...</div>}>
      <ResultsInner />
    </Suspense>
  );
}
