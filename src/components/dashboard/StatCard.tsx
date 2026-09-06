import { alpha } from "@/lib/utils";

export function StatCard({
  label,
  value,
  hint,
  accent = "#6d5efc",
}: {
  label: string;
  value: string;
  hint?: string;
  accent?: string;
}) {
  return (
    <div className="glass relative overflow-hidden rounded-2xl p-5">
      <span
        className="absolute -end-6 -top-6 size-20 rounded-full opacity-40 blur-2xl"
        style={{ background: alpha(accent, 0.6) }}
        aria-hidden
      />
      <p className="relative text-[10px] tracking-wider text-mist-600 uppercase">{label}</p>
      <p className="tnum font-display relative mt-2 text-2xl font-semibold">{value}</p>
      {hint ? <p className="relative mt-1 text-xs text-mist-500">{hint}</p> : null}
    </div>
  );
}
