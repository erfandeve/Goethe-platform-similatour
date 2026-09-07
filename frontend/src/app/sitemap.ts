import type { MetadataRoute } from "next";

import { locales } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { SITE_URL } from "@/lib/seo";

interface FeedEntry {
  slug: string;
  updated: string | null;
}

interface Feed {
  articles: FeedEntry[];
  courses: FeedEntry[];
  exams: FeedEntry[];
  podcasts: FeedEntry[];
  episodes: FeedEntry[];
}

const STATIC_PATHS = ["", "/courses", "/exams", "/podcasts", "/plans", "/about", "/contact", "/articles"];

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  let feed: Feed = { articles: [], courses: [], exams: [], podcasts: [], episodes: [] };
  try {
    feed = await apiFetch<Feed>("/sitemap-feed/", { revalidate: 3600 });
  } catch {
    // A sitemap without dynamic entries still beats a 500 for crawlers.
  }

  const entries: MetadataRoute.Sitemap = [];

  const alternatesFor = (path: string) => ({
    languages: Object.fromEntries(locales.map((code) => [code, `${SITE_URL}/${code}${path}`])),
  });

  for (const locale of locales) {
    for (const path of STATIC_PATHS) {
      entries.push({
        url: `${SITE_URL}/${locale}${path}`,
        lastModified: new Date(),
        changeFrequency: path === "" ? "daily" : "weekly",
        priority: path === "" ? 1 : 0.8,
        alternates: alternatesFor(path),
      });
    }

    const groups: [FeedEntry[], string, number][] = [
      [feed.courses, "/courses", 0.9],
      [feed.exams, "/exams", 0.9],
      [feed.podcasts, "/podcasts", 0.7],
      [feed.episodes, "/podcasts/episodes", 0.6],
      [feed.articles, "/articles", 0.85],
    ];

    for (const [items, prefix, priority] of groups) {
      for (const item of items) {
        const path = `${prefix}/${item.slug}`;
        entries.push({
          url: `${SITE_URL}/${locale}${path}`,
          lastModified: item.updated ? new Date(item.updated) : new Date(),
          changeFrequency: "weekly",
          priority,
          alternates: alternatesFor(path),
        });
      }
    }
  }

  return entries;
}
