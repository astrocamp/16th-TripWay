/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "light-blue": "#85B6FF",
        "blueGray": "#EBF0F6",
        "btn-blue": "#649DFF",
        "yellow": "#EDC951",
        "red":" #CC333F",
        "black": "#101828",
        "white":"#FFFFFF",
        "blue-btn":"#00A0B0",
        'blue-dc': '#005a64',
        "dark-gray":"#0F1828",
        "gray": "#878B93",
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
