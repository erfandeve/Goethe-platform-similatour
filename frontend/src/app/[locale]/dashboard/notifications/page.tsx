import { notFound } from "next/navigation";

import { NotificationList } from "@/components/dashboard/NotificationList";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { Notification } from "@/lib/types";

export default async function NotificationsPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetchAuthed<{ results: Notification[]; unread: number }>(
    "/auth/notifications/",
    { locale },
  );

  return (
    <div>
      <h1 className="font-display mb-8 text-2xl font-semibold">
        {dict.dashboard.nav.notifications}
      </h1>
      <NotificationList initial={data.results} locale={locale} dict={dict} />
    </div>
  );
}
