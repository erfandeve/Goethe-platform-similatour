import { notFound, redirect } from "next/navigation";

import { DashboardNav } from "@/components/dashboard/DashboardNav";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed, getAccessToken } from "@/lib/api";
import type { Message, Notification, User } from "@/lib/types";

export const metadata = { robots: { index: false, follow: false } };

export default async function DashboardLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const token = await getAccessToken();
  if (!token) redirect(`/${locale}/login?next=/${locale}/dashboard`);

  const dict = await getDictionary(locale);
  const [user, notifications, messages] = await Promise.all([
    apiFetchAuthed<User>("/auth/me/", { locale }).catch(() => null),
    apiFetchAuthed<{ unread: number; results: Notification[] }>("/auth/notifications/", {
      locale,
    }).catch(() => null),
    apiFetchAuthed<{ unread: number; results: Message[] }>("/auth/messages/", { locale }).catch(
      () => null,
    ),
  ]);

  if (!user) redirect(`/${locale}/login?next=/${locale}/dashboard`);

  return (
    <div className="container-page grid gap-8 py-10 lg:grid-cols-[16rem_1fr]">
      <div>
        <div className="mb-6">
          <p className="text-xs tracking-wider text-mist-600 uppercase">{dict.dashboard.greeting}</p>
          <p className="font-display mt-1 text-xl font-semibold">{user.full_name}</p>
        </div>
        <DashboardNav
          locale={locale}
          dict={dict}
          badges={{
            notifications: notifications?.unread ?? 0,
            messages: messages?.unread ?? 0,
          }}
        />
      </div>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
