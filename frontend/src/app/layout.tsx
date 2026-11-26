import type { Metadata } from "next";
import "./globals.css";
import { AppProvider } from "@/components/AppContext";
import { Shell } from "@/components/Shell";

export const metadata: Metadata = {
  title: "SOFA INTEL DZ — محرك البحث ومقارنة الأرائك والصالونات في الجزائر",
  description: "منصة متخصصة للبحث عن الأرائك والصالونات ومقارنة الجودة والأسعار في الجزائر — حقوق النشر © saifiwalid",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <AppProvider>
          <Shell>{children}</Shell>
        </AppProvider>
      </body>
    </html>
  );
}
