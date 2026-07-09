import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Clinic brand palette — placeholder, real tokens land with the
        // Frontend UI phase once we design the actual visual identity.
        brand: {
          50: "#eff6f5",
          500: "#0f766e",
          600: "#0d5f58",
          900: "#0a3d38",
        },
      },
    },
  },
  plugins: [],
};

export default config;
