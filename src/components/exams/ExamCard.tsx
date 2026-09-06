import Link from "next/link";

import { Badge, LevelBadge } from "@/components/ui/Badge";
import { CoverArt } from "@/components/ui/CoverArt";
import { Spotlight } from "@/components/ui/Spotlight";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { compact, formatNumber, formatPrice } from "@/lib/format";
import type { ExamCard as ExamCardType } from "@/lib/types";
import { alpha } from "@/lib/utils";

/**
 * A product-shaped card: the cover carries the image, everything a buyer needs
 * to compare sits underneath in a fixed order so a row of cards lines up.
 */
export function ExamCard({
  exam,
  locale,
  dict,
}: {
  exam: ExamCardType;
  locale: Locale;
  dict: Dictionary;
}) {
  return (
    <Spotlight accent={exam.accent} className="h-full">
      <Link
        href={`/${locale}/exams/${exam.slug}`}
        className="glass group relative flex h-full flex-col overflow-hidden rounded-3xl transition-all duration-500 hover:-translate-y-1.5 hover:border-white/20"
      >
        <div className="relative">
          <CoverArt
            accent={exam.accent}
            label={exam.level}
            caption={exam.exam_board}
            src={exam.cover}
            alt={exam.title}
            ratio="aspect-16/10"
          />

          <div className="absolute start-4 top-4 flex flex-wrap gap-2">
            {exam.kind === "frequent" ? (
              <Badge color="#f59e0b">{dict.home.exams.frequent}</Badge>
            ) : null}
            {exam.is_free ? <Badge color="#34d399">{dict.exams.card.free}</Badge> : null}
          </div>
        </div>

        <div className="flex flex-1 flex-col p-5">
          <div className="mb-3 flex items-center gap-2">
            <LevelBadge level={exam.level} />
            <span className="text-[11px] tracking-wide text-mist-500 uppercase">
              {exam.kind === "frequent" ? dict.exams.frequent.title : dict.exams.simulators.title}
            </span>
          </div>

          <h3 className="font-display text-lg leading-snug font-semibold text-balance transition-colors group-hover:text-violet-400">
            {exam.title}
          </h3>
          <p className="text-muted mt-2 line-clamp-2 text-sm">{exam.subtitle}</p>

          <div className="mt-4 flex flex-wrap gap-1.5">
            {exam.skills.slice(0, 4).map((skill, index) => (
              <span
                key={`${skill}-${index}`}
                className="rounded-lg px-2 py-1 text-[11px] font-medium"
                style={{ color: exam.accent, background: alpha(exam.accent, 0.1) }}
              >
                {dict.exams.skills[skill]}
              </span>
            ))}
          </div>

          <dl className="mt-5 grid grid-cols-3 gap-2 border-t border-white/8 pt-4 text-center">
            {[
              [dict.exams.card.questions, formatNumber(exam.questions_count, locale)],
              [dict.exams.card.minutes, formatNumber(exam.duration_minutes, locale)],
              [dict.exams.card.attempts, compact(exam.attempts_count, locale)],
            ].map(([label, value]) => (
              <div key={label}>
                <dt className="text-[10px] tracking-wider text-mist-600 uppercase">{label}</dt>
                <dd className="tnum font-display mt-0.5 text-base font-semibold">{value}</dd>
              </div>
            ))}
          </dl>

          <div className="mt-auto flex items-center justify-between gap-3 border-t border-white/8 pt-4">
            <span className="tnum font-display font-semibold">
              {formatPrice(exam.effective_price, locale, dict.exams.card.free)}
            </span>
            <span
              className="inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-xs font-semibold transition-transform group-hover:translate-x-0.5"
              style={{ background: alpha(exam.accent, 0.15), color: exam.accent }}
            >
              {exam.is_free ? dict.exams.card.start : dict.exams.card.buy}
              <span aria-hidden className="flip-x">
                →
              </span>
            </span>
          </div>
        </div>
      </Link>
    </Spotlight>
  );
}
