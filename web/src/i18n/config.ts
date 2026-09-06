export const locales = ["fa", "de", "en"] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = "fa";

export const localeMeta: Record<
  Locale,
  { label: string; native: string; dir: "rtl" | "ltr"; htmlLang: string; flag: string }
> = {
  fa: { label: "Persian", native: "فارسی", dir: "rtl", htmlLang: "fa-IR", flag: "🇮🇷" },
  de: { label: "German", native: "Deutsch", dir: "ltr", htmlLang: "de-DE", flag: "🇩🇪" },
  en: { label: "English", native: "English", dir: "ltr", htmlLang: "en-US", flag: "🇬🇧" },
};

export function isLocale(value: string | undefined): value is Locale {
  return !!value && (locales as readonly string[]).includes(value);
}
