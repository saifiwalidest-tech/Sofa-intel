"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ExternalLink, ShieldCheck, AlertTriangle } from "lucide-react";
import { apiFetch, Product, formatDZD } from "@/lib/api";

export default function ProductDetailPage() {
  const params = useParams<{ id: string }>();
  const [data, setData] = useState<{ product: Product; agent_analysis: any } | null>(null);

  useEffect(() => {
    if (!params?.id) return;
    apiFetch<{ product: Product; agent_analysis: any }>(`/api/v1/products/${params.id}`)
      .then(setData)
      .catch(() => {});
  }, [params?.id]);

  if (!data) return <div className="p-8 text-center">جاري تحميل التحليل الهندسي...</div>;
  const { product, agent_analysis } = data;

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <img
            src={product.images?.[0] || "/images/sofa-l-navy.svg"}
            alt={product.title}
            className="w-full h-72 object-cover rounded-2xl border border-wood-500/30"
          />
          <h1 className="text-2xl font-extrabold">{product.title}</h1>
          <p className="text-sm opacity-85">{product.description}</p>

          <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-3">
            <h2 className="font-bold text-base">التحليل الفني والهندسي للمنتج</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-ivory-100 dark:bg-navy-800">
                <div className="font-bold text-emerald-600">تحليل الرغوة</div>
                <div>{agent_analysis.foam_analysis.summary}</div>
              </div>
              <div className="p-3 rounded-xl bg-ivory-100 dark:bg-navy-800">
                <div className="font-bold text-emerald-600">الخشب والهيكل</div>
                <div>{agent_analysis.wood_analysis.summary}</div>
              </div>
              <div className="p-3 rounded-xl bg-ivory-100 dark:bg-navy-800">
                <div className="font-bold text-emerald-600">القماش والتعليق</div>
                <div>{agent_analysis.upholstery_analysis.summary}</div>
              </div>
              <div className="p-3 rounded-xl bg-ivory-100 dark:bg-navy-800">
                <div className="font-bold text-emerald-600">قناة البيع والمصدر</div>
                <div>{agent_analysis.channel_analysis.label_ar}: {agent_analysis.channel_analysis.note}</div>
              </div>
              {agent_analysis.category_specialist && (
                <div className="sm:col-span-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                  <div className="font-bold text-emerald-700 dark:text-emerald-400">معايير الفئة الهندسية</div>
                  <div>{agent_analysis.category_specialist.technical_note}</div>
                </div>
              )}
            </div>
          </div>

          <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-3">
            <h2 className="font-bold text-base">مصدر كل حقل وتوثيقه (Field-Level Provenance)</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-wood-500/20 text-right">
                    <th className="py-2">الحقل</th>
                    <th className="py-2">القيمة</th>
                    <th className="py-2">الحالة</th>
                    <th className="py-2">درجة الثقة</th>
                  </tr>
                </thead>
                <tbody>
                  {product.provenance_fields?.map((f, i) => (
                    <tr key={i} className="border-b border-wood-500/10">
                      <td className="py-2 font-mono">{f.field_name}</td>
                      <td className="py-2">{f.field_value || "غير متوفرة"}</td>
                      <td className="py-2">
                        <span className="px-2 py-0.5 rounded-full bg-ivory-100 dark:bg-navy-800">
                          {f.verification_status}
                        </span>
                      </td>
                      <td className="py-2">{Math.round(f.confidence * 100)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <aside className="space-y-4">
          <div className="rounded-2xl border border-wood-500/30 bg-white dark:bg-navy-900 p-5 space-y-3">
            <div className="text-2xl font-black text-emerald-600">{formatDZD(product.current_price_dzd)}</div>
            <div className="text-xs opacity-75">التوصيل: {formatDZD(product.delivery_cost_dzd)} · الإجمالي: {formatDZD(product.total_cost_dzd)}</div>
            <div className="p-3 rounded-xl bg-ivory-100 dark:bg-navy-800 text-xs space-y-1">
              <div className="flex justify-between">
                <span>نطاق الجودة:</span>
                <strong>{product.quality_score_min}–{product.quality_score_max}/100</strong>
              </div>
              <div className="flex justify-between">
                <span>اكتمال البيانات:</span>
                <strong>{product.data_completeness_score}%</strong>
              </div>
              <div className="flex justify-between">
                <span>ثقة الأدلة:</span>
                <strong>{product.evidence_confidence_score}%</strong>
              </div>
              <div className="flex justify-between">
                <span>القيمة مقابل السعر:</span>
                <strong>{product.value_for_money_score}/100</strong>
              </div>
            </div>

            <div className="text-xs space-y-1 pt-2">
              <div className="font-bold flex items-center gap-1">
                <ShieldCheck className="w-4 h-4 text-emerald-500" />
                مؤشرات البائع ({product.seller.name})
              </div>
              {agent_analysis.trust_analysis.risk_indicators.map((r: string, i: number) => (
                <div key={i} className="flex items-center gap-1 text-amber-600 dark:text-amber-400">
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                  <span>{r}</span>
                </div>
              ))}
            </div>

            <div className="pt-3 flex flex-col gap-2">
              <Link
                href="/quality-lab"
                className="w-full text-center rounded-xl bg-emerald-500 text-navy-950 font-bold py-2.5 text-xs"
              >
                توليد أسئلة التحقق للبائع
              </Link>
              <a
                href={product.source_url}
                target="_blank"
                rel="noreferrer"
                className="w-full text-center rounded-xl border border-wood-500/30 py-2 text-xs inline-flex items-center justify-center gap-1"
              >
                المصدر الأصلي <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
