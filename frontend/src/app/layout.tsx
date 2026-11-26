import type { Metadata } from "next";
import "./globals.css";
import { AppProvider } from "@/components/AppContext";
import { Shell } from "@/components/Shell";

export const metadata: Metadata = {
  title: "SOFA INTEL DZ — منصة استخبارات سوق الأرائك في الجزائر",
  description: "منصة ذكية متعددة الوكلاء للبحث عن الأرائك والصالونات ومقارنتها في الجزائر — حقوق النشر © saifiwalid",
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
