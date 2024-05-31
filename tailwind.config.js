/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'light-blue': '#85B6FF',
        'blue': '#EBF0F6',
        'blue-btn': '#00A0B0',
        'blue-dc': '#005a64',
        'btn-blue': '#649DFF',
      }
    },
  },
  plugins: [require("daisyui")],
};
