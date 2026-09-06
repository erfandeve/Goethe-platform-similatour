import clsx, { type ClassValue } from "clsx";

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export const LEVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"] as const;

export const LEVEL_COLORS: Record<string, string> = {
  A1: "#34d399",
  A2: "#22d3ee",
  B1: "#f59e0b",
  B2: "#ff6b6b",
  C1: "#e879f9",
  C2: "#a78bfa",
};

export function levelColor(level: string) {
  return LEVEL_COLORS[level] ?? "#6d5efc";
}

/** Turn a hex accent into an rgba string for glows and gradients. */
export function alpha(hex: string, amount: number) {
  const clean = hex.replace("#", "");
  const value = clean.length === 3 ? clean.split("").map((c) => c + c).join("") : clean;
  const r = parseInt(value.slice(0, 2), 16);
  const g = parseInt(value.slice(2, 4), 16);
  const b = parseInt(value.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${amount})`;
}

/**
 * Resolve a stored media path.
 *
 * The database keeps paths, not URLs, so the host is decided at runtime:
 * NEXT_PUBLIC_MEDIA_URL when the files are served next to the app (the
 * deployed setup, where `public/media` ships with the build), otherwise the API
 * host, which is what serves them in local development.
 */
export function mediaUrl(path: string) {
  if (!path) return "";
  if (/^https?:\/\//.test(path)) return path;

  const clean = path.startsWith("/") ? path : `/${path}`;
  const configured = process.env.NEXT_PUBLIC_MEDIA_URL;
  if (configured !== undefined) {
    // An empty value means "same origin" — the static files in public/.
    return `${configured.replace(/\/$/, "")}${clean}`;
  }

  const base = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8010/api").replace(
    /\/api\/?$/,
    "",
  );
  return `${base}${clean}`;
}
