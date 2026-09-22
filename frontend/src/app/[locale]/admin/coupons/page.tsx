import { notFound } from "next/navigation";

import { CouponsManager } from "@/components/admin/CouponsManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminCoupon } from "@/lib/admin";

export default async function AdminCouponsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ results: AdminCoupon[]; targets: string[] }>(
    "/admin/coupons/",
    { locale },
  ).catch(() => ({ results: [] as AdminCoupon[], targets: ["course", "exam", "exam_code", "plan"] }));

  return <CouponsManager initial={data.results} targets={data.targets} locale={locale} />;
}
