import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { EpisodeCard } from "@/components/podcasts/EpisodeCard";
import { Player } from "@/components/podcasts/Player";
import { LevelBadge } from "@/components/ui/Badge";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, type Locale } from "@/i18n/config";
import { apiFetch, getAccessToken } from "@/lib/api";
import { compact, formatDate, formatNumber } from "@/lib/format";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";
import type { EpisodeDetail } from "@/lib/types";

export const revalidate = 300;

async function loadEpisode(slug: string, locale: Locale, token: string | null) {
  try {
    return await apiFetch<EpisodeDetail>(`/podcasts/episodes/${slug}/`, {
      locale,
      token,
      revalidate: token ? 0 : 300,
    });
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
  const [dict, episode] = await Promise.all([
    getDictionary(locale),
    loadEpisode(slug, locale, null),
  ]);
  if (!episode) return {};
  return buildMetadata({
    title: episode.title,
    description: episode.description.slice(0, 155),
    path: `/podcasts/episodes/${slug}`,
    locale,
    siteName: dict.meta.siteName,
    type: "article",
  });
}

export default async function EpisodePage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const token = await getAccessToken();
  const episode = await loadEpisode(slug, locale, token);
  if (!episode) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "PodcastEpisode",
    name: episode.title,
    description: episode.description,
    url: `${SITE_URL}/${locale}/podcasts/episodes/${episode.slug}`,
    datePublished: episode.published_at,
    timeRequired: `PT${Math.round(episode.duration_seconds / 60)}M`,
    episodeNumber: episode.number,
    partOfSeries: {
      "@type": "PodcastSeries",
      name: episode.podcast?.title,
      url: `${SITE_URL}/${locale}/podcasts/${episode.podcast?.slug}`,
    },
    associatedMedia: { "@type": "MediaObject", contentUrl: episode.audio_url },
  };

  return (
    <>
      <JsonLd data={jsonLd} />

      <div className="container-page grid gap-10 py-12 lg:grid-cols-[1.6fr_1fr]">
        <div>
          <nav className="mb-6 flex flex-wrap items-center gap-2 text-xs text-mist-500">
            <Link href={`/${locale}`} className="hover:text-mist-200">
              {dict.nav.home}
            </Link>
            <span aria-hidden>/</span>
            <Link href={`/${locale}/podcasts`} className="hover:text-mist-200">
              {dict.nav.podcasts}
            </Link>
            {episode.podcast ? (
              <>
                <span aria-hidden>/</span>
                <Link
                  href={`/${locale}/podcasts/${episode.podcast.slug}`}
                  className="hover:text-mist-200"
                >
                  {episode.podcast.title}
                </Link>
              </>
            ) : null}
          </nav>

          <div className="flex flex-wrap items-center gap-3">
            <LevelBadge level={episode.level} />
            <span className="tnum text-xs text-mist-500">
              {formatNumber(Math.round(episode.duration_seconds / 60), locale)}{" "}
              {dict.podcasts.card.minutes}
            </span>
            <span className="tnum text-xs text-mist-500">
              {compact(episode.plays, locale)} {dict.podcasts.card.plays}
            </span>
            <span className="text-xs text-mist-600">{formatDate(episode.published_at, locale)}</span>
          </div>

          <h1 className="font-display mt-4 text-3xl leading-tight font-semibold text-balance md:text-5xl">
            {episode.title}
          </h1>
          <p className="text-muted mt-4 max-w-2xl">{episode.description}</p>

          <div className="mt-8">
            <Player episode={episode} locale={locale} dict={dict} isAuthed={Boolean(token)} />
          </div>
        </div>

        <aside className="lg:sticky lg:top-28 lg:self-start">
          <h2 className="font-display mb-4 text-lg font-semibold">{dict.podcasts.player.more}</h2>
          <div className="space-y-3">
            {episode.more_episodes.map((item) => (
              <EpisodeCard key={item.id} episode={item} locale={locale} dict={dict} />
            ))}
          </div>
        </aside>
      </div>
    </>
  );
}
