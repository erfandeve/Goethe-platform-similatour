import Link from "next/link";
import type { ReactNode } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";

export function AuthShell({
  locale,
  dict,
  title,
  subtitle,
  children,
}: {
  locale: Locale;
  dict: Dictionary;
  title: string;
  subtitle: string;
  children: ReactNode;
}) {
  return (
    <div className="container-page grid min-h-[80vh] items-center gap-14 py-12 lg:grid-cols-2">
      <div className="hidden lg:block">
        <Link
          href={`/${locale}`}
          className="text-xs font-semibold tracking-[0.25em] text-violet-400 uppercase"
        >
          {dict.meta.siteName}
        </Link>
        <h2 className="font-display mt-6 text-4xl leading-tight font-semibold text-balance">
          {dict.hero.titleTop}
          <span className="text-gradient block">{dict.hero.titleAccent}</span>
        </h2>
        <ul className="mt-10 space-y-4">
          {dict.auth.benefits.map((benefit) => (
            <li key={benefit} className="flex items-start gap-3">
              <span className="mt-0.5 grid size-6 shrink-0 place-items-center rounded-lg bg-mint-400/15 text-xs text-mint-400">
                ✓
              </span>
              <span className="text-sm text-mist-300">{benefit}</span>
            </li>
          ))}
        </ul>
        <div className="glass mt-12 rounded-3xl p-6">
          <p className="text-xs tracking-wider text-mist-600 uppercase">Demo</p>
          <p className="tnum mt-2 text-sm text-mist-300" dir="ltr">
            student@goteh.de · goteh1234
          </p>
        </div>
      </div>

      <div className="glass mx-auto w-full max-w-md rounded-3xl p-8 md:p-10">
        <h1 className="font-display text-3xl font-semibold">{title}</h1>
        <p className="text-muted mt-2 text-sm">{subtitle}</p>
        <div className="mt-8">{children}</div>
      </div>
    </div>
  );
}
