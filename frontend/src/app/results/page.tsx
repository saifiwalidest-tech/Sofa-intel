"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Bookmark, SlidersHorizontal, Factory, MapPin, PhoneCall, CheckCircle2 } from "lucide-react";
import { apiFetch, Product, Seller } from "@/lib/api";
import { ProductCard } from "@/components/ProductCard";

interface WilayaOption {
  code: string;
  name_ar: string;
  name_fr: string;
  offers_count: number;
}

function ResultsInner() {
  const sp = useSearchParams();
  const [items, setItems] = useState<Product[]>([]);
  const [suppliers, setSuppliers] = useState<Seller[]>([]);
  const [wilayas, setWilayas] = useState<WilayaOption[]>([]);
  const [tokens, setTokens] = useState<string[]>([]);
  const [q, setQ] = useState(sp.get("q") || "");
  const [wilayaCode, setWilayaCode] = useState(sp.get("wilaya_code") || "");
  const [sofaType, setSofaType] = useState("");
  const [foamDensity, setFoamDensity] = useState("");
  const [sourcePlatform, setSourcePlatform] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [documentedOnly, setDocumentedOnly] = useState(false);
  const [savedMsg, setSavedMsg] = useState("");

  useEffect(() => {
    apiFetch<{ wilayas: WilayaOption[] }>("/api/v1/geo/wilayas")
      .then((d) => setWilayas(d.wilayas))
      .catch(() => {});
  }, []);

  const fetchResults = async (overrideWilaya?: string) => {
    const activeWilaya = overrideWilaya !== undefined ? overrideWilaya : wilayaCode;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (activeWilaya) params.set("wilaya_code", activeWilaya);
    if (sofaType) params.set("sofa_type", sofaType);
    if (foamDensity) params.set("foam_density", foamDensity);
    if (sourcePlatform) params.set("source_platform", sourcePlatform);
    if (maxPrice) params.set("max_price", maxPrice);
    if (documentedOnly) params.set("documented_only", "true");

    const data = await apiFetch<{ items: Product[]; expanded_tokens: string[] }>(`/api/v1/products?${params.toString()}`);
    setItems(data.items);
    setTokens(data.expanded_tokens || []);

    if (activeWilaya) {
      const supRes = await apiFetch<{ items: Seller[] }>(`/api/v1/manufacturers?wilaya_code=${activeWilaya}`);
      setSuppliers(supRes.items);
    } else {
      setSuppliers([]);
    }
  };

  useEffect(() => {
    fetchResults().catch(() => {});
  }, [wilayaCode]);

  const saveCurrentSearch = async () => {
    await apiFetch("/api/v1/saved-searches", {
      method: "POST",
      body: JSON.stringify({
        name: q || `بحث مخصص (${wilayaCode || "كل الجزائر"})`,
        filters_json: { q, wilayaCode, sofaType, foamDensity, maxPrice, documentedOnly },
      }),
    });
    setSavedMsg("تم حفظ البحث بنجاح!");
  };

  const selectedWilayaObj = wilayas.find((w) => w.code === wilayaCode);

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
        <select
          value={wilayaCode}
          onChange={(e) => setWilayaCode(e.target.value)}
          className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2"
        >
          <option value="">كل الولايات (58 ولاية)</option>
          {wilayas.map((w) => (
            <option key={w.code} value={w.code}>
              {w.code} - {w.name_ar} ({w.offers_count})
            </option>
          ))}
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
        <select value={sourcePlatform} onChange={(e) => setSourcePlatform(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2">
          <option value="">كل المصادر والمنصات</option>
          <option value="facebook_marketplace">Facebook Marketplace</option>
          <option value="facebook_page">صفحات Facebook</option>
          <option value="instagram">Instagram</option>
          <option value="tiktok">TikTok</option>
          <option value="ouedkniss">Ouedkniss</option>
        </select>
        <input
          type="number"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          placeholder="أقصى سعر (دج)..."
          className="rounded-lg border border-wood-500/30 bg-transparent px-3 py-2"
        />
        <button
          onClick={() => fetchResults()}
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

      {wilayaCode && (
        <section className="rounded-2xl border border-emerald-500/30 bg-emerald-500/5 p-5 space-y-3">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <h2 className="font-bold text-base flex items-center gap-2">
              <Factory className="w-5 h-5 text-emerald-600" />
              معلومات الموردين والمصانع في ولاية {selectedWilayaObj ? `${selectedWilayaObj.code} — ${selectedWilayaObj.name_ar}` : wilayaCode} ({suppliers.length})
            </h2>
          </div>

          {suppliers.length === 0 ? (
            <p className="text-xs opacity-80">
              لا توجد بيانات موردين مسجلة أو موثقة حالياً في هذه الولاية داخل قاعدة البيانات المحلية (لا يتم اختلاق موردين غير موثقين). يمكنك إضافة مورد أو رابط إعلان عبر واجهة الإدخال المباشر.
            </p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              {suppliers.map((s) => (
                <div key={s.id} className="rounded-xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4 space-y-1.5">
                  <div className="flex items-center justify-between gap-2">
                    <strong className="text-sm">{s.name}</strong>
                    <span className="px-2 py-0.5 rounded-full bg-wood-500/20 text-wood-700 dark:text-wood-300 font-semibold">
                      {s.seller_type}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 opacity-85">
                    <MapPin className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                    <span>{s.wilaya_name} — {s.commune} | {s.business_address || "العنوان الدقيق غير متوفر"}</span>
                  </div>
                  <div className="flex items-center gap-1.5 opacity-85">
                    <PhoneCall className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                    <span>{s.public_contact || "لا توجد وسيلة اتصال عامة مسجلة"}</span>
                  </div>
                  <div className="flex flex-wrap gap-2 pt-1 text-[11px]">
                    <span className="font-semibold text-emerald-600">درجة الثقة: {s.trust_score}/100</span>
                    {s.has_written_warranty && <span className="inline-flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-emerald-500" /> ضمان مكتوب</span>}
                    {s.cash_on_delivery && <span className="inline-flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-emerald-500" /> دفع عند الاستلام</span>}
                    {s.custom_orders_supported && <span className="inline-flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-emerald-500" /> تفصيل حسب الطلب</span>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

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
