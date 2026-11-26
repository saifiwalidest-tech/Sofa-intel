"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { MapPin, Truck, Globe, PhoneCall, ExternalLink, Search } from "lucide-react";
import { apiFetch, formatDZD, Seller } from "@/lib/api";

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
  const [filterText, setFilterText] = useState("");
  const [selectedWilaya, setSelectedWilaya] = useState<WilayaInfo | null>(null);
  const [selectedCommune, setSelectedCommune] = useState<string>("");
  const [dbSuppliers, setDbSuppliers] = useState<Seller[]>([]);
  const [liveSuppliers, setLiveSuppliers] = useState<any[]>([]);
  const [loadingLive, setLoadingLive] = useState(false);

  useEffect(() => {
    apiFetch<{ wilayas: WilayaInfo[] }>(`/api/v1/geo/wilayas?user_wilaya_code=${userWilaya}`)
      .then((d) => setWilayas(d.wilayas))
      .catch(() => {});
  }, [userWilaya]);

  const inspectWilaya = async (w: WilayaInfo, commune?: string) => {
    setSelectedWilaya(w);
    setSelectedCommune(commune || "");
    setLiveSuppliers([]);
    setLoadingLive(true);
    try {
      const [mfgRes, liveRes] = await Promise.all([
        apiFetch<{ items: Seller[] }>(`/api/v1/manufacturers?wilaya_code=${w.code}`),
        apiFetch<{ items: any[] }>(
          `/api/v1/geo/discover-suppliers?wilaya_code=${w.code}${commune ? `&commune=${encodeURIComponent(commune)}` : ""}`
        ),
      ]);
      setDbSuppliers(mfgRes.items || []);
      setLiveSuppliers(liveRes.items || []);
    } catch {
      setLiveSuppliers([]);
    } finally {
      setLoadingLive(false);
    }
  };

  const filteredWilayas = wilayas.filter((w) => {
    const q = filterText.trim().toLowerCase();
    if (!q) return true;
    return (
      w.code.includes(q) ||
      w.name_ar.includes(q) ||
      w.name_fr.toLowerCase().includes(q) ||
      w.communes.some((c) => c.toLowerCase().includes(q))
    );
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">خريطة الجزائر: الورشات والشاورومات (58 ولاية وبلدياتها)</h1>
          <p className="text-xs opacity-75">
            اختر أي ولاية أو بلدية للبحث الحي في الإنترنت عن الموردين وأرقام الهواتف أو فتح الموقع مباشرة في خرائط Google.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <div className="relative">
            <Search className="w-4 h-4 absolute top-2.5 right-3 opacity-50" />
            <input
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
              placeholder="ابحث عن ولاية أو بلدية..."
              className="rounded-xl border border-wood-500/30 bg-white dark:bg-navy-900 pr-9 pl-3 py-2 text-xs"
            />
          </div>
          <select
            value={userWilaya}
            onChange={(e) => setUserWilaya(e.target.value)}
            className="rounded-xl border border-wood-500/30 bg-white dark:bg-navy-900 px-3 py-2 text-xs"
          >
            {wilayas.map((w) => (
              <option key={w.code} value={w.code}>موقعي: {w.code} - {w.name_ar}</option>
            ))}
          </select>
        </div>
      </div>

      {selectedWilaya && (
        <section className="rounded-2xl border-2 border-emerald-500/40 bg-white dark:bg-navy-900 p-5 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-bold text-emerald-600">
                الموردون والورشات في {selectedWilaya.code} — {selectedWilaya.name_ar} {selectedCommune ? `(${selectedCommune})` : ""}
              </h2>
              <p className="text-xs opacity-75">نتائج الدليل الموثق + نتائج المسح الحي من الإنترنت</p>
            </div>
            <a
              href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                `fabricant salon canape showroom ${selectedCommune || ""} ${selectedWilaya.name_fr} Algeria`
              )}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 rounded-xl bg-emerald-500 text-navy-950 font-bold px-4 py-2 text-xs"
            >
              <MapPin className="w-4 h-4" />
              فتح في خرائط Google
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

          {dbSuppliers.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              {dbSuppliers.map((s) => (
                <div key={s.id} className="rounded-xl border border-wood-500/25 p-3.5 space-y-1.5 bg-ivory-50 dark:bg-navy-800/60">
                  <div className="flex items-center justify-between gap-2">
                    <strong className="text-sm">{s.name}</strong>
                    <a
                      href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                        `${s.name} ${s.business_address || s.commune} ${s.wilaya_name} Algeria`
                      )}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-emerald-600 hover:underline font-semibold"
                    >
                      <MapPin className="w-3.5 h-3.5" />
                      خرائط Google
                    </a>
                  </div>
                  <div className="opacity-80">{s.business_address || `${s.commune}، ${s.wilaya_name}`}</div>
                  <div className="flex items-center gap-1.5 font-semibold text-emerald-700 dark:text-emerald-400">
                    <PhoneCall className="w-3.5 h-3.5" />
                    <span>{s.public_contact}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="space-y-2">
            <h3 className="font-bold text-xs flex items-center gap-1.5">
              <Globe className="w-4 h-4 text-emerald-500" />
              {loadingLive ? "جاري مسح الإنترنت بحثاً عن ورشات وشاورومات وأرقام هواتف..." : `نتائج البحث الحي من الإنترنت (${liveSuppliers.length})`}
            </h3>
            {!loadingLive && liveSuppliers.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                {liveSuppliers.map((it, idx) => (
                  <div key={idx} className="rounded-xl border border-wood-500/20 p-3.5 space-y-1.5">
                    <div className="flex items-start justify-between gap-2">
                      <a href={it.url} target="_blank" rel="noopener noreferrer" className="font-bold text-emerald-700 dark:text-emerald-400 hover:underline line-clamp-1">
                        {it.title}
                      </a>
                      <a
                        href={it.google_maps_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="shrink-0 inline-flex items-center gap-1 rounded-lg bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 font-semibold"
                        title="فتح الموقع في خرائط Google"
                      >
                        <MapPin className="w-3 h-3" />
                        خرائط
                      </a>
                    </div>
                    <p className="opacity-80 line-clamp-2">{it.snippet}</p>
                    {it.phones?.length > 0 && (
                      <div className="flex items-center gap-1.5 font-bold text-navy-900 dark:text-ivory-50">
                        <PhoneCall className="w-3.5 h-3.5 text-emerald-500" />
                        <span>{it.phones.join(" / ")}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredWilayas.map((w) => (
          <div key={w.code} className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-4 space-y-3 flex flex-col">
            <div className="flex items-center justify-between gap-2">
              <span className="font-bold flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-emerald-500" />
                {w.code} — {w.name_ar}
              </span>
              <a
                href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`fabricant salon canape ${w.name_fr} Algeria`)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 rounded-full bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 px-2.5 py-0.5 text-[11px] font-bold hover:bg-emerald-500/25"
                title="فتح الولاية في خرائط Google"
              >
                <MapPin className="w-3 h-3" />
                خرائط Google
              </a>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {w.communes.map((c) => (
                <div key={c} className="inline-flex items-center rounded-lg bg-ivory-100 dark:bg-navy-800 text-[11px] overflow-hidden border border-wood-500/20">
                  <button
                    onClick={() => inspectWilaya(w, c)}
                    className="px-2 py-1 hover:text-emerald-600 font-medium"
                    title={`بحث عن الموردين في بلدية ${c}`}
                  >
                    {c}
                  </button>
                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`salon canape meuble ${c} ${w.name_fr} Algeria`)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-1.5 py-1 border-r border-wood-500/20 text-emerald-600 hover:bg-emerald-500/10"
                    title={`فتح ${c} في خرائط Google`}
                  >
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              ))}
            </div>

            <div className="text-xs flex items-center justify-between pt-2 border-t border-wood-500/15 mt-auto">
              <span className="inline-flex items-center gap-1"><Truck className="w-3.5 h-3.5 text-wood-500" /> توصيل تقديري:</span>
              <strong>{formatDZD(w.estimated_delivery_dzd)} ({w.distance_km} كم)</strong>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => inspectWilaya(w)}
                className="rounded-xl bg-emerald-500 text-navy-950 py-1.5 text-xs font-bold hover:opacity-90"
              >
                بحث حي عن الموردين
              </button>
              <Link
                href={`/results?wilaya_code=${w.code}`}
                className="text-center rounded-xl bg-navy-900 dark:bg-navy-700 text-ivory-50 py-1.5 text-xs font-semibold hover:opacity-90"
              >
                العروض ({w.offers_count})
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
