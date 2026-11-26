"use client";

import React, { useState } from "react";
import { Sparkles, Send } from "lucide-react";
import { apiFetch, Product } from "@/lib/api";
import { ProductCard } from "@/components/ProductCard";

export default function ConsultantPage() {
  const [message, setMessage] = useState("عندي ميزانية 12 مليون سنتيم، نحب صالون L برغوة D36 وخشب الزان، قريب للبليدة، وما يكونش القماش يتوسخ بسرعة");
  const [result, setResult] = useState<{ summary_ar: string; understood_criteria: any; recommendations: { product: Product; match_score: number; estimated_delivered_total_dzd: number }[] } | null>(null);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    setLoading(true);
    try {
      const res = await apiFetch<any>("/api/v1/consultant/ask", {
        method: "POST",
        body: JSON.stringify({ message }),
      });
      setResult(res);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Sparkles className="w-6 h-6 text-emerald-500" />
        <h1 className="text-2xl font-bold">مستشار الشراء الشخصي</h1>
      </div>
      <p className="text-sm opacity-80">اكتب طلبك بالعربية، الدارجة الجزائرية، الفرنسية، أو الإنجليزية — يحول المستشار ميزانيتك (بما فيها السنتيم) إلى معايير بحث دقيقة.</p>

      <div className="flex flex-col sm:flex-row gap-2">
        <textarea
          rows={2}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-1 rounded-xl border border-wood-500/30 bg-white dark:bg-navy-900 p-3 text-sm"
        />
        <button
          onClick={ask}
          disabled={loading}
          className="rounded-xl bg-emerald-500 text-navy-950 font-bold px-6 py-3 text-sm inline-flex items-center justify-center gap-2"
        >
          <Send className="w-4 h-4" />
          {loading ? "جاري التحليل..." : "استشارة"}
        </button>
      </div>

      {result && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-4 text-sm">
            {result.summary_ar}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {result.recommendations.map((rec) => (
              <div key={rec.product.id} className="space-y-2">
                <div className="text-xs font-bold text-emerald-600">
                  نسبة التطابق: {rec.match_score} · الإجمالي التقديري بالتوصيل: {rec.estimated_delivered_total_dzd.toLocaleString("fr-DZ")} دج
                </div>
                <ProductCard product={rec.product} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
