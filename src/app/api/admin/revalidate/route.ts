import { cookies } from "next/headers";
import { revalidatePath } from "next/cache";
import { NextResponse } from "next/server";

import { API_BASE } from "@/lib/api";

/**
 * Drops the page cache after a back-office edit, so a new cover or price shows
 * on the site immediately instead of at the end of the revalidate window.
 * Staff-only: the session is verified against the API, never assumed.
 */
export async function POST() {
  const store = await cookies();
  const token = store.get("goteh_access")?.value;
  if (!token) {
    return NextResponse.json({ detail: "Not signed in." }, { status: 401 });
  }

  const me = await fetch(`${API_BASE}/auth/me/`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  if (!me.ok) {
    return NextResponse.json({ detail: "Not signed in." }, { status: 401 });
  }

  const user = (await me.json()) as { is_staff?: boolean };
  if (!user.is_staff) {
    return NextResponse.json({ detail: "Staff access required." }, { status: 403 });
  }

  // The catalogue is small; refreshing the whole tree is simpler and safer than
  // trying to name every page a single edit could appear on.
  revalidatePath("/", "layout");
  return NextResponse.json({ ok: true });
}
