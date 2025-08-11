/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{ts,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
    './web/src/**/*.{js,ts,jsx,tsx}'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        glass: 'rgba(15 15 15 / .62)',
        cyan: '#00E0FF',
        purple: '#A855F7',
        red: '#FF3B5C',
        green: '#00F5A0',
        dark: '#0F0F0F'
      },
      borderRadius: {
        card: '12px',
        modal: '24px'
      },
      fontFamily: {
        inter: ['var(--font-inter)', 'sans-serif'],
        space: ['var(--font-space)', 'sans-serif'],
        jetbrains: ['var(--font-mono)', 'monospace']
      }
    }
  },
  plugins: []
};
