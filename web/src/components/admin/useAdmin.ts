"use client";

import { useCallback, useState } from "react";

import { callApi } from "@/lib/client";

/**
 * One place for the request + feedback loop every admin screen repeats:
 * disable while in flight, surface the server's message, confirm on success.
 */
export function useAdmin() {
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState<{ message: string; tone: "ok" | "error" }>({
    message: "",
    tone: "ok",
  });

  const notify = useCallback((message: string, tone: "ok" | "error" = "ok") => {
    setToast({ message, tone });
    setTimeout(() => setToast({ message: "", tone: "ok" }), 3200);
  }, []);

  const run = useCallback(
    async <T,>(
      request: () => Promise<T>,
      { success, failure }: { success?: string; failure?: string } = {},
    ): Promise<T | null> => {
      setBusy(true);
      try {
        const result = await request();
        // Clear the page cache so the change is visible on the site right away.
        void fetch("/api/admin/revalidate", { method: "POST" }).catch(() => {});
        if (success) notify(success, "ok");
        return result;
      } catch (caught) {
        const error = caught as { message?: string };
        notify(error.message || failure || "Request failed", "error");
        return null;
      } finally {
        setBusy(false);
      }
    },
    [notify],
  );

  return { busy, toast, notify, run, call: callApi };
}
