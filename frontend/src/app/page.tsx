"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Search, Sparkles, Scale, MapPin, ShieldCheck, Factory } from "lucide-react";
import { apiFetch, Product } from "@/lib/api";
import { ProductCard } from "@/components/ProductCard";

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    apiFetch<{ items: Product[] }>("/api/v1/products")
      .then((d) => setProducts(d.items))
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-10">
      <section className="rounded-3xl bg-gradient-to-br from-navy-900 via-navy-800 to-navy-950 text-ivory-50 p-6 sm:p-10 shadow-xl border border-wood-500/30">
        <div className="max-w-3xl space-y-4">
          <span className="inline-flex items-center gap-2 rounded-full bg-emerald-500/20 text-emerald-400 px-3 py-1 text-xs font-semibold">
            <ShieldCheck className="w-4 h-4" />
            نظام من 18 وكيل ذكاء اصطناعي · توثيق مصدر كل معلومة
          </span>
          <h1 className="text-2xl sm:text-4xl font-extrabold leading-tight">
            اكتشف أفضل الأرائك والصالونات في الجزائر بالدليل الهندسي والسعر العادل
          </h1>
          <p className="text-ivory-200 text-sm sm:text-base">
            ابحث بالعربية، الدارجة، أو الفرنسية (مثل: صالون زاوية رغوة D36 خشب الزان في البليدة) وقارن الجودة الفعلية بدون بيانات مختلقة.
          </p>

          <form
            action="/results"
            method="GET"
            className="flex flex-col sm:flex-row gap-2 pt-2"
          >
            <div className="relative flex-1">
              <Search className="w-4 h-4 absolute top-3.5 right-3.5 text-navy-700" />
              <input
                name="q"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="مثال: صالون L موس 36 زان قماش anti-tache..."
                className="w-full rounded-xl bg-ivory-50 text-navy-900 pr-10 pl-4 py-3 text-sm outline-none"
              />
            </div>
            <button
              type="submit"
              className="rounded-xl bg-emerald-500 hover:bg-emerald-600 text-navy-950 font-bold px-6 py-3 text-sm transition"
            >
              بحث ذكي
            </button>
            <Link
              href="/consultant"
              className="rounded-xl bg-wood-500 hover:bg-wood-700 text-white font-bold px-5 py-3 text-sm text-center transition inline-flex items-center justify-center gap-1.5"
            >
              <Sparkles className="w-4 h-4" />
              اسأل المستشار
            </Link>
          </form>
        </div>
      </section>

      <section className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Link href="/results" className="rounded-2xl border border-wood-500/20 bg-white dark:bg-navy-900 p-4 hover:border-emerald-500 transition">
          <Search className="w-5 h-5 text-emerald-500 mb-2" />
          <div className="font-bold text-sm">19+ فلتر متقدم</div>
          <div className="text-xs opacity-70">الولاية، الرغوة، الخشب، الثقة</div>
        </Link>
        <Link href="/compare" className="rounded-2xl border border-wood-500/20 bg-white dark:bg-navy-900 p-4 hover:border-emerald-500 transition">
          <Scale className="w-5 h-5 text-emerald-500 mb-2" />
          <div className="font-bold text-sm">مقارنة حتى 6 صالونات</div>
          <div className="text-xs opacity-70">مخطط راداري + كشف النواقص</div>
        </Link>
        <Link href="/map" className="rounded-2xl border border-wood-500/20 bg-white dark:bg-navy-900 p-4 hover:border-emerald-500 transition">
          <MapPin className="w-5 h-5 text-emerald-500 mb-2" />
          <div className="font-bold text-sm">خريطة 58 ولاية</div>
          <div className="text-xs opacity-70">تقدير تكلفة التوصيل والمسافة</div>
        </Link>
        <Link href="/manufacturers" className="rounded-2xl border border-wood-500/20 bg-white dark:bg-navy-900 p-4 hover:border-emerald-500 transition">
          <Factory className="w-5 h-5 text-emerald-500 mb-2" />
          <div className="font-bold text-sm">دليل المصانع المباشرة</div>
          <div className="text-xs opacity-70">تفريق المصنع عن الوسيط</div>
        </Link>
      </section>

      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold">أحدث العروض المحللة (بيانات تجريبية للاختبار)</h2>
          <Link href="/results" className="text-sm text-emerald-600 font-semibold hover:underline">
            عرض كل النتائج ←
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {products.slice(0, 6).map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </section>
    </div>
  );
}
