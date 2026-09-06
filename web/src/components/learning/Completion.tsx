"use client";

import Link from "next/link";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";

export function PartComplete({
  partTitle,
  videos,
  attempts,
  average,
  accent,
  locale,
  dict,
  onNext,
}: {
  partTitle: string;
  videos: number;
  attempts: number;
  average: number;
  accent: string;
  locale: Locale;
  dict: Dictionary;
  onNext: () => void;
}) {
  return (
    <div className="glass rounded-3xl p-10 text-center">
      <span
        className="mx-auto grid size-16 place-items-center rounded-full text-2xl text-ink-950"
        style={{ background: accent }}
        aria-hidden
      >
        ✓
      </span>
      <h2 className="font-display mt-6 text-2xl font-semibold">{dict.learning.partDone.title}</h2>
      <p className="mt-2 text-sm text-mist-400" dir="ltr">
        {partTitle}
      </p>
      <p className="text-muted mt-3 text-sm">{dict.learning.partDone.body}</p>

      <dl className="mx-auto mt-8 grid max-w-md grid-cols-3 gap-4">
        {[
          [dict.learning.progress.videos, formatNumber(videos, locale)],
          [dict.learning.progress.attempts, formatNumber(attempts, locale)],
          [dict.learning.progress.average, `${formatNumber(average, locale)}%`],
        ].map(([label, value]) => (
          <div key={label} className="rounded-2xl bg-white/4 px-3 py-3">
            <dt className="text-[10px] tracking-wider text-mist-600 uppercase">{label}</dt>
            <dd className="tnum font-display mt-1 text-lg font-semibold">{value}</dd>
          </div>
        ))}
      </dl>

      <button
        type="button"
        onClick={onNext}
        className="mt-8 rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-7 py-3 text-sm font-semibold text-ink-950"
      >
        {dict.learning.partDone.next}
      </button>
    </div>
  );
}

export function CourseComplete({
  videos,
  attempts,
  average,
  estimate,
  locale,
  dict,
}: {
  videos: number;
  attempts: number;
  average: number;
  estimate: string;
  locale: Locale;
  dict: Dictionary;
}) {
  return (
    <div className="glass relative overflow-hidden rounded-3xl p-12 text-center">
      <div
        className="pointer-events-none absolute -top-32 start-1/2 size-96 -translate-x-1/2 rounded-full bg-mint-400/20 blur-3xl"
        aria-hidden
      />
      <div className="relative">
        <span className="mx-auto grid size-20 place-items-center rounded-full bg-mint-400 text-3xl text-ink-950" aria-hidden>
          ★
        </span>
        <h2 className="font-display mt-6 text-3xl font-semibold">{dict.learning.courseDone.title}</h2>
        <p className="text-muted mt-3">{dict.learning.courseDone.body}</p>

        <dl className="mx-auto mt-10 grid max-w-2xl grid-cols-2 gap-4 sm:grid-cols-4">
          {[
            [dict.learning.courseDone.totalVideos, formatNumber(videos, locale)],
            [dict.learning.courseDone.totalAttempts, formatNumber(attempts, locale)],
            [dict.learning.courseDone.average, `${formatNumber(average, locale)}%`],
            [dict.learning.courseDone.estimate, estimate || "—"],
          ].map(([label, value]) => (
            <div key={label} className="rounded-2xl bg-white/4 px-4 py-4">
              <dt className="text-[10px] tracking-wider text-mist-600 uppercase">{label}</dt>
              <dd className="tnum font-display mt-1 text-xl font-semibold">{value}</dd>
            </div>
          ))}
        </dl>

        <Link
          href={`/${locale}/dashboard/courses`}
          className="mt-10 inline-block rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-7 py-3 text-sm font-semibold text-ink-950"
        >
          {dict.learning.courseDone.backToPanel}
        </Link>
      </div>
    </div>
  );
}
