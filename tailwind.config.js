module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx}', './hooks/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#162033',
        canvas: '#f4f6fb',
        card: '#ffffff',
        muted: '#63708a',
        border: '#d9e0ec',
        accent: '#1760ff',
        accentSoft: '#e5eeff',
        accentStrong: '#0d45c7',
        success: '#0f9f6e',
        successSoft: '#dff6ed',
        warning: '#c77700',
        warningSoft: '#fff2dd',
        danger: '#d14343',
        dangerSoft: '#ffe6e6',
        panel: '#eef2f8',
      },
      borderRadius: {
        panel: '1.25rem',
      },
      boxShadow: {
        soft: '0 20px 45px rgba(22, 32, 51, 0.08)',
        lift: '0 8px 24px rgba(23, 96, 255, 0.12)',
      },
      fontFamily: {
        sans: ['"Avenir Next"', '"Segoe UI Variable Text"', '"Segoe UI"', '"Helvetica Neue"', 'sans-serif'],
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
