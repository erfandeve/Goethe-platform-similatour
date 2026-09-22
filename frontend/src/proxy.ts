import { NextRequest, NextResponse } from "next/server";

import { defaultLocale, locales } from "@/i18n/config";

const PUBLIC_FILE = /\.(.*)$/;

/**
 * The best supported language from Accept-Language, by the visitor's own
 * weights: "en-US,en;q=0.9,fa;q=0.5" is English, not Persian.
 */
function preferredLocale(header: string) {
  const ranked = header
    .split(",")
    .map((part, index) => {
      const [tag, ...params] = part.trim().toLowerCase().split(";");
      const q = Number(params.find((p) => p.trim().startsWith("q="))?.split("=")[1] ?? 1);
      return { base: tag.split("-")[0], q: Number.isFinite(q) ? q : 0, index };
    })
    .filter((entry) => entry.base && entry.q > 0)
    .sort((a, b) => b.q - a.q || a.index - b.index);
  return ranked.map((entry) => entry.base).find((base) => (locales as readonly string[]).includes(base));
}

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname === "/favicon.ico" ||
    PUBLIC_FILE.test(pathname)
  ) {
    return NextResponse.next();
  }

  const hasLocale = locales.some(
    (locale) => pathname === `/${locale}` || pathname.startsWith(`/${locale}/`),
  );
  if (hasLocale) return NextResponse.next();

  // Remember the visitor's last choice, otherwise negotiate from Accept-Language.
  const cookieLocale = request.cookies.get("NEXT_LOCALE")?.value;
  const fromHeader = preferredLocale(request.headers.get("accept-language") ?? "");
  const locale =
    (locales.includes(cookieLocale as never) && cookieLocale) || fromHeader || defaultLocale;

  const url = request.nextUrl.clone();
  url.pathname = `/${locale}${pathname === "/" ? "" : pathname}`;
  const response = NextResponse.redirect(url);
  // The answer depends on these headers, so caches must not share it.
  response.headers.set("Vary", "Accept-Language, Cookie");
  return response;
}

export const config = {
  matcher: ["/((?!_next|api|.*\\..*).*)"],
};
