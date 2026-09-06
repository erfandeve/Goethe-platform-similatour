import { NextResponse } from "next/server";

import { API_BASE } from "@/lib/api";
import { setSessionCookies } from "@/lib/session";

export async function POST(request: Request) {
  const body = await request.json();
  const response = await fetch(`${API_BASE}/auth/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });

  const payload = await response.json();
  if (!response.ok) {
    return NextResponse.json(payload, { status: response.status });
  }

  const result = NextResponse.json({ user: payload.user }, { status: 201 });
  setSessionCookies(result, payload.tokens);
  return result;
}
