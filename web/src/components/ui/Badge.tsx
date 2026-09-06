import type { ReactNode } from "react";

import { alpha, cn, levelColor } from "@/lib/utils";

export function Badge({
  children,
  color,
  className,
}: {
  children: ReactNode;
  color?: string;
  className?: string;
}) {
  const tone = color ?? "#8b7dff";
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold tracking-wide uppercase",
        className,
      )}
      style={{
        color: tone,
        background: alpha(tone, 0.12),
        border: `1px solid ${alpha(tone, 0.3)}`,
      }}
    >
      {children}
    </span>
  );
}

export function LevelBadge({ level, className }: { level: string; className?: string }) {
  return (
    <Badge color={levelColor(level)} className={cn("tnum", className)}>
      {level}
    </Badge>
  );
}
