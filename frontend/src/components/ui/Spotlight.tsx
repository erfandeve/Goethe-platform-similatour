"use client";

import type { MouseEvent, ReactNode } from "react";

import { alpha, cn } from "@/lib/utils";

/** Wraps a card so a soft light follows the pointer across its surface. */
export function Spotlight({
  children,
  accent = "#6d5efc",
  className,
}: {
  children: ReactNode;
  accent?: string;
  className?: string;
}) {
  function track(event: MouseEvent<HTMLDivElement>) {
    const rect = event.currentTarget.getBoundingClientRect();
    event.currentTarget.style.setProperty("--mx", `${event.clientX - rect.left}px`);
    event.currentTarget.style.setProperty("--my", `${event.clientY - rect.top}px`);
  }

  return (
    <div
      onMouseMove={track}
      style={{ ["--spot" as string]: alpha(accent, 0.22) }}
      className={cn("spotlight", className)}
    >
      {children}
    </div>
  );
}
