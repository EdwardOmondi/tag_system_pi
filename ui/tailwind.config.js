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
      },
      animation: {
        heartbeat: "heartbeat 2s ease  infinite  both",
        "bg-pan-top": "bg-pan-top 8s ease   both",
        "bounce-in-fwd": "bounce-in-fwd 1.3s ease   both"

      },
      keyframes: {
        "bounce-in-fwd": {
          "0%": {
            transform: "scale(0)",
            "animation-timing-function": "ease-in",
            opacity: "0"
          },
          "38%": {
            transform: "scale(1)",
            "animation-timing-function": "ease-out",
            opacity: "1"
          },
          "55%": {
            transform: "scale(.7)",
            "animation-timing-function": "ease-in"
          },
          "72%,89%,to": {
            transform: "scale(1)",
            "animation-timing-function": "ease-out"
          },
          "81%": {
            transform: "scale(.84)",
            "animation-timing-function": "ease-in"
          },
          "95%": {
            transform: "scale(.95)",
            "animation-timing-function": "ease-in"
          }
        },
        "bg-pan-top": {
          "0%": {
            "background-position": "50% 100%"
          },
          to: {
            "background-position": "50% 0%"
          }
        },
        heartbeat: {
          "0%": {
            transform: "scale(1)",
            "transform-origin": "center center",
            "animation-timing-function": "ease-out"
          },
          "10%": {
            transform: "scale(.91)",
            "animation-timing-function": "ease-in"
          },
          "17%": {
            transform: "scale(.98)",
            "animation-timing-function": "ease-out"
          },
          "33%": {
            transform: "scale(.87)",
            "animation-timing-function": "ease-in"
          },
          "45%": {
            transform: "scale(1)",
            "animation-timing-function": "ease-out"
          }
        }
      }
    },
  },
  plugins: [require('@tailwindcss/typography'),
  ],
}

