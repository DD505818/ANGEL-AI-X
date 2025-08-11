module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        glass: 'rgba(15 15 15 / .62)',
        cyan: '#00E0FF',
        purple: '#A855F7',
        red: '#FF3B5C',
        green: '#00F5A0',
        dark: '#0F0F0F',
      },
      fontFamily: {
        inter: ['var(--font-inter)', 'sans-serif'],
        space: ['var(--font-space)', 'sans-serif'],
        mono: ['var(--font-mono)', 'monospace'],
      },
      borderRadius: {
        card: '12px',
        modal: '24px',
      },
      boxShadow: {
        glass: 'inset 0 0 2px rgba(255,255,255,0.1)',
      },
    },
  },
  plugins: [],
};
