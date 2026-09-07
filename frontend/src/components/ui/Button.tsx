import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";

import { cn } from "@/lib/utils";

type Variant = "primary" | "ghost" | "outline" | "soft" | "danger";
type Size = "sm" | "md" | "lg";

const base =
  "relative inline-flex items-center justify-center gap-2 rounded-full font-medium transition-all duration-300 disabled:opacity-50 disabled:pointer-events-none whitespace-nowrap";

const variants: Record<Variant, string> = {
  primary:
    "bg-linear-to-r from-violet-500 to-cyan-400 text-ink-950 font-semibold shadow-[0_10px_40px_-12px_rgba(109,94,252,0.9)] hover:shadow-[0_16px_50px_-10px_rgba(109,94,252,1)] hover:-translate-y-0.5",
  soft: "glass text-mist-50 hover:border-white/20 hover:-translate-y-0.5",
  outline:
    "border border-white/15 text-mist-50 hover:bg-white/6 hover:border-white/30",
  ghost: "text-mist-400 hover:text-mist-50 hover:bg-white/5",
  danger: "bg-rose-400/15 text-rose-400 border border-rose-400/30 hover:bg-rose-400/25",
};

const sizes: Record<Size, string> = {
  sm: "h-9 px-4 text-sm",
  md: "h-11 px-6 text-sm",
  lg: "h-13 px-8 text-base",
};

interface Props {
  variant?: Variant;
  size?: Size;
  className?: string;
  children: ReactNode;
}

export function Button({
  variant = "primary",
  size = "md",
  className,
  children,
  ...props
}: Props & ComponentProps<"button">) {
  return (
    <button className={cn(base, variants[variant], sizes[size], className)} {...props}>
      {children}
    </button>
  );
}

export function ButtonLink({
  variant = "primary",
  size = "md",
  className,
  children,
  ...props
}: Props & ComponentProps<typeof Link>) {
  return (
    <Link className={cn(base, variants[variant], sizes[size], className)} {...props}>
      {children}
    </Link>
  );
}
