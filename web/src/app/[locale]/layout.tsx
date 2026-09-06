import type { Metadata, Viewport } from "next";
import { Bricolage_Grotesque, Manrope } from "next/font/google";
import localFont from "next/font/local";
import { notFound } from "next/navigation";

import "../globals.css";

import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { SessionProvider } from "@/components/layout/SessionProvider";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale, locales, localeMeta, type Locale } from "@/i18n/config";
import { apiFetchAuthed, getAccessToken } from "@/lib/api";
import { buildMetadata, SITE_URL } from "@/lib/seo";
import type { CartState, Notification, User } from "@/lib/types";

const display = Bricolage_Grotesque({
  subsets: ["latin"],
  variable: "--font-bricolage",
  display: "swap",
});

const body = Manrope({
  subsets: ["latin"],
  variable: "--font-manrope",
  display: "swap",
});

/**
 * Yekan Bakh (variable, one file for every weight) carries the Persian text.
 * It has no accented Latin — no ä, ö, ü or ß — and German words run through
 * every page here, so the face is scoped to the Arabic-script ranges and Latin
 * always comes from Manrope. Without that limit a word like "Brötchen" would
 * change typeface mid-word.
 */
const persian = localFont({
  src: "../fonts/YekanBakh-VF.woff2",
  variable: "--font-yekan",
  display: "swap",
  weight: "100 1000",
  // No auto-generated metric fallback: that family would claim the whole of
  // Unicode and, sitting first in the stacks below, would capture Latin too.
  adjustFontFallback: false,
  declarations: [
    {
      prop: "unicode-range",
      value:
        "U+0600-06FF, U+0750-077F, U+0870-088E, U+08A0-08FF, U+200C-200F, U+FB50-FDFF, U+FE70-FEFF",
    },
  ],
});

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export const viewport: Viewport = {
  themeColor: "#050510",
  colorScheme: "dark",
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const dict = await getDictionary(locale);

  return {
    metadataBase: new URL(SITE_URL),
    ...buildMetadata({
      title: `${dict.meta.siteName} — ${dict.meta.tagline}`,
      description: dict.meta.description,
      path: "",
      locale,
      siteName: dict.meta.siteName,
      keywords: [
        "Deutsch lernen",
        "German course",
        "Goethe Zertifikat",
        "آموزش زبان آلمانی",
        "آزمون گوته",
        "German podcast",
      ],
    }),
    title: {
      default: `${dict.meta.siteName} — ${dict.meta.tagline}`,
      template: `%s · ${dict.meta.siteName}`,
    },
    applicationName: dict.meta.siteName,
    formatDetection: { telephone: false },
  };
}

/** Header data: only fetched when a session cookie is present. */
async function loadSession(locale: Locale) {
  const token = await getAccessToken();
  if (!token) return { user: null, cartCount: 0, unread: 0 };

  const [user, cart, notifications] = await Promise.all([
    apiFetchAuthed<User>("/auth/me/", { locale }).catch(() => null),
    apiFetchAuthed<CartState>("/cart/", { locale }).catch(() => null),
    apiFetchAuthed<{ results: Notification[]; unread: number }>("/auth/notifications/", {
      locale,
    }).catch(() => null),
  ]);

  return {
    user,
    cartCount: cart?.count ?? 0,
    unread: notifications?.unread ?? 0,
  };
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const dict = await getDictionary(locale);
  const session = await loadSession(locale);
  const meta = localeMeta[locale];

  return (
    <html
      lang={meta.htmlLang}
      dir={meta.dir}
      className={`${display.variable} ${body.variable} ${persian.variable}`}
      suppressHydrationWarning
    >
      <body className="min-h-dvh antialiased">
        <SessionProvider
          initialUser={session.user}
          initialCartCount={session.cartCount}
          initialUnread={session.unread}
        >
          <a
            href="#main"
            className="sr-only focus:not-sr-only focus:fixed focus:start-4 focus:top-4 focus:z-100 focus:rounded-full focus:bg-violet-500 focus:px-5 focus:py-2 focus:text-sm focus:text-ink-950"
          >
            {dict.nav.home}
          </a>
          <Header locale={locale} dict={dict} />
          <main id="main" className="pt-24">
            {children}
          </main>
          <Footer locale={locale} dict={dict} />
        </SessionProvider>
      </body>
    </html>
  );
}
