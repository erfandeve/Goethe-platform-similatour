import Link from "next/link";

import { Reveal } from "@/components/ui/Reveal";
import { Section, SectionHeading } from "@/components/ui/Section";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import type { Category } from "@/lib/types";
import { alpha } from "@/lib/utils";

const ICONS: Record<string, string> = {
  layers: "M12 3 2 8l10 5 10-5-10-5Zm0 9L2 17l10 5 10-5-10-5Z",
  target: "M12 3a9 9 0 1 0 9 9M12 7a5 5 0 1 0 5 5M12 12h9",
  chat: "M4 5h16v11H9l-5 4V5Z",
  book: "M4 4h9a3 3 0 0 1 3 3v13a3 3 0 0 0-3-3H4V4Zm16 0h-1a3 3 0 0 0-3 3v13a3 3 0 0 1 3-3h1V4Z",
  briefcase: "M3 8h18v12H3V8Zm6 0V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2",
  heart: "M12 20s-7-4.5-7-9a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 4.5-7 9-7 9Z",
};

export function CategoryGrid({
  categories,
  locale,
  dict,
}: {
  categories: Category[];
  locale: Locale;
  dict: Dictionary;
}) {
  return (
    <Section>
      <SectionHeading
        eyebrow={dict.nav.courses}
        title={dict.home.categories.title}
        subtitle={dict.home.categories.subtitle}
      />
      <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-3">
        {categories.map((category, index) => (
          <Reveal key={category.id} delay={index * 0.05}>
            <Link
              href={`/${locale}/courses?category=${category.slug}`}
              className="glass group flex h-full flex-col items-start gap-3 rounded-2xl p-4 transition-all duration-500 hover:-translate-y-1 hover:border-white/20 sm:flex-row sm:gap-4 sm:rounded-3xl sm:p-6"
            >
              <span
                className="grid size-10 shrink-0 place-items-center rounded-xl transition-transform duration-500 group-hover:scale-110 sm:size-12 sm:rounded-2xl"
                style={{ background: alpha(category.color, 0.14), color: category.color }}
                aria-hidden
              >
                <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="1.7">
                  <path d={ICONS[category.icon] ?? ICONS.layers} strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </span>
              <span className="min-w-0">
                <span className="font-display block text-sm leading-6 font-semibold sm:text-base">{category.title}</span>
                <span className="tnum mt-1 block text-xs text-mist-500">
                  {category.count ?? 0} {dict.courses.filters.results}
                </span>
              </span>
              <span
                className="flip-x ms-auto hidden text-mist-600 transition-transform group-hover:translate-x-1 sm:inline"
                aria-hidden
              >
                →
              </span>
            </Link>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
