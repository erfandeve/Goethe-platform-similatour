import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ExamCard } from "@/components/exams/ExamCard";
import { Carousel } from "@/components/ui/Carousel";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { breadcrumbs, buildMetadata, JsonLd, keywordsFor, SITE_URL } from "@/lib/seo";
import type { ExamCard as ExamCardType } from "@/lib/types";

// Short window so a cover or price edited in the back office shows up quickly.
export const revalidate = 30;

interface ExamListResponse {
  results: ExamCardType[];
  grouped: { simulator: ExamCardType[]; frequent: ExamCardType[] };
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const dict = await getDictionary(locale);
  return buildMetadata({
    title: dict.exams.title,
    description: dict.exams.subtitle,
    path: "/exams",
    locale,
    siteName: dict.meta.siteName,
    keywords: keywordsFor(locale, [
      locale === "fa" ? "سیمیلیتور زبان آلمانی" : "German exam simulator",
      locale === "fa" ? "شبیه ساز آزمون گوته" : "Goethe exam simulator",
      locale === "fa" ? "آزمون آنلاین زبان آلمانی" : "German exam practice online",
      "A1 A2 B1 B2 C1",
      "Goethe Prüfung",
    ]),
  });
}

export default async function ExamsPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetch<ExamListResponse>("/exams/?page_size=40", {
    locale,
    revalidate: 30,
  });

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: dict.exams.title,
    itemListElement: data.results.map((exam, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: exam.title,
      url: `${SITE_URL}/${locale}/exams/${exam.slug}`,
    })),
  };

  return (
    <>
      <JsonLd data={jsonLd} />

      <div className="container-page pt-10 pb-4">
        <p className="text-xs font-semibold tracking-[0.25em] text-violet-400 uppercase">
          {dict.nav.exams}
        </p>
        <h1 className="font-display mt-3 text-4xl leading-tight font-semibold text-balance md:text-6xl">
          {dict.exams.title}
        </h1>
        <p className="text-muted mt-4 max-w-2xl text-lg">{dict.exams.subtitle}</p>
      </div>

      <section className="container-page py-12">
        <header className="mb-8">
          <h2 className="font-display text-2xl font-semibold">{dict.exams.simulators.title}</h2>
          <p className="text-muted mt-2 text-sm">{dict.exams.simulators.body}</p>
        </header>
        <Carousel label={dict.exams.simulators.title}>
          {data.grouped.simulator.map((exam) => (
            <ExamCard key={exam.id} exam={exam} locale={locale} dict={dict} />
          ))}
        </Carousel>
      </section>

      <section className="container-page pb-24">
        <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="font-display text-2xl font-semibold">{dict.exams.frequent.title}</h2>
            <p className="text-muted mt-2 text-sm">{dict.exams.frequent.body}</p>
          </div>
          <span className="rounded-full bg-amber-400/12 px-3 py-1.5 text-xs font-semibold text-amber-400">
            B2 · C1
          </span>
        </header>
        <Carousel label={dict.exams.frequent.title}>
          {data.grouped.frequent.map((exam) => (
            <ExamCard key={exam.id} exam={exam} locale={locale} dict={dict} />
          ))}
        </Carousel>
      </section>
    </>
  );
}
