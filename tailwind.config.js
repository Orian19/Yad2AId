/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./frontend/extension/**/*.{html,js}",
    "./components/**/*.{html,js}",
    "./server/**/*.{html,js}",
    "./user/**/*.{html,js}",
    "./*.{html,js}"  // For any HTML or JS files in the root directory
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ["light", "dark"], // Add more themes as needed
  },
}