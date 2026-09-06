"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input, Textarea } from "@/components/ui/Field";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatDate } from "@/lib/format";
import type { Message } from "@/lib/types";
import { cn } from "@/lib/utils";

export function MessageCenter({
  initial,
  locale,
  dict,
}: {
  initial: Message[];
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();
  const [items, setItems] = useState(initial);
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);

  async function open(message: Message) {
    if (message.is_read) return;
    setItems(items.map((item) => (item.id === message.id ? { ...item, is_read: true } : item)));
    await callApi(`auth/messages/${message.id}/read`, { method: "POST" }).catch(() => {});
    router.refresh();
  }

  async function send(event: React.FormEvent) {
    event.preventDefault();
    if (!body.trim()) return;
    setBusy(true);
    try {
      const created = await callApi<Message>("auth/messages/send", {
        method: "POST",
        body: { subject, body },
        locale,
      });
      setItems([created, ...items]);
      setSubject("");
      setBody("");
      setSent(true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid gap-8 lg:grid-cols-[1.5fr_1fr]">
      <div>
        {items.length ? (
          <ul className="space-y-3">
            {items.map((message) => (
              <li key={message.id}>
                <button
                  type="button"
                  onClick={() => open(message)}
                  className={cn(
                    "glass w-full rounded-2xl p-5 text-start transition hover:border-white/20",
                    !message.is_read && "border-white/16",
                  )}
                >
                  <div className="flex items-center gap-3">
                    <span
                      className={cn(
                        "grid size-9 shrink-0 place-items-center rounded-full text-xs font-bold",
                        message.sender_role === "teacher"
                          ? "bg-cyan-400/15 text-cyan-400"
                          : message.sender_role === "student"
                            ? "bg-white/10 text-mist-300"
                            : "bg-violet-500/15 text-violet-400",
                      )}
                    >
                      {message.sender_name.slice(0, 1)}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block text-sm font-semibold">{message.sender_name}</span>
                      <span className="block text-xs text-mist-600">
                        {formatDate(message.created_at, locale)}
                      </span>
                    </span>
                    {!message.is_read ? (
                      <span className="size-2 rounded-full bg-violet-400" aria-hidden />
                    ) : null}
                  </div>
                  {message.subject ? (
                    <p className="mt-3 text-sm font-medium text-mist-100">{message.subject}</p>
                  ) : null}
                  <p className="mt-1.5 text-xs leading-relaxed text-mist-400">{message.body}</p>
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <Empty title={dict.dashboard.messages.empty} icon="✉" />
        )}
      </div>

      <form onSubmit={send} className="glass h-fit space-y-4 rounded-3xl p-6 lg:sticky lg:top-28">
        <h2 className="font-display text-lg font-semibold">{dict.dashboard.messages.reply}</h2>
        <Field label={dict.dashboard.messages.subject}>
          <Input value={subject} onChange={(event) => setSubject(event.target.value)} />
        </Field>
        <Field label={dict.dashboard.messages.body}>
          <Textarea value={body} onChange={(event) => setBody(event.target.value)} required />
        </Field>
        <Button type="submit" className="w-full" disabled={busy}>
          {busy ? dict.common.loading : dict.dashboard.messages.send}
        </Button>
        {sent ? (
          <p className="text-center text-xs text-mint-400">{dict.dashboard.messages.sent}</p>
        ) : null}
      </form>
    </div>
  );
}
