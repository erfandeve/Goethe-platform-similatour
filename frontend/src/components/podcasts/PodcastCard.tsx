import Link from "next/link";

import { LevelBadge } from "@/components/ui/Badge";
import { CoverArt } from "@/components/ui/CoverArt";
import { Spotlight } from "@/components/ui/Spotlight";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { compact } from "@/lib/format";
import type { Podcast } from "@/lib/types";

export function PodcastCard({
  podcast,
  locale,
  dict,
}: {
  podcast: Podcast;
  locale: Locale;
  dict: Dictionary;
}) {
  return (
    <Spotlight accent={podcast.accent} className="h-full">
      <Link
        href={`/${locale}/podcasts/${podcast.slug}`}
        className="glass group flex h-full flex-col overflow-hidden rounded-3xl transition-all duration-500 hover:-translate-y-1.5 hover:border-white/20"
      >
        <CoverArt
          accent={podcast.accent}
          label={podcast.title.slice(0, 2)}
          caption={podcast.category?.title ?? ""}
          src={podcast.cover}
          alt={podcast.title}
          ratio="aspect-square"
        />
        <div className="flex flex-1 flex-col p-5">
          <div className="mb-3 flex items-center gap-2">
            <LevelBadge level={podcast.level} />
            <span className="tnum text-[11px] text-mist-500">
              {podcast.episodes_count} {dict.podcasts.card.episodes}
            </span>
          </div>
          <h3 className="font-display text-lg leading-snug font-semibold transition-colors group-hover:text-violet-400">
            {podcast.title}
          </h3>
          <p className="text-muted mt-2 line-clamp-2 text-sm">{podcast.tagline}</p>
          <div className="mt-auto flex items-center gap-2 pt-4 text-xs text-mist-500">
            <span className="grid size-6 place-items-center rounded-full bg-white/8 text-[10px] font-bold">
              {podcast.host_name.slice(0, 1)}
            </span>
            <span>{podcast.host_name}</span>
            <span className="tnum ms-auto">
              {compact(podcast.plays, locale)} {dict.podcasts.card.plays}
            </span>
          </div>
        </div>
      </Link>
    </Spotlight>
  );
}
