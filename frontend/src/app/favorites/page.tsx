"use client";

import React, { useEffect, useState } from "react";
import { apiFetch, Product } from "@/lib/api";
import { useApp } from "@/components/AppContext";
import { ProductCard } from "@/components/ProductCard";

export default function FavoritesPage() {
  const { favoriteIds } = useApp();
  const [items, setItems] = useState<Product[]>([]);

  useEffect(() => {
    apiFetch<{ items: Product[] }>("/api/v1/products")
      .then((d) => setItems(d.items.filter((p) => favoriteIds.includes(p.id))))
      .catch(() => {});
  }, [favoriteIds]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">قائمة المفضلة ({items.length})</h1>
      {items.length === 0 ? (
        <div className="p-8 text-center rounded-2xl border border-wood-500/20">لا توجد عروض في المفضلة بعد.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {items.map((p) => <ProductCard key={p.id} product={p} />)}
        </div>
      )}
    </div>
  );
}
