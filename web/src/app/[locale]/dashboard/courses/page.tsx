import Link from "next/link";
import { notFound } from "next/navigation";

import { LevelBadge } from "@/components/ui/Badge";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { CoverArt } from "@/components/ui/CoverArt";
import { Progress } from "@/components/ui/Progress";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import { formatDate, formatNumber } from "@/lib/format";
import type { Enrollment, Paginated } from "@/lib/types";

export default async function MyCoursesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetchAuthed<Paginated<Enrollment>>("/my/courses/", { locale });

  return (
    <div>
      <h1 className="font-display mb-8 text-2xl font-semibold">{dict.dashboard.nav.courses}</h1>

      {data.results.length ? (
        <div className="grid gap-5 md:grid-cols-2">
          {data.results.map((enrollment) => {
            const course = enrollment.course;
            if (!course) return null;
            return (
              <article key={enrollment.id} className="glass overflow-hidden rounded-3xl">
                <CoverArt
                  accent={course.accent}
                  label={course.level}
                  caption={course.category?.title ?? ""}
                  src={course.cover}
                  alt={course.title}
                  ratio="aspect-16/7"
                />
                <div className="p-5">
                  <div className="flex items-center gap-3">
                    <LevelBadge level={course.level} />
                    <span className="text-xs text-mist-600">
                      {dict.dashboard.courses.lastActivity}:{" "}
                      {formatDate(enrollment.last_activity, locale)}
                    </span>
                  </div>

                  <h2 className="font-display mt-3 text-base font-semibold">{course.title}</h2>

                  <div className="mt-4">
                    <Progress value={enrollment.progress} color={course.accent} showLabel />
                  </div>

                  <div className="mt-4 flex flex-wrap items-center gap-4 text-xs text-mist-500">
                    <span className="tnum">
                      {formatNumber(enrollment.completed_lessons, locale)} /{" "}
                      {formatNumber(course.lessons_count, locale)} {dict.courses.card.lessons}
                    </span>
                    <span className="tnum">
                      {formatNumber(enrollment.minutes_spent, locale)} {dict.common.minutes}
                    </span>
                  </div>

                  <div className="mt-5 flex flex-wrap gap-3">
                    <ButtonLink href={`/${locale}/learn/${course.slug}`} size="sm">
                      {dict.dashboard.courses.resume}
                    </ButtonLink>
                    {enrollment.certificate_url ? (
                      <Link
                        href={enrollment.certificate_url}
                        className="glass rounded-full px-4 py-2 text-xs text-mint-400"
                      >
                        {dict.dashboard.courses.certificate}
                      </Link>
                    ) : null}
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      ) : (
        <Empty
          title={dict.dashboard.overview.empty}
          action={<ButtonLink href={`/${locale}/courses`}>{dict.dashboard.courses.browse}</ButtonLink>}
        />
      )}
    </div>
  );
}
