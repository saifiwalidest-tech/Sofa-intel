"use client";

import React, { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function ReportPage() {
  const [productId, setProductId] = useState("");
  const [reason, setReason] = useState("مواصفات غير مطابقة");
  const [details, setDetails] = useState("");
  const [done, setDone] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await apiFetch("/api/v1/reports", {
      method: "POST",
      body: JSON.stringify({ product_id: productId || null, reason, details }),
    });
    setDone(true);
  };

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">الإبلاغ عن إعلان غير صحيح</h1>
      {done ? (
        <div className="p-4 rounded-xl bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 text-sm">
          تم استلام بلاغك وتسجيله للمراجعة. شكراً لمساهمتك في موثوقية السوق.
        </div>
      ) : (
        <form onSubmit={submit} className="space-y-4 rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 text-sm">
          <input value={productId} onChange={(e) => setProductId(e.target.value)} placeholder="معرف المنتج (اختياري)" className="w-full rounded-lg border border-wood-500/30 bg-transparent px-3 py-2" />
          <input value={reason} onChange={(e) => setReason(e.target.value)} required className="w-full rounded-lg border border-wood-500/30 bg-transparent px-3 py-2" />
          <textarea value={details} onChange={(e) => setDetails(e.target.value)} required rows={4} placeholder="اشرح التناقض أو الخطأ..." className="w-full rounded-lg border border-wood-500/30 bg-transparent px-3 py-2" />
          <button type="submit" className="rounded-xl bg-emerald-500 text-navy-950 font-bold px-6 py-2.5">إرسال البلاغ</button>
        </form>
      )}
    </div>
  );
}
