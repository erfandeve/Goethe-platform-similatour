import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { CoverArt } from "@/components/ui/CoverArt";
import { Section, SectionHeading } from "@/components/ui/Section";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { orOffline } from "@/lib/offline";
import { buildMetadata, JsonLd, keywordsFor, SITE_URL } from "@/lib/seo";
import type { ArticleCard } from "@/lib/types";

export const revalidate = 300;

const LIST_KEYWORDS: Record<string, string[]> = {
  fa: ["مقالات زبان آلمانی", "نحوه خواندن زبان آلمانی", "نحوه ثبت نام آزمون گوته"],
  en: ["German learning articles", "how to study German", "Goethe exam registration"],
  de: ["Artikel zum Deutschlernen", "Deutsch lernen", "Goethe-Prüfung anmelden"],
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
    title: `${dict.site.articles.title} | ${dict.meta.siteName}`,
    description: dict.site.articles.subtitle,
    path: "/articles",
    locale,
    siteName: dict.meta.siteName,
    absolute: true,
    keywords: keywordsFor(locale, LIST_KEYWORDS[locale]),
  });
}

export default async function ArticlesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);

  const [data] = await orOffline(
    apiFetch<{ results: ArticleCard[] }>("/articles/", { locale, revalidate: 300 }),
    { results: [] as ArticleCard[] },
  );

  const collection = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: dict.site.articles.title,
    description: dict.site.articles.subtitle,
    url: `${SITE_URL}/${locale}/articles`,
    inLanguage: locale,
    hasPart: data.results.map((article) => ({
      "@type": "Article",
      headline: article.title,
      url: `${SITE_URL}/${locale}/articles/${article.slug}`,
      datePublished: article.published_at,
      dateModified: article.updated_at,
    })),
  };

  return (
    <>
      <JsonLd data={collection} />
      <Section>
        <SectionHeading
          as="h1"
          eyebrow={dict.meta.siteName}
          title={dict.site.articles.title}
          subtitle={dict.site.articles.subtitle}
        />
        <p className="-mt-6 mb-12 max-w-2xl text-mist-400">{dict.site.articles.intro}</p>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {data.results.map((article) => (
            <article
              key={article.slug}
              className="group flex flex-col overflow-hidden rounded-3xl border border-white/10 bg-white/[0.02] transition hover:border-white/20"
            >
              <Link href={`/${locale}/articles/${article.slug}`} className="block">
                <CoverArt
                  src={article.cover}
                  alt={article.title}
                  accent="#8b7dff"
                  label={article.focus_keyword}
                  ratio="aspect-16/9"
                  className="transition duration-500 group-hover:scale-[1.03]"
                />
              </Link>
              <div className="flex flex-1 flex-col gap-3 p-6">
                <h2 className="font-display text-lg leading-8 font-semibold text-white">
                  <Link href={`/${locale}/articles/${article.slug}`}>{article.title}</Link>
                </h2>
                <p className="line-clamp-3 flex-1 text-sm leading-7 text-mist-400">
                  {article.excerpt}
                </p>
                <p className="text-xs text-mist-500">
                  {article.reading_minutes.toLocaleString(locale)} {dict.site.articles.readingTime}
                  {" · "}
                  {article.words.toLocaleString(locale)} {dict.site.articles.wordsLabel}
                </p>
              </div>
            </article>
          ))}
        </div>
      </Section>
    </>
  );
}
