import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { ArticleBody } from "@/components/articles/ArticleBody";
import { CoverArt } from "@/components/ui/CoverArt";
import { Section } from "@/components/ui/Section";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { alternates, JsonLd, SITE_URL } from "@/lib/seo";
import type { ArticleDetail } from "@/lib/types";

export const revalidate = 300;

async function loadArticle(slug: string, locale: string) {
  try {
    return await apiFetch<ArticleDetail>(`/articles/${slug}/`, {
      locale: locale as never,
      revalidate: 300,
    });
  } catch {
    return null;
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}): Promise<Metadata> {
  const { locale, slug } = await params;
  if (!isLocale(locale)) return {};
  const article = await loadArticle(slug, locale);
  if (!article) return {};

  const path = `/articles/${slug}`;
  const url = `${SITE_URL}/${locale}${path}`;

  return {
    title: { absolute: article.meta_title },
    description: article.meta_description,
    keywords: article.keywords,
    alternates: alternates(path, locale),
    robots: { index: true, follow: true, "max-image-preview": "large" },
    openGraph: {
      type: "article",
      title: article.title,
      description: article.meta_description,
      url,
      siteName: "Lexora",
      publishedTime: article.published_at ?? undefined,
      modifiedTime: article.updated_at ?? undefined,
      images: [{ url: `${SITE_URL}/og-default.png`, width: 1200, height: 630, alt: article.title }],
    },
    twitter: {
      card: "summary_large_image",
      title: article.title,
      description: article.meta_description,
      images: [`${SITE_URL}/og-default.png`],
    },
  };
}

export default async function ArticlePage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();

  const [dict, article] = await Promise.all([getDictionary(locale), loadArticle(slug, locale)]);
  if (!article) notFound();

  const toc = article.body.filter((block) => block.type === "h2");
  const url = `${SITE_URL}/${locale}/articles/${article.slug}`;

  const schema = [
    {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: article.title,
      description: article.meta_description,
      inLanguage: locale,
      datePublished: article.published_at,
      dateModified: article.updated_at,
      wordCount: article.words,
      keywords: article.keywords.join(", "),
      mainEntityOfPage: { "@type": "WebPage", "@id": url },
      image: [`${SITE_URL}/og-default.png`],
      author: { "@type": "Organization", name: "Lexora", url: `${SITE_URL}/${locale}` },
      publisher: {
        "@type": "Organization",
        name: "Lexora",
        url: `${SITE_URL}/${locale}`,
        logo: { "@type": "ImageObject", url: `${SITE_URL}/og-default.png` },
      },
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: dict.nav.home, item: `${SITE_URL}/${locale}` },
        {
          "@type": "ListItem",
          position: 2,
          name: dict.site.articles.title,
          item: `${SITE_URL}/${locale}/articles`,
        },
        { "@type": "ListItem", position: 3, name: article.title, item: url },
      ],
    },
    ...(article.faq.length
      ? [
          {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            mainEntity: article.faq.map((item) => ({
              "@type": "Question",
              name: item.q,
              acceptedAnswer: { "@type": "Answer", text: item.a },
            })),
          },
        ]
      : []),
  ];

  return (
    <>
      <JsonLd data={schema} />

      <article>
        <Section className="pb-10">
          <nav aria-label="breadcrumb" className="mb-8 text-sm text-mist-500">
            <ol className="flex flex-wrap items-center gap-2">
              <li>
                <Link href={`/${locale}`} className="hover:text-white">
                  {dict.nav.home}
                </Link>
              </li>
              <li aria-hidden>/</li>
              <li>
                <Link href={`/${locale}/articles`} className="hover:text-white">
                  {dict.site.articles.title}
                </Link>
              </li>
            </ol>
          </nav>

          <header className="max-w-3xl">
            <h1 className="font-display text-3xl leading-[1.35] font-bold text-white md:text-[2.6rem]">
              {article.title}
            </h1>
            <p className="mt-6 text-lg leading-9 text-mist-300">{article.excerpt}</p>
            <p className="mt-6 flex flex-wrap gap-x-4 gap-y-2 text-xs text-mist-500">
              {article.updated_at && (
                <span>
                  {dict.site.articles.updated}: {article.updated_at.slice(0, 10)}
                </span>
              )}
              <span>
                {article.reading_minutes.toLocaleString(locale)} {dict.site.articles.readingTime}
              </span>
              <span>
                {article.words.toLocaleString(locale)} {dict.site.articles.wordsLabel}
              </span>
            </p>
          </header>

          <div className="mt-10 overflow-hidden rounded-3xl border border-white/10">
            <CoverArt
              src={article.cover}
              alt={article.title}
              accent="#8b7dff"
              label={article.focus_keyword}
              ratio="aspect-21/9"
            />
          </div>
        </Section>

        <Section className="pt-0 pb-20">
          <div className="grid gap-12 lg:grid-cols-[minmax(0,1fr)_280px]">
            {/* min-w-0: a grid item defaults to min-content width, so without it
                the widest table stretches the column past the viewport. */}
            <div className="min-w-0 max-w-3xl">
              <ArticleBody body={article.body} locale={locale} />

              {article.faq.length > 0 && (
                <section className="mt-16">
                  <h2 className="font-display mb-6 text-2xl font-bold text-white">
                    {dict.site.articles.faqTitle}
                  </h2>
                  <div className="flex flex-col gap-3">
                    {article.faq.map((item) => (
                      <details
                        key={item.q}
                        className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-4"
                      >
                        <summary className="cursor-pointer list-none font-semibold text-white marker:content-none">
                          {item.q}
                        </summary>
                        <p className="mt-3 text-[16px] leading-8 text-mist-300">{item.a}</p>
                      </details>
                    ))}
                  </div>
                </section>
              )}

              {article.related.length > 0 && (
                <section className="mt-16">
                  <h2 className="font-display mb-6 text-2xl font-bold text-white">
                    {dict.site.articles.related}
                  </h2>
                  <div className="grid gap-4 sm:grid-cols-2">
                    {article.related.map((item) => (
                      <Link
                        key={item.slug}
                        href={`/${locale}/articles/${item.slug}`}
                        className="rounded-2xl border border-white/10 bg-white/[0.02] p-5 transition hover:border-white/25"
                      >
                        <p className="font-display leading-8 font-semibold text-white">
                          {item.title}
                        </p>
                        <p className="mt-2 line-clamp-2 text-sm leading-7 text-mist-400">
                          {item.excerpt}
                        </p>
                      </Link>
                    ))}
                  </div>
                </section>
              )}
            </div>

            <aside className="hidden lg:block">
              <nav
                aria-label={dict.site.articles.toc}
                className="sticky top-28 rounded-2xl border border-white/10 bg-white/[0.02] p-5"
              >
                <p className="font-display mb-4 text-sm font-semibold text-white">
                  {dict.site.articles.toc}
                </p>
                <ol className="flex flex-col gap-2.5">
                  {toc.map((heading) =>
                    heading.type === "h2" ? (
                      <li key={heading.id}>
                        <a
                          href={`#${heading.id}`}
                          className="text-sm leading-6 text-mist-400 transition hover:text-white"
                        >
                          {heading.text}
                        </a>
                      </li>
                    ) : null,
                  )}
                </ol>
              </nav>
            </aside>
          </div>
        </Section>
      </article>
    </>
  );
}
