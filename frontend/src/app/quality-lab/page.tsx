"use client";

import React, { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function QualityLabPage() {
  const [weights, setWeights] = useState({ foam: 25, structure: 25, upholstery: 15, suspension: 15, craftsmanship: 10, warranty: 10 });
  const [ranked, setRanked] = useState<any[]>([]);
  const [lang, setLang] = useState<"ar" | "darja" | "fr">("darja");
  const [foam, setFoam] = useState("D36");
  const [wood, setWood] = useState("الزان (Hêtre)");
  const [checklist, setChecklist] = useState<{ questions: string[]; ready_message: string } | null>(null);

  const recalcScores = async () => {
    const res = await apiFetch<{ items: any[] }>("/api/v1/scoring/custom", {
      method: "POST",
      body: JSON.stringify(weights),
    });
    setRanked(res.items);
  };

  const generateChecklist = async () => {
    const res = await apiFetch<{ questions: string[]; ready_message: string }>("/api/v1/verification-lab/checklist", {
      method: "POST",
      body: JSON.stringify({ language: lang, foam_density: foam, wood_type: wood }),
    });
    setChecklist(res);
  };

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">مختبر تحليل الجودة والتحقق قبل الشراء</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <section className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-4">
          <h2 className="font-bold text-base">تخصيص أوزان Sofa Quality Index</h2>
          <div className="grid grid-cols-2 gap-3 text-xs">
            {Object.entries(weights).map(([k, v]) => (
              <label key={k} className="space-y-1">
                <span className="block font-semibold">{k}: {v}</span>
                <input
                  type="range"
                  min={0}
                  max={50}
                  value={v}
                  onChange={(e) => setWeights((prev) => ({ ...prev, [k]: Number(e.target.value) }))}
                  className="w-full accent-emerald-500"
                />
              </label>
            ))}
          </div>
          <button onClick={recalcScores} className="rounded-xl bg-emerald-500 text-navy-950 font-bold px-5 py-2 text-xs">
            إعادة ترتيب العروض بأوزاني
          </button>
          {ranked.length > 0 && (
            <div className="space-y-2 pt-2 text-xs">
              {ranked.map((r) => (
                <div key={r.id} className="flex justify-between p-2 rounded-lg bg-ivory-100 dark:bg-navy-800">
                  <span className="truncate max-w-[240px]">{r.title}</span>
                  <strong>{r.quality_score_min}–{r.quality_score_max}/100</strong>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-4">
          <h2 className="font-bold text-base">أداة الفحص وتوليد رسالة البائع</h2>
          <div className="grid grid-cols-3 gap-2 text-xs">
            <select value={lang} onChange={(e) => setLang(e.target.value as any)} className="rounded-lg border border-wood-500/30 bg-transparent px-2 py-2">
              <option value="darja">الدارجة الجزائرية</option>
              <option value="ar">العربية الفصحى</option>
              <option value="fr">Français</option>
            </select>
            <input value={foam} onChange={(e) => setFoam(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-2 py-2" placeholder="الرغوة (D36)" />
            <input value={wood} onChange={(e) => setWood(e.target.value)} className="rounded-lg border border-wood-500/30 bg-transparent px-2 py-2" placeholder="الخشب" />
          </div>
          <button onClick={generateChecklist} className="rounded-xl bg-navy-900 dark:bg-emerald-600 text-ivory-50 font-bold px-5 py-2 text-xs">
            توليد الأسئلة والرسالة الجاهزة
          </button>
          {checklist && (
            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 whitespace-pre-wrap">
                <strong>الرسالة الجاهزة لإرسالها للبائع:</strong>
                <p className="mt-1">{checklist.ready_message}</p>
              </div>
              <ul className="list-disc mr-4 space-y-1 opacity-85">
                {checklist.questions.map((q, i) => <li key={i}>{q}</li>)}
              </ul>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
