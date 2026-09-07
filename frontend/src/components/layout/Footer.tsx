import Link from "next/link";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";

import { Logo } from "./Logo";
import { NewsletterForm } from "./NewsletterForm";

export function Footer({ locale, dict }: { locale: Locale; dict: Dictionary }) {
  const columns = [
    {
      title: dict.footer.learn,
      links: [
        { href: `/${locale}/courses`, label: dict.nav.courses },
        { href: `/${locale}/exams`, label: dict.nav.exams },
        { href: `/${locale}/podcasts`, label: dict.nav.podcasts },
        { href: `/${locale}/courses?level=A1`, label: `${dict.common.level} A1` },
        { href: `/${locale}/courses?level=B2`, label: `${dict.common.level} B2` },
      ],
    },
    {
      title: dict.footer.company,
      links: [
        { href: `/${locale}/about`, label: dict.footer.links.about },
        { href: `/${locale}/articles`, label: dict.nav.articles },
        { href: `/${locale}/contact`, label: dict.footer.links.contact },
      ],
    },
    {
      title: dict.footer.support,
      links: [
        { href: `/${locale}`, label: dict.footer.links.faq },
        { href: `/${locale}`, label: dict.footer.links.help },
        { href: `/${locale}`, label: dict.footer.links.terms },
        { href: `/${locale}`, label: dict.footer.links.privacy },
      ],
    },
  ];

  return (
    <footer className="relative mt-24 border-t border-white/8">
      <div className="container-page py-16">
        <div className="grid gap-12 lg:grid-cols-[1.4fr_2fr_1.4fr]">
          <div>
            <Logo locale={locale} label={dict.meta.siteName} />
            <p className="text-muted mt-5 max-w-xs text-sm leading-relaxed">{dict.footer.about}</p>
            <div className="mt-6 flex gap-2">
              {["A1", "A2", "B1", "B2", "C1"].map((level) => (
                <span
                  key={level}
                  className="tnum rounded-lg border border-white/10 px-2 py-1 text-[11px] font-semibold text-mist-400"
                >
                  {level}
                </span>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-8 sm:grid-cols-3">
            {columns.map((column) => (
              <div key={column.title}>
                <h3 className="mb-4 text-xs font-semibold tracking-[0.2em] text-mist-500 uppercase">
                  {column.title}
                </h3>
                <ul className="space-y-2.5">
                  {column.links.map((link, index) => (
                    <li key={`${link.href}-${index}`}>
                      <Link
                        href={link.href}
                        className="text-sm text-mist-400 transition hover:text-mist-50"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="glass rounded-3xl p-6">
            <h3 className="font-display text-lg font-semibold">{dict.footer.newsletter.title}</h3>
            <p className="text-muted mt-2 text-sm">{dict.footer.newsletter.body}</p>
            <NewsletterForm dict={dict} />
          </div>
        </div>

        <div className="mt-14 flex flex-col items-center justify-between gap-4 border-t border-white/8 pt-8 text-xs text-mist-600 sm:flex-row">
          <p>
            © {new Date().getFullYear()} {dict.meta.siteName}. {dict.footer.rights}
          </p>
          <p className="tracking-wide">{dict.meta.tagline}</p>
        </div>
      </div>
    </footer>
  );
}
