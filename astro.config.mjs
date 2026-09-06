import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://atharvasharma.co.in',
  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    mdx(),
  ],
});
