import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { PlanCards, type Plan } from "@/components/billing/PlanCards";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetch, getAccessToken } from "@/lib/api";
import { buildMetadata } from "@/lib/seo";

export const revalidate = 30;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const dict = await getDictionary(locale);
  return buildMetadata({
    title: dict.plans.title,
    description: dict.plans.subtitle,
    path: "/plans",
    locale,
    siteName: dict.meta.siteName,
  });
}

export default async function PlansPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const dict = await getDictionary(locale);
  const token = await getAccessToken();
  const data = await apiFetch<{ results: Plan[] }>("/plans/", {
    locale,
    token,
    revalidate: token ? 0 : 30,
  }).catch(() => ({ results: [] as Plan[] }));

  return (
    <div className="container-page py-12">
      <header className="mb-12 text-center">
        <p className="text-xs font-semibold tracking-[0.25em] text-violet-400 uppercase">
          {dict.plans.title}
        </p>
        <h1 className="font-display mt-3 text-4xl leading-tight font-semibold text-balance md:text-5xl">
          {dict.plans.subtitle}
        </h1>
      </header>

      <PlanCards plans={data.results} locale={locale} dict={dict} />
    </div>
  );
}
