"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatDate } from "@/lib/format";
import type { Notification } from "@/lib/types";
import { cn } from "@/lib/utils";

const KIND_TONE: Record<string, string> = {
  system: "#8b7dff",
  course: "#22d3ee",
  exam: "#ff6b6b",
  payment: "#34d399",
  podcast: "#f59e0b",
};

export function NotificationList({
  initial,
  locale,
  dict,
}: {
  initial: Notification[];
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();
  const [items, setItems] = useState(initial);

  async function markAll() {
    setItems(items.map((item) => ({ ...item, is_read: true })));
    await callApi("auth/notifications/read-all", { method: "POST" }).catch(() => {});
    router.refresh();
  }

  async function markOne(id: string) {
    setItems(items.map((item) => (item.id === id ? { ...item, is_read: true } : item)));
    await callApi(`auth/notifications/${id}/read`, { method: "POST" }).catch(() => {});
    router.refresh();
  }

  if (!items.length) return <Empty title={dict.dashboard.notifications.empty} icon="✓" />;

  const unread = items.filter((item) => !item.is_read).length;

  return (
    <div>
      {unread ? (
        <div className="mb-5 flex items-center justify-between">
          <span className="tnum text-xs text-mist-500">
            {unread} {dict.dashboard.notifications.unread}
          </span>
          <Button variant="ghost" size="sm" onClick={markAll}>
            {dict.dashboard.notifications.markAll}
          </Button>
        </div>
      ) : null}

      <ul className="space-y-3">
        {items.map((item) => {
          const tone = KIND_TONE[item.kind] ?? "#8b7dff";
          const content = (
            <>
              <span
                className="mt-1.5 size-2 shrink-0 rounded-full"
                style={{ background: item.is_read ? "transparent" : tone }}
                aria-hidden
              />
              <span className="min-w-0 flex-1">
                <span className="block text-sm font-semibold">{item.title}</span>
                <span className="mt-1 block text-xs leading-relaxed text-mist-400">
                  {item.body}
                </span>
                <span className="mt-2 block text-[11px] text-mist-600">
                  {formatDate(item.created_at, locale)}
                </span>
              </span>
            </>
          );

          return (
            <li key={item.id}>
              {item.link ? (
                <Link
                  href={`/${locale}${item.link}`}
                  onClick={() => markOne(item.id)}
                  className={cn(
                    "glass flex gap-3 rounded-2xl p-5 transition hover:border-white/20",
                    !item.is_read && "border-white/16",
                  )}
                >
                  {content}
                </Link>
              ) : (
                <button
                  type="button"
                  onClick={() => markOne(item.id)}
                  className="glass flex w-full gap-3 rounded-2xl p-5 text-start"
                >
                  {content}
                </button>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
