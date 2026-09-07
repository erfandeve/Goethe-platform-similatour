"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { logout } from "@/lib/client";
import { cn } from "@/lib/utils";

const AI_SPEAKING_COURSE = "einreise-nach-deutschland";

import { LocaleSwitcher } from "./LocaleSwitcher";
import { Logo } from "./Logo";
import { useSession } from "./SessionProvider";

export function Header({ locale, dict }: { locale: Locale; dict: Dictionary }) {
  const { user, cartCount } = useSession();
  const pathname = usePathname();
  const router = useRouter();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [menu, setMenu] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    const frame = requestAnimationFrame(onScroll);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", onScroll);
    };
  }, []);

  // Closing the menus belongs to the navigation itself, not to an effect.
  const [menuRoute, setMenuRoute] = useState(pathname);
  if (menuRoute !== pathname) {
    setMenuRoute(pathname);
    setOpen(false);
    setMenu(false);
  }

  const links = [
    { href: `/${locale}/courses`, label: dict.nav.courses },
    { href: `/${locale}/exams`, label: dict.nav.exams },
    { href: `/${locale}/podcasts`, label: dict.nav.podcasts },
    // The AI speaking course sells itself from its own course page.
    {
      href: `/${locale}/courses/${AI_SPEAKING_COURSE}`,
      label: dict.nav.aiSpeaking,
      badge: true,
    },
    { href: `/${locale}/plans`, label: dict.nav.plansNav },
    { href: `/${locale}/articles`, label: dict.nav.articles },
  ];

  async function signOut() {
    await logout();
    router.push(`/${locale}`);
    router.refresh();
  }

  return (
    <header
      className={cn(
        "fixed inset-x-0 top-0 z-50 transition-all duration-500",
        scrolled ? "py-2.5" : "py-5",
      )}
    >
      <div className="container-page">
        <div
          className={cn(
            "flex items-center gap-4 rounded-full px-4 py-2.5 transition-all duration-500 md:px-5",
            scrolled ? "glass-strong shadow-[var(--shadow-lift)]" : "border border-transparent",
          )}
        >
          <Logo locale={locale} label={dict.meta.siteName} />

          <nav className="ms-6 hidden items-center gap-1 lg:flex">
            {links.map((link) => {
              const active = pathname.startsWith(link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={cn(
                    "relative rounded-full px-4 py-2 text-sm transition",
                    active ? "text-mist-50" : "text-mist-400 hover:text-mist-50",
                  )}
                >
                  {active ? (
                    <span className="absolute inset-0 rounded-full bg-white/7" aria-hidden />
                  ) : null}
                  <span className="relative flex items-center gap-1.5">
                    {link.label}
                    {link.badge ? (
                      <span className="rounded-md bg-cyan-400/15 px-1.5 py-0.5 text-[9px] font-bold tracking-wide text-cyan-400 uppercase">
                        AI
                      </span>
                    ) : null}
                  </span>
                </Link>
              );
            })}
          </nav>

          <div className="ms-auto flex items-center gap-2">
            <LocaleSwitcher locale={locale} />

            <Link
              href={`/${locale}/cart`}
              className="glass relative grid size-10 place-items-center rounded-full transition hover:border-white/20"
              aria-label={dict.nav.cart}
            >
              <svg viewBox="0 0 24 24" className="size-4.5" fill="none" aria-hidden>
                <path
                  d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.5a2 2 0 0 0 2-1.6L20.5 8H6.2"
                  stroke="currentColor"
                  strokeWidth="1.7"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <circle cx="10" cy="20" r="1.4" fill="currentColor" />
                <circle cx="17" cy="20" r="1.4" fill="currentColor" />
              </svg>
              {cartCount > 0 ? (
                <span className="tnum absolute -end-0.5 -top-0.5 grid size-5 place-items-center rounded-full bg-violet-500 text-[10px] font-bold text-ink-950">
                  {cartCount}
                </span>
              ) : null}
            </Link>

            {user ? (
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setMenu((value) => !value)}
                  className="glass flex h-10 items-center gap-2 rounded-full ps-1.5 pe-3.5 transition hover:border-white/20"
                >
                  <span className="grid size-7 place-items-center rounded-full bg-linear-to-br from-violet-500 to-cyan-400 text-[11px] font-bold text-ink-950">
                    {user.full_name.slice(0, 1).toUpperCase()}
                  </span>
                  <span className="hidden max-w-24 truncate text-sm md:inline">
                    {user.first_name || user.full_name}
                  </span>
                </button>

                {menu ? (
                  <>
                    <div className="fixed inset-0 z-40" onClick={() => setMenu(false)} />
                    <div className="glass-strong absolute end-0 z-50 mt-2 w-56 overflow-hidden rounded-2xl p-1.5">
                      <Link
                        href={`/${locale}/dashboard`}
                        className="block rounded-xl px-3 py-2.5 text-sm transition hover:bg-white/6"
                      >
                        {dict.nav.dashboard}
                      </Link>
                      <Link
                        href={`/${locale}/dashboard/profile`}
                        className="block rounded-xl px-3 py-2.5 text-sm transition hover:bg-white/6"
                      >
                        {dict.dashboard.nav.profile}
                      </Link>
                      {user.is_staff ? (
                        <Link
                          href={`/${locale}/admin`}
                          className="block rounded-xl px-3 py-2.5 text-sm text-cyan-400 transition hover:bg-white/6"
                        >
                          {dict.nav.admin}
                        </Link>
                      ) : null}
                      <button
                        type="button"
                        onClick={signOut}
                        className="block w-full rounded-xl px-3 py-2.5 text-start text-sm text-rose-400 transition hover:bg-rose-400/10"
                      >
                        {dict.nav.logout}
                      </button>
                    </div>
                  </>
                ) : null}
              </div>
            ) : (
              <div className="hidden items-center gap-2 sm:flex">
                <Link
                  href={`/${locale}/login`}
                  className="rounded-full px-4 py-2 text-sm text-mist-400 transition hover:text-mist-50"
                >
                  {dict.nav.login}
                </Link>
                <Link
                  href={`/${locale}/register`}
                  className="rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-4 py-2 text-sm font-semibold text-ink-950 transition hover:-translate-y-0.5"
                >
                  {dict.nav.register}
                </Link>
              </div>
            )}

            <button
              type="button"
              onClick={() => setOpen((value) => !value)}
              className="glass grid size-10 place-items-center rounded-full lg:hidden"
              aria-label={open ? dict.nav.close : dict.nav.menu}
            >
              <svg viewBox="0 0 24 24" className="size-4.5" fill="none" aria-hidden>
                {open ? (
                  <path d="m6 6 12 12M18 6 6 18" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                ) : (
                  <path d="M4 7h16M4 12h16M4 17h10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {open ? (
          <nav className="glass-strong mt-2 flex flex-col gap-1 rounded-3xl p-3 lg:hidden">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="rounded-2xl px-4 py-3 text-sm transition hover:bg-white/6"
              >
                {link.label}
              </Link>
            ))}
            {!user ? (
              <div className="mt-1 grid grid-cols-2 gap-2">
                <Link
                  href={`/${locale}/login`}
                  className="rounded-2xl border border-white/12 px-4 py-3 text-center text-sm"
                >
                  {dict.nav.login}
                </Link>
                <Link
                  href={`/${locale}/register`}
                  className="rounded-2xl bg-linear-to-r from-violet-500 to-cyan-400 px-4 py-3 text-center text-sm font-semibold text-ink-950"
                >
                  {dict.nav.register}
                </Link>
              </div>
            ) : null}
          </nav>
        ) : null}
      </div>
    </header>
  );
}
