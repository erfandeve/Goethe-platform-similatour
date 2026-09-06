"use client";

/** Thin wrapper around the same-origin proxy that carries the session cookie. */
export async function callApi<T>(
  path: string,
  options: { method?: string; body?: unknown; locale?: string } = {},
): Promise<T> {
  const { method = "GET", body, locale } = options;
  const url = new URL(`/api/proxy/${path.replace(/^\/+|\/+$/g, "")}`, window.location.origin);
  if (locale) url.searchParams.set("locale", locale);

  const response = await fetch(url.toString(), {
    method,
    headers: { "Content-Type": "application/json" },
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw Object.assign(new Error(payload.detail ?? "Request failed"), {
      status: response.status,
      code: payload.code,
      fields: payload.fields ?? {},
    });
  }
  return payload as T;
}

export async function login(email: string, password: string) {
  const response = await fetch("/api/session/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const payload = await response.json();
  if (!response.ok) throw Object.assign(new Error(payload.detail ?? "Login failed"), payload);
  return payload.user;
}

export async function register(data: Record<string, string>) {
  const response = await fetch("/api/session/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const payload = await response.json();
  if (!response.ok) throw Object.assign(new Error(payload.detail ?? "Sign up failed"), payload);
  return payload.user;
}

export async function logout() {
  await fetch("/api/session/logout", { method: "POST" });
}
