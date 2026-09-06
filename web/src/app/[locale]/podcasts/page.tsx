import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { EpisodeCard } from "@/components/podcasts/EpisodeCard";
import { PodcastCard } from "@/components/podcasts/PodcastCard";
import { Reveal } from "@/components/ui/Reveal";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";
import type { Category, Episode, Paginated, Podcast } from "@/lib/types";
import { alpha } from "@/lib/utils";

export const revalidate = 300;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const dict = await getDictionary(locale);
  return buildMetadata({
    title: dict.podcasts.title,
    description: dict.podcasts.subtitle,
    path: "/podcasts",
    locale,
    siteName: dict.meta.siteName,
    keywords: ["Deutsch Podcast", "German listening", "پادکست آلمانی"],
  });
}

export default async function PodcastsPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const query = await searchParams;
  const dict = await getDictionary(locale);

  const category = typeof query.category === "string" ? query.category : "";
  const level = typeof query.level === "string" ? query.level : "";

  const search = new URLSearchParams({ page_size: "12" });
  if (category) search.set("category", category);
  if (level) search.set("level", level);

  const [shows, episodes, categories] = await Promise.all([
    apiFetch<Paginated<Podcast>>(`/podcasts/?${search.toString()}`, { locale, revalidate: 300 }),
    apiFetch<Paginated<Episode>>("/podcasts/episodes/?page_size=8", { locale, revalidate: 300 }),
    apiFetch<{ results: Category[] }>("/categories/?kind=podcast", { locale, revalidate: 900 }),
  ]);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: dict.podcasts.title,
    itemListElement: shows.results.map((show, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: show.title,
      url: `${SITE_URL}/${locale}/podcasts/${show.slug}`,
    })),
  };

  return (
    <>
      <JsonLd data={jsonLd} />

      <div className="container-page pt-10 pb-6">
        <p className="text-xs font-semibold tracking-[0.25em] text-violet-400 uppercase">
          {dict.nav.podcasts}
        </p>
        <h1 className="font-display mt-3 text-4xl leading-tight font-semibold text-balance md:text-6xl">
          {dict.podcasts.title}
        </h1>
        <p className="text-muted mt-4 max-w-2xl text-lg">{dict.podcasts.subtitle}</p>
      </div>

      <div className="container-page pb-6">
        <div className="flex flex-wrap gap-2">
          <Link
            href={`/${locale}/podcasts`}
            className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
              category ? "glass text-mist-300" : "bg-violet-500 text-ink-950"
            }`}
          >
            {dict.podcasts.allShows}
          </Link>
          {categories.results.map((item) => (
            <Link
              key={item.slug}
              href={`/${locale}/podcasts?category=${item.slug}`}
              className="rounded-full px-4 py-2 text-xs font-semibold transition"
              style={
                category === item.slug
                  ? { background: item.color, color: "#050510" }
                  : { background: alpha(item.color, 0.12), color: item.color }
              }
            >
              {item.title}
            </Link>
          ))}
        </div>
      </div>

      <div className="container-page grid gap-10 pb-24 lg:grid-cols-[1.7fr_1fr]">
        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {shows.results.map((show, index) => (
            <Reveal key={show.id} delay={index * 0.06}>
              <PodcastCard podcast={show} locale={locale} dict={dict} />
            </Reveal>
          ))}
        </div>

        <aside>
          <h2 className="font-display mb-4 text-xl font-semibold">{dict.podcasts.latest}</h2>
          <div className="space-y-3">
            {episodes.results.map((episode, index) => (
              <Reveal key={episode.id} delay={index * 0.04}>
                <EpisodeCard episode={episode} locale={locale} dict={dict} />
              </Reveal>
            ))}
          </div>
        </aside>
      </div>
    </>
  );
}
