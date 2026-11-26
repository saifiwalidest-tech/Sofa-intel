"use client";

import React from "react";
import Link from "next/link";
import { Moon, Sun, Scale, Heart, ShieldCheck, Globe } from "lucide-react";
import { useApp } from "./AppContext";

const NAV_LINKS = [
  { href: "/", ar: "الرئيسية", fr: "Accueil", en: "Home" },
  { href: "/search", ar: "البحث المتقدم", fr: "Recherche", en: "Search" },
  { href: "/results", ar: "العروض", fr: "Offres", en: "Results" },
  { href: "/compare", ar: "المقارنة", fr: "Comparer", en: "Compare" },
  { href: "/consultant", ar: "مستشار الشراء", fr: "Conseiller", en: "Advisor" },
  { href: "/quality-lab", ar: "مختبر الجودة", fr: "Labo Qualité", en: "Quality Lab" },
  { href: "/map", ar: "خريطة الجزائر", fr: "Carte DZ", en: "Map" },
  { href: "/manufacturers", ar: "المصانع", fr: "Fabricants", en: "Factories" },
  { href: "/price-observatory", ar: "مرصد الأسعار", fr: "Observatoire", en: "Prices" },
  { href: "/weekly-deals", ar: "أفضل العروض", fr: "Meilleures Offres", en: "Weekly Deals" },
  { href: "/visual-search", ar: "بحث بالصورة", fr: "Recherche Visuelle", en: "Visual Search" },
  { href: "/admin", ar: "الإدارة", fr: "Admin", en: "Admin" },
];

export function Shell({ children }: { children: React.ReactNode }) {
  const { locale, setLocale, dark, toggleDark, compareIds, favoriteIds } = useApp();

  return (
    <div className="min-h-screen flex flex-col bg-ivory-50 text-navy-900 dark:bg-navy-950 dark:text-ivory-50 transition-colors">
      <header className="sticky top-0 z-40 border-b border-wood-500/20 bg-navy-900 text-ivory-50 shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-3">
          <Link href="/" className="flex items-center gap-2 font-bold text-lg tracking-tight">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500 text-navy-950 font-black">
              S
            </span>
            <span>SOFA INTEL DZ</span>
          </Link>

          <nav className="flex flex-wrap items-center gap-3 text-xs sm:text-sm">
            {NAV_LINKS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="hover:text-emerald-400 transition-colors px-1.5 py-1 rounded"
              >
                {item[locale]}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            <Link
              href="/compare"
              className="inline-flex items-center gap-1 rounded-full bg-navy-800 px-2.5 py-1 text-xs hover:bg-navy-700"
            >
              <Scale className="w-3.5 h-3.5 text-emerald-400" />
              <span>{compareIds.length}</span>
            </Link>
            <Link
              href="/favorites"
              className="inline-flex items-center gap-1 rounded-full bg-navy-800 px-2.5 py-1 text-xs hover:bg-navy-700"
            >
              <Heart className="w-3.5 h-3.5 text-wood-300" />
              <span>{favoriteIds.length}</span>
            </Link>
            <button
              onClick={() => setLocale(locale === "ar" ? "fr" : locale === "fr" ? "en" : "ar")}
              className="inline-flex items-center gap-1 rounded-full bg-navy-800 px-2.5 py-1 text-xs hover:bg-navy-700"
              title="Switch Language / RTL-LTR"
            >
              <Globe className="w-3.5 h-3.5 text-emerald-400" />
              <span className="uppercase">{locale}</span>
            </button>
            <button
              onClick={toggleDark}
              className="rounded-full bg-navy-800 p-1.5 hover:bg-navy-700"
              aria-label="Toggle Theme"
            >
              {dark ? <Sun className="w-4 h-4 text-wood-300" /> : <Moon className="w-4 h-4 text-ivory-100" />}
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6">{children}</main>

      <footer className="border-t border-wood-500/20 bg-navy-900 text-ivory-100 text-xs py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>SOFA INTEL DZ — منصة متخصصة للبحث ومقارنة جودة وأسعار الأرائك في الجزائر</span>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <Link href="/methodology" className="hover:text-emerald-400">المصادر والمنهجية</Link>
            <Link href="/guide" className="hover:text-emerald-400">الدليل التقني</Link>
            <Link href="/alerts" className="hover:text-emerald-400">التنبيهات</Link>
            <Link href="/report" className="hover:text-emerald-400">الإبلاغ عن إعلان</Link>
          </div>
          <div className="font-semibold text-wood-300">
            جميع الحقوق محفوظة © 2026 saifiwalid
          </div>
        </div>
      </footer>
    </div>
  );
}
