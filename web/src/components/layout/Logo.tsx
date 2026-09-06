import Link from "next/link";

import type { Locale } from "@/i18n/config";

export function Logo({ locale, label }: { locale: Locale; label: string }) {
  return (
    <Link href={`/${locale}`} className="group flex items-center gap-3" aria-label={label}>
      <span className="relative grid size-10 place-items-center">
        <span className="absolute inset-0 rounded-xl bg-linear-to-br from-violet-500 to-cyan-400 opacity-90 transition-transform duration-500 group-hover:rotate-12" />
        <span className="absolute inset-[1.5px] rounded-[10px] bg-ink-950/85" />
        <svg viewBox="0 0 24 24" className="relative size-5" fill="none" aria-hidden>
          <path
            d="M18.5 7.2A7 7 0 1 0 19 12h-6"
            stroke="url(#g)"
            strokeWidth="2.1"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <defs>
            <linearGradient id="g" x1="4" y1="4" x2="20" y2="20">
              <stop stopColor="#8b7dff" />
              <stop offset="1" stopColor="#22d3ee" />
            </linearGradient>
          </defs>
        </svg>
      </span>
      <span className="flex flex-col leading-none">
        <span className="font-display text-lg font-semibold tracking-tight">{label}</span>
        <span className="text-[10px] tracking-[0.3em] text-mist-500 uppercase">Deutsch</span>
      </span>
    </Link>
  );
}
