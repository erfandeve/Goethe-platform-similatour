"use client";

import { useState } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";
import type { SpeakingAttempt } from "@/lib/learning";
import { alpha } from "@/lib/utils";

const CATEGORY_ORDER = [
  "grammar",
  "vocabulary",
  "sentence_structure",
  "word_order",
  "naturalness",
  "relevance",
] as const;

function scoreTone(score: number) {
  if (score >= 80) return "#34d399";
  if (score >= 60) return "#f59e0b";
  return "#ff6b6b";
}

/**
 * The verdict, ordered by what the learner needs first: the score, the sentence
 * they should have said, and the buttons — all without scrolling. The longer
 * breakdown sits behind a toggle so a good answer does not bury the next step.
 */
export function SpeakingResult({
  attempt,
  locale,
  dict,
  onRetry,
  onContinue,
  onReplay,
  isLast,
}: {
  attempt: SpeakingAttempt;
  locale: Locale;
  dict: Dictionary;
  onRetry: () => void;
  onContinue: () => void;
  onReplay: () => void;
  isLast: boolean;
}) {
  const [open, setOpen] = useState(false);
  const analysis = attempt.analysis;
  if (!analysis) return null;

  const tone = scoreTone(analysis.overall_score);
  const circumference = 2 * Math.PI * 26;

  return (
    <div className="space-y-3">
      {/* score · verdict · what to say instead — the essentials, above the fold */}
      <div className="glass rounded-3xl p-5">
        <div className="flex items-center gap-4">
          <div className="relative grid size-16 shrink-0 place-items-center">
            <svg viewBox="0 0 64 64" className="absolute size-16 -rotate-90" aria-hidden>
              <circle cx="32" cy="32" r="26" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="5" />
              <circle
                cx="32"
                cy="32"
                r="26"
                fill="none"
                stroke={tone}
                strokeWidth="5"
                strokeLinecap="round"
                strokeDasharray={`${(analysis.overall_score / 100) * circumference} ${circumference}`}
              />
            </svg>
            <span className="tnum font-display text-lg font-bold">
              {formatNumber(analysis.overall_score, locale)}
            </span>
          </div>

          <div className="min-w-0 flex-1">
            <p className="text-[11px] tracking-wider text-mist-500 uppercase">
              {dict.learning.result.score} · {analysis.cefr_estimate}
            </p>
            <p className="mt-1 line-clamp-3 text-sm leading-relaxed text-mist-200">
              {analysis.summary}
            </p>
          </div>
        </div>

        <div className="mt-4 border-t border-white/8 pt-4">
          <p className="mb-1.5 text-[11px] tracking-wider text-mist-500 uppercase">
            {dict.learning.result.corrected}
          </p>
          <p
            className="rounded-2xl px-4 py-3 text-sm leading-relaxed text-mint-400"
            style={{ background: alpha("#34d399", 0.1) }}
            lang="de"
            dir="ltr"
          >
            {analysis.corrected_answer}
          </p>
        </div>

        {!analysis.is_relevant ? (
          <p className="mt-3 rounded-2xl border border-amber-400/25 bg-amber-400/10 px-4 py-2.5 text-xs text-amber-300">
            {dict.learning.result.notRelevant}
          </p>
        ) : null}
      </div>

      {/* the next step is always reachable without scrolling */}
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={onContinue}
          className="flex-1 rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-5 py-3 text-sm font-semibold text-ink-950"
        >
          {isLast ? dict.learning.partDone.next : dict.learning.actions.continue}
        </button>
        <button type="button" onClick={onRetry} className="glass rounded-full px-5 py-3 text-sm">
          {dict.learning.actions.retry}
        </button>
        <button type="button" onClick={onReplay} className="glass rounded-full px-5 py-3 text-sm">
          {dict.learning.actions.replay}
        </button>
      </div>

      {analysis.mistakes.length ? (
        <div className="glass rounded-3xl p-5">
          <h3 className="mb-3 text-[11px] tracking-wider text-mist-500 uppercase">
            {dict.learning.result.mistakes}
          </h3>
          <ul className="space-y-3.5">
            {analysis.mistakes.slice(0, open ? undefined : 2).map((mistake, index) => (
              <li key={index} className="border-s-2 border-rose-400/40 ps-3.5">
                <p className="text-xs text-rose-300 line-through" lang="de" dir="ltr">
                  {mistake.original}
                </p>
                <p className="mt-1 text-sm font-medium text-mint-400" lang="de" dir="ltr">
                  {mistake.correction}
                </p>
                <p className="mt-1.5 text-xs leading-relaxed text-mist-400">
                  {mistake.explanation}
                </p>
              </li>
            ))}
          </ul>
          {!open && analysis.mistakes.length > 2 ? (
            <p className="tnum mt-3 text-xs text-mist-600">
              +{formatNumber(analysis.mistakes.length - 2, locale)}
            </p>
          ) : null}
        </div>
      ) : null}

      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="glass w-full rounded-2xl px-5 py-2.5 text-xs text-mist-400 transition hover:text-mist-100"
      >
        {open ? dict.learning.result.hideDetails : dict.learning.result.details}
      </button>

      {open ? (
        <div className="space-y-3">
          <div className="glass rounded-3xl p-5">
            <h3 className="mb-2 text-[11px] tracking-wider text-mist-500 uppercase">
              {dict.learning.result.yourAnswer}
            </h3>
            <p className="text-sm text-mist-300" lang="de" dir="ltr">
              {attempt.transcript}
            </p>
          </div>

          <div className="glass rounded-3xl p-5">
            <h3 className="mb-4 text-[11px] tracking-wider text-mist-500 uppercase">
              {dict.learning.result.categories}
            </h3>
            <div className="space-y-3">
              {CATEGORY_ORDER.map((key) => {
                const value = analysis.categories?.[key] ?? 0;
                return (
                  <div key={key}>
                    <div className="mb-1 flex items-center justify-between text-xs">
                      <span className="text-mist-400">{dict.learning.categories[key]}</span>
                      <span className="tnum text-mist-500">{formatNumber(value, locale)}</span>
                    </div>
                    <div className="h-1.5 overflow-hidden rounded-full bg-white/8">
                      <div
                        className="h-full rounded-full transition-[width] duration-700"
                        style={{ width: `${value}%`, background: scoreTone(value) }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {analysis.positive_feedback.length ? (
            <div className="glass rounded-3xl p-5">
              <h3 className="mb-3 text-[11px] tracking-wider text-mist-500 uppercase">
                {dict.learning.result.positives}
              </h3>
              <ul className="space-y-2">
                {analysis.positive_feedback.map((item, index) => (
                  <li key={index} className="flex gap-2.5 text-sm text-mist-300">
                    <span className="text-mint-400" aria-hidden>
                      ✓
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          {analysis.improvement_tips.length ? (
            <div className="glass rounded-3xl p-5">
              <h3 className="mb-3 text-[11px] tracking-wider text-mist-500 uppercase">
                {dict.learning.result.tips}
              </h3>
              <ul className="space-y-2">
                {analysis.improvement_tips.map((item, index) => (
                  <li key={index} className="flex gap-2.5 text-sm text-mist-300">
                    <span className="text-amber-400" aria-hidden>
                      →
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
