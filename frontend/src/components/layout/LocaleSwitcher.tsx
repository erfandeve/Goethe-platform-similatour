"use client";

import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";

import { locales, localeMeta, type Locale } from "@/i18n/config";
import { cn } from "@/lib/utils";

export function LocaleSwitcher({ locale }: { locale: Locale }) {
  const pathname = usePathname();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  function switchTo(next: Locale) {
    const rest = pathname.replace(new RegExp(`^/${locale}`), "") || "";
    // eslint-disable-next-line react-hooks/immutability -- remembers the choice for the proxy
    document.cookie = `NEXT_LOCALE=${next};path=/;max-age=31536000;samesite=lax`;
    setOpen(false);
    router.push(`/${next}${rest}`);
    router.refresh();
  }

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="glass flex h-10 items-center gap-2 rounded-full px-3.5 text-sm transition hover:border-white/20"
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <span aria-hidden>{localeMeta[locale].flag}</span>
        <span className="hidden font-medium sm:inline">{localeMeta[locale].native}</span>
        <svg viewBox="0 0 12 12" className={cn("size-3 transition-transform", open && "rotate-180")} aria-hidden>
          <path d="M2 4.5 6 8.5l4-4" stroke="currentColor" strokeWidth="1.5" fill="none" strokeLinecap="round" />
        </svg>
      </button>

      {open ? (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <ul
            role="listbox"
            className="glass-strong absolute end-0 z-50 mt-2 w-44 overflow-hidden rounded-2xl p-1.5 shadow-[var(--shadow-lift)]"
          >
            {locales.map((code) => (
              <li key={code}>
                <button
                  type="button"
                  onClick={() => switchTo(code)}
                  className={cn(
                    "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition",
                    code === locale ? "bg-violet-500/15 text-violet-400" : "hover:bg-white/6",
                  )}
                >
                  <span aria-hidden>{localeMeta[code].flag}</span>
                  <span className="font-medium">{localeMeta[code].native}</span>
                  <span className="ms-auto text-[10px] tracking-wider text-mist-600 uppercase">
                    {code}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </>
      ) : null}
    </div>
  );
}
