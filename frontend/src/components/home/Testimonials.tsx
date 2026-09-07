import { Reveal } from "@/components/ui/Reveal";
import { Section, SectionHeading } from "@/components/ui/Section";
import type { Dictionary } from "@/i18n/get-dictionary";

export function Testimonials({ dict }: { dict: Dictionary }) {
  return (
    <Section>
      <SectionHeading title={dict.home.testimonials.title} align="center" />
      <div className="grid gap-5 md:grid-cols-3">
        {dict.home.testimonials.items.map((item, index) => (
          <Reveal key={item.name} delay={index * 0.08}>
            <figure className="glass flex h-full flex-col rounded-3xl p-7">
              <span className="font-display text-4xl leading-none text-violet-400/60" aria-hidden>
                &ldquo;
              </span>
              <blockquote className="mt-3 flex-1 text-sm leading-relaxed text-mist-200">
                {item.body}
              </blockquote>
              <figcaption className="mt-6 flex items-center gap-3 border-t border-white/8 pt-5">
                <span className="grid size-9 place-items-center rounded-full bg-linear-to-br from-violet-500 to-cyan-400 text-xs font-bold text-ink-950">
                  {item.name.slice(0, 1)}
                </span>
                <span>
                  <span className="block text-sm font-semibold">{item.name}</span>
                  <span className="block text-xs text-mist-500">{item.level}</span>
                </span>
              </figcaption>
            </figure>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
