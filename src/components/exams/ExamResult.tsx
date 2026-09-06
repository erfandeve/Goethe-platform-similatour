"use client";

import { ButtonLink } from "@/components/ui/Button";
import { Progress } from "@/components/ui/Progress";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatClock, formatNumber } from "@/lib/format";
import type { Attempt } from "@/lib/types";
import { cn, levelColor } from "@/lib/utils";

export function ExamResult({
  attempt,
  locale,
  dict,
  slug,
}: {
  attempt: Attempt;
  locale: Locale;
  dict: Dictionary;
  slug?: string;
}) {
  const examSlug = slug ?? attempt.exam?.slug ?? "";
  const passed = attempt.passed;
  const tone = passed ? "#34d399" : "#ff6b6b";

  return (
    <div className="container-page pb-24">
      <div className="glass relative overflow-hidden rounded-[2rem] p-8 text-center md:p-14">
        <div
          className="pointer-events-none absolute -top-40 start-1/2 size-[32rem] -translate-x-1/2 rounded-full opacity-25 blur-3xl"
          style={{ background: tone }}
          aria-hidden
        />

        <div className="relative">
          <p className="text-xs font-semibold tracking-[0.25em] text-mist-500 uppercase">
            {dict.exams.result.title}
          </p>

          {/* Score dial */}
          <div className="mx-auto mt-8 grid size-44 place-items-center">
            <svg viewBox="0 0 120 120" className="absolute size-44 -rotate-90" aria-hidden>
              <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="8" />
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke={tone}
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={`${(attempt.score / 100) * 327} 327`}
              />
            </svg>
            <span className="relative text-center">
              <span className="tnum font-display block text-5xl font-semibold">
                {formatNumber(attempt.score, locale)}
                <span className="text-2xl">%</span>
              </span>
              <span className="mt-1 block text-[11px] tracking-wider text-mist-500 uppercase">
                {dict.exams.result.score}
              </span>
            </span>
          </div>

          <p
            className="font-display mt-6 text-2xl font-semibold"
            style={{ color: tone }}
          >
            {passed ? dict.exams.result.passed : dict.exams.result.failed}
          </p>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <span className="glass rounded-2xl px-5 py-3">
              <span className="block text-[10px] tracking-wider text-mist-600 uppercase">
                {dict.exams.result.estimate}
              </span>
              <span
                className="tnum font-display mt-1 block text-xl font-semibold"
                style={{ color: levelColor(attempt.cefr_estimate) }}
              >
                {attempt.cefr_estimate}
              </span>
            </span>
            <span className="glass rounded-2xl px-5 py-3">
              <span className="block text-[10px] tracking-wider text-mist-600 uppercase">
                {dict.exams.card.questions}
              </span>
              <span className="tnum font-display mt-1 block text-xl font-semibold">
                {formatNumber(attempt.correct_count, locale)}
              </span>
            </span>
            <span className="glass rounded-2xl px-5 py-3">
              <span className="block text-[10px] tracking-wider text-mist-600 uppercase">
                {dict.exams.runner.timeLeft}
              </span>
              <span className="tnum font-display mt-1 block text-xl font-semibold">
                {formatClock(attempt.duration_seconds)}
              </span>
            </span>
          </div>
        </div>
      </div>

      {attempt.section_results.length ? (
        <section className="mt-10">
          <h2 className="font-display mb-5 text-xl font-semibold">{dict.exams.result.bySkill}</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {attempt.section_results
              .filter((row) => row.max_score > 0)
              .map((row) => {
                const percent = Math.round((row.score / row.max_score) * 100);
                return (
                  <div key={row.skill} className="glass rounded-2xl p-5">
                    <div className="mb-3 flex items-center justify-between">
                      <span className="text-sm font-semibold">{dict.exams.skills[row.skill]}</span>
                      <span className="tnum text-sm text-mist-400">
                        {formatNumber(row.score, locale)} / {formatNumber(row.max_score, locale)}
                      </span>
                    </div>
                    <Progress value={percent} color={percent >= 60 ? "#34d399" : "#ff6b6b"} showLabel />
                  </div>
                );
              })}
          </div>
        </section>
      ) : null}

      {attempt.review?.length ? (
        <section className="mt-12">
          <h2 className="font-display mb-5 text-xl font-semibold">{dict.exams.result.review}</h2>
          <ol className="space-y-3">
            {attempt.review.map((row, index) => {
              const graded = row.is_correct !== null;
              return (
                <li key={row.key} className="glass rounded-2xl p-5">
                  <header className="flex items-start gap-3">
                    <span
                      className={cn(
                        "tnum grid size-7 shrink-0 place-items-center rounded-lg text-xs font-bold",
                        !graded
                          ? "bg-amber-400/15 text-amber-400"
                          : row.is_correct
                            ? "bg-mint-400/15 text-mint-400"
                            : "bg-rose-400/15 text-rose-400",
                      )}
                    >
                      {index + 1}
                    </span>
                    <p className="flex-1 text-sm font-medium text-mist-100">{row.prompt}</p>
                    <span className="text-[10px] tracking-wider text-mist-600 uppercase">
                      {dict.exams.skills[row.skill]}
                    </span>
                  </header>

                  {!graded ? (
                    <p className="mt-3 ps-10 text-xs text-amber-400">
                      {dict.exams.result.teacherGraded}
                    </p>
                  ) : (
                    <div className="mt-3 space-y-1.5 ps-10 text-xs">
                      <p className="text-mint-400">
                        {dict.exams.result.correct}: {row.options[row.correct_index]}
                      </p>
                      {!row.is_correct ? (
                        <p className="text-rose-400">
                          {dict.exams.result.wrong}:{" "}
                          {typeof row.given === "number" && row.options[row.given]
                            ? row.options[row.given]
                            : "—"}
                        </p>
                      ) : null}
                      {row.explanation ? (
                        <p className="text-mist-400">
                          {dict.exams.result.explanation}: {row.explanation}
                        </p>
                      ) : null}
                    </div>
                  )}
                </li>
              );
            })}
          </ol>
        </section>
      ) : null}

      <div className="mt-12 flex flex-wrap justify-center gap-3">
        {examSlug ? (
          <ButtonLink href={`/${locale}/exams/${examSlug}/attempt`} variant="soft">
            {dict.exams.result.retake}
          </ButtonLink>
        ) : null}
        <ButtonLink href={`/${locale}/dashboard/exams`}>{dict.dashboard.nav.exams}</ButtonLink>
        <ButtonLink href={`/${locale}/exams`} variant="outline">
          {dict.exams.result.backToExams}
        </ButtonLink>
      </div>
    </div>
  );
}
