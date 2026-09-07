"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { cn } from "@/lib/utils";

const ITEMS = [
  { key: "overview", href: "", icon: "M4 12h6V4H4v8Zm10 8h6v-8h-6v8ZM4 20h6v-5H4v5Zm10-11h6V4h-6v5Z" },
  { key: "courses", href: "/courses", icon: "M4 5h9a3 3 0 0 1 3 3v11a3 3 0 0 0-3-3H4V5Zm16 0h-1a3 3 0 0 0-3 3v11a3 3 0 0 1 3-3h1V5Z" },
  { key: "exams", href: "/exams", icon: "M6 3h9l4 4v14H6V3Zm3 9h7M9 16h5" },
  { key: "wallet", href: "/wallet", icon: "M3 7h15a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Zm13 6h2" },
  { key: "orders", href: "/orders", icon: "M4 6h16v14H4V6Zm4-3v6m8-6v6M8 13h8" },
  { key: "notifications", href: "/notifications", icon: "M12 3a6 6 0 0 0-6 6v4l-2 3h16l-2-3V9a6 6 0 0 0-6-6Zm-2 16a2 2 0 0 0 4 0" },
  { key: "messages", href: "/messages", icon: "M4 5h16v11H9l-5 4V5Z" },
  { key: "profile", href: "/profile", icon: "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm-8 8a8 8 0 0 1 16 0" },
] as const;

export function DashboardNav({
  locale,
  dict,
  badges,
}: {
  locale: Locale;
  dict: Dictionary;
  badges: { notifications: number; messages: number };
}) {
  const pathname = usePathname();
  const root = `/${locale}/dashboard`;

  return (
    <nav className="glass sticky top-28 h-fit rounded-3xl p-2.5">
      <ul className="flex gap-1.5 overflow-x-auto lg:flex-col lg:overflow-visible">
        {ITEMS.map((item) => {
          const href = `${root}${item.href}`;
          const active = item.href ? pathname.startsWith(href) : pathname === root;
          const badge =
            item.key === "notifications"
              ? badges.notifications
              : item.key === "messages"
                ? badges.messages
                : 0;

          return (
            <li key={item.key}>
              <Link
                href={href}
                className={cn(
                  "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm whitespace-nowrap transition",
                  active
                    ? "bg-linear-to-r from-violet-500/20 to-cyan-400/10 text-mist-50"
                    : "text-mist-400 hover:bg-white/5 hover:text-mist-100",
                )}
              >
                <svg
                  viewBox="0 0 24 24"
                  className="size-4.5 shrink-0"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.6"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden
                >
                  <path d={item.icon} />
                </svg>
                <span className="flex-1">{dict.dashboard.nav[item.key]}</span>
                {badge > 0 ? (
                  <span className="tnum grid size-5 place-items-center rounded-full bg-violet-500 text-[10px] font-bold text-ink-950">
                    {badge}
                  </span>
                ) : null}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
