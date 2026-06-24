/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        terminal: {
          bg: '#0a0a0a',
          text: '#ffffff',
          green: '#00ff88',
          border: 'rgba(255,255,255,0.08)',
        },
        'neon-green': '#00ff88',
        'neon-green-dim': '#00c853',
        'futuristic-black': '#0a0a0a',
        'futuristic-card': '#111111',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Orbitron', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulseSlow 6s ease-in-out infinite',
      },
      keyframes: {
        pulseSlow: {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.6' },
          '50%': { transform: 'scale(1.08)', opacity: '0.9' },
        }
      }
    },
  },
  plugins: [],
}
