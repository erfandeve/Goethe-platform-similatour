import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { API_BASE } from "@/lib/api";

/**
 * Audio upload passes through here rather than the JSON proxy: the recording is
 * multipart, and this keeps the access token in the httpOnly cookie where page
 * scripts cannot read it. The OpenAI key lives only on the Django side.
 */
export async function POST(request: Request) {
  const store = await cookies();
  const token = store.get("goteh_access")?.value;
  if (!token) {
    return NextResponse.json(
      { success: false, error: "Not signed in." },
      { status: 401 },
    );
  }

  const incoming = await request.formData();
  const forwarded = new FormData();
  for (const [key, value] of incoming.entries()) {
    forwarded.append(key, value);
  }

  const response = await fetch(`${API_BASE}/ai/transcribe/`, {
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

// Recordings are capped server-side; this only needs to outlast the upload.
export const maxDuration = 120;
