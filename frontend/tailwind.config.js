/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      spacing: {
        text: "clamp(45ch,50%,75ch)",
      },
      listStyleType: {square: "square",},
      colors: {
        kuRed: "#901A1E",
        kuGray: "#333333",
        darkGray: "#2b2d41",
        dulledWhite: "#F4F5F7",
        greyedOut: "#8D99AD",
        brand: {
          100: "#270102",
          200: "#370002",
          300: "#630307",
          400: "#780D10",
          500: "#901A1E",
          600: "#B84044",
          700: "#D27275",
          800: "#E5A3A5",
          900: "#FCEBEC",
        },
        neutral: {
          100: "#03080E",
          200: "#101E2D",
          300: "#1A2A39",
          400: "#273441",
          500: "#3A4550",
          600: "#7B7E81",
          700: "#C2C2C2",
          800: "#F2EFEF",
          900: "#FFFFFF",
        },
        green: {
          100: "#013100",
          200: "#026200",
          300: "#049001",
          400: "#0FBC0C",
          500: "#24D921",
          600: "#3EEE3B",
          700: "#71FF6F",
          800: "#88FF86",
          900: "#AEFFAC",
        },
        orange: {
          100: "#302300",
          200: "#624600",
          300: "#906801",
          400: "#BC8A0C",
          500: "#D9A521",
          600: "#EEBB3B",
          700: "#FFD66F",
          800: "#FFDD86",
          900: "#FFE8AC",
        },
        red: {
          100: "#300000",
          200: "#620000",
          300: "#900101",
          400: "#BC0C0C",
          500: "#D92121",
          600: "#EE3B3B",
          700: "#FF6F6F",
          800: "#FF8686",
          900: "#FFACAC",
        },
        blue: {
          100: "#001330",
          200: "#002762",
          300: "#013B90",
          400: "#0C52BC",
          500: "#216AD9",
          600: "#3B82EE",
          700: "#6FA8FF",
          800: "#86B6FF",
          900: "#ACCDFF",
        },
      },
    },
    keyframes: {
      fadeIn: {
        '0%': { opacity: '0' },
        '100%': { opacity: '1' }
      }
    },
    animation: {
      fadeIn: 'fadeIn 0.5s ease-in-out'
    }
  },
  plugins: [
    require('flowbite/plugin'),
  ]
}
