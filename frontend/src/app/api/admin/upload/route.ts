import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { API_BASE } from "@/lib/api";

/**
 * Media uploads are multipart, which the JSON proxy cannot carry. The access
 * token stays in its httpOnly cookie; Django re-checks staff rights.
 *
 * `?kind=image` and `?kind=audio` route to their endpoints; anything else
 * uploads a lesson video. The kind decides the destination here, never the
 * client's own path.
 */
export async function POST(request: Request) {
  const store = await cookies();
  const token = store.get("goteh_access")?.value;
  if (!token) {
    return NextResponse.json({ detail: "Not signed in." }, { status: 401 });
  }

  const incoming = await request.formData();
  const forwarded = new FormData();
  for (const [key, value] of incoming.entries()) forwarded.append(key, value);

  const kind = new URL(request.url).searchParams.get("kind");
  const endpoint = kind === "image" ? "image" : kind === "audio" ? "audio" : "video";

  const response = await fetch(`${API_BASE}/admin/upload/${endpoint}/`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: forwarded,
    cache: "no-store",
  });

  const text = await response.text();
  return new NextResponse(text, {
    status: response.status,
    headers: { "Content-Type": "application/json" },
  });
}

export const maxDuration = 300;
