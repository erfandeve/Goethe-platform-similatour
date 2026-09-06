import type { Metadata } from "next";

import { locales, localeMeta, type Locale } from "@/i18n/config";

export const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://goteh.academy";

/** hreflang map for a path that exists in every language. */
export function alternates(path: string, locale: Locale) {
  const clean = path.startsWith("/") ? path : `/${path}`;
  const languages: Record<string, string> = {};
  for (const code of locales) {
    languages[localeMeta[code].htmlLang] = `${SITE_URL}/${code}${clean}`;
  }
  languages["x-default"] = `${SITE_URL}/de${clean}`;
  return { canonical: `${SITE_URL}/${locale}${clean}`, languages };
}

export function buildMetadata({
  title,
  description,
  path,
  locale,
  image,
  siteName,
  type = "website",
  keywords,
}: {
  title: string;
  description: string;
  path: string;
  locale: Locale;
  image?: string;
  siteName: string;
  type?: "website" | "article";
  keywords?: string[];
}): Metadata {
  const url = `${SITE_URL}/${locale}${path.startsWith("/") ? path : `/${path}`}`;
  const ogImage = image?.startsWith("http") ? image : `${SITE_URL}/og-default.png`;

  return {
    title,
    description,
    keywords,
    alternates: alternates(path, locale),
    openGraph: {
      title,
      description,
      url,
      siteName,
      type,
      locale: localeMeta[locale].htmlLang.replace("-", "_"),
      images: [{ url: ogImage, width: 1200, height: 630, alt: title }],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [ogImage],
    },
    robots: { index: true, follow: true, "max-image-preview": "large" },
  };
}

export function JsonLd({ data }: { data: Record<string, unknown> | Record<string, unknown>[] }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
