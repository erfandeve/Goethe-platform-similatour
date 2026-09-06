import { Reveal } from "@/components/ui/Reveal";
import { Section, SectionHeading } from "@/components/ui/Section";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { compact } from "@/lib/format";
import type { Instructor } from "@/lib/types";

export function Teachers({
  instructors,
  locale,
  dict,
}: {
  instructors: Instructor[];
  locale: Locale;
  dict: Dictionary;
}) {
  if (!instructors.length) return null;

  return (
    <Section>
      <SectionHeading
        eyebrow={dict.nav.instructors}
        title={dict.home.teachers.title}
        subtitle={dict.home.teachers.subtitle}
      />
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {instructors.map((instructor, index) => (
          <Reveal key={instructor.id} delay={index * 0.07}>
            <article className="glass group h-full rounded-3xl p-6 text-center transition-all duration-500 hover:-translate-y-1 hover:border-white/20">
              <span className="font-display mx-auto grid size-20 place-items-center rounded-full bg-linear-to-br from-violet-500/25 to-cyan-400/25 text-2xl font-semibold ring-1 ring-white/12">
                {instructor.name
                  .split(" ")
                  .map((part) => part[0])
                  .slice(0, 2)
                  .join("")}
              </span>
              <h3 className="font-display mt-5 text-base font-semibold">{instructor.name}</h3>
              <p className="text-muted mt-1.5 text-xs leading-relaxed">{instructor.headline}</p>
              <div className="mt-4 flex items-center justify-center gap-4 border-t border-white/8 pt-4 text-xs text-mist-500">
                <span className="tnum flex items-center gap-1">
                  <span className="text-amber-400" aria-hidden>
                    ★
                  </span>
                  {instructor.rating.toFixed(1)}
                </span>
                <span className="tnum">
                  {compact(instructor.students, locale)} {dict.common.students}
                </span>
              </div>
            </article>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
