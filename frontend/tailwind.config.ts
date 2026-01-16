import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        aether: {
          void: '#0a0612',
          deep: '#1a0a2e',
          purple: '#2d1b4e',
          violet: '#4a2c6a',
          gold: '#c9a962',
          'gold-light': '#e8d5a3',
          'gold-dark': '#8b7340',
          cream: '#f5f0e8',
          mist: 'rgba(201, 169, 98, 0.1)',
        }
      },
      fontFamily: {
        display: ['"Playfair Display"', 'Georgia', 'serif'],
        body: ['"DM Sans"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'aurora': 'linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 25%, #1a0a2e 50%, #4a2c6a 75%, #1a0a2e 100%)',
        'gold-shimmer': 'linear-gradient(90deg, transparent, rgba(201, 169, 98, 0.3), transparent)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'particle': 'particle 8s linear infinite',
        'aurora': 'aurora 15s ease infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-20px) rotate(1deg)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(201, 169, 98, 0.2)' },
          '100%': { boxShadow: '0 0 40px rgba(201, 169, 98, 0.4)' },
        },
        particle: {
          '0%': { transform: 'translateY(100vh) rotate(0deg)', opacity: '0' },
          '10%': { opacity: '1' },
          '90%': { opacity: '1' },
          '100%': { transform: 'translateY(-100vh) rotate(720deg)', opacity: '0' },
        },
        aurora: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
        'gold': '0 0 30px rgba(201, 169, 98, 0.3)',
        'gold-lg': '0 0 60px rgba(201, 169, 98, 0.4)',
        'inner-gold': 'inset 0 0 30px rgba(201, 169, 98, 0.1)',
      },
    },
  },
  plugins: [],
}

export default config
