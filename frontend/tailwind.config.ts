import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
    "*.{js,ts,jsx,tsx,mdx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "#000000",
        foreground: "#ffffff",
        primary: {
          DEFAULT: "#1DFD26",
          foreground: "#000000",
          50: "#f0fef1",
          100: "#dcfcde",
          200: "#bcf7c0",
          300: "#8aef93",
          400: "#51e05e",
          500: "#1DFD26",
          600: "#18d121",
          700: "#16a51d",
          800: "#17821d",
          900: "#156b1c",
          950: "#063c0b",
        },
        secondary: {
          DEFAULT: "#0D3014",
          foreground: "#ffffff",
          50: "#f0f9f1",
          100: "#dcf2de",
          200: "#bce5c0",
          300: "#8dd097",
          400: "#57b467",
          500: "#349745",
          600: "#267a34",
          700: "#20612b",
          800: "#1c4e25",
          900: "#0D3014",
          950: "#0a2610",
        },
        muted: {
          DEFAULT: "#1a1a1a",
          foreground: "#a3a3a3",
        },
        accent: {
          DEFAULT: "#262626",
          foreground: "#ffffff",
        },
        destructive: {
          DEFAULT: "#dc2626",
          foreground: "#ffffff",
        },
        card: {
          DEFAULT: "#111111",
          foreground: "#ffffff",
        },
        popover: {
          DEFAULT: "#111111",
          foreground: "#ffffff",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config

export default config
