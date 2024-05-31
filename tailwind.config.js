/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "light-blue": "#85B6FF",
        "blueGray": '#EBF0F6',
        "btn-blue": "#649DFF",
        "yellow": "#EDC951",
        "red":" #CC333F",
        "black": "#101828",
        "gray": "#878B93",
        "white":"#FFFFFF",
      },
      borderRadius: {
        "custom-20": "20px",
        "custom-50": "50px",
      },
    },
  },
  plugins: [require("daisyui")],
};
