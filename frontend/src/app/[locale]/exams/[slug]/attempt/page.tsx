import { notFound, redirect } from "next/navigation";

import { ExamRunner } from "@/components/exams/ExamRunner";
import { ExamStart } from "@/components/exams/goethe/ExamStart";
import { GoetheRunner } from "@/components/exams/goethe/GoetheRunner";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch, getAccessToken } from "@/lib/api";
import type { ExamDetail, ExamModuleSummary } from "@/lib/types";

export const metadata = { robots: { index: false, follow: false } };

interface GoetheExam extends ExamDetail {
  format: "goethe" | "simple";
  modules: ExamModuleSummary[];
}

export default async function ExamAttemptPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string; slug: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();

  const token = await getAccessToken();
  if (!token) redirect(`/${locale}/login?next=/${locale}/exams/${slug}/attempt`);

  const dict = await getDictionary(locale);
  const exam = await apiFetch<GoetheExam>(`/exams/${slug}/`, {
    locale,
    token,
    revalidate: 0,
  }).catch(() => null);
  if (!exam) notFound();

  // Level simulators built from the Goethe model sets run in the exam player;
  // the older question banks keep the simple runner until they are converted.
  if (exam.format !== "goethe") {
    return <ExamRunner slug={slug} locale={locale} dict={dict} />;
  }

  const query = await searchParams;
  const requested = typeof query.module === "string" ? query.module : "";
  const selected = exam.modules.find((entry) => entry.skill === requested);

  if (!selected) {
    return (
      <ExamStart
        slug={slug}
        title={exam.title}
        level={exam.level}
        board={exam.exam_board}
        modules={exam.modules}
        locale={locale}
        dict={dict}
        brand={dict.meta.siteName}
      />
    );
  }

  return (
    <GoetheRunner
      slug={slug}
      moduleSkill={selected.skill}
      locale={locale}
      dict={dict}
      brand={dict.meta.siteName}
    />
  );
}
