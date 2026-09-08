import { notFound, redirect } from "next/navigation";

import { AdminNav } from "@/components/admin/AdminNav";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed, getAccessToken } from "@/lib/api";
import type { User } from "@/lib/types";

export const metadata = { robots: { index: false, follow: false } };

export default async function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const token = await getAccessToken();
  if (!token) redirect(`/${locale}/login?next=/${locale}/admin`);

  // The gate that matters is on the API; this only avoids showing an empty shell.
  const user = await apiFetchAuthed<User & { is_staff?: boolean }>("/auth/me/", {
    locale,
  }).catch(() => null);
  if (!user) redirect(`/${locale}/login?next=/${locale}/admin`);

  return (
    <div className="container-page grid gap-8 py-10 lg:grid-cols-[15rem_1fr]">
      {/* min-w-0: the nav scrolls sideways on a phone, and without this the
          column sizes to its content and drags the whole page wide. */}
      <div className="min-w-0">
        <div className="mb-6">
          <p className="text-xs tracking-wider text-mist-600 uppercase">Admin</p>
          <p className="font-display mt-1 text-xl font-semibold">{user.full_name}</p>
        </div>
        <AdminNav locale={locale} />
      </div>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
