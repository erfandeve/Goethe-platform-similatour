import Link from "next/link";

import { LevelBadge } from "@/components/ui/Badge";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";
import type { Episode } from "@/lib/types";
import { alpha } from "@/lib/utils";

export function EpisodeCard({
  episode,
  locale,
  dict,
}: {
  episode: Episode;
  locale: Locale;
  dict: Dictionary;
}) {
  const accent = episode.podcast?.accent ?? "#6d5efc";
  const minutes = Math.round(episode.duration_seconds / 60);

  return (
    <Link
      href={`/${locale}/podcasts/episodes/${episode.slug}`}
      className="glass group flex items-center gap-4 rounded-2xl p-4 transition-all duration-400 hover:translate-x-1 hover:border-white/20 rtl:hover:-translate-x-1"
    >
      <span
        className="grid size-12 shrink-0 place-items-center rounded-2xl transition-transform group-hover:scale-105"
        style={{ background: alpha(accent, 0.18), color: accent }}
        aria-hidden
      >
        <svg viewBox="0 0 24 24" className="size-5 flip-x" fill="currentColor">
          <path d="M8 5.5v13l11-6.5-11-6.5Z" />
        </svg>
      </span>

      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <LevelBadge level={episode.level} />
          {episode.is_premium ? (
            <span className="text-[10px] font-semibold tracking-wider text-amber-400 uppercase">
              {dict.podcasts.player.premium}
            </span>
          ) : null}
        </div>
        <h3 className="mt-1.5 truncate text-sm font-semibold">{episode.title}</h3>
        <p className="truncate text-xs text-mist-500">{episode.podcast?.title}</p>
      </div>

      <span className="tnum shrink-0 text-xs text-mist-500">
        {formatNumber(minutes, locale)} {dict.podcasts.card.minutes}
      </span>
    </Link>
  );
}
