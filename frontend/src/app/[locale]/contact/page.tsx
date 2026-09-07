import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ContactForm } from "@/components/layout/ContactForm";
import { Section, SectionHeading } from "@/components/ui/Section";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, locales } from "@/i18n/config";
import { buildMetadata, JsonLd, SITE_URL } from "@/lib/seo";

export const revalidate = 3600;

export const CONTACT_EMAIL = "support@lexora.academy";

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

const KEYWORDS: Record<string, string[]> = {
  fa: ["تماس با ما", "پشتیبانی لکسورا", "Lexora", "لکسورا", "سیمیلیتور زبان آلمانی"],
  en: ["contact Lexora", "Lexora support", "German language simulator", "Goethe exam help"],
  de: ["Kontakt Lexora", "Lexora Support", "Deutsch-Simulator", "Goethe-Prüfung Hilfe"],
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const dict = await getDictionary(locale);
  return buildMetadata({
    title: `${dict.site.contact.title} | ${dict.site.contact.subtitle}`,
    description: dict.site.contact.intro,
    path: "/contact",
    locale,
    siteName: dict.meta.siteName,
    absolute: true,
    keywords: KEYWORDS[locale],
  });
}

export default async function ContactPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const t = dict.site.contact;

  const schema = [
    {
      "@context": "https://schema.org",
      "@type": "ContactPage",
      name: t.title,
      description: t.intro,
      url: `${SITE_URL}/${locale}/contact`,
      inLanguage: locale,
      mainEntity: {
        "@type": "Organization",
        name: "Lexora",
        url: `${SITE_URL}/${locale}`,
        email: CONTACT_EMAIL,
        contactPoint: [
          {
            "@type": "ContactPoint",
            contactType: "customer support",
            email: CONTACT_EMAIL,
            availableLanguage: ["fa", "de", "en"],
          },
        ],
      },
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      mainEntity: t.faq.map((item) => ({
        "@type": "Question",
        name: item.q,
        acceptedAnswer: { "@type": "Answer", text: item.a },
      })),
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: dict.nav.home, item: `${SITE_URL}/${locale}` },
        { "@type": "ListItem", position: 2, name: t.title, item: `${SITE_URL}/${locale}/contact` },
      ],
    },
  ];

  const facts = [
    { label: t.emailLabel, value: CONTACT_EMAIL, href: `mailto:${CONTACT_EMAIL}` },
    { label: t.supportLabel, value: t.supportValue },
    { label: t.responseLabel, value: t.responseValue },
  ];

  return (
    <>
      <JsonLd data={schema} />

      <Section className="pb-10">
        <SectionHeading as="h1" eyebrow="Lexora" title={t.title} subtitle={t.subtitle} />
        <p className="-mt-6 max-w-2xl text-lg leading-9 text-mist-300">{t.intro}</p>
      </Section>

      <Section className="py-10">
        <div className="grid gap-10 lg:grid-cols-[320px_minmax(0,1fr)]">
          <div className="flex flex-col gap-4">
            {facts.map((fact) => (
              <div
                key={fact.label}
                className="rounded-2xl border border-white/10 bg-white/[0.02] p-6"
              >
                <p className="mb-1 text-xs tracking-wider text-mist-500 uppercase">{fact.label}</p>
                {fact.href ? (
                  <a href={fact.href} className="font-medium text-white hover:text-violet-300">
                    {fact.value}
                  </a>
                ) : (
                  <p className="font-medium text-white">{fact.value}</p>
                )}
              </div>
            ))}
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/[0.02] p-8">
            <h2 className="font-display mb-6 text-xl font-semibold text-white">{t.formTitle}</h2>
            <ContactForm
              labels={{
                name: t.name,
                email: t.email,
                subject: t.subject,
                message: t.message,
                send: t.send,
                sent: t.sent,
              }}
              mailto={CONTACT_EMAIL}
            />
          </div>
        </div>
      </Section>

      <Section className="pt-10">
        <h2 className="font-display mb-6 text-2xl font-bold text-white">{t.faqTitle}</h2>
        <div className="flex max-w-3xl flex-col gap-3">
          {t.faq.map((item) => (
            <details
              key={item.q}
              className="rounded-2xl border border-white/10 bg-white/[0.02] px-6 py-4"
            >
              <summary className="cursor-pointer list-none font-semibold text-white marker:content-none">
                {item.q}
              </summary>
              <p className="mt-3 leading-8 text-mist-300">{item.a}</p>
            </details>
          ))}
        </div>
      </Section>
    </>
  );
}
