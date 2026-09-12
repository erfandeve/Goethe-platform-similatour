"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { mediaUrl } from "@/lib/utils";

import type { AudioTrack } from "./types";

/**
 * The listening player: a ring that fills as the recording plays. There is no
 * scrubbing and no pause — the track runs the number of times the exam allows,
 * with a short break between passes, and then stays silent.
 */
export function AudioRing({
  track,
  onPlay,
  onFinished,
  prompt = "Lesen Sie jetzt die Aufgaben.",
}: {
  track: AudioTrack;
  onPlay?: () => void;
  onFinished?: () => void;
  /** What to do during the reading time; picture tasks look at the pictures instead. */
  prompt?: string;
}) {
  const audio = useRef<HTMLAudioElement>(null);
  const [progress, setProgress] = useState(0);
  const [countdown, setCountdown] = useState(track.pre_read_seconds);
  const [pass, setPass] = useState(0); // completed passes
  const [state, setState] = useState<"reading" | "playing" | "pause" | "done">("reading");

  // The runner mounts one AudioRing per track, so no reset effect is needed.
  const start = useCallback(() => {
    setState("playing");
    onPlay?.();
    const element = audio.current;
    if (!element) return;
    element.currentTime = 0;
    void element.play().catch(() => setState("done"));
  }, [onPlay]);

  useEffect(() => {
    if (state !== "reading") return;
    const timer = setTimeout(
      () => (countdown <= 1 ? start() : setCountdown(countdown - 1)),
      1000,
    );
    return () => clearTimeout(timer);
  }, [state, countdown, start]);

  // A text heard twice repeats itself after a short break, as in the real exam.
  useEffect(() => {
    if (state !== "pause") return;
    const timer = setTimeout(start, 5000);
    return () => clearTimeout(timer);
  }, [state, start]);

  const circumference = 2 * Math.PI * 46;
  const playing = state === "playing";

  return (
    <div className="flex flex-col items-center py-10" style={{ background: "#f4f4f2" }}>
      <audio
        ref={audio}
        src={mediaUrl(track.url)}
        preload="auto"
        onTimeUpdate={(event) => {
          const element = event.currentTarget;
          setProgress(element.duration ? element.currentTime / element.duration : 0);
        }}
        onEnded={() => {
          const done = pass + 1;
          setPass(done);
          setProgress(1);
          if (done < track.plays) {
            setState("pause");
          } else {
            setState("done");
            onFinished?.();
          }
        }}
      >
        <track kind="captions" />
      </audio>

      <div className="relative grid size-32 place-items-center">
        <svg viewBox="0 0 100 100" className="absolute size-32 -rotate-90" aria-hidden>
          <circle cx="50" cy="50" r="46" fill="#fff" stroke="#dcdcd8" strokeWidth="3" />
          <circle
            cx="50"
            cy="50"
            r="46"
            fill="none"
            stroke="var(--exam-green)"
            strokeWidth="3.5"
            strokeLinecap="round"
            strokeDasharray={`${progress * circumference} ${circumference}`}
          />
        </svg>
        <span className="relative flex flex-col items-center gap-1">
          <svg viewBox="0 0 24 24" className="size-7" fill="currentColor" aria-hidden>
            <path d="M4 9v6h4l5 4V5L8 9H4Zm12.5 3a4.5 4.5 0 0 0-2-3.7v7.4a4.5 4.5 0 0 0 2-3.7Zm2.5 0a7 7 0 0 0-3.5-6v2.1a5 5 0 0 1 0 7.8V18a7 7 0 0 0 3.5-6Z" />
          </svg>
          <span className="flex h-4 items-end gap-0.5" aria-hidden>
            {[0.35, 0.8, 0.5, 1, 0.3, 0.6].map((height, index) => (
              <span
                key={index}
                className="w-0.5 bg-current transition-all duration-300"
                style={{
                  height: playing ? `${height * 100}%` : "12%",
                  opacity: playing ? 1 : 0.35,
                }}
              />
            ))}
          </span>
        </span>
      </div>

      <p className="mt-4 text-sm font-semibold" style={{ color: "var(--exam-green-dark)" }} dir="ltr">
        {track.label}
      </p>

      <p className="mt-1 max-w-md text-center text-xs" style={{ color: "var(--exam-muted)" }} dir="ltr">
        {state === "reading"
          ? `${prompt} Der Text startet in ${countdown} Sekunden.`
          : state === "playing"
            ? track.plays > 1
              ? `Sie hören den Text ${track.plays}× · Durchgang ${pass + 1}`
              : "Sie hören den Text einmal."
            : state === "pause"
              ? "Kurze Pause – der Text wird gleich wiederholt."
              : "Der Text wurde abgespielt."}
      </p>
    </div>
  );
}
