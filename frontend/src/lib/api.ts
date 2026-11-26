/* API Client & Shared Types for SOFA INTEL DZ — Copyright (c) 2026 saifiwalid */

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001";

export interface Seller {
  id: string;
  name: string;
  seller_type: string;
  wilaya_code: string;
  wilaya_name: string;
  commune: string;
  business_address: string | null;
  public_contact: string | null;
  latitude: number | null;
  longitude: number | null;
  has_written_warranty: boolean;
  cash_on_delivery: boolean;
  provides_invoice: boolean;
  custom_orders_supported: boolean;
  trust_score: number;
  is_demo: boolean;
}

export interface ProvenanceField {
  field_name: string;
  field_value: string | null;
  verification_status: string;
  source_name: string;
  source_url: string | null;
  confidence: number;
  extracted_at: string;
}

export interface Product {
  id: string;
  title: string;
  description: string | null;
  sofa_type: string;
  condition: string;
  images: string[];
  seats_count: number | null;
  dimensions_cm: string | null;
  foam_type: string | null;
  foam_density_claimed: string | null;
  foam_density_documented: boolean;
  foam_firmness: string | null;
  foam_thickness_cm: number | null;
  wood_type: string | null;
  assembly_method: string | null;
  suspension_type: string | null;
  fabric_type: string | null;
  fabric_properties: string[];
  color: string | null;
  original_price_dzd: number | null;
  current_price_dzd: number;
  price_status: string;
  warranty_months: number | null;
  delivery_available: boolean;
  delivery_cost_dzd: number | null;
  total_cost_dzd: number;
  primary_source_name: string;
  source_url: string;
  published_at: string;
  last_verified_at: string;
  availability_status: string;
  quality_score_min: number;
  quality_score_max: number;
  quality_score_midpoint: number;
  value_for_money_score: number;
  evidence_confidence_score: number;
  data_completeness_score: number;
  comfort_suitability_score: number;
  delivery_cost_score: number;
  is_demo: boolean;
  seller: Seller;
  provenance_fields?: ProvenanceField[];
  price_history?: { price_dzd: number; recorded_at: string; source_name: string }[];
}

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

export function formatDZD(amount: number | null | undefined): string {
  if (amount === null || amount === undefined) return "غير محدد";
  return `${amount.toLocaleString("fr-DZ")} دج`;
}
