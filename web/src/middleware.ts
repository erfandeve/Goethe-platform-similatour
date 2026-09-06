import { NextRequest, NextResponse } from "next/server";

import { defaultLocale, locales } from "@/i18n/config";

const PUBLIC_FILE = /\.(.*)$/;

export function middleware(request: NextRequest) {
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
  const header = request.headers.get("accept-language") ?? "";
  const fromHeader = locales.find((locale) => header.toLowerCase().includes(locale));
  const locale =
    (locales.includes(cookieLocale as never) && cookieLocale) || fromHeader || defaultLocale;

  const url = request.nextUrl.clone();
  url.pathname = `/${locale}${pathname === "/" ? "" : pathname}`;
  return NextResponse.redirect(url);
}

export const config = {
  matcher: ["/((?!_next|api|.*\\..*).*)"],
};
