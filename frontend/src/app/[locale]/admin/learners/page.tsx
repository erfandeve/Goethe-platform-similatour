import { notFound } from "next/navigation";

import { LearnersManager } from "@/components/admin/LearnersManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminLearnerPage } from "@/lib/admin";

export default async function AdminLearnersPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<AdminLearnerPage>("/admin/learners/", { locale }).catch(
    (): AdminLearnerPage => ({
      results: [],
      podium: [],
      meta: { page: 1, size: 25, total: 0, pages: 1 },
      sort: "points",
    }),
  );

  return <LearnersManager initial={data} locale={locale} />;
}
