import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { API_BASE } from "@/lib/api";
import { setSessionCookies, type Tokens } from "@/lib/session";

/**
 * Browser-side calls go through here so the access token can stay in an
 * httpOnly cookie instead of being readable by scripts on the page.
 *
 * The proxy also renews an expired access token on the fly: exam modules run
 * longer than a token lives, and a student must not be thrown out mid-exam.
 */
async function callApi(path: string[], search: URLSearchParams, method: string, body: string | null, token?: string) {
  const target = new URL(`${API_BASE}/${path.join("/")}/`);
  search.forEach((value, key) => target.searchParams.set(key, value));

  const init: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    cache: "no-store",
  };
  if (body !== null) init.body = body;

  return fetch(target.toString(), init);
}

async function refreshAccess(refreshToken: string) {
  const response = await fetch(`${API_BASE}/auth/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refreshToken }),
    cache: "no-store",
  });
  if (!response.ok) return null;
  const payload = (await response.json()) as { tokens: Tokens };
  return payload.tokens ?? null;
}

async function forward(request: Request, path: string[]) {
  const store = await cookies();
  const access = store.get("goteh_access")?.value;
  const refresh = store.get("goteh_refresh")?.value;

  const search = new URL(request.url).searchParams;
  const method = request.method;
  const body = ["GET", "HEAD"].includes(method) ? null : await request.text();

  let upstream = await callApi(path, search, method, body, access);
  let renewed: Tokens | null = null;

  if (upstream.status === 401 && refresh) {
    renewed = await refreshAccess(refresh);
    if (renewed) {
      upstream = await callApi(path, search, method, body, renewed.access);
    }
  }

  const text = await upstream.text();
  // 204/304 carry no body, and constructing a Response with one throws.
  const empty = upstream.status === 204 || upstream.status === 304;
  const response = new NextResponse(empty ? null : text, {
    status: upstream.status,
    ...(empty ? {} : { headers: { "Content-Type": "application/json" } }),
  });
  if (renewed) setSessionCookies(response, renewed);
  return response;
}

type Context = { params: Promise<{ path: string[] }> };

export async function GET(request: Request, { params }: Context) {
  return forward(request, (await params).path);
}
export async function POST(request: Request, { params }: Context) {
  return forward(request, (await params).path);
}
export async function PUT(request: Request, { params }: Context) {
  return forward(request, (await params).path);
}
export async function PATCH(request: Request, { params }: Context) {
  return forward(request, (await params).path);
}
export async function DELETE(request: Request, { params }: Context) {
  return forward(request, (await params).path);
}
