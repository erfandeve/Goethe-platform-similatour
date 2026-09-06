import { notFound } from "next/navigation";

import { ProfileForm } from "@/components/dashboard/ProfileForm";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { User } from "@/lib/types";

export default async function ProfilePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const user = await apiFetchAuthed<User>("/auth/me/", { locale });

  return (
    <div>
      <h1 className="font-display mb-8 text-2xl font-semibold">{dict.dashboard.nav.profile}</h1>
      <ProfileForm user={user} locale={locale} dict={dict} />
    </div>
  );
}
