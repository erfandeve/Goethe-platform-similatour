import { notFound } from "next/navigation";

import { PodcastsManager } from "@/components/admin/PodcastsManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminCategory, AdminPodcast } from "@/lib/admin";

export default async function AdminPodcastsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const [podcasts, categories] = await Promise.all([
    apiFetchAuthed<{ results: AdminPodcast[] }>("/admin/podcasts/", { locale }).catch(() => ({
      results: [] as AdminPodcast[],
    })),
    apiFetchAuthed<{ results: AdminCategory[] }>("/admin/categories/", { locale }).catch(() => ({
      results: [] as AdminCategory[],
    })),
  ]);

  return (
    <PodcastsManager
      initial={podcasts.results}
      categories={categories.results}
      locale={locale}
    />
  );
}
