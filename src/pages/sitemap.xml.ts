import { getCollection } from 'astro:content';

export async function GET(context: any) {
  const siteUrl = context.site?.toString().replace(/\/$/, '') || 'https://rj-rishi91.github.io';
  const base = (import.meta.env.BASE_URL || '').replace(/\/$/, '');
  const rootUrl = `${siteUrl}${base}`;

  const staticPages = [
    { path: '', priority: '1.0', changefreq: 'weekly', image: 'assets/images/atharva-studio-bw-stool.png', title: 'Atharva Sharma Modeling Portfolio' },
    { path: 'digitals', priority: '0.8', changefreq: 'monthly', image: 'assets/images/atharva-studio-bw-stool.png', title: 'Atharva Sharma Digitals' },
    { path: 'portfolio', priority: '0.9', changefreq: 'weekly', image: 'assets/images/atharva-kurta-palace-night.jpg', title: 'Atharva Sharma Lookbook Portfolio' },
    { path: 'stats', priority: '0.8', changefreq: 'monthly', image: 'assets/images/atharva-studio-bw-stool.png', title: 'Atharva Sharma Specifications' },
    { path: 'about', priority: '0.8', changefreq: 'monthly', image: 'assets/images/atharva-studio-bw-stool.png', title: 'About Atharva Sharma' },
    { path: 'journal', priority: '0.8', changefreq: 'weekly', image: 'assets/images/atharva-studio-bw-stool.png', title: 'Atharva Sharma Journal' },
    { path: 'contact', priority: '0.8', changefreq: 'monthly', image: 'assets/images/atharva-studio-bw-stool.png', title: 'Book Atharva Sharma' },
    { path: 'comp-card', priority: '0.8', changefreq: 'monthly', image: 'assets/images/atharva-studio-bw-stool.png', title: 'Atharva Sharma Comp-Card' },
  ];

  const journalEntries = await getCollection('journal');
  const today = new Date().toISOString().split('T')[0];

  const urls: Array<{ loc: string; lastmod?: string; changefreq: string; priority: string; imageLoc?: string; imageTitle?: string }> = [];

  staticPages.forEach((page) => {
    urls.push({
      loc: page.path ? `${rootUrl}/${page.path}` : rootUrl,
      lastmod: today,
      changefreq: page.changefreq,
      priority: page.priority,
      imageLoc: `${rootUrl}/${page.image}`,
      imageTitle: page.title,
    });
  });

  journalEntries.forEach((entry) => {
    urls.push({
      loc: `${rootUrl}/journal/${entry.slug}`,
      lastmod: entry.data.date,
      changefreq: 'monthly',
      priority: '0.7',
      imageLoc: `${rootUrl}/${entry.data.heroImage}`,
      imageTitle: entry.data.title,
    });
  });

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${urls
  .map(
    (u) => `  <url>
    <loc>${u.loc}</loc>
    ${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
    ${u.imageLoc ? `<image:image>
      <image:loc>${u.imageLoc}</image:loc>
      <image:title>${u.imageTitle}</image:title>
    </image:image>` : ''}
  </url>`
  )
  .join('\n')}
</urlset>`;

  return new Response(sitemapXml, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
