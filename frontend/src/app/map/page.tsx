"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { MapPin, Truck } from "lucide-react";
import { apiFetch, formatDZD } from "@/lib/api";

interface WilayaInfo {
  code: string;
  name_ar: string;
  name_fr: string;
  lat: number;
  lon: number;
  communes: string[];
  offers_count: number;
  estimated_delivery_dzd: number;
  distance_km: number;
}

export default function AlgeriaMapPage() {
  const [userWilaya, setUserWilaya] = useState("16");
  const [wilayas, setWilayas] = useState<WilayaInfo[]>([]);

  useEffect(() => {
    apiFetch<{ wilayas: WilayaInfo[] }>(`/api/v1/geo/wilayas?user_wilaya_code=${userWilaya}`)
      .then((d) => setWilayas(d.wilayas))
      .catch(() => {});
  }, [userWilaya]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">خريطة عروض الجزائر وتقدير التوصيل</h1>
          <p className="text-xs opacity-75">58 ولاية — حساب المسافة وتقدير تكلفة النقل من المصنع إلى ولايتك</p>
        </div>
        <select
          value={userWilaya}
          onChange={(e) => setUserWilaya(e.target.value)}
          className="rounded-xl border border-wood-500/30 bg-white dark:bg-navy-900 px-4 py-2 text-sm"
        >
          {wilayas.map((w) => (
            <option key={w.code} value={w.code}>{w.code} - {w.name_ar} ({w.name_fr})</option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {wilayas.filter((w) => w.offers_count > 0 || ["09", "16", "19", "31", "15", "25"].includes(w.code)).map((w) => (
          <div key={w.code} className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-emerald-500" />
                {w.code} — {w.name_ar}
              </span>
              <span className="rounded-full bg-emerald-500/15 text-emerald-600 px-2.5 py-0.5 text-xs font-bold">
                {w.offers_count} عروض
              </span>
            </div>
            <div className="text-xs opacity-75">البلديات: {w.communes.join("، ")}</div>
            <div className="text-xs flex items-center justify-between pt-2 border-t border-wood-500/15">
              <span className="inline-flex items-center gap-1"><Truck className="w-3.5 h-3.5 text-wood-500" /> توصيل تقديري:</span>
              <strong>{formatDZD(w.estimated_delivery_dzd)} ({w.distance_km} كم)</strong>
            </div>
            <Link
              href={`/results?wilaya_code=${w.code}`}
              className="block text-center rounded-xl bg-navy-900 dark:bg-emerald-600 text-ivory-50 py-1.5 text-xs font-semibold hover:opacity-90"
            >
              عرض الموردين والعروض ←
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
