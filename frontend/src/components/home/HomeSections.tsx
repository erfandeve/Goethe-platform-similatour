import Link from "next/link";

import { CoverArt } from "@/components/ui/CoverArt";
import { Reveal } from "@/components/ui/Reveal";
import { Section } from "@/components/ui/Section";
import type { Locale } from "@/i18n/config";
import type { HomeSection } from "@/lib/types";
import { cn } from "@/lib/utils";

function Prose({ paragraphs }: { paragraphs: string[] }) {
  return (
    <div className="flex flex-col gap-5">
      {paragraphs.map((text, index) => (
        <p key={index} className="text-[17px] leading-9 text-mist-300">
          {text}
        </p>
      ))}
    </div>
  );
}

function Cta({ section, locale }: { section: HomeSection; locale: Locale }) {
  if (!section.cta_label || !section.cta_href) return null;
  return (
    <Link
      href={`/${locale}${section.cta_href}`}
      className="mt-8 inline-flex w-fit items-center gap-2 rounded-full bg-white px-6 py-3 text-sm font-semibold text-ink-950 transition hover:bg-white/90"
    >
      {section.cta_label}
    </Link>
  );
}

function Heading({ section, as: Tag = "h2" }: { section: HomeSection; as?: "h2" | "h3" }) {
  return (
    <>
      {section.eyebrow && (
        <p className="mb-3 text-xs font-semibold tracking-[0.25em] text-violet-400 uppercase">
          {section.eyebrow}
        </p>
      )}
      <Tag className="font-display text-3xl leading-tight font-semibold text-balance text-white md:text-4xl">
        {section.title}
      </Tag>
      {section.subtitle && <p className="text-muted mt-4 text-lg">{section.subtitle}</p>}
    </>
  );
}

/** One editable block from the back office, laid out by its `kind`. */
function Block({ section, locale }: { section: HomeSection; locale: Locale }) {
  switch (section.kind) {
    case "text_image":
      return (
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div className={cn(section.image_side === "start" && "lg:order-2")}>
            <Heading section={section} />
            <div className="mt-6">
              <Prose paragraphs={section.paragraphs} />
            </div>
            <Cta section={section} locale={locale} />
          </div>
          <div
            className={cn(
              "overflow-hidden rounded-3xl border border-white/10",
              section.image_side === "start" && "lg:order-1",
            )}
          >
            <CoverArt
              src={section.image}
              alt={section.image_alt}
              accent={section.accent}
              label={section.eyebrow || section.title}
              ratio="aspect-4/3"
            />
          </div>
        </div>
      );

    case "features":
      return (
        <>
          <div className="max-w-2xl">
            <Heading section={section} />
          </div>
          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {section.items.map((entry) => (
              <div
                key={entry.title}
                className="rounded-2xl border border-white/10 bg-white/[0.02] p-6"
              >
                <h3 className="font-display mb-3 leading-7 font-semibold text-white">
                  {entry.title}
                </h3>
                <p className="text-sm leading-7 text-mist-400">{entry.body}</p>
              </div>
            ))}
          </div>
        </>
      );

    case "stats":
      return (
        <>
          <div className="max-w-2xl">
            <Heading section={section} />
          </div>
          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {section.items.map((entry) => (
              <div key={entry.body} className="rounded-2xl border border-white/10 p-6">
                <p className="font-display text-3xl font-bold text-white">{entry.title}</p>
                <p className="mt-2 text-sm text-mist-400">{entry.body}</p>
              </div>
            ))}
          </div>
        </>
      );

    case "faq":
      return (
        <>
          <div className="max-w-2xl">
            <Heading section={section} />
          </div>
          <div className="mt-10 flex max-w-3xl flex-col gap-3">
            {section.items.map((entry) => (
              <details
                key={entry.title}
                className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-4"
              >
                <summary className="cursor-pointer list-none font-semibold text-white marker:content-none">
                  {entry.title}
                </summary>
                <p className="mt-3 leading-8 text-mist-300">{entry.body}</p>
              </details>
            ))}
          </div>
        </>
      );

    case "cta":
      return (
        <div className="flex flex-col items-start gap-6 rounded-3xl border border-violet-400/25 bg-linear-to-br from-violet-500/10 to-cyan-400/[0.06] p-10 md:flex-row md:items-center md:justify-between">
          <div className="max-w-2xl">
            <Heading section={section} />
            <div className="mt-4">
              <Prose paragraphs={section.paragraphs} />
            </div>
          </div>
          <Cta section={section} locale={locale} />
        </div>
      );

    case "rich_text":
    default:
      return (
        <div className="max-w-3xl">
          <Heading section={section} />
          <div className="mt-6">
            <Prose paragraphs={section.paragraphs} />
          </div>
          {section.items.length > 0 && (
            <ul className="mt-6 flex flex-col gap-3">
              {section.items.map((entry) => (
                <li key={entry.title} className="flex gap-3 text-[17px] leading-8 text-mist-300">
                  <span aria-hidden className="mt-3 size-1.5 shrink-0 rounded-full bg-violet-400" />
                  <span>
                    <strong className="font-semibold text-white">{entry.title}</strong>
                    {entry.body ? ` — ${entry.body}` : ""}
                  </span>
                </li>
              ))}
            </ul>
          )}
          <Cta section={section} locale={locale} />
        </div>
      );
  }
}

/** One editable section, ready to drop between two catalogue blocks. */
export function HomeSectionBlock({
  section,
  locale,
}: {
  section: HomeSection;
  locale: Locale;
}) {
  return (
    <Section id={section.key}>
      <Reveal>
        <Block section={section} locale={locale} />
      </Reveal>
    </Section>
  );
}

export function HomeSections({
  sections,
  locale,
}: {
  sections: HomeSection[];
  locale: Locale;
}) {
  return (
    <>
      {sections.map((section) => (
        <HomeSectionBlock key={section.key} section={section} locale={locale} />
      ))}
    </>
  );
}
