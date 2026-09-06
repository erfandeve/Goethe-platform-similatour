import { cookies } from "next/headers";

import type { Locale } from "@/i18n/config";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8010/api";

type FetchOptions = RequestInit & {
  locale?: Locale;
  /** Seconds; 0 disables the cache for personalised data. */
  revalidate?: number;
  token?: string | null;
};

export class ApiError extends Error {
  status: number;
  code: string;
  fields: Record<string, string>;

  constructor(status: number, payload: { detail?: string; code?: string; fields?: Record<string, string> }) {
    super(payload?.detail ?? "Request failed");
    this.status = status;
    this.code = payload?.code ?? "error";
    this.fields = payload?.fields ?? {};
  }
}

export async function apiFetch<T>(path: string, options: FetchOptions = {}): Promise<T> {
  const { locale, revalidate = 60, token, headers, ...rest } = options;
  const url = new URL(`${API_BASE}${path}`);
  if (locale && !url.searchParams.has("locale")) url.searchParams.set("locale", locale);

  const response = await fetch(url.toString(), {
    ...rest,
    headers: {
      "Content-Type": "application/json",
      ...(locale ? { "X-Locale": locale } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    ...(revalidate === 0 ? { cache: "no-store" } : { next: { revalidate } }),
  });

  if (!response.ok) {
    let payload: Record<string, string> = {};
    try {
      payload = await response.json();
    } catch {
      payload = { detail: response.statusText };
    }
    throw new ApiError(response.status, payload);
  }
  return response.json() as Promise<T>;
}

/**
 * Server-side fetch that carries the signed-in student's token.
 *
 * A server component cannot write cookies, so when the access token has expired
 * it renews one in memory for this render. The refreshed pair is persisted the
 * next time the browser goes through the proxy route.
 */
export async function apiFetchAuthed<T>(path: string, options: FetchOptions = {}): Promise<T> {
  const store = await cookies();
  const token = store.get("goteh_access")?.value ?? null;

  try {
    return await apiFetch<T>(path, { ...options, token, revalidate: 0 });
  } catch (caught) {
    const refresh = store.get("goteh_refresh")?.value;
    if (!(caught instanceof ApiError) || caught.status !== 401 || !refresh) throw caught;

    const renewed = await fetch(`${API_BASE}/auth/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
      cache: "no-store",
    });
    if (!renewed.ok) throw caught;

    const { tokens } = (await renewed.json()) as { tokens?: { access: string } };
    if (!tokens?.access) throw caught;

    return apiFetch<T>(path, { ...options, token: tokens.access, revalidate: 0 });
  }
}

export async function getAccessToken() {
  const store = await cookies();
  return store.get("goteh_access")?.value ?? null;
}
