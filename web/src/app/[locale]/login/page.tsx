import { notFound } from "next/navigation";

import { AuthForm } from "@/components/layout/AuthForm";
import { AuthShell } from "@/components/layout/AuthShell";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";

export const metadata = { robots: { index: false, follow: true } };

export default async function LoginPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);

  return (
    <AuthShell
      locale={locale}
      dict={dict}
      title={dict.auth.loginTitle}
      subtitle={dict.auth.loginSubtitle}
    >
      <AuthForm mode="login" locale={locale} dict={dict} />
    </AuthShell>
  );
}
