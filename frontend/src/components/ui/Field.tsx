"use client";

import type { ComponentProps, ReactNode } from "react";

import { cn } from "@/lib/utils";

const control =
  "w-full rounded-2xl bg-white/4 border border-white/10 px-4 py-3 text-sm text-mist-50 placeholder:text-mist-600 transition focus:border-violet-400/60 focus:bg-white/6 outline-none";

export function Field({
  label,
  error,
  hint,
  children,
}: {
  label: string;
  error?: string;
  hint?: string;
  children: ReactNode;
}) {
  return (
    <label className="block">
      <span className="mb-2 block text-xs font-medium tracking-wide text-mist-400">{label}</span>
      {children}
      {error ? (
        <span className="mt-1.5 block text-xs text-rose-400">{error}</span>
      ) : hint ? (
        <span className="mt-1.5 block text-xs text-mist-600">{hint}</span>
      ) : null}
    </label>
  );
}

export function Input({ className, ...props }: ComponentProps<"input">) {
  return <input className={cn(control, className)} {...props} />;
}

export function Textarea({ className, ...props }: ComponentProps<"textarea">) {
  return <textarea className={cn(control, "min-h-28 resize-y", className)} {...props} />;
}

export function Select({ className, children, ...props }: ComponentProps<"select">) {
  return (
    <select className={cn(control, "appearance-none pe-10", className)} {...props}>
      {children}
    </select>
  );
}

export function Toggle({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: (value: boolean) => void;
  label: string;
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className="flex w-full items-center justify-between gap-4 rounded-2xl border border-white/8 bg-white/3 px-4 py-3 text-start text-sm transition hover:border-white/15"
    >
      <span className="text-mist-200">{label}</span>
      <span
        className={cn(
          "relative h-6 w-11 shrink-0 rounded-full transition-colors",
          checked ? "bg-violet-500" : "bg-white/12",
        )}
      >
        <span
          className={cn(
            "absolute top-1 size-4 rounded-full bg-white transition-all",
            checked ? "start-6" : "start-1",
          )}
        />
      </span>
    </button>
  );
}
