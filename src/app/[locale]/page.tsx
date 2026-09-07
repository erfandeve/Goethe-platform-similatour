import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { CategoryGrid } from "@/components/home/CategoryGrid";
import { CtaBanner } from "@/components/home/CtaBanner";
import { Hero } from "@/components/home/Hero";
import { Marquee } from "@/components/home/Marquee";
import { MethodSteps } from "@/components/home/MethodSteps";
import { Teachers } from "@/components/home/Teachers";
import { Testimonials } from "@/components/home/Testimonials";
import { CourseCard } from "@/components/courses/CourseCard";
import { ExamCard } from "@/components/exams/ExamCard";
import { EpisodeCard } from "@/components/podcasts/EpisodeCard";
import { PodcastCard } from "@/components/podcasts/PodcastCard";
import { ButtonLink } from "@/components/ui/Button";
import { Carousel } from "@/components/ui/Carousel";
import { Reveal } from "@/components/ui/Reveal";
import { Section, SectionHeading } from "@/components/ui/Section";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch } from "@/lib/api";
import { EMPTY_HOME, orOffline } from "@/lib/offline";
import { OfflineNotice } from "@/components/layout/OfflineNotice";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";
import type { HomePayload } from "@/lib/types";

export const revalidate = 300;

/** The phrases the home page is meant to rank for, per language. */
const HOME_KEYWORDS: Record<string, string[]> = {
  fa: [
    "سیمیلیتور زبان آلمانی",
    "لکسورا",
    "Lexora",
    "شبیه ساز آزمون گوته",
    "آزمون آنلاین زبان آلمانی",
    "آموزش زبان آلمانی",
    "دوره زبان آلمانی A1 تا C1",
    "سوالات پرتکرار B2",
    "مکالمه با هوش مصنوعی آلمانی",
    "آلمانی در محیط",
  ],
  en: [
    "German language simulator",
    "Lexora",
    "Goethe exam simulator",
    "German exam practice online",
    "learn German A1 to C1",
    "AI German speaking practice",
  ],
  de: [
    "Deutsch-Simulator",
    "Lexora",
    "Goethe-Prüfungssimulator",
    "Deutsch online üben",
    "Deutsch lernen A1 bis C1",
    "KI-Sprechtraining Deutsch",
  ],
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
    title: `${dict.meta.siteName} | ${dict.meta.tagline}`,
    absolute: true,
    description: dict.meta.description,
    path: "",
    locale,
    siteName: dict.meta.siteName,
    keywords: HOME_KEYWORDS[locale],
  });
}

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const dict = await getDictionary(locale);
  const [data, online] = await orOffline<HomePayload>(
    apiFetch<HomePayload>("/home/", { locale, revalidate: 300 }),
    EMPTY_HOME,
  );

  const organization = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    name: "Lexora",
    alternateName: ["لکسورا", dict.meta.siteName],
    url: `${SITE_URL}/${locale}`,
    description: dict.meta.description,
    sameAs: [] as string[],
    address: { "@type": "PostalAddress", addressCountry: "DE" },
    knowsLanguage: ["fa", "de", "en"],
  };

  const website = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Lexora",
    alternateName: dict.meta.siteName,
    url: `${SITE_URL}/${locale}`,
    inLanguage: locale,
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${SITE_URL}/${locale}/courses?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    },
  };

  const courseList = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    itemListElement: data.featured_courses.map((course, index) => ({
      "@type": "ListItem",
      position: index + 1,
      url: `${SITE_URL}/${locale}/courses/${course.slug}`,
      name: course.title,
    })),
  };

  return (
    <>
      {!online && <OfflineNotice locale={locale} />}
      <JsonLd data={[organization, website, courseList]} />

      <Hero locale={locale} dict={dict} stats={data.stats} />
      <Marquee />

      <CategoryGrid categories={data.categories} locale={locale} dict={dict} />

      <Section>
        <SectionHeading
          eyebrow={dict.common.featured}
          title={dict.home.featured.title}
          subtitle={dict.home.featured.subtitle}
          action={
            <ButtonLink href={`/${locale}/courses`} variant="outline">
              {dict.home.featured.cta}
            </ButtonLink>
          }
        />
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {data.featured_courses.slice(0, 6).map((course, index) => (
            <Reveal key={course.id} delay={index * 0.06}>
              <CourseCard course={course} locale={locale} dict={dict} />
            </Reveal>
          ))}
        </div>
      </Section>

      <Section id="exams">
        <SectionHeading
          eyebrow={dict.nav.exams}
          title={dict.home.exams.title}
          subtitle={dict.home.exams.subtitle}
          action={
            <ButtonLink href={`/${locale}/exams`} variant="outline">
              {dict.home.exams.cta}
            </ButtonLink>
          }
        />

        <h3 className="mb-5 flex items-center gap-3 text-sm font-semibold tracking-[0.2em] text-mist-500 uppercase">
          {dict.home.exams.simulators}
          <span className="h-px flex-1 bg-white/8" aria-hidden />
        </h3>
        <Carousel label={dict.home.exams.simulators}>
          {data.simulators.map((exam) => (
            <ExamCard key={exam.id} exam={exam} locale={locale} dict={dict} />
          ))}
        </Carousel>

        <h3 className="mt-16 mb-5 flex items-center gap-3 text-sm font-semibold tracking-[0.2em] text-mist-500 uppercase">
          {dict.home.exams.frequent}
          <span className="h-px flex-1 bg-white/8" aria-hidden />
          <span className="text-[11px] normal-case tracking-normal text-mist-600">
            {dict.home.exams.frequentNote}
          </span>
        </h3>
        <Carousel label={dict.home.exams.frequent}>
          {data.frequent_exams.map((exam) => (
            <ExamCard key={exam.id} exam={exam} locale={locale} dict={dict} />
          ))}
        </Carousel>
      </Section>

      <Section>
        <SectionHeading
          eyebrow={dict.nav.podcasts}
          title={dict.home.podcasts.title}
          subtitle={dict.home.podcasts.subtitle}
          action={
            <ButtonLink href={`/${locale}/podcasts`} variant="outline">
              {dict.home.podcasts.cta}
            </ButtonLink>
          }
        />
        <div className="grid gap-8 lg:grid-cols-[1.6fr_1fr]">
          <div className="grid gap-5 sm:grid-cols-2">
            {data.podcasts.map((podcast, index) => (
              <Reveal key={podcast.id} delay={index * 0.06}>
                <PodcastCard podcast={podcast} locale={locale} dict={dict} />
              </Reveal>
            ))}
          </div>
          <div>
            <h3 className="mb-4 text-sm font-semibold tracking-[0.2em] text-mist-500 uppercase">
              {dict.home.podcasts.latest}
            </h3>
            <div className="space-y-3">
              {data.latest_episodes.slice(0, 6).map((episode, index) => (
                <Reveal key={episode.id} delay={index * 0.05}>
                  <EpisodeCard episode={episode} locale={locale} dict={dict} />
                </Reveal>
              ))}
            </div>
          </div>
        </div>
      </Section>

      <MethodSteps dict={dict} />
      <Teachers instructors={data.instructors} locale={locale} dict={dict} />
      <Testimonials dict={dict} />
      <CtaBanner locale={locale} dict={dict} />
    </>
  );
}
