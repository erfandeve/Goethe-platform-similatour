import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export function Section({
  children,
  className,
  id,
}: {
  children: ReactNode;
  className?: string;
  id?: string;
}) {
  return (
    <section id={id} className={cn("container-page py-20 md:py-28", className)}>
      {children}
    </section>
  );
}

export function SectionHeading({
  eyebrow,
  title,
  subtitle,
  action,
  align = "start",
  as: Heading = "h2",
}: {
  eyebrow?: string;
  title: string;
  subtitle?: string;
  action?: ReactNode;
  align?: "start" | "center";
  /** A page whose heading IS the page title passes "h1". */
  as?: "h1" | "h2";
}) {
  return (
    <div
      className={cn(
        "mb-12 flex flex-col gap-5 md:flex-row md:items-end md:justify-between",
        align === "center" && "md:flex-col md:items-center md:text-center",
      )}
    >
      <div className={cn("max-w-2xl", align === "center" && "mx-auto text-center")}>
        {eyebrow ? (
          <p className="mb-3 text-xs font-semibold tracking-[0.25em] text-violet-400 uppercase">
            {eyebrow}
          </p>
        ) : null}
        <Heading className="font-display text-3xl leading-tight font-semibold text-balance md:text-5xl">
          {title}
        </Heading>
        {subtitle ? <p className="text-muted mt-4 text-base md:text-lg">{subtitle}</p> : null}
      </div>
      {action ? <div className="shrink-0">{action}</div> : null}
    </div>
  );
}
