"use client";

import Link from "next/link";
import { useEffect } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatClock, formatNumber } from "@/lib/format";

import type { ResultPayload } from "./GoetheRunner";

const MODULE_NAMES: Record<string, string> = {
  lesen: "Lesen",
  hoeren: "Hören",
  schreiben: "Schreiben",
};

export function GoetheResult({
  result,
  slug,
  locale,
  dict,
  brand,
}: {
  result: ResultPayload;
  slug: string;
  locale: Locale;
  dict: Dictionary;
  brand: string;
}) {
  useEffect(() => {
    document.body.dataset.mode = "exam";
    return () => {
      delete document.body.dataset.mode;
    };
  }, []);

  const graded = result.review.filter((row) => row.is_correct !== null);
  const written = result.review.filter((row) => row.type === "writing");
  // A writing module carries no auto-scored points: it goes to a teacher.
  const pendingReview = result.max_score === 0;

  return (
    <div
      dir="ltr"
      className="exam-root fixed inset-0 flex flex-col"
      style={{ background: "var(--exam-page)" }}
    >
      <header
        className="flex h-16 shrink-0 items-center justify-between px-6 text-white"
        style={{ background: "var(--exam-bar)" }}
      >
        <span className="flex items-center gap-3">
          <span
            className="grid size-9 place-items-center rounded-full border-2 text-[13px] font-bold"
            style={{ borderColor: "var(--exam-green)", color: "var(--exam-green)" }}
            aria-hidden
          >
            G
          </span>
          <span className="text-xs font-semibold tracking-wide">{brand.toUpperCase()}</span>
        </span>
        <span className="text-sm" dir="ltr">
          {MODULE_NAMES[result.module] ?? result.module} — Ergebnis
        </span>
      </header>

      <div className="exam-scroll flex-1 p-6">
        <div className="mx-auto max-w-4xl">
          <div className="mb-6 bg-white p-8 text-center" style={{ border: "1px solid var(--exam-line)" }}>
            <p className="text-xs tracking-[0.2em] uppercase" dir="auto" style={{ color: "var(--exam-muted)" }}>
              {dict.exams.result.title}
            </p>

            {pendingReview ? (
              <div className="mt-8">
                <span
                  className="mx-auto grid size-20 place-items-center rounded-full text-3xl text-white"
                  style={{ background: "var(--exam-green)" }}
                  aria-hidden
                >
                  ✓
                </span>
                <p className="mt-6 text-lg font-bold">{dict.exams.result.teacherGraded}</p>
                <p className="mt-2 text-sm" style={{ color: "var(--exam-muted)" }}>
                  {dict.dashboard.messages.sent}
                </p>
              </div>
            ) : (
              <>
            <div className="mx-auto mt-6 grid size-40 place-items-center">
              <svg viewBox="0 0 120 120" className="absolute size-40 -rotate-90" aria-hidden>
                <circle cx="60" cy="60" r="52" fill="none" stroke="#e2e2de" strokeWidth="9" />
                <circle
                  cx="60"
                  cy="60"
                  r="52"
                  fill="none"
                  stroke={result.passed ? "var(--exam-green)" : "#d9534f"}
                  strokeWidth="9"
                  strokeLinecap="round"
                  strokeDasharray={`${(result.score / 100) * 327} 327`}
                />
              </svg>
              <span className="relative text-center">
                <span className="tnum block text-4xl font-bold">
                  {formatNumber(result.score, locale)}%
                </span>
                <span className="tnum block text-xs" style={{ color: "var(--exam-muted)" }}>
                  {formatNumber(result.raw_score, locale)} / {formatNumber(result.max_score, locale)}
                </span>
              </span>
            </div>

            <p
              dir="auto"
              className="mt-5 text-lg font-bold"
              style={{ color: result.passed ? "var(--exam-green-dark)" : "#c9302c" }}
            >
              {result.passed ? dict.exams.result.passed : dict.exams.result.failed}
            </p>
            </>
            )}

            <div
              dir="auto"
              className={pendingReview ? "hidden" : "mt-6 flex flex-wrap justify-center gap-8 text-sm"}
            >
              <span>
                <span className="block text-xs" style={{ color: "var(--exam-muted)" }}>
                  {dict.exams.result.estimate}
                </span>
                <b className="tnum">{result.cefr_estimate}</b>
              </span>
              <span>
                <span className="block text-xs" style={{ color: "var(--exam-muted)" }}>
                  {dict.exams.card.questions}
                </span>
                <b className="tnum">
                  {formatNumber(result.correct_count, locale)} / {formatNumber(graded.length, locale)}
                </b>
              </span>
              <span>
                <span className="block text-xs" style={{ color: "var(--exam-muted)" }}>
                  {dict.exams.runner.timeLeft}
                </span>
                <b className="tnum">{formatClock(result.duration_seconds)}</b>
              </span>
            </div>
          </div>

          {graded.length ? (
            <section className="mb-6 bg-white p-6" style={{ border: "1px solid var(--exam-line)" }}>
              <h2 className="mb-4 text-sm font-bold">{dict.exams.result.review}</h2>
              <ul>
                {graded.map((row) => (
                  <li
                    key={row.key}
                    className="flex items-start gap-3 border-b py-3 last:border-0"
                    style={{ borderColor: "var(--exam-line)" }}
                  >
                    <span
                      className="tnum mt-0.5 grid size-6 shrink-0 place-items-center text-xs font-bold text-white"
                      style={{ background: row.is_correct ? "var(--exam-green)" : "#d9534f" }}
                    >
                      {row.number}
                    </span>
                    <span className="min-w-0 flex-1" dir="ltr">
                      <span className="exam-body block">{row.prompt}</span>
                      <span className="mt-1 block text-xs" style={{ color: "var(--exam-muted)" }}>
                        {dict.exams.result.correct}: <b>{row.answer_label}</b>
                        {!row.is_correct ? (
                          <>
                            {" · "}
                            {dict.exams.result.wrong}: {row.given_label || "—"}
                          </>
                        ) : null}
                      </span>
                      {row.explanation ? (
                        <span className="mt-1 block text-xs" style={{ color: "var(--exam-muted)" }}>
                          {row.explanation}
                        </span>
                      ) : null}
                    </span>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}

          {written.length ? (
            <section className="mb-6 bg-white p-6" style={{ border: "1px solid var(--exam-line)" }}>
              <h2 className="mb-2 text-sm font-bold">{dict.exams.result.teacherGraded}</h2>
              {written.map((row) => (
                <article key={row.key} className="mt-4">
                  <p className="text-xs font-semibold" dir="ltr">
                    {row.prompt}
                  </p>
                  <p
                    className="exam-body mt-2 border p-4 whitespace-pre-wrap"
                    style={{ borderColor: "var(--exam-line)" }}
                    dir="ltr"
                    lang="de"
                  >
                    {row.given_text || "—"}
                  </p>
                </article>
              ))}
            </section>
          ) : null}

          <div className="flex flex-wrap justify-center gap-3 pb-10">
            <Link
              href={`/${locale}/exams/${slug}`}
              className="px-6 py-3 text-sm font-semibold text-white"
              style={{ background: "var(--exam-green)" }}
            >
              {dict.exams.result.backToExams}
            </Link>
            <Link
              href={`/${locale}/dashboard/exams`}
              className="border px-6 py-3 text-sm font-semibold"
              style={{ borderColor: "var(--exam-line)" }}
            >
              {dict.dashboard.nav.exams}
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
