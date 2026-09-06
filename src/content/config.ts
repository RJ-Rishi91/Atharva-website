import { defineCollection, z } from 'astro:content';

const journalCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.string(),
    dispatchId: z.string(),
    date: z.string(),
    readTime: z.string(),
    volume: z.string().default('VOL. 04 // ISSUE 08'),
    heroImage: z.string(),
    heroImageAlt: z.string(),
    focusPosition: z.string().default('center 35%'),
    curator: z.string().default('ATHARVA SHARMA'),
    board: z.string().default('DIRECT MALE RUNWAY'),
    location: z.string().default('UDAIPUR / MUMBAI / GLOBAL'),
    status: z.string().default('AVAILABLE'),
    order: z.number().default(1),
    prevSlug: z.string().optional(),
    prevTitle: z.string().optional(),
    nextSlug: z.string().optional(),
    nextTitle: z.string().optional(),
  }),
});

export const collections = {
  journal: journalCollection,
};
