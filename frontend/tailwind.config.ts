import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          950: "#060B19",
          900: "#0B132B",
          800: "#1C2541",
          700: "#2B3A67",
        },
        ivory: {
          50: "#FAF9F6",
          100: "#F4F1EA",
          200: "#E8E2D5",
        },
        emerald: {
          500: "#10B981",
          600: "#059669",
          700: "#047857",
        },
        wood: {
          300: "#DFC3A5",
          500: "#C89B6E",
          700: "#8B5A2B",
        },
      },
    },
  },
  plugins: [],
};

export default config;
