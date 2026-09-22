import type { Metadata } from "next";

import { locales, localeMeta, type Locale } from "@/i18n/config";

/**
 * The public origin every canonical, hreflang, sitemap and OG URL is built
 * from. It is inlined at build time, so a production build must be made with
 * the real domain set — see DEPLOY.md.
 */
export const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000").replace(/\/+$/, "");

/** hreflang map for a path that exists in every language. */
export function alternates(path: string, locale: Locale) {
  // The home page is "/fa", never "/fa/": one URL per page, or Google sees two.
  const clean = !path || path === "/" ? "" : path.startsWith("/") ? path : `/${path}`;
  const languages: Record<string, string> = {};
  for (const code of locales) {
    languages[localeMeta[code].htmlLang] = `${SITE_URL}/${code}${clean}`;
  }
  languages["x-default"] = `${SITE_URL}/fa${clean}`;
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
  absolute = false,
}: {
  title: string;
  description: string;
  path: string;
  locale: Locale;
  image?: string;
  siteName: string;
  type?: "website" | "article";
  keywords?: string[];
  /** Skip the layout's `%s · siteName` template — the title already reads whole. */
  absolute?: boolean;
}): Metadata {
  const url = alternates(path, locale).canonical;
  // A page's own cover when it has one, otherwise the brand card in its language.
  const ogImage = image?.startsWith("http")
    ? image
    : image?.startsWith("/")
      ? `${SITE_URL}${image}`
      : `${SITE_URL}/og-${locale}.jpg`;

  return {
    title: absolute ? { absolute: title } : title,
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

/**
 * A search snippet of 120–160 characters from the pieces a page has: a short
 * subtitle alone is too thin for Google, a long description gets cut mid-word.
 */
export function snippet(...parts: (string | null | undefined)[]) {
  const text = parts
    .map((part) => (part ?? "").replace(/\s+/g, " ").trim())
    .filter(Boolean)
    .filter((part, index, all) => all.indexOf(part) === index)
    .join(" — ");
  if (text.length <= 160) return text;
  const cut = text.slice(0, 157);
  const space = cut.lastIndexOf(" ");
  return `${(space > 110 ? cut.slice(0, space) : cut).replace(/[\s,.;:،—-]+$/, "")}…`;
}

/** Brand plus the head terms every page should carry, per language. */
const BASE_KEYWORDS: Record<Locale, string[]> = {
  fa: ["لکسورا", "Lexora", "سیمیلیتور زبان آلمانی", "آموزش زبان آلمانی", "آزمون گوته"],
  en: ["Lexora", "German language simulator", "learn German", "Goethe exam"],
  de: ["Lexora", "Deutsch-Simulator", "Deutsch lernen", "Goethe-Prüfung"],
};

/** Page-specific terms first — they carry the most weight — then the brand. */
export function keywordsFor(locale: Locale, specific: (string | undefined)[] = []) {
  const cleaned = specific.filter((k): k is string => Boolean(k));
  return Array.from(new Set([...cleaned, ...BASE_KEYWORDS[locale]]));
}

/** Home > section > page, the trail Google renders under the result. */
export function breadcrumbs(locale: Locale, trail: { name: string; path: string }[]) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: trail.map((step, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: step.name,
      item: `${SITE_URL}/${locale}${step.path}`,
    })),
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
