import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { AddToCartButton } from "@/components/courses/AddToCartButton";
import { SittingPicker } from "@/components/exams/SittingPicker";
import { LevelBadge } from "@/components/ui/Badge";
import { ButtonLink } from "@/components/ui/Button";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, type Locale } from "@/i18n/config";
import { apiFetch, getAccessToken } from "@/lib/api";
import { compact, formatNumber, formatPrice } from "@/lib/format";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";
import type { ExamDetail } from "@/lib/types";
import { alpha } from "@/lib/utils";

const MODULE_LABELS: Record<string, string> = {
  lesen: "Lesen",
  hoeren: "Hören",
  schreiben: "Schreiben",
  sprechen: "Sprechen",
};

export const revalidate = 300;

async function loadExam(slug: string, locale: Locale, token: string | null) {
  try {
    return await apiFetch<ExamDetail>(`/exams/${slug}/`, {
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
  const [dict, exam] = await Promise.all([getDictionary(locale), loadExam(slug, locale, null)]);
  if (!exam) return {};
  return buildMetadata({
    title: exam.title,
    description: exam.subtitle || exam.description.slice(0, 155),
    path: `/exams/${slug}`,
    locale,
    siteName: dict.meta.siteName,
    keywords: [exam.level, exam.exam_board, "Prüfung", "آزمون"],
  });
}

export default async function ExamDetailPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const token = await getAccessToken();
  const exam = await loadExam(slug, locale, token);
  if (!exam) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Quiz",
    name: exam.title,
    description: exam.description,
    url: `${SITE_URL}/${locale}/exams/${exam.slug}`,
    educationalLevel: exam.level,
    inLanguage: exam.language,
    numberOfQuestions: exam.questions_count,
    provider: { "@type": "EducationalOrganization", name: dict.meta.siteName },
  };

  return (
    <>
      <JsonLd data={jsonLd} />

      <div className="relative overflow-hidden">
        <div
          className="pointer-events-none absolute -top-48 end-0 size-[38rem] rounded-full opacity-20 blur-3xl"
          style={{ background: exam.accent }}
          aria-hidden
        />
        <div className="container-page relative grid gap-10 py-12 lg:grid-cols-[1.5fr_1fr]">
          <div>
            <nav className="mb-6 flex items-center gap-2 text-xs text-mist-500">
              <Link href={`/${locale}`} className="hover:text-mist-200">
                {dict.nav.home}
              </Link>
              <span aria-hidden>/</span>
              <Link href={`/${locale}/exams`} className="hover:text-mist-200">
                {dict.nav.exams}
              </Link>
            </nav>

            <div className="flex flex-wrap items-center gap-3">
              <LevelBadge level={exam.level} />
              <span className="text-xs tracking-wide text-mist-500 uppercase">
                {exam.exam_board}
              </span>
              {exam.kind === "frequent" ? (
                <span className="rounded-full bg-amber-400/12 px-2.5 py-1 text-[11px] font-semibold text-amber-400 uppercase">
                  {dict.home.exams.frequent}
                </span>
              ) : null}
            </div>

            <h1 className="font-display mt-5 text-4xl leading-tight font-semibold text-balance md:text-6xl">
              {exam.title}
            </h1>
            <p className="text-muted mt-5 max-w-2xl text-lg">{exam.subtitle}</p>
            <p className="text-muted mt-6 max-w-2xl leading-relaxed">{exam.description}</p>

            <ul className="mt-8 grid gap-3 sm:grid-cols-2">
              {exam.highlights.map((item) => (
                <li key={item} className="glass flex items-center gap-3 rounded-2xl px-4 py-3">
                  <span style={{ color: exam.accent }} aria-hidden>
                    ✦
                  </span>
                  <span className="text-sm text-mist-200">{item}</span>
                </li>
              ))}
            </ul>

            <section className="mt-12">
              <h2 className="font-display mb-5 text-2xl font-semibold">
                {dict.exams.card.skills}
              </h2>

              {/* Goethe model sets are organised in modules, each sat separately. */}
              {exam.modules?.length ? (
                <div className="space-y-3">
                  {exam.modules.map((module) => (
                    <div
                      key={module.skill}
                      className="glass flex flex-wrap items-center gap-4 rounded-2xl px-5 py-4"
                    >
                      <span
                        className="grid size-10 shrink-0 place-items-center rounded-xl text-[11px] font-bold uppercase"
                        style={{ background: alpha(exam.accent, 0.14), color: exam.accent }}
                        aria-hidden
                      >
                        {MODULE_LABELS[module.skill].slice(0, 2)}
                      </span>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-semibold" dir="ltr">
                          {MODULE_LABELS[module.skill]}
                          <span className="ms-2 font-normal text-mist-500">{module.title}</span>
                        </p>
                        <p className="text-xs text-mist-500">{module.intro}</p>
                      </div>
                      <span className="tnum text-xs text-mist-400">
                        {formatNumber(module.items_count, locale)} {dict.exams.card.questions}
                      </span>
                      <span className="tnum text-xs text-mist-400">
                        {formatNumber(module.duration_minutes, locale)} {dict.common.minutes}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
              <div className="space-y-3">
                {exam.sections.map((section) => (
                  <div
                    key={section.index}
                    className="glass flex flex-wrap items-center gap-4 rounded-2xl px-5 py-4"
                  >
                    <span
                      className="grid size-10 shrink-0 place-items-center rounded-xl text-xs font-bold"
                      style={{ background: alpha(exam.accent, 0.14), color: exam.accent }}
                      aria-hidden
                    >
                      {section.index + 1}
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-semibold">{dict.exams.skills[section.skill]}</p>
                      <p className="text-xs text-mist-500">{section.instructions}</p>
                    </div>
                    <span className="tnum text-xs text-mist-400">
                      {formatNumber(section.questions_count, locale)} {dict.exams.card.questions}
                    </span>
                    <span className="tnum text-xs text-mist-400">
                      {formatNumber(section.duration_minutes, locale)} {dict.common.minutes}
                    </span>
                  </div>
                ))}
              </div>
              )}
            </section>
          </div>

          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div className="glass rounded-3xl p-7">
              <div
                className="font-display grid h-28 place-items-center rounded-2xl text-5xl font-bold"
                style={{
                  background: `linear-gradient(140deg, ${alpha(exam.accent, 0.35)}, transparent)`,
                  color: exam.accent,
                }}
                aria-hidden
              >
                {exam.level}
              </div>

              <dl className="mt-6 space-y-3 text-sm">
                {[
                  [dict.exams.card.questions, formatNumber(exam.questions_count, locale)],
                  [
                    dict.exams.card.minutes,
                    `${formatNumber(exam.duration_minutes, locale)} ${dict.common.minutes}`,
                  ],
                  [dict.exams.card.passScore, `${formatNumber(exam.pass_score, locale)}%`],
                  [dict.exams.card.attempts, compact(exam.attempts_count, locale)],
                ].map(([label, value]) => (
                  <div key={label} className="flex items-center justify-between">
                    <dt className="text-mist-500">{label}</dt>
                    <dd className="tnum font-semibold">{value}</dd>
                  </div>
                ))}
              </dl>

              <div className="mt-6 border-t border-white/8 pt-5">
                <p className="tnum font-display mb-4 text-2xl font-semibold">
                  {formatPrice(exam.effective_price, locale, dict.exams.card.free)}
                </p>

                {exam.has_access ? (
                  <ButtonLink
                    href={`/${locale}/exams/${exam.slug}/attempt`}
                    size="lg"
                    className="w-full"
                  >
                    {dict.exams.card.start}
                  </ButtonLink>
                ) : exam.codes?.length ? null : (
                  <AddToCartButton
                    slug={exam.slug}
                    itemType="exam"
                    locale={locale}
                    dict={dict}
                    isFree={false}
                  />
                )}

                {exam.codes?.length ? (
                  <SittingPicker
                    slug={exam.slug}
                    codes={exam.codes}
                    basePrice={exam.base_price ?? exam.effective_price}
                    accent={exam.accent}
                    locale={locale}
                    dict={dict}
                  />
                ) : null}

                {exam.last_attempt ? (
                  <Link
                    href={`/${locale}/dashboard/exams`}
                    className="tnum mt-4 block text-center text-xs text-mist-500 hover:text-mist-200"
                  >
                    {dict.exams.result.score}: {formatNumber(exam.last_attempt.score, locale)}%
                  </Link>
                ) : null}
              </div>
            </div>
          </aside>
        </div>
      </div>
    </>
  );
}
