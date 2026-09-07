import { notFound } from "next/navigation";

import { SectionsManager } from "@/components/admin/SectionsManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";

export default async function AdminSectionsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ results: Parameters<typeof SectionsManager>[0]["initial"] }>(
    "/admin/sections/",
    { locale },
  ).catch(() => ({ results: [] }));

  return <SectionsManager initial={data.results} />;
}
