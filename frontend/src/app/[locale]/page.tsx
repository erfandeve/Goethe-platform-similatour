import type { Metadata } from "next";
import type { ReactNode } from "react";
import { notFound } from "next/navigation";

import { CategoryGrid } from "@/components/home/CategoryGrid";
import { CtaBanner } from "@/components/home/CtaBanner";
import { Hero } from "@/components/home/Hero";
import { HomeSectionBlock } from "@/components/home/HomeSections";
import { Marquee } from "@/components/home/Marquee";
import { MethodSteps } from "@/components/home/MethodSteps";
import { Testimonials } from "@/components/home/Testimonials";
import { TopLearners, type TopLearner } from "@/components/home/TopLearners";
import { CourseCard } from "@/components/courses/CourseCard";
import { ExamCard } from "@/components/exams/ExamCard";
import { EpisodeCard } from "@/components/podcasts/EpisodeCard";
import { PodcastCard } from "@/components/podcasts/PodcastCard";
import { ButtonLink } from "@/components/ui/Button";
import { Carousel } from "@/components/ui/Carousel";
import { Section, SectionHeading } from "@/components/ui/Section";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, localeMeta } from "@/i18n/config";
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
    "لکس آرت",
    "LexArt",
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
    "LexArt",
    "Goethe exam simulator",
    "German exam practice online",
    "learn German A1 to C1",
    "AI German speaking practice",
  ],
  de: [
    "Deutsch-Simulator",
    "LexArt",
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
  const [[data, online], podium] = await Promise.all([
    orOffline<HomePayload>(apiFetch<HomePayload>("/home/", { locale, revalidate: 300 }), EMPTY_HOME),
    // The podium is extra: if it fails, the page simply goes without it.
    apiFetch<{ results: TopLearner[] }>("/learners/top/", { locale, revalidate: 300 })
      .then((payload) => payload.results)
      .catch(() => [] as TopLearner[]),
  ]);

  // One brand entity across every language page (same @id), named the way
  // searchers in that language write it, with the other spellings attached.
  const brandNames = ["LexArt", "لکس آرت", "لکس‌آرت", "لکسارت", "Lex Art"];
  const brandName = locale === "fa" ? "لکس آرت" : "LexArt";
  const organization = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    "@id": `${SITE_URL}/#organization`,
    name: brandName,
    alternateName: brandNames.filter((name) => name !== brandName),
    url: `${SITE_URL}/`,
    description: dict.meta.description,
    logo: {
      "@type": "ImageObject",
      url: `${SITE_URL}/icon-512.png`,
      width: 512,
      height: 512,
    },
    image: `${SITE_URL}/og-${locale}.jpg`,
    // Social profiles, comma-separated in NEXT_PUBLIC_SAME_AS, tie the brand
    // to its accounts in Google's knowledge panel.
    sameAs: (process.env.NEXT_PUBLIC_SAME_AS ?? "").split(",").map((url) => url.trim()).filter(Boolean),
    knowsLanguage: ["fa", "de", "en"],
  };

  // Google reads the site name from WebSite markup on the home page.
  const website = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": `${SITE_URL}/#website`,
    name: brandName,
    alternateName: brandNames.filter((name) => name !== brandName),
    url: `${SITE_URL}/`,
    inLanguage: localeMeta[locale].htmlLang,
    publisher: { "@id": `${SITE_URL}/#organization` },
  };

  /* A cached payload from before sections existed has no `sections` key, and
     an older API would not send one either — neither should take the page down. */
  const sections = data.sections ?? [];
  const faqSection = sections.find((section) => section.kind === "faq");
  const faqSchema = faqSection
    ? {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        mainEntity: faqSection.items.map((entry) => ({
          "@type": "Question",
          name: entry.title,
          acceptedAnswer: { "@type": "Answer", text: entry.body },
        })),
      }
    : null;

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

  const coursesBlock = (
    <Section key="courses">
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
      <Carousel
        label={dict.home.featured.title}
        grid="md:grid-cols-2 lg:grid-cols-3"
        autoplay={3000}
      >
        {data.featured_courses.slice(0, 6).map((course) => (
          <CourseCard key={course.id} course={course} locale={locale} dict={dict} />
        ))}
      </Carousel>
    </Section>
  );

  const examsBlock = (
    <Section key="exams" id="exams">
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

      {data.frequent_exams.length > 0 && (
        <>
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
        </>
      )}
    </Section>
  );

  const podcastsBlock = (
    <Section key="podcasts">
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
      <div className="grid grid-cols-[minmax(0,1fr)] gap-8 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]">
        <Carousel label={dict.home.podcasts.title} grid="md:grid-cols-2" autoplay={3000}>
          {data.podcasts.map((podcast) => (
            <PodcastCard key={podcast.id} podcast={podcast} locale={locale} dict={dict} />
          ))}
        </Carousel>
        <div className="min-w-0">
          <h3 className="mb-4 text-sm font-semibold tracking-[0.2em] text-mist-500 uppercase">
            {dict.home.podcasts.latest}
          </h3>
          <Carousel label={dict.home.podcasts.latest} grid="md:grid-cols-1 md:gap-3">
            {data.latest_episodes.slice(0, 6).map((episode) => (
              <EpisodeCard key={episode.id} episode={episode} locale={locale} dict={dict} />
            ))}
          </Carousel>
        </div>
      </div>
    </Section>
  );

  /* The page alternates prose and catalogue: an editable section, then a
     slider, then the next section, and so on. Reordering sections in the back
     office therefore changes which block each one sits above. */
  const catalogue = [coursesBlock, examsBlock, podcastsBlock];
  const interleaved: ReactNode[] = [];
  for (let i = 0; i < Math.max(sections.length, catalogue.length); i += 1) {
    const section = sections[i];
    if (section) {
      interleaved.push(
        <HomeSectionBlock key={section.key} section={section} locale={locale} />,
      );
    }
    if (catalogue[i]) interleaved.push(catalogue[i]);
  }

  return (
    <>
      {!online && <OfflineNotice locale={locale} />}
      <JsonLd data={[organization, website, courseList, ...(faqSchema ? [faqSchema] : [])]} />

      <Hero locale={locale} dict={dict} stats={data.stats} />
      <Marquee />

      <CategoryGrid categories={data.categories} locale={locale} dict={dict} />

      {interleaved}

      <MethodSteps dict={dict} />
      <TopLearners learners={podium} locale={locale} dict={dict} />
      <Testimonials dict={dict} />
      <CtaBanner locale={locale} dict={dict} />
    </>
  );
}
