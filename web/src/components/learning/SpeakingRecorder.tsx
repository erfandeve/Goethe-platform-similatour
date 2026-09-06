"use client";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";
import type { SpeakingState } from "@/lib/learning";
import { alpha, cn } from "@/lib/utils";

import type { SpeakingError } from "@/hooks/useSpeakingTeacher";

const BUSY: SpeakingState[] = ["UPLOADING", "TRANSCRIBING", "ANALYZING"];

export function SpeakingRecorder({
  state,
  waitingForLearner = false,
  error,
  errorDetail,
  elapsed,
  remaining,
  maxSeconds,
  accent,
  locale,
  dict,
  onStart,
  onStop,
  onCancel,
  onRetry,
}: {
  state: SpeakingState;
  /** True when the learner opted out of the automatic start. */
  waitingForLearner?: boolean;
  error: SpeakingError | null;
  errorDetail: string;
  elapsed: number;
  remaining: number;
  maxSeconds: number;
  accent: string;
  locale: Locale;
  dict: Dictionary;
  onStart: () => void;
  onStop: () => void;
  onCancel: () => void;
  onRetry: () => void;
}) {
  const recording = state === "RECORDING";
  const busy = BUSY.includes(state);

  const statusText = recording
    ? dict.learning.states.listening
    : state === "UPLOADING"
      ? dict.learning.states.processing
      : state === "TRANSCRIBING"
        ? dict.learning.states.transcribing
        : state === "ANALYZING"
          ? dict.learning.states.analyzing
          : state === "ERROR"
            ? dict.learning.states.error
            : dict.learning.states.idle;

  const errorText =
    error === "unsupported"
      ? dict.learning.recorder.unsupported
      : error === "denied"
        ? dict.learning.recorder.denied
        : error === "too_short"
          ? dict.learning.recorder.tooShort
          : error === "empty"
            ? dict.learning.result.empty
            : errorDetail || dict.common.error;

  return (
    <div className="glass rounded-3xl p-6 text-center">
      <div className="relative mx-auto grid size-28 place-items-center">
        {recording ? (
          <span
            className="absolute inset-0 animate-ping rounded-full"
            style={{ background: alpha(accent, 0.25) }}
            aria-hidden
          />
        ) : null}

        <button
          type="button"
          onClick={recording ? onStop : onStart}
          disabled={busy}
          className={cn(
            "relative grid size-24 place-items-center rounded-full transition-transform",
            !busy && "hover:scale-105",
            busy && "cursor-wait opacity-70",
          )}
          style={{
            background: recording ? "#ff6b6b" : accent,
            color: "#05050f",
          }}
          aria-label={recording ? dict.learning.recorder.stop : dict.learning.recorder.start}
        >
          {busy ? (
            <span className="size-8 animate-spin rounded-full border-2 border-ink-950/25 border-t-ink-950" />
          ) : recording ? (
            <svg viewBox="0 0 24 24" className="size-8" fill="currentColor" aria-hidden>
              <rect x="6.5" y="6.5" width="11" height="11" rx="2" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" className="size-9" fill="currentColor" aria-hidden>
              <path d="M12 15a3.5 3.5 0 0 0 3.5-3.5v-5a3.5 3.5 0 1 0-7 0v5A3.5 3.5 0 0 0 12 15Z" />
              <path d="M18.5 11.5a6.5 6.5 0 0 1-13 0H4a8 8 0 0 0 7 7.93V22h2v-2.57a8 8 0 0 0 7-7.93h-1.5Z" />
            </svg>
          )}
        </button>
      </div>

      <p className="mt-5 text-sm font-medium text-mist-100" aria-live="polite">
        {statusText}
      </p>
      {waitingForLearner && !recording && !busy && state !== "ERROR" ? (
        <p className="mt-1.5 text-xs text-mist-500">{dict.learning.recorder.manualHint}</p>
      ) : null}

      {recording ? (
        <>
          <p className="tnum mt-2 text-xs text-mist-500">
            {formatNumber(Math.floor(elapsed), locale)}s ·{" "}
            {formatNumber(Math.ceil(remaining), locale)}s {dict.learning.recorder.remaining}
          </p>
          <div className="mx-auto mt-3 h-1 w-40 overflow-hidden rounded-full bg-white/10">
            <div
              className="h-full rounded-full transition-[width] duration-200"
              style={{ width: `${(elapsed / maxSeconds) * 100}%`, background: accent }}
            />
          </div>
          <div className="mt-4 flex justify-center gap-2">
            <button
              type="button"
              onClick={onStop}
              className="rounded-full px-5 py-2 text-xs font-semibold text-ink-950"
              style={{ background: accent }}
            >
              {dict.learning.recorder.stop}
            </button>
            <button
              type="button"
              onClick={onCancel}
              className="glass rounded-full px-5 py-2 text-xs"
            >
              {dict.learning.recorder.cancel}
            </button>
          </div>
        </>
      ) : null}

      {state === "ERROR" ? (
        <div className="mt-4">
          <p className="rounded-2xl border border-rose-400/25 bg-rose-400/10 px-4 py-3 text-xs text-rose-300">
            {errorText}
          </p>
          {error !== "unsupported" ? (
            <button
              type="button"
              onClick={onRetry}
              className="mt-3 rounded-full px-5 py-2 text-xs font-semibold text-ink-950"
              style={{ background: accent }}
            >
              {dict.learning.actions.retry}
            </button>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
