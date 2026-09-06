import { notFound } from "next/navigation";

import { MessageCenter } from "@/components/dashboard/MessageCenter";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { Message } from "@/lib/types";

export default async function MessagesPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetchAuthed<{ results: Message[]; unread: number }>("/auth/messages/", {
    locale,
  });

  return (
    <div>
      <h1 className="font-display mb-8 text-2xl font-semibold">{dict.dashboard.nav.messages}</h1>
      <MessageCenter initial={data.results} locale={locale} dict={dict} />
    </div>
  );
}
