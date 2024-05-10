/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'light-blue': '#85B6FF',
        'blue': '#EBF0F6',
        'btn-blue': '#649DFF',
      }
    },
  },
  plugins: [require("daisyui")],
}
