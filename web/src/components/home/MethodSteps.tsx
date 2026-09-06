import { Reveal } from "@/components/ui/Reveal";
import { Section, SectionHeading } from "@/components/ui/Section";
import type { Dictionary } from "@/i18n/get-dictionary";

export function MethodSteps({ dict }: { dict: Dictionary }) {
  return (
    <Section>
      <SectionHeading
        eyebrow="Method"
        title={dict.home.method.title}
        subtitle={dict.home.method.subtitle}
        align="center"
      />

      <ol className="relative grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {/* Connecting hairline behind the steps on wide screens */}
        <span
          className="pointer-events-none absolute inset-x-0 top-11 hidden h-px bg-linear-to-r from-transparent via-white/12 to-transparent lg:block"
          aria-hidden
        />
        {dict.home.method.steps.map((step, index) => (
          <Reveal key={step.title} delay={index * 0.08}>
            <li className="glass relative h-full rounded-3xl p-7">
              <span className="font-display tnum grid size-11 place-items-center rounded-2xl bg-linear-to-br from-violet-500 to-cyan-400 text-base font-bold text-ink-950">
                {index + 1}
              </span>
              <h3 className="font-display mt-5 text-lg font-semibold">{step.title}</h3>
              <p className="text-muted mt-2 text-sm leading-relaxed">{step.body}</p>
            </li>
          </Reveal>
        ))}
      </ol>
    </Section>
  );
}
