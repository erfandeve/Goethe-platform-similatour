import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { EpisodeCard } from "@/components/podcasts/EpisodeCard";
import { LevelBadge } from "@/components/ui/Badge";
import { CoverArt } from "@/components/ui/CoverArt";
import { Reveal } from "@/components/ui/Reveal";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, type Locale } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { compact, formatNumber } from "@/lib/format";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";
import type { Podcast } from "@/lib/types";

export const revalidate = 300;

async function loadShow(slug: string, locale: Locale) {
  try {
    return await apiFetch<Podcast>(`/podcasts/${slug}/`, { locale, revalidate: 300 });
  } catch {
    return null;
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}): Promise<Metadata> {
  const { locale, slug } = await params;
  if (!isLocale(locale)) return {};
  const [dict, show] = await Promise.all([getDictionary(locale), loadShow(slug, locale)]);
  if (!show) return {};
  return buildMetadata({
    title: show.title,
    description: show.tagline || (show.description ?? "").slice(0, 155),
    path: `/podcasts/${slug}`,
    locale,
    siteName: dict.meta.siteName,
    type: "article",
  });
}

export default async function PodcastDetailPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const show = await loadShow(slug, locale);
  if (!show) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "PodcastSeries",
    name: show.title,
    description: show.description ?? show.tagline,
    url: `${SITE_URL}/${locale}/podcasts/${show.slug}`,
    inLanguage: show.language,
    author: { "@type": "Person", name: show.host_name },
  };

  return (
    <>
      <JsonLd data={jsonLd} />

      <div className="container-page py-12">
        <nav className="mb-6 flex items-center gap-2 text-xs text-mist-500">
          <Link href={`/${locale}`} className="hover:text-mist-200">
            {dict.nav.home}
          </Link>
          <span aria-hidden>/</span>
          <Link href={`/${locale}/podcasts`} className="hover:text-mist-200">
            {dict.nav.podcasts}
          </Link>
        </nav>

        <div className="grid gap-8 md:grid-cols-[18rem_1fr]">
          <div className="glass overflow-hidden rounded-3xl">
            <CoverArt
              accent={show.accent}
              label={show.title.slice(0, 2)}
              caption={show.category?.title ?? ""}
              src={show.cover}
              alt={show.title}
              ratio="aspect-square"
            />
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-3">
              <LevelBadge level={show.level} />
              <span className="tnum text-xs text-mist-500">
                {formatNumber(show.episodes_count, locale)} {dict.podcasts.card.episodes}
              </span>
              <span className="tnum text-xs text-mist-500">
                {compact(show.plays, locale)} {dict.podcasts.card.plays}
              </span>
            </div>

            <h1 className="font-display mt-4 text-4xl leading-tight font-semibold text-balance md:text-5xl">
              {show.title}
            </h1>
            <p className="text-muted mt-4 text-lg">{show.tagline}</p>
            {show.description ? (
              <p className="text-muted mt-5 max-w-2xl leading-relaxed">{show.description}</p>
            ) : null}

            <div className="mt-6 flex items-center gap-3 text-sm text-mist-300">
              <span className="grid size-9 place-items-center rounded-full bg-white/8 text-xs font-bold">
                {show.host_name.slice(0, 1)}
              </span>
              <span>
                <span className="block text-[11px] tracking-wider text-mist-600 uppercase">
                  {dict.podcasts.card.host}
                </span>
                {show.host_name}
              </span>
            </div>
          </div>
        </div>

        <section className="mt-14">
          <h2 className="font-display mb-5 text-2xl font-semibold">{dict.podcasts.episodes}</h2>
          <div className="grid gap-3 lg:grid-cols-2">
            {(show.episodes ?? []).map((episode, index) => (
              <Reveal key={episode.id} delay={Math.min(index, 8) * 0.04}>
                <EpisodeCard episode={episode} locale={locale} dict={dict} />
              </Reveal>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
