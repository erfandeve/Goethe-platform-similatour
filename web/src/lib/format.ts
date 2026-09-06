import type { Locale } from "@/i18n/config";

const numberLocale: Record<Locale, string> = { fa: "fa-IR", de: "de-DE", en: "en-US" };

export function formatNumber(value: number, locale: Locale) {
  return new Intl.NumberFormat(numberLocale[locale]).format(value);
}

/** Prices are stored in Rial; Persian shows Toman, the unit people actually use. */
export function formatPrice(rial: number, locale: Locale, freeLabel: string) {
  if (!rial) return freeLabel;
  if (locale === "fa") {
    return `${new Intl.NumberFormat("fa-IR").format(Math.round(rial / 10))} تومان`;
  }
  return `${new Intl.NumberFormat(numberLocale[locale]).format(rial)} IRR`;
}

export function formatDuration(minutes: number, locale: Locale, unit: { h: string; min: string }) {
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  const n = (value: number) => formatNumber(value, locale);
  if (hours && rest) return `${n(hours)} ${unit.h} ${n(rest)} ${unit.min}`;
  if (hours) return `${n(hours)} ${unit.h}`;
  return `${n(minutes)} ${unit.min}`;
}

export function formatClock(seconds: number) {
  const s = Math.max(0, Math.floor(seconds));
  const m = Math.floor(s / 60);
  const h = Math.floor(m / 60);
  const pad = (value: number) => value.toString().padStart(2, "0");
  return h ? `${h}:${pad(m % 60)}:${pad(s % 60)}` : `${m}:${pad(s % 60)}`;
}

export function formatDate(iso: string | null, locale: Locale) {
  if (!iso) return "—";
  const date = new Date(iso);
  return new Intl.DateTimeFormat(locale === "fa" ? "fa-IR" : numberLocale[locale], {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(date);
}

export function compact(value: number, locale: Locale) {
  return new Intl.NumberFormat(numberLocale[locale], {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

export function discountPercent(price: number, discounted: number) {
  if (!price || !discounted || discounted >= price) return 0;
  return Math.round(((price - discounted) / price) * 100);
}
