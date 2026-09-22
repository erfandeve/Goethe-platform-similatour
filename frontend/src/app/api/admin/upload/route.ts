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

  const kind = new URL(request.url).searchParams.get("kind");
  const endpoint = kind === "image" ? "image" : kind === "audio" ? "audio" : "video";

  // Stream the upload straight through. Parsing it here would hold a whole
  // lesson video in memory — hundreds of MB on a server with 2 GB in total.
  const response = await fetch(`${API_BASE}/admin/upload/${endpoint}/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": request.headers.get("content-type") ?? "application/octet-stream",
      ...(request.headers.get("content-length")
        ? { "Content-Length": request.headers.get("content-length")! }
        : {}),
    },
    body: request.body,
    // Required by Node's fetch for a streamed request body.
    duplex: "half",
    cache: "no-store",
  } as RequestInit & { duplex: "half" });

  const text = await response.text();
  return new NextResponse(text, {
    status: response.status,
    headers: { "Content-Type": "application/json" },
  });
}

export const maxDuration = 300;
