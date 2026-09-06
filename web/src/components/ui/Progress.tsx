import { cn } from "@/lib/utils";

export function Progress({
  value,
  color = "#6d5efc",
  className,
  showLabel = false,
}: {
  value: number;
  color?: string;
  className?: string;
  showLabel?: boolean;
}) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/8">
        <div
          className="h-full rounded-full transition-[width] duration-700"
          style={{
            width: `${clamped}%`,
            background: `linear-gradient(90deg, ${color}, #22d3ee)`,
            boxShadow: `0 0 16px ${color}66`,
          }}
        />
      </div>
      {showLabel ? (
        <span className="tnum text-xs font-semibold text-mist-200">{clamped}%</span>
      ) : null}
    </div>
  );
}
