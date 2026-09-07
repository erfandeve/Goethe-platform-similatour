import "server-only";

import type { Locale } from "./config";
import type { Dictionary } from "./dictionaries/en";

const loaders = {
  fa: () => import("./dictionaries/fa").then((m) => m.default),
  de: () => import("./dictionaries/de").then((m) => m.default),
  en: () => import("./dictionaries/en").then((m) => m.default),
} satisfies Record<Locale, () => Promise<Dictionary>>;

export async function getDictionary(locale: Locale): Promise<Dictionary> {
  return loaders[locale]();
}

export type { Dictionary };
