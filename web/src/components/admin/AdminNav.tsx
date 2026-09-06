"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import type { Locale } from "@/i18n/config";
import { cn } from "@/lib/utils";

const ITEMS = [
  { href: "", label: "نمای کلی", labelDe: "Übersicht", icon: "M4 12h6V4H4v8Zm10 8h6v-8h-6v8ZM4 20h6v-5H4v5Zm10-11h6V4h-6v5Z" },
  { href: "/courses", label: "دوره‌ها", labelDe: "Kurse", icon: "M4 5h9a3 3 0 0 1 3 3v11a3 3 0 0 0-3-3H4V5Zm16 0h-1a3 3 0 0 0-3 3v11a3 3 0 0 1 3-3h1V5Z" },
  { href: "/categories", label: "دسته‌بندی‌ها", labelDe: "Kategorien", icon: "M12 3 2 8l10 5 10-5-10-5Zm0 9L2 17l10 5 10-5-10-5Z" },
  { href: "/speaking", label: "مکالمه با AI", labelDe: "KI-Sprechen", icon: "M12 15a3.5 3.5 0 0 0 3.5-3.5v-5a3.5 3.5 0 1 0-7 0v5A3.5 3.5 0 0 0 12 15Zm6.5-3.5a6.5 6.5 0 0 1-13 0M12 18v3" },
  { href: "/exams", label: "آزمون‌ها", labelDe: "Prüfungen", icon: "M6 3h9l4 4v14H6V3Zm3 9h7M9 16h5" },
  { href: "/podcasts", label: "پادکست‌ها", labelDe: "Podcasts", icon: "M12 14a3 3 0 0 0 3-3V6a3 3 0 1 0-6 0v5a3 3 0 0 0 3 3Zm6-3a6 6 0 0 1-12 0M12 17v4" },
  { href: "/plans", label: "اشتراک‌ها", labelDe: "Abos", icon: "M3 7h18v12H3V7Zm0 5h18M8 16h4" },
];

export function AdminNav({ locale }: { locale: Locale }) {
  const pathname = usePathname();
  const root = `/${locale}/admin`;

  return (
    <nav className="glass sticky top-28 h-fit rounded-3xl p-2.5">
      <ul className="flex gap-1.5 overflow-x-auto lg:flex-col lg:overflow-visible">
        {ITEMS.map((item) => {
          const href = `${root}${item.href}`;
          const active = item.href ? pathname.startsWith(href) : pathname === root;
          return (
            <li key={item.href}>
              <Link
                href={href}
                className={cn(
                  "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm whitespace-nowrap transition",
                  active
                    ? "bg-linear-to-r from-violet-500/20 to-cyan-400/10 text-mist-50"
                    : "text-mist-400 hover:bg-white/5 hover:text-mist-100",
                )}
              >
                <svg viewBox="0 0 24 24" className="size-4.5 shrink-0" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden>
                  <path d={item.icon} strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                {locale === "fa" ? item.label : item.labelDe}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
