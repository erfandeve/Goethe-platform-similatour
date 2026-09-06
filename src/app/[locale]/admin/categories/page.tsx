import { notFound } from "next/navigation";

import { CategoriesManager } from "@/components/admin/CategoriesManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminCategory } from "@/lib/admin";

export default async function AdminCategoriesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ results: AdminCategory[] }>("/admin/categories/", {
    locale,
  }).catch(() => ({ results: [] as AdminCategory[] }));

  return <CategoriesManager initial={data.results} />;
}
