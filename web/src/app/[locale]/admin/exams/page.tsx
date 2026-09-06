import { notFound } from "next/navigation";

import { ExamsManager } from "@/components/admin/ExamsManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminExam } from "@/lib/admin";

export default async function AdminExamsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ results: AdminExam[] }>("/admin/exams/", {
    locale,
  }).catch(() => ({ results: [] as AdminExam[] }));

  return <ExamsManager initial={data.results} locale={locale} />;
}
