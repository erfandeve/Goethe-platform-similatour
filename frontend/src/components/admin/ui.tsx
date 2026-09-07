"use client";

import { useEffect, type ReactNode } from "react";

import { Input, Textarea } from "@/components/ui/Field";
import type { Translated } from "@/lib/admin";
import { cn } from "@/lib/utils";

/** One label, three languages — the shape the catalogue actually stores. */
export function TranslatedField({
  label,
  value,
  onChange,
  multiline = false,
  required = false,
}: {
  label: string;
  value: Translated;
  onChange: (next: Translated) => void;
  multiline?: boolean;
  required?: boolean;
}) {
  const Field = multiline ? Textarea : Input;
  const locales: { key: keyof Translated; flag: string; dir: "rtl" | "ltr" }[] = [
    { key: "fa", flag: "فا", dir: "rtl" },
    { key: "de", flag: "DE", dir: "ltr" },
    { key: "en", flag: "EN", dir: "ltr" },
  ];

  return (
    <div>
      <span className="mb-2 block text-xs font-medium tracking-wide text-mist-400">
        {label}
        {required ? <span className="ms-1 text-rose-400">*</span> : null}
      </span>
      <div className="space-y-2">
        {locales.map((locale) => (
          <div key={locale.key} className="flex items-start gap-2">
            <span className="mt-3 w-7 shrink-0 text-[10px] font-bold tracking-wider text-mist-600 uppercase">
              {locale.flag}
            </span>
            <Field
              value={value?.[locale.key] ?? ""}
              dir={locale.dir}
              onChange={(event: { target: { value: string } }) =>
                onChange({ ...value, [locale.key]: event.target.value })
              }
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export function Modal({
  open,
  title,
  onClose,
  children,
  wide = false,
}: {
  open: boolean;
  title: string;
  onClose: () => void;
  children: ReactNode;
  wide?: boolean;
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => event.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-100 grid place-items-center overflow-y-auto bg-ink-950/80 p-4 backdrop-blur-sm">
      <div
        className={cn(
          "glass-strong my-8 w-full rounded-3xl p-6 md:p-8",
          wide ? "max-w-3xl" : "max-w-xl",
        )}
      >
        <div className="mb-6 flex items-center justify-between gap-4">
          <h2 className="font-display text-lg font-semibold">{title}</h2>
          <button
            type="button"
            onClick={onClose}
            className="glass grid size-9 place-items-center rounded-full text-sm"
            aria-label="Close"
          >
            ✕
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}

export function Panel({
  title,
  description,
  action,
  children,
}: {
  title: string;
  /** One line under the heading, for panels whose rules are not obvious. */
  description?: string;
  action?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="glass rounded-3xl p-6">
      <header className="mb-5 flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="font-display text-lg font-semibold">{title}</h2>
          {description ? <p className="mt-1 text-xs text-mist-500">{description}</p> : null}
        </div>
        {action}
      </header>
      {children}
    </section>
  );
}

export function Toast({ message, tone }: { message: string; tone: "ok" | "error" }) {
  if (!message) return null;
  return (
    <div
      className={cn(
        "fixed bottom-6 start-1/2 z-100 -translate-x-1/2 rounded-2xl px-5 py-3 text-sm shadow-[var(--shadow-lift)] rtl:translate-x-1/2",
        tone === "ok"
          ? "border border-mint-400/30 bg-mint-400/15 text-mint-400"
          : "border border-rose-400/30 bg-rose-400/15 text-rose-300",
      )}
      role="status"
    >
      {message}
    </div>
  );
}
