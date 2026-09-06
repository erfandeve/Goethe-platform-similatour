import type { NextResponse } from "next/server";

export interface Tokens {
  access: string;
  refresh: string;
  expires_in: number;
}

const secure = process.env.NODE_ENV === "production";

export function setSessionCookies(response: NextResponse, tokens: Tokens) {
  response.cookies.set("goteh_access", tokens.access, {
    httpOnly: true,
    sameSite: "lax",
    secure,
    path: "/",
    maxAge: tokens.expires_in,
  });
  response.cookies.set("goteh_refresh", tokens.refresh, {
    httpOnly: true,
    sameSite: "lax",
    secure,
    path: "/",
    maxAge: 60 * 60 * 24 * 14,
  });
}

export function clearSessionCookies(response: NextResponse) {
  response.cookies.delete("goteh_access");
  response.cookies.delete("goteh_refresh");
}
