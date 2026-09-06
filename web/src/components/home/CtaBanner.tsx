import { ButtonLink } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";
import { Section } from "@/components/ui/Section";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";

export function CtaBanner({ locale, dict }: { locale: Locale; dict: Dictionary }) {
  return (
    <Section>
      <Reveal>
        <div className="glass relative overflow-hidden rounded-[2.5rem] px-8 py-16 text-center md:px-16 md:py-24">
          <div
            className="pointer-events-none absolute -top-32 start-1/2 size-[36rem] -translate-x-1/2 rounded-full bg-violet-500/25 blur-3xl"
            aria-hidden
          />
          <div className="relative mx-auto max-w-2xl">
            <h2 className="font-display text-3xl leading-tight font-semibold text-balance md:text-5xl">
              {dict.home.cta.title}
            </h2>
            <p className="text-muted mt-5 text-base md:text-lg">{dict.home.cta.body}</p>
            <div className="mt-9 flex flex-wrap justify-center gap-3">
              <ButtonLink href={`/${locale}/register`} size="lg">
                {dict.home.cta.primary}
              </ButtonLink>
              <ButtonLink href={`/${locale}/courses`} size="lg" variant="outline">
                {dict.home.cta.secondary}
              </ButtonLink>
            </div>
          </div>
        </div>
      </Reveal>
    </Section>
  );
}
