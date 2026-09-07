import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { AddToCartButton } from "@/components/courses/AddToCartButton";
import { CourseCard } from "@/components/courses/CourseCard";
import { Curriculum } from "@/components/courses/Curriculum";
import { LevelBadge } from "@/components/ui/Badge";
import { ButtonLink } from "@/components/ui/Button";
import { CoverArt } from "@/components/ui/CoverArt";
import { Reveal } from "@/components/ui/Reveal";
import { Section, SectionHeading } from "@/components/ui/Section";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, type Locale } from "@/i18n/config";
import { apiFetch, getAccessToken } from "@/lib/api";
import {
  compact,
  discountPercent,
  formatDate,
  formatDuration,
  formatNumber,
  formatPrice,
} from "@/lib/format";
import { breadcrumbs, buildMetadata, JsonLd, keywordsFor, SITE_URL } from "@/lib/seo";
import type { CourseDetail } from "@/lib/types";

export const revalidate = 300;

async function loadCourse(slug: string, locale: Locale, token: string | null = null) {
  try {
    // Signed in, the answer includes `is_enrolled`, so it must not be cached
    // across visitors — otherwise an owner is shown "add to cart" for a course
    // they already bought.
    return await apiFetch<CourseDetail>(`/courses/${slug}/`, {
      locale,
      token,
      revalidate: token ? 0 : 300,
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
  const [dict, course] = await Promise.all([getDictionary(locale), loadCourse(slug, locale)]);
  if (!course) return {};

  return buildMetadata({
    title: course.title,
    description: course.subtitle || course.description.slice(0, 155),
    path: `/courses/${slug}`,
    locale,
    siteName: dict.meta.siteName,
    type: "article",
    image: course.cover,
    keywords: keywordsFor(locale, [
      course.title,
      ...course.tags,
      `${dict.common.level} ${course.level}`,
      "Deutschkurs",
    ]),
  });
}

export default async function CourseDetailPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const token = await getAccessToken();
  const course = await loadCourse(slug, locale, token);
  if (!course) notFound();

  const off = discountPercent(course.price, course.discount_price);
  const totalLessons = course.curriculum.reduce((sum, section) => sum + section.lessons.length, 0);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Course",
    name: course.title,
    description: course.description,
    url: `${SITE_URL}/${locale}/courses/${course.slug}`,
    inLanguage: course.language,
    educationalLevel: course.level,
    provider: {
      "@type": "EducationalOrganization",
      name: dict.meta.siteName,
      url: `${SITE_URL}/${locale}`,
    },
    ...(course.reviews_count
      ? {
          aggregateRating: {
            "@type": "AggregateRating",
            ratingValue: course.rating,
            reviewCount: course.reviews_count,
          },
        }
      : {}),
    offers: {
      "@type": "Offer",
      price: course.effective_price,
      priceCurrency: "IRR",
      availability: "https://schema.org/InStock",
      url: `${SITE_URL}/${locale}/courses/${course.slug}`,
    },
    hasCourseInstance: {
      "@type": "CourseInstance",
      courseMode: course.format === "live" ? "Onsite" : "Online",
      courseWorkload: `PT${Math.round(course.duration_minutes / 60)}H`,
    },
  };

  const facts = [
    { label: dict.courses.detail.sections, value: formatNumber(course.curriculum.length, locale) },
    { label: dict.courses.card.lessons, value: formatNumber(totalLessons, locale) },
    {
      label: dict.courses.detail.totalLength,
      value: formatDuration(course.duration_minutes, locale, {
        h: dict.common.hours,
        min: dict.common.minutes,
      }),
    },
    { label: dict.courses.card.students, value: compact(course.students_count, locale) },
  ];

  return (
    <>
      <JsonLd
        data={[
          jsonLd,
          breadcrumbs(locale, [
            { name: dict.nav.home, path: "" },
            { name: dict.nav.courses, path: "/courses" },
            { name: course.title, path: `/courses/${course.slug}` },
          ]),
        ]}
      />

      <div className="relative overflow-hidden">
        <div
          className="pointer-events-none absolute -top-40 start-1/4 size-[40rem] rounded-full opacity-25 blur-3xl"
          style={{ background: course.accent }}
          aria-hidden
        />
        <div className="container-page relative grid gap-10 py-12 lg:grid-cols-[1.5fr_1fr]">
          <div>
            <nav className="mb-6 flex items-center gap-2 text-xs text-mist-500">
              <Link href={`/${locale}`} className="hover:text-mist-200">
                {dict.nav.home}
              </Link>
              <span aria-hidden>/</span>
              <Link href={`/${locale}/courses`} className="hover:text-mist-200">
                {dict.nav.courses}
              </Link>
              {course.category ? (
                <>
                  <span aria-hidden>/</span>
                  <Link
                    href={`/${locale}/courses?category=${course.category.slug}`}
                    className="hover:text-mist-200"
                  >
                    {course.category.title}
                  </Link>
                </>
              ) : null}
            </nav>

            <div className="flex flex-wrap items-center gap-3">
              <LevelBadge level={course.level} />
              <span className="text-xs tracking-wide text-mist-500 uppercase">
                {dict.courses.formats[course.format]}
              </span>
              {course.is_bestseller ? (
                <span className="rounded-full bg-amber-400/12 px-2.5 py-1 text-[11px] font-semibold text-amber-400 uppercase">
                  {dict.common.bestseller}
                </span>
              ) : null}
            </div>

            <h1 className="font-display mt-5 text-4xl leading-tight font-semibold text-balance md:text-6xl">
              {course.title}
            </h1>
            <p className="text-muted mt-5 max-w-2xl text-lg">{course.subtitle}</p>

            <div className="mt-7 flex flex-wrap items-center gap-6 text-sm">
              <span className="flex items-center gap-2">
                <span className="text-amber-400" aria-hidden>
                  ★
                </span>
                <span className="tnum font-semibold">{course.rating.toFixed(1)}</span>
                <span className="tnum text-mist-500">({course.reviews_count})</span>
              </span>
              {course.instructor ? (
                <span className="flex items-center gap-2 text-mist-300">
                  <span className="grid size-7 place-items-center rounded-full bg-white/8 text-[11px] font-bold">
                    {course.instructor.name.slice(0, 1)}
                  </span>
                  {course.instructor.name}
                </span>
              ) : null}
              {course.starts_at ? (
                <span className="text-mist-500">
                  {dict.courses.detail.startsAt}: {formatDate(course.starts_at, locale)}
                </span>
              ) : null}
            </div>

            <dl className="mt-10 grid max-w-xl grid-cols-2 gap-5 sm:grid-cols-4">
              {facts.map((fact) => (
                <div key={fact.label} className="glass rounded-2xl px-4 py-3">
                  <dt className="text-[10px] tracking-wider text-mist-600 uppercase">
                    {fact.label}
                  </dt>
                  <dd className="tnum font-display mt-1 text-lg font-semibold">{fact.value}</dd>
                </div>
              ))}
            </dl>
          </div>

          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div className="glass overflow-hidden rounded-3xl">
              <CoverArt
                accent={course.accent}
                label={course.level}
                caption={course.category?.title ?? ""}
                src={course.cover}
                alt={course.title}
                ratio="aspect-16/9"
              />
              <div className="p-6">
                <div className="flex flex-wrap items-end gap-3">
                  <span className="tnum font-display text-3xl font-semibold">
                    {formatPrice(course.effective_price, locale, dict.common.free)}
                  </span>
                  {off > 0 ? (
                    <>
                      <span className="tnum text-sm text-mist-600 line-through">
                        {formatPrice(course.price, locale, dict.common.free)}
                      </span>
                      <span className="tnum rounded-lg bg-rose-400/15 px-2 py-1 text-xs font-semibold text-rose-400">
                        {off}% {dict.common.off}
                      </span>
                    </>
                  ) : null}
                </div>

                <div className="mt-6">
                  {course.is_enrolled ? (
                    <ButtonLink
                      href={`/${locale}/learn/${course.slug}`}
                      size="lg"
                      className="w-full"
                    >
                      {dict.learning.actions.resume}
                    </ButtonLink>
                  ) : (
                    <AddToCartButton
                      slug={course.slug}
                      itemType="course"
                      locale={locale}
                      dict={dict}
                      isFree={course.effective_price === 0}
                      isOwned={false}
                    />
                  )}
                </div>

                <ul className="mt-6 space-y-2.5 border-t border-white/8 pt-5 text-sm text-mist-300">
                  {[
                    `${formatNumber(totalLessons, locale)} ${dict.courses.card.lessons}`,
                    formatDuration(course.duration_minutes, locale, {
                      h: dict.common.hours,
                      min: dict.common.minutes,
                    }),
                    dict.courses.formats[course.format],
                  ].map((item) => (
                    <li key={item} className="flex items-center gap-2.5">
                      <span className="text-mint-400" aria-hidden>
                        ✓
                      </span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </aside>
        </div>
      </div>

      <div className="container-page grid gap-12 pb-20 lg:grid-cols-[1.5fr_1fr]">
        <div className="space-y-14">
          <section>
            <h2 className="font-display mb-5 text-2xl font-semibold">
              {dict.courses.detail.outcomes}
            </h2>
            <ul className="grid gap-3 sm:grid-cols-2">
              {course.outcomes.map((outcome) => (
                <li key={outcome} className="glass flex items-start gap-3 rounded-2xl px-4 py-3.5">
                  <span className="mt-0.5 text-mint-400" aria-hidden>
                    ✓
                  </span>
                  <span className="text-sm text-mist-200">{outcome}</span>
                </li>
              ))}
            </ul>
          </section>

          <section>
            <h2 className="font-display mb-5 text-2xl font-semibold">
              {dict.courses.detail.overview}
            </h2>
            <p className="text-muted leading-relaxed whitespace-pre-line">{course.description}</p>
          </section>

          <section>
            <h2 className="font-display mb-5 text-2xl font-semibold">
              {dict.courses.detail.curriculum}
            </h2>
            <Curriculum sections={course.curriculum} locale={locale} dict={dict} />
          </section>

          {course.reviews.length ? (
            <section>
              <h2 className="font-display mb-5 text-2xl font-semibold">
                {dict.courses.detail.reviews}
              </h2>
              <div className="space-y-3">
                {course.reviews.map((review) => (
                  <article key={review.id} className="glass rounded-2xl p-5">
                    <header className="flex items-center gap-3">
                      <span className="grid size-9 place-items-center rounded-full bg-linear-to-br from-violet-500 to-cyan-400 text-xs font-bold text-ink-950">
                        {review.author_name.slice(0, 1)}
                      </span>
                      <span>
                        <span className="block text-sm font-semibold">{review.author_name}</span>
                        <span className="tnum block text-xs text-amber-400">
                          {"★".repeat(review.rating)}
                        </span>
                      </span>
                      <span className="ms-auto text-xs text-mist-600">
                        {formatDate(review.created_at, locale)}
                      </span>
                    </header>
                    <p className="mt-3 text-sm leading-relaxed text-mist-200">{review.body}</p>
                  </article>
                ))}
              </div>
            </section>
          ) : null}
        </div>

        <aside className="space-y-8">
          {course.instructor ? (
            <section className="glass rounded-3xl p-6">
              <h2 className="mb-4 text-xs font-semibold tracking-[0.2em] text-mist-500 uppercase">
                {dict.courses.detail.instructor}
              </h2>
              <div className="flex items-center gap-4">
                <span className="font-display grid size-14 place-items-center rounded-2xl bg-linear-to-br from-violet-500/25 to-cyan-400/25 text-lg font-semibold ring-1 ring-white/12">
                  {course.instructor.name.slice(0, 1)}
                </span>
                <div>
                  <p className="font-display font-semibold">{course.instructor.name}</p>
                  <p className="text-xs text-mist-500">{course.instructor.headline}</p>
                </div>
              </div>
              {course.instructor.bio ? (
                <p className="text-muted mt-4 text-sm leading-relaxed">{course.instructor.bio}</p>
              ) : null}
            </section>
          ) : null}

          <section className="glass rounded-3xl p-6">
            <h2 className="mb-4 text-xs font-semibold tracking-[0.2em] text-mist-500 uppercase">
              {dict.courses.detail.requirements}
            </h2>
            <ul className="space-y-2.5">
              {course.requirements.map((item) => (
                <li key={item} className="flex items-start gap-2.5 text-sm text-mist-300">
                  <span className="mt-1 size-1.5 shrink-0 rounded-full bg-violet-400" aria-hidden />
                  {item}
                </li>
              ))}
            </ul>
          </section>
        </aside>
      </div>

      {course.related.length ? (
        <Section>
          <SectionHeading title={dict.courses.detail.related} />
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {course.related.map((item, index) => (
              <Reveal key={item.id} delay={index * 0.06}>
                <CourseCard course={item} locale={locale} dict={dict} />
              </Reveal>
            ))}
          </div>
        </Section>
      ) : null}
    </>
  );
}
