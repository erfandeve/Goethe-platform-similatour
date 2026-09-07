import Link from "next/link";

import { Badge, LevelBadge } from "@/components/ui/Badge";
import { CoverArt } from "@/components/ui/CoverArt";
import { Spotlight } from "@/components/ui/Spotlight";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { compact, discountPercent, formatDuration, formatPrice } from "@/lib/format";
import type { CourseCard as CourseCardType } from "@/lib/types";
import { cn } from "@/lib/utils";

export function CourseCard({
  course,
  locale,
  dict,
  className,
}: {
  course: CourseCardType;
  locale: Locale;
  dict: Dictionary;
  className?: string;
}) {
  const off = discountPercent(course.price, course.discount_price);

  return (
    <Spotlight accent={course.accent} className={cn("h-full", className)}>
      <Link
        href={`/${locale}/courses/${course.slug}`}
        className="glass group relative flex h-full flex-col overflow-hidden rounded-3xl transition-all duration-500 hover:-translate-y-1.5 hover:border-white/20"
      >
        <div className="relative">
          <CoverArt
            accent={course.accent}
            label={course.level}
            caption={course.category?.title ?? ""}
            src={course.cover}
            alt={course.title}
          />
          <div className="absolute start-4 top-4 flex gap-2">
            {course.is_bestseller ? (
              <Badge color="#f59e0b">{dict.common.bestseller}</Badge>
            ) : null}
            {off > 0 ? (
              <Badge color="#ff6b6b" className="tnum">
                {off}% {dict.common.off}
              </Badge>
            ) : null}
          </div>
        </div>

        <div className="relative flex flex-1 flex-col p-5">
          <div className="mb-3 flex items-center gap-2">
            <LevelBadge level={course.level} />
            <span className="text-[11px] tracking-wide text-mist-500 uppercase">
              {dict.courses.formats[course.format]}
            </span>
          </div>

          <h3 className="font-display text-lg leading-snug font-semibold text-balance transition-colors group-hover:text-violet-400">
            {course.title}
          </h3>
          <p className="text-muted mt-2 line-clamp-2 text-sm">{course.subtitle}</p>

          <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-mist-500">
            <span className="tnum">
              {course.lessons_count} {dict.courses.card.lessons}
            </span>
            <span className="tnum">
              {formatDuration(course.duration_minutes, locale, {
                h: dict.common.hours,
                min: dict.common.minutes,
              })}
            </span>
            <span className="tnum">
              {compact(course.students_count, locale)} {dict.courses.card.students}
            </span>
          </div>

          <div className="mt-5 flex items-end justify-between gap-3 border-t border-white/8 pt-4">
            <div className="flex items-center gap-2">
              <span className="text-amber-400" aria-hidden>
                ★
              </span>
              <span className="tnum text-sm font-semibold">{course.rating.toFixed(1)}</span>
              <span className="tnum text-xs text-mist-600">({course.reviews_count})</span>
            </div>
            <div className="text-end">
              {course.discount_price ? (
                <span className="tnum block text-xs text-mist-600 line-through">
                  {formatPrice(course.price, locale, dict.common.free)}
                </span>
              ) : null}
              <span className="tnum font-display text-base font-semibold text-mist-50">
                {formatPrice(course.effective_price, locale, dict.common.free)}
              </span>
            </div>
          </div>
        </div>
      </Link>
    </Spotlight>
  );
}
