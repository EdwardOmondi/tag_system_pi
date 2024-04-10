/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': {
          '50': '#f3f6fb',
          '100': '#e4eaf5',
          '200': '#cfdbee',
          '300': '#aec3e2',
          '400': '#84a1d2',
          '500': '#6a86c7',
          '600': '#576fb9',
          '700': '#4c5da9',
          '800': '#434e8a',
          '900': '#39436f',
          '950': '#262b45',
        },
        'secondary': {
          '50': '#faf7f2',
          '100': '#f4ede0',
          '200': '#e8dac0',
          '300': '#d2b584',
          '400': '#c9a26e',
          '500': '#be8b51',
          '600': '#b07646',
          '700': '#925f3c',
          '800': '#764e36',
          '900': '#60412e',
          '950': '#332017',
        },
      }
    },
  },
  plugins: [require('@tailwindcss/typography'),
  ],
}

