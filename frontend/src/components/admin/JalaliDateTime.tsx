"use client";

import { JALALI_MONTHS, jalaliMonthLength, toGregorian, toJalali } from "@/lib/jalali";

const select =
  "rounded-xl border border-white/10 bg-white/4 px-2 py-2.5 text-sm text-mist-50 outline-none transition focus:border-violet-400/60 [&>option]:bg-ink-900";

const fa = (n: number) => new Intl.NumberFormat("fa-IR", { useGrouping: false }).format(n);

/**
 * A Solar Hijri date and time, in the admin's local time. The value in and
 * out is an ISO string (or "" for none), so nothing else has to know about
 * the calendar.
 */
export function JalaliDateTime({
  value,
  onChange,
  emptyLabel,
  defaultTime = "23:59",
}: {
  value: string;
  onChange: (iso: string) => void;
  /** Shown when there is no date, as the button that sets one. */
  emptyLabel: string;
  defaultTime?: string;
}) {
  if (!value) {
    return (
      <button
        type="button"
        onClick={() => {
          const now = new Date();
          const [h, m] = defaultTime.split(":").map(Number);
          now.setHours(h, m, 0, 0);
          onChange(now.toISOString());
        }}
        className="w-full rounded-2xl border border-dashed border-white/15 px-4 py-3 text-sm text-mist-400 transition hover:border-white/30 hover:text-mist-100"
      >
        {emptyLabel}
      </button>
    );
  }

  const date = new Date(value);
  const { jy, jm, jd } = toJalali(date.getFullYear(), date.getMonth() + 1, date.getDate());
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const thisYear = toJalali(new Date().getFullYear(), new Date().getMonth() + 1, new Date().getDate()).jy;
  const years = Array.from({ length: 7 }, (_, i) => thisYear - 1 + i);
  if (!years.includes(jy)) years.unshift(jy);
  // Five-minute steps, plus whatever odd minute a saved value already has.
  const minuteOptions = Array.from(new Set([...Array.from({ length: 12 }, (_, i) => i * 5), 59, minutes])).sort(
    (x, y) => x - y,
  );

  function set(next: { y?: number; m?: number; d?: number; h?: number; min?: number }) {
    const y = next.y ?? jy;
    const m = next.m ?? jm;
    // Moving from the 31st into a 30-day month lands on the last day, not the next month.
    const d = Math.min(next.d ?? jd, jalaliMonthLength(y, m));
    const g = toGregorian(y, m, d);
    onChange(new Date(g.gy, g.gm - 1, g.gd, next.h ?? hours, next.min ?? minutes).toISOString());
  }

  return (
    <div className="flex flex-wrap items-center gap-2" dir="rtl">
      <select aria-label="روز" className={select} value={jd} onChange={(e) => set({ d: Number(e.target.value) })}>
        {Array.from({ length: jalaliMonthLength(jy, jm) }, (_, i) => i + 1).map((d) => (
          <option key={d} value={d}>
            {fa(d)}
          </option>
        ))}
      </select>
      <select aria-label="ماه" className={select} value={jm} onChange={(e) => set({ m: Number(e.target.value) })}>
        {JALALI_MONTHS.map((name, i) => (
          <option key={name} value={i + 1}>
            {name}
          </option>
        ))}
      </select>
      <select aria-label="سال" className={select} value={jy} onChange={(e) => set({ y: Number(e.target.value) })}>
        {years.map((y) => (
          <option key={y} value={y}>
            {fa(y)}
          </option>
        ))}
      </select>
      <span className="text-xs text-mist-500">ساعت</span>
      <select aria-label="دقیقه" className={select} value={minutes} onChange={(e) => set({ min: Number(e.target.value) })}>
        {minuteOptions.map((m) => (
          <option key={m} value={m}>
            {fa(m).padStart(2, "۰")}
          </option>
        ))}
      </select>
      <span className="text-mist-500">:</span>
      <select aria-label="ساعت" className={select} value={hours} onChange={(e) => set({ h: Number(e.target.value) })}>
        {Array.from({ length: 24 }, (_, h) => h).map((h) => (
          <option key={h} value={h}>
            {fa(h).padStart(2, "۰")}
          </option>
        ))}
      </select>
      <button
        type="button"
        onClick={() => onChange("")}
        aria-label="حذف تاریخ"
        className="rounded-full px-2 py-1 text-xs text-mist-500 transition hover:bg-white/5 hover:text-rose-300"
      >
        ✕
      </button>
    </div>
  );
}
