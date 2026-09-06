import { ButtonLink } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";
import { SceneMount } from "@/components/three/SceneMount";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { compact } from "@/lib/format";
import type { HomePayload } from "@/lib/types";

export function Hero({
  locale,
  dict,
  stats,
}: {
  locale: Locale;
  dict: Dictionary;
  stats: HomePayload["stats"];
}) {
  const numbers = [
    { value: compact(stats.students, locale), label: dict.hero.stats.students },
    { value: compact(stats.courses, locale), label: dict.hero.stats.courses },
    { value: compact(stats.exams, locale), label: dict.hero.stats.exams },
    { value: compact(stats.episodes, locale), label: dict.hero.stats.episodes },
  ];

  return (
    <section className="relative overflow-hidden">
      <div className="container-page relative grid min-h-[86vh] items-center gap-12 py-16 lg:grid-cols-[1.05fr_0.95fr]">
        <div className="relative z-10">
          <Reveal>
            <span className="glass inline-flex items-center gap-2 rounded-full px-4 py-2 text-xs font-medium tracking-wide text-mist-200">
              <span className="size-1.5 animate-pulse rounded-full bg-mint-400" aria-hidden />
              {dict.hero.eyebrow}
            </span>
          </Reveal>

          <Reveal delay={0.08}>
            <h1 className="font-display mt-7 text-5xl leading-[1.05] font-semibold text-balance sm:text-6xl lg:text-7xl">
              {dict.hero.titleTop}
              <span className="text-gradient block">{dict.hero.titleAccent}</span>
            </h1>
          </Reveal>

          <Reveal delay={0.16}>
            <p className="text-muted mt-7 max-w-xl text-lg leading-relaxed">{dict.hero.subtitle}</p>
          </Reveal>

          <Reveal delay={0.24}>
            <div className="mt-9 flex flex-wrap gap-3">
              <ButtonLink href={`/${locale}/courses`} size="lg">
                {dict.hero.primary}
              </ButtonLink>
              <ButtonLink href={`/${locale}/exams/simulator-a1`} size="lg" variant="soft">
                {dict.hero.secondary}
              </ButtonLink>
            </div>
          </Reveal>

          <Reveal delay={0.32}>
            <dl className="mt-14 grid max-w-xl grid-cols-2 gap-x-10 gap-y-7 sm:grid-cols-4">
              {numbers.map((item) => (
                <div key={item.label} className="min-w-0">
                  <dt className="tnum font-display text-2xl font-semibold text-mist-50">
                    {item.value}
                  </dt>
                  <dd className="mt-1 text-[10px] leading-tight tracking-wide text-balance text-mist-500 uppercase">
                    {item.label}
                  </dd>
                </div>
              ))}
            </dl>
          </Reveal>
        </div>

        <div className="relative h-[26rem] w-full lg:h-[38rem]">
          <SceneMount className="absolute inset-0" />
          {/* Floating CEFR chips orbiting the 3D core */}
          <div className="pointer-events-none absolute inset-0 hidden lg:block">
            {[
              { label: "A1", top: "12%", start: "8%", delay: "0s" },
              { label: "B2", top: "68%", start: "4%", delay: "1.2s" },
              { label: "C1", top: "22%", start: "78%", delay: "0.6s" },
              { label: "ß", top: "78%", start: "72%", delay: "1.8s" },
            ].map((chip) => (
              <span
                key={chip.label}
                className="glass animate-float tnum absolute rounded-2xl px-3.5 py-2 text-sm font-semibold"
                style={{ top: chip.top, insetInlineStart: chip.start, animationDelay: chip.delay }}
              >
                {chip.label}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-32 bg-linear-to-t from-ink-950 to-transparent" />
    </section>
  );
}
