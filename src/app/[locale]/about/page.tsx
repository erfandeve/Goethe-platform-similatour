import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ButtonLink } from "@/components/ui/Button";
import { Section, SectionHeading } from "@/components/ui/Section";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, locales } from "@/i18n/config";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";

export const revalidate = 3600;

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

const KEYWORDS: Record<string, string[]> = {
  fa: [
    "لکسورا",
    "Lexora",
    "درباره ما",
    "سیمیلیتور زبان آلمانی",
    "آموزش زبان آلمانی",
    "آکادمی زبان آلمانی",
  ],
  en: ["Lexora", "about Lexora", "German language simulator", "German academy", "Goethe exam prep"],
  de: ["Lexora", "über Lexora", "Deutsch-Simulator", "Deutsch-Akademie", "Goethe-Prüfung"],
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const dict = await getDictionary(locale);
  return buildMetadata({
    title: `${dict.site.about.title} | ${dict.meta.tagline}`,
    description: dict.site.about.intro,
    path: "/about",
    locale,
    siteName: dict.meta.siteName,
    absolute: true,
    keywords: KEYWORDS[locale],
  });
}

export default async function AboutPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const t = dict.site.about;

  const schema = [
    {
      "@context": "https://schema.org",
      "@type": "AboutPage",
      name: t.title,
      description: t.intro,
      url: `${SITE_URL}/${locale}/about`,
      inLanguage: locale,
      mainEntity: {
        "@type": "EducationalOrganization",
        name: "Lexora",
        alternateName: "لکسورا",
        url: `${SITE_URL}/${locale}`,
        description: dict.meta.description,
        address: { "@type": "PostalAddress", addressCountry: "DE" },
      },
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: dict.nav.home, item: `${SITE_URL}/${locale}` },
        { "@type": "ListItem", position: 2, name: t.title, item: `${SITE_URL}/${locale}/about` },
      ],
    },
  ];

  return (
    <>
      <JsonLd data={schema} />

      <Section className="pb-10">
        <SectionHeading as="h1" eyebrow="Lexora" title={t.title} subtitle={t.subtitle} />
        <p className="-mt-6 max-w-3xl text-lg leading-9 text-mist-300">{t.intro}</p>
      </Section>

      <Section className="py-10">
        <div className="grid gap-10 md:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-white/[0.02] p-8">
            <h2 className="font-display mb-4 text-2xl font-bold text-white">{t.missionTitle}</h2>
            <p className="leading-9 text-mist-300">{t.mission}</p>
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/[0.02] p-8">
            <h2 className="font-display mb-4 text-2xl font-bold text-white">{t.storyTitle}</h2>
            <p className="leading-9 text-mist-300">{t.story}</p>
          </div>
        </div>
      </Section>

      <Section className="py-10">
        <h2 className="font-display mb-8 text-2xl font-bold text-white md:text-3xl">
          {t.valuesTitle}
        </h2>
        <div className="grid gap-5 sm:grid-cols-2">
          {t.values.map((value) => (
            <div
              key={value.title}
              className="rounded-2xl border border-white/10 bg-white/[0.02] p-6"
            >
              <h3 className="font-display mb-2 text-lg font-semibold text-white">{value.title}</h3>
              <p className="text-[15px] leading-8 text-mist-400">{value.body}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section className="pt-10">
        <div className="flex flex-col items-start gap-6 rounded-3xl border border-violet-400/25 bg-linear-to-br from-violet-500/10 to-cyan-400/[0.06] p-10 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="font-display text-2xl font-bold text-white">{t.ctaTitle}</h2>
            <p className="mt-2 text-mist-300">{t.ctaBody}</p>
          </div>
          <ButtonLink href={`/${locale}/exams`}>{t.ctaButton}</ButtonLink>
        </div>
      </Section>
    </>
  );
}
