import type { Config } from "tailwindcss";

export default {
  content: ["./pages/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}", "./app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        "spotify-green": "#1db954",
        "spotify-black-1": "#212121",
        "spotify-black-2": "#121212",
        "spotify-gray-1": "#535353",
        "spotify-gray-2": "#b3b3b3",
      },
    },
  },
  plugins: [],
} satisfies Config;
