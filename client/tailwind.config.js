/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors : {
        "primary-200" : "#111827", /* Changed from indigo to deep premium black/slate */
        "primary-100" : "#374151",
        "secondary-200" : "#059669", /* A premium emerald green for success/Add to Cart */
        "secondary-100" : "#10B981",
        "brand-yellow" : "#FBBF24",
        "brand-light" : "#F8FAFC", 
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(0, 0, 0, 0.05)',
        'premium': '0 10px 40px -4px rgba(0, 0, 0, 0.08)',
        'float': '0 20px 40px -8px rgba(0, 0, 0, 0.12)',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      }
    },
  },
  plugins: [],
}
