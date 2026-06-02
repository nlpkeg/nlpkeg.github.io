// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// GitHub Pages org site: nlpkeg/nlpkeg.github.io serves at root.
export default defineConfig({
  site: 'https://nlpkeg.github.io',
  base: '/',
  i18n: {
    defaultLocale: 'zh',
    locales: ['zh', 'en'],
    routing: {
      prefixDefaultLocale: false, // zh at /, en at /en/
    },
  },
  vite: {
    // Cast: Tailwind's Vite plugin and Astro's bundled Vite ship slightly
    // different Plugin types; the runtime is compatible.
    plugins: [/** @type {any} */ (tailwindcss())],
  },
});
