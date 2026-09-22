import { Avatar } from "@/components/ui/Avatar";
import { Reveal } from "@/components/ui/Reveal";
import { Section, SectionHeading } from "@/components/ui/Section";
import type { Locale } from "@/i18n/config";
import type { Dictionary } from "@/i18n/get-dictionary";
import { formatNumber } from "@/lib/format";
import { cn } from "@/lib/utils";

export interface TopLearner {
  rank: number;
  name: string;
  avatar: string;
  level: string;
  city: string;
  note: string;
  stats: { lessons_done: number; exams_passed: number; exam_score: number; course_progress: number };
}

const MEDAL: Record<number, { emoji: string; ring: string; glow: string; lift: string }> = {
  1: {
    emoji: "🥇",
    ring: "from-amber-200 via-amber-400 to-amber-600",
    glow: "shadow-[0_24px_80px_-30px_rgba(251,191,36,0.55)]",
    lift: "md:-translate-y-6",
  },
  2: {
    emoji: "🥈",
    ring: "from-slate-100 via-slate-300 to-slate-500",
    glow: "shadow-[0_24px_80px_-34px_rgba(203,213,225,0.4)]",
    lift: "",
  },
  3: {
    emoji: "🥉",
    ring: "from-orange-200 via-orange-400 to-orange-700",
    glow: "shadow-[0_24px_80px_-34px_rgba(251,146,60,0.45)]",
    lift: "",
  },
};

/**
 * The podium the back office picks. Renders nothing until someone is on it,
 * so an empty showcase never leaves a hole in the home page.
 */
export function TopLearners({
  learners,
  locale,
  dict,
}: {
  learners: TopLearner[];
  locale: Locale;
  dict: Dictionary;
}) {
  if (!learners.length) return null;
  const copy = dict.home.topLearners;
  const n = (value: number) => formatNumber(value, locale);

  return (
    <Section>
      <SectionHeading eyebrow={copy.eyebrow} title={copy.title} subtitle={copy.subtitle} align="center" />
      <ol className="mx-auto flex max-w-5xl flex-col gap-5 md:flex-row md:items-end md:justify-center md:pt-6">
        {learners.map((learner, index) => {
          const medal = MEDAL[learner.rank] ?? MEDAL[3];
          // On wide screens the winner stands in the middle, as on a podium.
          const order = learner.rank === 1 ? "md:order-2" : learner.rank === 2 ? "md:order-1" : "md:order-3";
          return (
            <li key={learner.rank} className={cn("md:w-1/3", order, medal.lift)}>
              <Reveal delay={index * 0.08}>
                <figure className={cn("glass relative flex flex-col items-center rounded-3xl px-6 pt-8 pb-6 text-center", medal.glow)}>
                  <span className="absolute top-4 start-4 text-2xl" aria-hidden>
                    {medal.emoji}
                  </span>
                  <span className="sr-only">
                    {copy.rank} {n(learner.rank)}
                  </span>

                  <span className={cn("rounded-full bg-linear-to-br p-[3px]", medal.ring)}>
                    <Avatar
                      src={learner.avatar}
                      name={learner.name || copy.fallbackName}
                      className="font-display size-20 border-2 border-ink-950 text-2xl"
                      fallbackClassName="bg-ink-900 font-semibold"
                    />
                  </span>

                  <figcaption className="mt-4">
                    <span className="font-display block text-lg font-semibold" dir="auto">
                      {learner.name || copy.fallbackName}
                    </span>
                    <span className="mt-1 block text-xs text-mist-500">
                      {learner.level}
                      {learner.city ? ` · ${learner.city}` : ""}
                    </span>
                  </figcaption>

                  {learner.note ? (
                    <p className="mt-4 text-sm leading-relaxed text-mist-200">{learner.note}</p>
                  ) : null}

                  <dl className="mt-5 grid w-full grid-cols-3 gap-2 border-t border-white/8 pt-4 text-center">
                    {[
                      { label: copy.lessons, value: n(learner.stats.lessons_done) },
                      { label: copy.exams, value: n(learner.stats.exams_passed) },
                      {
                        label: copy.average,
                        value: learner.stats.exam_score
                          ? `${n(learner.stats.exam_score)}${locale === "fa" ? "٪" : "%"}`
                          : "—",
                      },
                    ].map((stat) => (
                      // dt comes first in the markup; the number is shown on top.
                      <div key={stat.label} className="flex flex-col-reverse justify-end">
                        <dt className="text-[11px] text-mist-500">{stat.label}</dt>
                        <dd className="tnum font-display text-lg font-semibold">{stat.value}</dd>
                      </div>
                    ))}
                  </dl>
                </figure>
              </Reveal>
            </li>
          );
        })}
      </ol>
    </Section>
  );
}
