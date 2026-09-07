import { notFound } from "next/navigation";

import { ArticlesManager } from "@/components/admin/ArticlesManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";

export default async function AdminArticlesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ results: Parameters<typeof ArticlesManager>[0]["initial"] }>(
    "/admin/articles/",
    { locale },
  ).catch(() => ({ results: [] }));

  return <ArticlesManager initial={data.results} />;
}
