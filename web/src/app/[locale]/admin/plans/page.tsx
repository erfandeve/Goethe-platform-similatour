import { notFound } from "next/navigation";

import { PlansManager } from "@/components/admin/PlansManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminPlan } from "@/lib/admin";

export default async function AdminPlansPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ results: AdminPlan[]; perks: string[] }>(
    "/admin/plans/",
    { locale },
  ).catch(() => ({ results: [] as AdminPlan[], perks: [] as string[] }));

  return <PlansManager initial={data.results} perks={data.perks} locale={locale} />;
}
