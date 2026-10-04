// src/pages/rss.xml.ts
// Standards-compliant RSS 2.0 Feed for Google News, Feed Readers & Fast Crawling
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context: any) {
  const siteUrl = context.site?.toString().replace(/\/$/, '') || 'https://atharvasharma.co.in';
  const journalEntries = await getCollection('journal');
  
  // Sort posts by publication date descending
  const sortedPosts = journalEntries.sort(
    (a, b) => new Date(b.data.date).getTime() - new Date(a.data.date).getTime()
  );

  return rss({
    title: 'ATHARVA SHARMA // Editorial Journal & Dispatches',
    description: 'Personal repository of Indian male fashion model Atharva Sharma documenting runway mechanics, high-fashion campaigns, royal draping, and contemporary South Asian menswear.',
    site: siteUrl,
    items: sortedPosts.map((post) => ({
      title: post.data.title,
      pubDate: new Date(post.data.date),
      description: post.data.description,
      link: `/journal/${post.slug}`,
      categories: [post.data.category],
      author: 'atharva@atharvasharma.co.in (Atharva Sharma)',
    })),
    customData: `<language>en-us</language><copyright>© 2026 Atharva Sharma. All rights reserved.</copyright>`,
  });
}
