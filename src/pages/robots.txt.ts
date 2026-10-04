// src/pages/robots.txt.ts
// Dynamic robots.txt route with site url resolution

export async function GET(context: any) {
  const siteUrl = context.site?.toString().replace(/\/$/, '') || 'https://atharvasharma.co.in';

  const robots = `# ==============================================================================
# Robots Exclusion Standard for Atharva Sharma Modeling Portfolio
# Host: ${siteUrl}
# Contact: atharva@atharvasharma.co.in
# ==============================================================================

User-agent: *
Allow: /
Allow: /assets/
Allow: /journal/
Allow: /portfolio/
Allow: /comp-card/
Allow: /digitals/
Allow: /stats/
Allow: /about/
Allow: /contact/
Allow: /privacy-policy/
Allow: /terms/
Allow: /sitemap/

Disallow: /admin
Disallow: /admin/
Disallow: /admin/*
Disallow: /api/admin/
Disallow: /api/admin/*

User-agent: Googlebot
Allow: /
Disallow: /admin/
Disallow: /api/admin/

User-agent: Googlebot-Image
Allow: /assets/
Allow: /

User-agent: Bingbot
Allow: /
Disallow: /admin/
Disallow: /api/admin/

User-agent: Applebot
Allow: /
Disallow: /admin/
Disallow: /api/admin/

User-agent: ChatGPT-User
Allow: /
Disallow: /admin/

User-agent: GPTBot
Allow: /
Disallow: /admin/

User-agent: PerplexityBot
Allow: /
Disallow: /admin/

User-agent: ClaudeBot
Allow: /
Disallow: /admin/

Sitemap: ${siteUrl}/sitemap.xml
`;

  return new Response(robots, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
}
