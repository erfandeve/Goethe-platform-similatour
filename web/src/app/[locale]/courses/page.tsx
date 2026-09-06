import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";

import { CourseCard } from "@/components/courses/CourseCard";
import { CourseFilters } from "@/components/courses/CourseFilters";
import { CourseToolbar } from "@/components/courses/CourseToolbar";
import { Pagination } from "@/components/courses/Pagination";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Reveal } from "@/components/ui/Reveal";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";
import type { Category, CourseCard as CourseCardType } from "@/lib/types";

interface CourseListResponse {
  results: CourseCardType[];
  meta: { page: number; page_size: number; total: number; pages: number };
  facets: {
    levels: { value: string; count: number }[];
    languages: { value: string; count: number }[];
    formats: { value: string; count: number }[];
    categories: (Category & { count: number })[];
    price_range: { min: number; max: number };
  };
}

const FILTER_KEYS = ["level", "language", "format", "category", "free", "q", "sort", "page"] as const;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const dict = await getDictionary(locale);
  return buildMetadata({
    title: `${dict.courses.title} — ${dict.courses.subtitle}`,
    description: dict.meta.description,
    path: "/courses",
    locale,
    siteName: dict.meta.siteName,
  });
}

export default async function CoursesPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const query = await searchParams;
  const dict = await getDictionary(locale);

  const search = new URLSearchParams();
  for (const key of FILTER_KEYS) {
    const value = query[key];
    if (typeof value === "string" && value) search.set(key, value);
  }
  search.set("page_size", "12");

  const data = await apiFetch<CourseListResponse>(`/courses/?${search.toString()}`, {
    locale,
    revalidate: 120,
  });

  const breadcrumbs = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: dict.nav.home, item: `${SITE_URL}/${locale}` },
      {
        "@type": "ListItem",
        position: 2,
        name: dict.courses.title,
        item: `${SITE_URL}/${locale}/courses`,
      },
    ],
  };

  return (
    <>
      <JsonLd data={breadcrumbs} />

      <div className="container-page pt-10 pb-6">
        <p className="text-xs font-semibold tracking-[0.25em] text-violet-400 uppercase">
          {dict.nav.courses}
        </p>
        <h1 className="font-display mt-3 text-4xl leading-tight font-semibold text-balance md:text-6xl">
          {dict.courses.title}
        </h1>
        <p className="text-muted mt-4 max-w-2xl text-lg">{dict.courses.subtitle}</p>
      </div>

      <div className="container-page grid gap-8 pb-24 lg:grid-cols-[18rem_1fr]">
        <Suspense fallback={<div className="glass h-96 rounded-3xl" />}>
          <CourseFilters
            facets={data.facets}
            locale={locale}
            dict={dict}
            total={data.meta.total}
          />
        </Suspense>

        <div>
          <Suspense fallback={<div className="glass mb-8 h-12 rounded-2xl" />}>
            <CourseToolbar dict={dict} locale={locale} total={data.meta.total} />
          </Suspense>

          {data.results.length ? (
            <>
              <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
                {data.results.map((course, index) => (
                  <Reveal key={course.id} delay={Math.min(index, 6) * 0.05}>
                    <CourseCard course={course} locale={locale} dict={dict} />
                  </Reveal>
                ))}
              </div>
              <Suspense fallback={null}>
                <Pagination page={data.meta.page} pages={data.meta.pages} />
              </Suspense>
            </>
          ) : (
            <Empty
              title={dict.courses.empty.title}
              body={dict.courses.empty.body}
              action={
                <ButtonLink href={`/${locale}/courses`} variant="soft">
                  {dict.courses.filters.clear}
                </ButtonLink>
              }
            />
          )}
        </div>
      </div>
    </>
  );
}
