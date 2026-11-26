"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

type Locale = "ar" | "fr" | "en";

interface AppCtxValue {
  locale: Locale;
  setLocale: (l: Locale) => void;
  dir: "rtl" | "ltr";
  dark: boolean;
  toggleDark: () => void;
  compareIds: string[];
  toggleCompare: (id: string) => void;
  clearCompare: () => void;
  favoriteIds: string[];
  toggleFavorite: (id: string) => void;
}

const AppContext = createContext<AppCtxValue | null>(null);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocale] = useState<Locale>("ar");
  const [dark, setDark] = useState(false);
  const [compareIds, setCompareIds] = useState<string[]>(["demo-sofa-001", "demo-sofa-002", "demo-sofa-003"]);
  const [favoriteIds, setFavoriteIds] = useState<string[]>(["demo-sofa-001"]);

  const dir: "rtl" | "ltr" = locale === "ar" ? "rtl" : "ltr";

  useEffect(() => {
    document.documentElement.dir = dir;
    document.documentElement.lang = locale;
  }, [dir, locale]);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  const toggleDark = () => setDark((d) => !d);

  const toggleCompare = (id: string) => {
    setCompareIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : prev.length < 6 ? [...prev, id] : prev
    );
  };

  const clearCompare = () => setCompareIds([]);

  const toggleFavorite = (id: string) => {
    setFavoriteIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
  };

  return (
    <AppContext.Provider
      value={{
        locale,
        setLocale,
        dir,
        dark,
        toggleDark,
        compareIds,
        toggleCompare,
        clearCompare,
        favoriteIds,
        toggleFavorite,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used inside AppProvider");
  return ctx;
}
