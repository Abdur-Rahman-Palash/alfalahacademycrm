import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          gold: '#C9A84C',
          navy: '#1B2A4A',
          ivory: '#FAF8F3',
          emerald: '#2E7D52',
          charcoal: '#2D2D2D',
          gray: '#F0EDE8',
          red: '#C0392B',
          blue: '#3B82F6'
        }
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['"Inter"', 'sans-serif'],
        arabic: ['"Amiri"', 'serif'],
        mono: ['"JetBrains Mono"', 'monospace']
      },
      borderRadius: {
        'card': '16px'
      },
      boxShadow: {
        'card': '0 4px 20px rgba(0, 0, 0, 0.08)'
      }
    }
  },
  plugins: [],
}

export default config
