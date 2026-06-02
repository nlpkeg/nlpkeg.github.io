import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Research directions (6). See docs design §3.1.
const research = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/research' }),
  schema: z.object({
    order: z.number(),
    icon: z.string(),
    titleZh: z.string(),
    titleEn: z.string(),
    summaryZh: z.string(),
    summaryEn: z.string(),
    highlights: z.array(z.string()).default([]),
  }),
});

// Open-source tools (maps github.com/nlpkeg).
const tools = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/tools' }),
  schema: z.object({
    order: z.number(),
    name: z.string(),
    badge: z.string().optional(), // e.g. "ACL 2025 Demo · MIT"
    stars: z.string().optional(), // free-form: "★ 14" / "benchmark"
    url: z.string().url().optional(),
    descZh: z.string(),
    descEn: z.string(),
    flagship: z.boolean().default(false),
  }),
});

// Faculty / students.
const people = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/people' }),
  schema: z.object({
    order: z.number(),
    nameZh: z.string(),
    nameEn: z.string(),
    roleZh: z.string(),
    roleEn: z.string(),
    group: z.enum(['faculty', 'engineer', 'secretary', 'phd', 'master']).default('faculty'),
    advisor: z.boolean().default(true), // 研究生导师 label (faculty only)
    interestsZh: z.string(),
    interestsEn: z.string(),
    bioZh: z.string().optional(),
    bioEn: z.string().optional(),
    photo: z.string().optional(),
    active: z.boolean().default(true),
    links: z
      .object({
        homepage: z.string().url().optional(),
        scholar: z.string().url().optional(),
        dblp: z.string().url().optional(),
        github: z.string().url().optional(),
        email: z.string().optional(),
      })
      .default({}),
  }),
});

// Publications. Links point to the official venue page (ACL Anthology / OpenReview / AAAI / proceedings).
const publications = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/publications' }),
  schema: z.object({
    title: z.string(),
    authors: z.string(),
    venue: z.string(), // e.g. "ACL 2025 (Demo)"
    year: z.number(),
    highlight: z.string().optional(), // e.g. "Spotlight" / "Oral" / "Best Paper"
    links: z
      .object({
        paper: z.string().url().optional(), // official venue URL
        arxiv: z.string().url().optional(),
        code: z.string().url().optional(),
        bibtex: z.string().optional(),
        project: z.string().url().optional(),
      })
      .default({}),
  }),
});

// News / blog (bilingual via `lang`).
const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: z.object({
    lang: z.enum(['zh', 'en']).default('zh'),
    title: z.string(),
    date: z.coerce.date(),
    tag: z.string().optional(),
    summary: z.string(),
    cover: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { research, tools, people, publications, news };
