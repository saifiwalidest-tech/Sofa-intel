"use client";

import React from "react";
import Link from "next/link";
import { Heart, Scale, MapPin, ShieldAlert, CheckCircle2 } from "lucide-react";
import { Product, formatDZD } from "@/lib/api";
import { useApp } from "./AppContext";

export function ProductCard({ product }: { product: Product }) {
  const { compareIds, toggleCompare, favoriteIds, toggleFavorite } = useApp();
  const inCompare = compareIds.includes(product.id);
  const inFav = favoriteIds.includes(product.id);

  return (
    <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 shadow-sm hover:shadow-md transition-all overflow-hidden flex flex-col">
      <div className="relative h-44 bg-navy-900 flex items-center justify-center">
        <img
          src={product.images?.[0] || "/images/sofa-l-navy.svg"}
          alt={product.title}
          className="h-full w-full object-cover"
        />
        {product.is_demo && (
          <span className="absolute top-2 right-2 rounded-full bg-amber-500/95 text-navy-950 text-[10px] font-bold px-2.5 py-0.5">
            DEMO DATA — للاختبار فقط
          </span>
        )}
        <span className="absolute bottom-2 left-2 rounded-full bg-navy-950/80 text-ivory-50 text-[11px] px-2.5 py-0.5">
          {product.sofa_type} · {product.seats_count ? `${product.seats_count} مقاعد` : "مقاعد غير محددة"}
        </span>
      </div>

      <div className="p-4 flex-1 flex flex-col gap-3">
        <div className="flex items-start justify-between gap-2">
          <Link href={`/products/${product.id}`} className="font-bold text-sm sm:text-base hover:text-emerald-600 line-clamp-2">
            {product.title}
          </Link>
        </div>

        <div className="flex items-center gap-1.5 text-xs text-navy-700 dark:text-ivory-200">
          <MapPin className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
          <span>{product.seller.wilaya_name} ({product.seller.commune})</span>
          <span className="mx-1">·</span>
          <span className="text-wood-700 dark:text-wood-300 font-medium">{product.seller.seller_type}</span>
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs bg-ivory-100 dark:bg-navy-800/70 rounded-xl p-2.5">
          <div>
            <span className="opacity-70 block">الرغوة</span>
            <span className="font-semibold inline-flex items-center gap-1">
              {product.foam_density_claimed || "غير محدد"}
              {product.foam_density_documented ? (
                <span title="موثقة بشهادة"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /></span>
              ) : (
                <span title="ادعاء بائع فقط / ناقصة"><ShieldAlert className="w-3.5 h-3.5 text-amber-500" /></span>
              )}
            </span>
          </div>
          <div>
            <span className="opacity-70 block">الخشب</span>
            <span className="font-semibold">{product.wood_type || "غير محدد"}</span>
          </div>
          <div>
            <span className="opacity-70 block">نطاق الجودة</span>
            <span className="font-bold text-emerald-600 dark:text-emerald-400">
              {product.quality_score_min}–{product.quality_score_max}/100
            </span>
          </div>
          <div>
            <span className="opacity-70 block">اكتمال البيانات</span>
            <span className="font-semibold">{product.data_completeness_score}%</span>
          </div>
        </div>

        <div className="mt-auto pt-2 border-t border-wood-500/15 flex items-center justify-between gap-2">
          <div>
            <div className="text-lg font-extrabold text-navy-900 dark:text-emerald-400">
              {formatDZD(product.current_price_dzd)}
            </div>
            <div className="text-[11px] opacity-70">
              الإجمالي بالتوصيل: {formatDZD(product.total_cost_dzd)}
            </div>
          </div>

          <div className="flex items-center gap-1.5">
            <button
              onClick={() => toggleCompare(product.id)}
              className={`p-2 rounded-lg border text-xs transition ${
                inCompare
                  ? "bg-emerald-500 text-navy-950 border-emerald-500 font-bold"
                  : "border-wood-500/30 hover:bg-ivory-100 dark:hover:bg-navy-800"
              }`}
              title="إضافة للمقارنة"
            >
              <Scale className="w-4 h-4" />
            </button>
            <button
              onClick={() => toggleFavorite(product.id)}
              className={`p-2 rounded-lg border text-xs transition ${
                inFav
                  ? "bg-wood-500 text-white border-wood-500"
                  : "border-wood-500/30 hover:bg-ivory-100 dark:hover:bg-navy-800"
              }`}
              title="المفضلة"
            >
              <Heart className="w-4 h-4" />
            </button>
            <Link
              href={`/products/${product.id}`}
              className="rounded-lg bg-navy-900 dark:bg-emerald-600 text-ivory-50 px-3 py-2 text-xs font-semibold hover:opacity-90"
            >
              التفاصيل
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
