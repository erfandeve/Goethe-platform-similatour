import { notFound } from "next/navigation";

import { LevelBadge } from "@/components/ui/Badge";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Progress } from "@/components/ui/Progress";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import { formatClock, formatDate, formatNumber } from "@/lib/format";
import type { Attempt, Paginated } from "@/lib/types";

export default async function MyExamsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetchAuthed<Paginated<Attempt>>("/my/attempts/", { locale });

  return (
    <div>
      <h1 className="font-display mb-8 text-2xl font-semibold">{dict.dashboard.nav.exams}</h1>

      {data.results.length ? (
        <div className="space-y-4">
          {data.results.map((attempt) => (
            <article key={attempt.id} className="glass rounded-3xl p-6">
              <div className="flex flex-wrap items-center gap-4">
                <span
                  className={`tnum font-display grid size-16 shrink-0 place-items-center rounded-2xl text-xl font-bold ${
                    attempt.status !== "finished" || attempt.max_score === 0
                      ? "bg-white/8 text-mist-400"
                      : attempt.passed
                        ? "bg-mint-400/15 text-mint-400"
                        : "bg-rose-400/15 text-rose-400"
                  }`}
                >
                  {attempt.status !== "finished"
                    ? "…"
                    : attempt.max_score === 0
                      ? "✎"
                      : formatNumber(attempt.score, locale)}
                </span>

                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    {attempt.exam ? <LevelBadge level={attempt.exam.level} /> : null}
                    <span className="text-xs text-mist-600">
                      {formatDate(attempt.started_at, locale)}
                    </span>
                  </div>
                  <h2 className="font-display mt-2 text-base font-semibold">
                    {attempt.exam?.title}
                  </h2>
                  <p className="tnum mt-1 text-xs text-mist-500">
                    {attempt.status !== "finished"
                      ? dict.dashboard.exams.inProgress
                      : attempt.max_score === 0
                        ? dict.exams.result.teacherGraded
                        : `${dict.exams.result.estimate}: ${attempt.cefr_estimate} · ${formatClock(attempt.duration_seconds)}`}
                  </p>
                </div>

                {attempt.exam ? (
                  <ButtonLink
                    href={`/${locale}/exams/${attempt.exam.slug}/attempt`}
                    variant="soft"
                    size="sm"
                  >
                    {attempt.status === "finished"
                      ? dict.exams.result.retake
                      : dict.exams.card.start}
                  </ButtonLink>
                ) : null}
              </div>

              {attempt.section_results.filter((row) => row.max_score > 0).length ? (
                <div className="mt-5 grid gap-3 border-t border-white/8 pt-5 sm:grid-cols-2">
                  {attempt.section_results
                    .filter((row) => row.max_score > 0)
                    .map((row) => {
                      const percent = Math.round((row.score / row.max_score) * 100);
                      return (
                        <div key={row.skill}>
                          <div className="mb-1.5 flex items-center justify-between text-xs">
                            <span className="text-mist-400">{dict.exams.skills[row.skill]}</span>
                            <span className="tnum text-mist-500">
                              {formatNumber(row.score, locale)}/{formatNumber(row.max_score, locale)}
                            </span>
                          </div>
                          <Progress value={percent} color={percent >= 60 ? "#34d399" : "#ff6b6b"} />
                        </div>
                      );
                    })}
                </div>
              ) : null}
            </article>
          ))}
        </div>
      ) : (
        <Empty
          title={dict.dashboard.exams.empty}
          action={<ButtonLink href={`/${locale}/exams`}>{dict.nav.exams}</ButtonLink>}
        />
      )}
    </div>
  );
}
