"use client";

import React, { useEffect, useState } from "react";
import { apiFetch, Product, formatDZD } from "@/lib/api";
import { useApp } from "@/components/AppContext";
import { RadarChart } from "@/components/RadarChart";

export default function ComparePage() {
  const { compareIds, toggleCompare } = useApp();
  const [data, setData] = useState<{ items: Product[]; insights: any } | null>(null);

  useEffect(() => {
    if (compareIds.length < 2) {
      setData(null);
      return;
    }
    apiFetch<{ items: Product[]; insights: any }>("/api/v1/compare", {
      method: "POST",
      body: JSON.stringify({ product_ids: compareIds }),
    })
      .then(setData)
      .catch(() => {});
  }, [compareIds]);

  if (compareIds.length < 2) {
    return (
      <div className="p-10 text-center rounded-2xl border border-wood-500/20">
        اختر منتجين على الأقل (حتى 6 منتجات) من صفحة العروض لبدء المقارنة المباشرة.
      </div>
    );
  }

  if (!data) return <div className="p-8 text-center">جاري تحليل الفروقات...</div>;

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">لوحة المقارنة الاحترافية ({data.items.length} / 6)</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5">
          <h2 className="font-bold text-sm mb-3">المخطط الراداري للفروقات الفنية</h2>
          <RadarChart products={data.items} />
        </div>

        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-3 text-xs">
          <h2 className="font-bold text-base text-emerald-600">إجابات المقارنة الذكية</h2>
          <p><strong>لماذا الأفضل جودة؟</strong> {data.insights.why_best_quality}</p>
          <p><strong>لماذا الأغلى سعراً؟</strong> {data.insights.why_most_expensive}</p>
          <p><strong>هل فرق السعر مبرر؟</strong> {data.insights.price_difference_justified ? "نعم، الأعلى سعراً يتصدر الجودة الموثقة." : "ليس بالضرورة — توجد عروض بقيمة أفضل مقابل السعر."}</p>
          {data.insights.verification_needed?.length > 0 && (
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30">
              <strong>معلومات يجب التحقق منها قبل الشراء:</strong>
              <ul className="list-disc mr-4 mt-1 space-y-1">
                {data.insights.verification_needed.map((v: any) => (
                  <li key={v.product_id}>{v.title}: {v.verify_before_buying.join("، ")}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900">
        <table className="w-full text-xs text-right">
          <thead className="bg-navy-900 text-ivory-50">
            <tr>
              <th className="p-3">المعيار</th>
              {data.items.map((p) => (
                <th key={p.id} className="p-3 min-w-[180px]">
                  <div>{p.title}</div>
                  <button onClick={() => toggleCompare(p.id)} className="text-[10px] text-amber-300 underline mt-1">
                    إزالة
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-wood-500/15">
            <tr>
              <td className="p-3 font-bold">السعر الحالي</td>
              {data.items.map((p) => <td key={p.id} className="p-3 font-bold text-emerald-600">{formatDZD(p.current_price_dzd)}</td>)}
            </tr>
            <tr>
              <td className="p-3 font-bold">التكلفة بالتوصيل</td>
              {data.items.map((p) => <td key={p.id} className="p-3">{formatDZD(p.total_cost_dzd)}</td>)}
            </tr>
            <tr>
              <td className="p-3 font-bold">نطاق الجودة (/100)</td>
              {data.items.map((p) => <td key={p.id} className="p-3 font-bold">{p.quality_score_min}–{p.quality_score_max}</td>)}
            </tr>
            <tr>
              <td className="p-3 font-bold">اكتمال البيانات</td>
              {data.items.map((p) => <td key={p.id} className="p-3">{p.data_completeness_score}%</td>)}
            </tr>
            <tr>
              <td className="p-3 font-bold">الرغوة</td>
              {data.items.map((p) => (
                <td key={p.id} className="p-3">
                  {p.foam_density_claimed || "غير محدد"} ({p.foam_density_documented ? "موثقة" : "ادعاء بائع"})
                </td>
              ))}
            </tr>
            <tr>
              <td className="p-3 font-bold">الخشب</td>
              {data.items.map((p) => <td key={p.id} className="p-3">{p.wood_type || "غير محدد (بيانات مفقودة)"}</td>)}
            </tr>
            <tr>
              <td className="p-3 font-bold">التعليق</td>
              {data.items.map((p) => <td key={p.id} className="p-3">{p.suspension_type || "غير محدد (بيانات مفقودة)"}</td>)}
            </tr>
            <tr>
              <td className="p-3 font-bold">الضمان</td>
              {data.items.map((p) => <td key={p.id} className="p-3">{p.warranty_months ? `${p.warranty_months} شهر` : "غير محدد"}</td>)}
            </tr>
            <tr>
              <td className="p-3 font-bold">الولاية</td>
              {data.items.map((p) => <td key={p.id} className="p-3">{p.seller.wilaya_name} ({p.seller.commune})</td>)}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
