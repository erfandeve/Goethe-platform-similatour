"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatClock } from "@/lib/format";
import type { EpisodeDetail } from "@/lib/types";
import { alpha, cn, mediaUrl } from "@/lib/utils";

const SPEEDS = [0.75, 1, 1.25, 1.5];

export function Player({
  episode,
  locale,
  dict,
  isAuthed,
}: {
  episode: EpisodeDetail;
  locale: Locale;
  dict: Dictionary;
  isAuthed: boolean;
}) {
  const audio = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const [time, setTime] = useState(episode.progress?.position_seconds ?? 0);
  const [duration, setDuration] = useState(episode.duration_seconds);
  const [speed, setSpeed] = useState(1);
  const [showTranslation, setShowTranslation] = useState(true);
  const [bookmarked, setBookmarked] = useState(episode.bookmarked);
  const accent = episode.podcast?.accent ?? "#6d5efc";

  const played = (time / (duration || 1)) * 100;
  const activeLine = episode.transcript.findIndex(
    (line) => time >= line.start && time < line.end,
  );

  const toggle = useCallback(() => {
    const element = audio.current;
    if (!element) return;
    if (element.paused) {
      void element.play().catch(() => setPlaying(false));
      void callApi(`podcasts/episodes/${episode.slug}/play`, { method: "POST" }).catch(() => {});
    } else {
      element.pause();
    }
  }, [episode.slug]);

  function seek(seconds: number) {
    const element = audio.current;
    if (!element) return;
    element.currentTime = Math.max(0, Math.min(duration, seconds));
    setTime(element.currentTime);
  }

  // Persist the listening position so the panel can offer "continue listening".
  useEffect(() => {
    if (!isAuthed) return;
    const timer = setInterval(() => {
      const element = audio.current;
      if (!element || element.paused) return;
      void callApi(`podcasts/episodes/${episode.slug}/progress`, {
        method: "POST",
        body: {
          position_seconds: Math.floor(element.currentTime),
          completed: element.currentTime / (element.duration || 1) > 0.95,
        },
      }).catch(() => {});
    }, 20000);
    return () => clearInterval(timer);
  }, [episode.slug, isAuthed]);

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.code === "Space" && event.target === document.body) {
        event.preventDefault();
        toggle();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [toggle]);

  async function toggleBookmark() {
    if (!isAuthed) return;
    const previous = bookmarked;
    setBookmarked(!previous);
    try {
      const data = await callApi<{ bookmarked: boolean }>(
        `podcasts/episodes/${episode.slug}/bookmark`,
        { method: "POST" },
      );
      setBookmarked(data.bookmarked);
    } catch {
      setBookmarked(previous);
    }
  }

  return (
    <div className="space-y-8">
      <div className="glass rounded-3xl p-6 md:p-8">
        <audio
          ref={audio}
          src={mediaUrl(episode.audio_url)}
          preload="metadata"
          onPlay={() => setPlaying(true)}
          onPause={() => setPlaying(false)}
          onTimeUpdate={(event) => setTime(event.currentTarget.currentTime)}
          onLoadedMetadata={(event) => {
            setDuration(event.currentTarget.duration || episode.duration_seconds);
            if (episode.progress?.position_seconds) {
              event.currentTarget.currentTime = episode.progress.position_seconds;
            }
          }}
        >
          <track kind="captions" />
        </audio>

        <div className="flex items-center gap-5">
          <button
            type="button"
            onClick={toggle}
            className="grid size-16 shrink-0 place-items-center rounded-full transition hover:scale-105"
            style={{ background: accent, color: "#050510" }}
            aria-label={playing ? dict.podcasts.player.pause : dict.podcasts.player.play}
          >
            {playing ? (
              <svg viewBox="0 0 24 24" className="size-6" fill="currentColor" aria-hidden>
                <rect x="7" y="5" width="3.5" height="14" rx="1" />
                <rect x="13.5" y="5" width="3.5" height="14" rx="1" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" className="size-6 flip-x" fill="currentColor" aria-hidden>
                <path d="M8 5.5v13l11-6.5-11-6.5Z" />
              </svg>
            )}
          </button>

          <div className="min-w-0 flex-1">
            <div className="mb-2 flex items-center justify-between text-xs text-mist-500">
              <span className="tnum">{formatClock(time)}</span>
              <span className="tnum">{formatClock(duration)}</span>
            </div>
            <input
              type="range"
              min={0}
              max={duration || 1}
              value={time}
              onChange={(event) => seek(Number(event.target.value))}
              className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-white/10 accent-violet-400"
              style={{
                // The played portion grows from the start edge, which is the
                // right-hand side once the page is in Persian.
                background: `linear-gradient(to ${locale === "fa" ? "left" : "right"}, ${accent} ${played}%, rgba(255,255,255,0.1) ${played}%)`,
              }}
              aria-label={dict.podcasts.player.play}
            />
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={() => seek(time - 15)}
                className="glass rounded-lg px-2.5 py-1.5 text-xs"
              >
                −15s
              </button>
              <button
                type="button"
                onClick={() => seek(time + 15)}
                className="glass rounded-lg px-2.5 py-1.5 text-xs"
              >
                +15s
              </button>
              <div className="flex items-center gap-1">
                {SPEEDS.map((value) => (
                  <button
                    key={value}
                    type="button"
                    onClick={() => {
                      setSpeed(value);
                      if (audio.current) audio.current.playbackRate = value;
                    }}
                    className={cn(
                      "tnum rounded-lg px-2.5 py-1.5 text-xs transition",
                      speed === value ? "text-ink-950" : "glass text-mist-400",
                    )}
                    style={speed === value ? { background: accent } : undefined}
                  >
                    {value}×
                  </button>
                ))}
              </div>
              {isAuthed ? (
                <button
                  type="button"
                  onClick={toggleBookmark}
                  className={cn(
                    "glass ms-auto rounded-lg px-3 py-1.5 text-xs transition",
                    bookmarked && "text-amber-400",
                  )}
                >
                  {bookmarked ? "★" : "☆"} {dict.podcasts.bookmarks}
                </button>
              ) : null}
            </div>
          </div>
        </div>
      </div>

      {episode.transcript.length ? (
        <section>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-xl font-semibold">
              {dict.podcasts.player.transcript}
            </h2>
            <button
              type="button"
              onClick={() => setShowTranslation((value) => !value)}
              className="glass rounded-full px-4 py-2 text-xs transition hover:border-white/25"
            >
              {showTranslation
                ? dict.podcasts.player.hideTranslation
                : dict.podcasts.player.showTranslation}
            </button>
          </div>

          <ol className="space-y-2">
            {episode.transcript.map((line, index) => {
              const active = index === activeLine;
              return (
                <li key={`${line.start}-${index}`}>
                  <button
                    type="button"
                    onClick={() => seek(line.start)}
                    className={cn(
                      "flex w-full gap-4 rounded-2xl border px-5 py-4 text-start transition",
                      active
                        ? "border-transparent"
                        : "border-white/8 hover:border-white/20 hover:bg-white/3",
                    )}
                    style={active ? { background: alpha(accent, 0.14) } : undefined}
                  >
                    <span className="tnum w-12 shrink-0 pt-0.5 text-xs text-mist-600">
                      {formatClock(line.start)}
                    </span>
                    <span className="min-w-0 flex-1">
                      {line.speaker ? (
                        <span
                          className="mb-1 block text-[11px] font-semibold tracking-wider uppercase"
                          style={{ color: accent }}
                        >
                          {line.speaker}
                        </span>
                      ) : null}
                      <span lang="de" dir="ltr" className="block text-sm leading-relaxed text-start text-mist-100">
                        {line.text}
                      </span>
                      {showTranslation && line.translation ? (
                        <span
                          lang={locale}
                          className="mt-1.5 block text-xs leading-relaxed text-mist-500"
                        >
                          {line.translation}
                        </span>
                      ) : null}
                    </span>
                  </button>
                </li>
              );
            })}
          </ol>
        </section>
      ) : null}

      {episode.vocabulary.length ? (
        <section>
          <h2 className="font-display mb-4 text-xl font-semibold">
            {dict.podcasts.player.vocabulary}
          </h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {episode.vocabulary.map((item) => (
              <div key={item.term} className="glass rounded-2xl p-5">
                <p lang="de" dir="ltr" className="font-display text-start text-lg font-semibold">
                  {item.article ? (
                    <span className="me-1.5 text-sm" style={{ color: accent }}>
                      {item.article}
                    </span>
                  ) : null}
                  {item.term}
                </p>
                <p className="mt-1.5 text-sm text-mist-300">{item.meaning}</p>
                {item.example ? (
                  <p lang="de" dir="ltr" className="mt-3 border-s-2 border-white/12 ps-3 text-start text-xs text-mist-500">
                    {item.example}
                  </p>
                ) : null}
              </div>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
