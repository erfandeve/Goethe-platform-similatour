import Link from "next/link";
import { notFound } from "next/navigation";

import { StatCard } from "@/components/dashboard/StatCard";
import { LevelBadge } from "@/components/ui/Badge";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Progress } from "@/components/ui/Progress";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import { compact, formatDate, formatNumber, formatPrice } from "@/lib/format";
import type { Attempt, Enrollment, User } from "@/lib/types";

interface DashboardPayload {
  user: User;
  stats: {
    courses: number;
    completed_courses: number;
    exams_taken: number;
    average_score: number;
    minutes_spent: number;
    streak_days: number;
    wallet_balance: number;
  };
  enrollments: Enrollment[];
  attempts: Attempt[];
  unread_notifications: number;
  unread_messages: number;
}

export default async function DashboardPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetchAuthed<DashboardPayload>("/auth/dashboard/", { locale });

  return (
    <div className="space-y-10">
      <header className="glass relative overflow-hidden rounded-3xl p-7 md:p-9">
        <div
          className="pointer-events-none absolute -top-24 end-0 size-72 rounded-full bg-violet-500/25 blur-3xl"
          aria-hidden
        />
        <div className="relative flex flex-wrap items-center gap-6">
          <span className="font-display grid size-16 place-items-center rounded-2xl bg-linear-to-br from-violet-500 to-cyan-400 text-2xl font-bold text-ink-950">
            {data.user.full_name.slice(0, 1).toUpperCase()}
          </span>
          <div className="min-w-0 flex-1">
            <h1 className="font-display text-2xl font-semibold">{data.user.full_name}</h1>
            <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-mist-400">
              <span className="flex items-center gap-1.5">
                {dict.dashboard.stats.level} <LevelBadge level={data.user.current_level} />
              </span>
              <span className="flex items-center gap-1.5">
                {dict.dashboard.stats.target} <LevelBadge level={data.user.target_level} />
              </span>
              <span dir="ltr">{data.user.email}</span>
            </div>
          </div>
          <div className="w-full max-w-56">
            <p className="mb-2 text-[11px] tracking-wider text-mist-600 uppercase">
              {dict.dashboard.overview.profileCompletion}
            </p>
            <Progress value={data.user.profile_completion} showLabel />
            {data.user.profile_completion < 100 ? (
              <Link
                href={`/${locale}/dashboard/profile`}
                className="mt-2 inline-block text-xs text-violet-400 underline-offset-4 hover:underline"
              >
                {dict.dashboard.overview.completeProfile}
              </Link>
            ) : null}
          </div>
        </div>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label={dict.dashboard.stats.courses}
          value={formatNumber(data.stats.courses, locale)}
          hint={`${formatNumber(data.stats.completed_courses, locale)} ${dict.dashboard.stats.completed}`}
        />
        <StatCard
          label={dict.dashboard.stats.exams}
          value={formatNumber(data.stats.exams_taken, locale)}
          hint={`${dict.dashboard.stats.average}: ${formatNumber(data.stats.average_score, locale)}%`}
          accent="#22d3ee"
        />
        <StatCard
          label={dict.dashboard.stats.minutes}
          value={compact(data.stats.minutes_spent, locale)}
          hint={`${formatNumber(data.stats.streak_days, locale)} ${dict.dashboard.stats.streak}`}
          accent="#f59e0b"
        />
        <StatCard
          label={dict.dashboard.stats.balance}
          value={formatPrice(data.stats.wallet_balance, locale, dict.common.free)}
          accent="#34d399"
        />
      </section>

      <section>
        <div className="mb-5 flex items-center justify-between">
          <h2 className="font-display text-xl font-semibold">{dict.dashboard.overview.continue}</h2>
          <Link
            href={`/${locale}/dashboard/courses`}
            className="text-xs text-violet-400 underline-offset-4 hover:underline"
          >
            {dict.common.viewAll}
          </Link>
        </div>

        {data.enrollments.length ? (
          <div className="grid gap-4 md:grid-cols-2">
            {data.enrollments.slice(0, 4).map((enrollment) => (
              <article key={enrollment.id} className="glass rounded-2xl p-5">
                <div className="flex items-center gap-3">
                  {enrollment.course ? <LevelBadge level={enrollment.course.level} /> : null}
                  <span className="text-xs text-mist-600">
                    {formatDate(enrollment.last_activity, locale)}
                  </span>
                </div>
                <h3 className="mt-3 line-clamp-1 text-sm font-semibold">
                  {enrollment.course?.title}
                </h3>
                <div className="mt-4">
                  <Progress
                    value={enrollment.progress}
                    color={enrollment.course?.accent}
                    showLabel
                  />
                </div>
                {enrollment.course ? (
                  <Link
                    href={`/${locale}/learn/${enrollment.course.slug}`}
                    className="mt-4 inline-block text-xs text-violet-400 underline-offset-4 hover:underline"
                  >
                    {dict.dashboard.courses.resume} →
                  </Link>
                ) : null}
              </article>
            ))}
          </div>
        ) : (
          <Empty
            title={dict.dashboard.overview.empty}
            action={
              <ButtonLink href={`/${locale}/courses`}>{dict.dashboard.courses.browse}</ButtonLink>
            }
          />
        )}
      </section>

      <section>
        <div className="mb-5 flex items-center justify-between">
          <h2 className="font-display text-xl font-semibold">
            {dict.dashboard.overview.recentExams}
          </h2>
          <Link
            href={`/${locale}/dashboard/exams`}
            className="text-xs text-violet-400 underline-offset-4 hover:underline"
          >
            {dict.common.viewAll}
          </Link>
        </div>

        {data.attempts.length ? (
          <div className="space-y-3">
            {data.attempts.slice(0, 4).map((attempt) => (
              <Link
                key={attempt.id}
                href={`/${locale}/dashboard/exams`}
                className="glass flex items-center gap-4 rounded-2xl p-4 transition hover:border-white/20"
              >
                <span
                  className={`tnum grid size-12 shrink-0 place-items-center rounded-xl text-sm font-bold ${
                    attempt.passed
                      ? "bg-mint-400/15 text-mint-400"
                      : "bg-rose-400/15 text-rose-400"
                  }`}
                >
                  {formatNumber(attempt.score, locale)}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold">{attempt.exam?.title}</p>
                  <p className="text-xs text-mist-500">{formatDate(attempt.started_at, locale)}</p>
                </div>
                <span className="text-xs text-mist-400">{attempt.cefr_estimate}</span>
              </Link>
            ))}
          </div>
        ) : (
          <Empty
            title={dict.dashboard.exams.empty}
            action={<ButtonLink href={`/${locale}/exams`}>{dict.nav.exams}</ButtonLink>}
          />
        )}
      </section>
    </div>
  );
}
