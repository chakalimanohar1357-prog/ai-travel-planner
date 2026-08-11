/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#fff5f0",
          100: "#ffe8db",
          400: "#ff8c5a",
          500: "#ff5a1f",
          600: "#e8480f",
          700: "#c23a0c",
        },
        ink: {
          900: "#1a1a1a",
          700: "#333333",
          500: "#6b6b6b",
        },
      },
      fontFamily: {
        display: ["Poppins", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
      boxShadow: {
        card: "0 2px 16px rgba(0,0,0,0.08)",
        "card-hover": "0 8px 30px rgba(0,0,0,0.14)",
      },
      borderRadius: {
        xl2: "1.25rem",
      },
    },
  },
  plugins: [],
};