"use client";

import { forwardRef, useCallback, useEffect, useImperativeHandle, useRef, useState } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import { formatClock } from "@/lib/format";
import type { LessonVideo } from "@/lib/learning";
import { cn, mediaUrl } from "@/lib/utils";

export interface VideoPlayerHandle {
  play: () => Promise<void>;
  pause: () => void;
  replay: () => Promise<void>;
}

/**
 * A full HTML5 player: normal controls stay available, and every position
 * change is reported upwards so lesson progress survives a reload.
 */
export const VideoPlayer = forwardRef<
  VideoPlayerHandle,
  {
    video: LessonVideo;
    dict: Dictionary;
    accent: string;
    autoPlay: boolean;
    onEnded: () => void;
    onProgress: (position: number, duration: number) => void;
    onAutoplayBlocked: () => void;
  }
>(function VideoPlayer(
  { video, dict, accent, autoPlay, onEnded, onProgress, onAutoplayBlocked },
  ref,
) {
  const element = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);
  const [position, setPosition] = useState(0);
  const [duration, setDuration] = useState(video.duration_seconds || 0);
  const [volume, setVolume] = useState(1);
  const [blocked, setBlocked] = useState(false);
  const reported = useRef(0);

  const play = useCallback(async () => {
    const node = element.current;
    if (!node) return;
    try {
      await node.play();
      setBlocked(false);
    } catch {
      // Autoplay policies vary; surface a play button instead of stalling.
      setBlocked(true);
      onAutoplayBlocked();
    }
  }, [onAutoplayBlocked]);

  useImperativeHandle(ref, () => ({
    play,
    pause: () => element.current?.pause(),
    replay: async () => {
      const node = element.current;
      if (!node) return;
      node.currentTime = 0;
      await play();
    },
  }));

  // Keep the latest callbacks reachable without making them effect dependencies:
  // the parent re-renders several times a second while recording, and a changing
  // identity here would reload and restart the clip on every one of those renders.
  const latest = useRef({ play, autoPlay });
  latest.current = { play, autoPlay };

  // A new lesson — and only a new lesson — starts from the top of its own file.
  useEffect(() => {
    const node = element.current;
    if (!node) return;
    setPosition(0);
    setBlocked(false);
    reported.current = 0;
    node.load();
    if (latest.current.autoPlay) void latest.current.play();
  }, [video.id]);

  function seek(next: number) {
    const node = element.current;
    if (!node) return;
    node.currentTime = Math.max(0, Math.min(duration || node.duration || 0, next));
  }

  return (
    <div className="relative overflow-hidden rounded-3xl bg-black/60 ring-1 ring-white/10">
      <video
        ref={element}
        className="aspect-video w-full bg-black"
        playsInline
        preload="metadata"
        poster={video.poster_url ? mediaUrl(video.poster_url) : undefined}
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
        onLoadedMetadata={(event) => {
          const node = event.currentTarget;
          setDuration(node.duration || video.duration_seconds);
          const resume = video.progress?.position_seconds ?? 0;
          if (resume > 1 && !video.progress?.completed && resume < node.duration - 1) {
            node.currentTime = resume;
          }
        }}
        onTimeUpdate={(event) => {
          const node = event.currentTarget;
          setPosition(node.currentTime);
          // Save at most every five seconds; the end is saved by onEnded.
          if (node.currentTime - reported.current >= 5) {
            reported.current = node.currentTime;
            onProgress(node.currentTime, node.duration || 0);
          }
        }}
        onEnded={(event) => {
          setPlaying(false);
          onProgress(event.currentTarget.duration || 0, event.currentTarget.duration || 0);
          onEnded();
        }}
      >
        <source src={mediaUrl(video.video_url)} type="video/mp4" />
        <track kind="captions" />
      </video>

      {blocked ? (
        <button
          type="button"
          onClick={play}
          className="absolute inset-0 grid place-items-center bg-ink-950/60 backdrop-blur-sm"
        >
          <span className="flex flex-col items-center gap-3">
            <span
              className="grid size-16 place-items-center rounded-full text-ink-950"
              style={{ background: accent }}
              aria-hidden
            >
              <svg viewBox="0 0 24 24" className="size-7 flip-x" fill="currentColor">
                <path d="M8 5.5v13l11-6.5-11-6.5Z" />
              </svg>
            </span>
            <span className="text-sm text-mist-200">{dict.learning.autoplayBlocked}</span>
          </span>
        </button>
      ) : null}

      <div className="flex flex-wrap items-center gap-3 border-t border-white/8 bg-ink-900/80 px-4 py-3">
        <button
          type="button"
          onClick={() => (playing ? element.current?.pause() : void play())}
          className="grid size-10 shrink-0 place-items-center rounded-full text-ink-950 transition hover:scale-105"
          style={{ background: accent }}
          aria-label={playing ? "Pause" : dict.learning.actions.play}
        >
          {playing ? (
            <svg viewBox="0 0 24 24" className="size-4" fill="currentColor" aria-hidden>
              <rect x="7" y="5" width="3.5" height="14" rx="1" />
              <rect x="13.5" y="5" width="3.5" height="14" rx="1" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" className="size-4 flip-x" fill="currentColor" aria-hidden>
              <path d="M8 5.5v13l11-6.5-11-6.5Z" />
            </svg>
          )}
        </button>

        <button type="button" onClick={() => seek(position - 5)} className="glass rounded-lg px-2.5 py-1.5 text-xs">
          −5s
        </button>
        <button type="button" onClick={() => seek(position + 5)} className="glass rounded-lg px-2.5 py-1.5 text-xs">
          +5s
        </button>

        <span className="tnum text-xs text-mist-500">{formatClock(position)}</span>
        <input
          type="range"
          min={0}
          max={duration || 1}
          step={0.1}
          value={position}
          onChange={(event) => seek(Number(event.target.value))}
          className="h-1.5 min-w-24 flex-1 cursor-pointer appearance-none rounded-full"
          style={{
            background: `linear-gradient(90deg, ${accent} ${(position / (duration || 1)) * 100}%, rgba(255,255,255,0.12) ${(position / (duration || 1)) * 100}%)`,
          }}
          aria-label="Seek"
        />
        <span className="tnum text-xs text-mist-500">{formatClock(duration)}</span>

        <input
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={volume}
          onChange={(event) => {
            const next = Number(event.target.value);
            setVolume(next);
            if (element.current) element.current.volume = next;
          }}
          className="hidden h-1.5 w-20 cursor-pointer appearance-none rounded-full bg-white/12 sm:block"
          aria-label="Volume"
        />

        <button
          type="button"
          onClick={() => element.current?.requestFullscreen?.()}
          className={cn("glass rounded-lg px-2.5 py-1.5 text-xs")}
          aria-label="Fullscreen"
        >
          ⛶
        </button>
      </div>
    </div>
  );
});
