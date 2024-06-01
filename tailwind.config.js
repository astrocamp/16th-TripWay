/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "home-yellow": "#EDC951",
        "btn-red":" #CC333F",
        "number-black": "#101828",
        "base-white":"#FFFFFF",
        "light-blue": "#85B6FF",
        "blueGray": "#EBF0F6",
        "blue": "#EBF0F6",
        "btn-blue": "#649DFF",
        "blue-btn":"#00A0B0",
        'blue-dc': '#005a64',
        "dark-gray":"#0F1828",
        "hover-gray": "#878B93",
        "light-gray":"#CFD1D4",
      },
      borderRadius: {
        "custom-20": "20px",
        "custom-50": "50px",
      },
    },
  },
  variants: {
    extend: {
      textColor: ["checked"],
    },
  },
  plugins: [require("daisyui")],
};
