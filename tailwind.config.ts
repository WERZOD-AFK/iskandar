import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Telegram WebApp runtime'da --tg-theme-* larni body'ga inject qiladi
        // (src/lib/telegram.ts). Shu o'zgaruvchilarga bog'lab qo'yamiz, shunda
        // Mini App foydalanuvchining Telegram mavzusiga (dark/light) avtomatik moslashadi.
        tgbg: "var(--tg-bg, #ffffff)",
        tgsecondary: "var(--tg-secondary-bg, #f0f0f3)",
        tgtext: "var(--tg-text, #0f1115)",
        tghint: "var(--tg-hint, #8a8f98)",
        tglink: "var(--tg-link, #2aabee)",
        tgbutton: "var(--tg-button, #2aabee)",
        tgbuttontext: "var(--tg-button-text, #ffffff)",
        // Stars — Telegram Stars belgisining o'ziga xos oltin rangi
        star: {
          DEFAULT: "#FFB300",
          light: "#FFD65A",
          deep: "#E68A00",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          '"SF Pro Text"',
          '"Segoe UI"',
          "Roboto",
          '"Helvetica Neue"',
          "Arial",
          "sans-serif",
        ],
      },
      keyframes: {
        shimmer: {
          "0%": { backgroundPosition: "-150% 0" },
          "100%": { backgroundPosition: "150% 0" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-4px)" },
        },
        "pop-in": {
          "0%": { transform: "scale(0.96)", opacity: "0" },
          "100%": { transform: "scale(1)", opacity: "1" },
        },
      },
      animation: {
        shimmer: "shimmer 2.8s linear infinite",
        float: "float 3.2s ease-in-out infinite",
        "pop-in": "pop-in 0.18s ease-out",
      },
    },
  },
  plugins: [],
} satisfies Config;
