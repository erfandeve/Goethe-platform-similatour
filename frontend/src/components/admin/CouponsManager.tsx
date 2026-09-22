"use client";

import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input, Select, Textarea } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminCoupon, CouponRedemption } from "@/lib/admin";
import { COUPON_STATUS_LABELS, COUPON_TARGET_LABELS } from "@/lib/admin";
import { formatDate, formatNumber, formatPrice } from "@/lib/format";
import { cn } from "@/lib/utils";

import { JalaliDateTime } from "./JalaliDateTime";
import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast } from "./ui";

/** Amounts are typed in Toman — the unit people think in — and stored in Rial. */
interface Draft {
  id?: string;
  code: string;
  kind: "percent" | "amount";
  value: string;
  max_discount_toman: string;
  min_total_toman: string;
  applies_to: string[];
  starts_at: string;
  expires_at: string;
  max_uses: string;
  per_user_limit: string;
  is_active: boolean;
  note: string;
}

const STATUS_TONE: Record<AdminCoupon["status"], string> = {
  active: "bg-mint-400/15 text-mint-400",
  scheduled: "bg-cyan-400/15 text-cyan-300",
  inactive: "bg-white/8 text-mist-500",
  expired: "bg-rose-400/12 text-rose-300",
  used_up: "bg-amber-400/12 text-amber-300",
};

/** End of the day, N days from now, as ISO. Dates are kept as ISO strings throughout. */
function daysFromNow(days: number) {
  const date = new Date();
  date.setDate(date.getDate() + days);
  date.setHours(23, 59, 0, 0);
  return date.toISOString();
}

const blank = (): Draft => ({
  code: "",
  kind: "percent",
  value: "10",
  max_discount_toman: "",
  min_total_toman: "",
  applies_to: [],
  starts_at: "",
  expires_at: daysFromNow(30),
  max_uses: "100",
  per_user_limit: "1",
  is_active: true,
  note: "",
});

const toDraft = (row: AdminCoupon): Draft => ({
  id: row.id,
  code: row.code,
  kind: row.kind,
  value: row.kind === "amount" ? String(row.value / 10) : String(row.value),
  max_discount_toman: row.max_discount ? String(row.max_discount / 10) : "",
  min_total_toman: row.min_total ? String(row.min_total / 10) : "",
  applies_to: row.applies_to,
  starts_at: row.starts_at ?? "",
  expires_at: row.expires_at ?? "",
  max_uses: String(row.max_uses),
  per_user_limit: String(row.per_user_limit),
  is_active: row.is_active,
  note: row.note,
});

const rial = (toman: string) => Math.round((Number(toman) || 0) * 10);

export function CouponsManager({
  initial,
  targets,
  locale,
}: {
  initial: AdminCoupon[];
  targets: string[];
  locale: Locale;
}) {
  const { busy, toast, run, call, notify } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [usage, setUsage] = useState<{ coupon: AdminCoupon; rows: CouponRedemption[] } | null>(null);

  const n = (value: number) => formatNumber(value, locale);

  function describe(row: AdminCoupon) {
    const off =
      row.kind === "percent"
        ? `${n(row.value)}٪ تخفیف${row.max_discount ? ` (حداکثر ${formatPrice(row.max_discount, locale, "—")})` : ""}`
        : `${formatPrice(row.value, locale, "—")} تخفیف`;
    const scope = row.applies_to.length
      ? row.applies_to.map((t) => COUPON_TARGET_LABELS[t] ?? t).join("، ")
      : "همه محصولات";
    return `${off} · ${scope}`;
  }

  async function save() {
    if (!draft) return;
    const value = draft.kind === "amount" ? rial(draft.value) : Number(draft.value) || 0;
    const body = {
      code: draft.code.trim(),
      kind: draft.kind,
      value,
      max_discount: draft.kind === "percent" ? rial(draft.max_discount_toman) : 0,
      min_total: rial(draft.min_total_toman),
      applies_to: draft.applies_to,
      starts_at: draft.starts_at || null,
      expires_at: draft.expires_at || null,
      max_uses: Number(draft.max_uses) || 0,
      per_user_limit: Number(draft.per_user_limit) || 0,
      is_active: draft.is_active,
      note: draft.note,
    };

    const saved = draft.id
      ? await run(() => call<AdminCoupon>(`admin/coupons/${draft.id}`, { method: "PATCH", body }), {
          success: "کد تخفیف ذخیره شد",
        })
      : await run(() => call<AdminCoupon>("admin/coupons", { method: "POST", body }), {
          success: "کد تخفیف ساخته شد",
        });
    if (!saved) return;
    setRows((current) =>
      draft.id ? current.map((row) => (row.id === saved.id ? saved : row)) : [saved, ...current],
    );
    setDraft(null);
  }

  async function toggle(row: AdminCoupon) {
    const saved = await run(
      () => call<AdminCoupon>(`admin/coupons/${row.id}`, { method: "PATCH", body: { is_active: !row.is_active } }),
      { success: row.is_active ? "غیرفعال شد" : "فعال شد" },
    );
    if (saved) setRows((current) => current.map((item) => (item.id === saved.id ? saved : item)));
  }

  async function remove(row: AdminCoupon) {
    if (!confirm(`کد «${row.code}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/coupons/${row.id}`, { method: "DELETE" }), {
      success: "حذف شد",
    });
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  async function showUsage(row: AdminCoupon) {
    const detail = await run(() =>
      call<AdminCoupon & { redemptions: CouponRedemption[] }>(`admin/coupons/${row.id}`),
    );
    if (detail) setUsage({ coupon: detail, rows: detail.redemptions });
  }

  async function copy(code: string) {
    try {
      await navigator.clipboard.writeText(code);
      notify("کد کپی شد");
    } catch {
      notify(code);
    }
  }

  return (
    <>
      <Panel
        title="کدهای تخفیف"
        description="هر کد را به هر کسی بدهی، موقع خرید در سبد خرید واردش می‌کند. تاریخ انقضا، تعداد کل استفاده و سهم هر نفر را خودت تعیین می‌کنی."
        action={<Button onClick={() => setDraft(blank())}>+ کد تخفیف جدید</Button>}
      >
        {rows.length ? (
          <ul className="space-y-2">
            {rows.map((row) => (
              <li
                key={row.id}
                className="flex flex-wrap items-center gap-x-4 gap-y-2 rounded-2xl border border-white/8 px-4 py-3"
              >
                <button
                  type="button"
                  onClick={() => copy(row.code)}
                  title="کپی کد"
                  dir="ltr"
                  className="tnum rounded-xl border border-dashed border-violet-400/40 bg-violet-500/10 px-3 py-2 font-mono text-sm font-bold tracking-wider text-violet-200 transition hover:bg-violet-500/20"
                >
                  {row.code}
                </button>

                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-semibold">{describe(row)}</span>
                  <span className="block truncate text-xs text-mist-500">
                    {row.expires_at ? `تا ${formatDate(row.expires_at, locale)}` : "بدون تاریخ انقضا"}
                    {row.note ? ` · ${row.note}` : ""}
                  </span>
                </span>

                <button
                  type="button"
                  onClick={() => showUsage(row)}
                  className="tnum text-xs text-mist-400 underline-offset-4 hover:text-mist-100 hover:underline"
                >
                  {n(row.used_count)} / {row.max_uses ? n(row.max_uses) : "∞"} استفاده
                </button>

                <span className={cn("rounded-full px-3 py-1.5 text-[11px] font-semibold", STATUS_TONE[row.status])}>
                  {COUPON_STATUS_LABELS[row.status]}
                </span>

                <span className="flex items-center gap-1">
                  <button type="button" onClick={() => setDraft(toDraft(row))} className="glass rounded-full px-4 py-1.5 text-xs">
                    ویرایش
                  </button>
                  <button
                    type="button"
                    onClick={() => toggle(row)}
                    disabled={busy}
                    className="rounded-full px-3 py-1.5 text-xs text-mist-400 transition hover:bg-white/5"
                  >
                    {row.is_active ? "غیرفعال کن" : "فعال کن"}
                  </button>
                  {row.used_count ? null : (
                    <button
                      type="button"
                      onClick={() => remove(row)}
                      className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                    >
                      حذف
                    </button>
                  )}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <Empty title="هنوز کد تخفیفی نساخته‌ای" body="با دکمه بالا اولین کد را بساز." icon="%" />
        )}
      </Panel>

      <Modal open={!!draft} wide title={draft?.id ? "ویرایش کد تخفیف" : "کد تخفیف جدید"} onClose={() => setDraft(null)}>
        {draft ? (
          <div className="space-y-5">
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="کد" hint="خالی بگذاری، یک کد تصادفی ساخته می‌شود. فقط حروف انگلیسی و عدد.">
                <Input
                  dir="ltr"
                  className="font-mono tracking-wider uppercase"
                  value={draft.code}
                  maxLength={32}
                  placeholder="SUMMER30"
                  onChange={(e) => setDraft({ ...draft, code: e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, "") })}
                />
              </Field>
              <Field label="نوع تخفیف">
                <Select
                  value={draft.kind}
                  onChange={(e) => setDraft({ ...draft, kind: e.target.value as Draft["kind"], value: "" })}
                >
                  <option value="percent">درصدی</option>
                  <option value="amount">مبلغ ثابت</option>
                </Select>
              </Field>
              <Field label={draft.kind === "percent" ? "درصد تخفیف (۱ تا ۱۰۰)" : "مبلغ تخفیف (تومان)"}>
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  min={1}
                  max={draft.kind === "percent" ? 100 : undefined}
                  value={draft.value}
                  onChange={(e) => setDraft({ ...draft, value: e.target.value })}
                />
              </Field>
              {draft.kind === "percent" ? (
                <Field label="سقف تخفیف (تومان)" hint="اختیاری — خالی یعنی بدون سقف">
                  <Input
                    type="number"
                    dir="ltr"
                    className="tnum"
                    min={0}
                    value={draft.max_discount_toman}
                    onChange={(e) => setDraft({ ...draft, max_discount_toman: e.target.value })}
                  />
                </Field>
              ) : (
                <div />
              )}
            </div>

            <div className="rounded-2xl border border-white/10 p-4">
              <p className="mb-3 text-sm font-medium">مدت اعتبار</p>
              <div className="space-y-4">
                <Field label="از" hint="خالی = از همین الان">
                  <JalaliDateTime
                    value={draft.starts_at}
                    defaultTime="00:00"
                    emptyLabel="از همین الان — برای تعیین تاریخ شروع بزن"
                    onChange={(starts_at) => setDraft({ ...draft, starts_at })}
                  />
                </Field>
                <Field label="تا" hint="خالی = بدون انقضا">
                  <JalaliDateTime
                    value={draft.expires_at}
                    emptyLabel="بدون انقضا — برای تعیین تاریخ پایان بزن"
                    onChange={(expires_at) => setDraft({ ...draft, expires_at })}
                  />
                </Field>
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {[1, 7, 30, 90].map((days) => (
                  <button
                    key={days}
                    type="button"
                    onClick={() => setDraft({ ...draft, expires_at: daysFromNow(days) })}
                    className="rounded-full border border-white/12 px-3 py-1 text-xs text-mist-300 transition hover:bg-white/5"
                  >
                    {n(days)} روز
                  </button>
                ))}
                <button
                  type="button"
                  onClick={() => setDraft({ ...draft, expires_at: "" })}
                  className="rounded-full border border-white/12 px-3 py-1 text-xs text-mist-300 transition hover:bg-white/5"
                >
                  بدون انقضا
                </button>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="تعداد کل استفاده" hint="بین همه کاربرها — ۰ یعنی نامحدود">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  min={0}
                  value={draft.max_uses}
                  onChange={(e) => setDraft({ ...draft, max_uses: e.target.value })}
                />
              </Field>
              <Field label="استفاده برای هر نفر" hint="۰ یعنی نامحدود">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  min={0}
                  value={draft.per_user_limit}
                  onChange={(e) => setDraft({ ...draft, per_user_limit: e.target.value })}
                />
              </Field>
              <Field label="حداقل مبلغ سبد خرید (تومان)" hint="اختیاری">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  min={0}
                  value={draft.min_total_toman}
                  onChange={(e) => setDraft({ ...draft, min_total_toman: e.target.value })}
                />
              </Field>
            </div>

            <div>
              <span className="mb-2 block text-xs text-mist-400">روی چه چیزهایی اعمال شود (هیچ‌کدام = همه)</span>
              <div className="flex flex-wrap gap-2">
                {targets.map((target) => {
                  const on = draft.applies_to.includes(target);
                  return (
                    <button
                      key={target}
                      type="button"
                      aria-pressed={on}
                      onClick={() =>
                        setDraft({
                          ...draft,
                          applies_to: on
                            ? draft.applies_to.filter((item) => item !== target)
                            : [...draft.applies_to, target],
                        })
                      }
                      className={cn(
                        "rounded-full border px-4 py-1.5 text-xs transition",
                        on ? "border-violet-400/60 bg-violet-500/20 text-violet-100" : "border-white/12 text-mist-400 hover:bg-white/5",
                      )}
                    >
                      {COUPON_TARGET_LABELS[target] ?? target}
                    </button>
                  );
                })}
              </div>
            </div>

            <Field label="یادداشت (فقط برای خودت)" hint="مثلاً برای چه کسی یا کدام کمپین">
              <Textarea value={draft.note} maxLength={300} onChange={(e) => setDraft({ ...draft, note: e.target.value })} />
            </Field>

            <label className="flex items-center gap-3 text-sm text-mist-300">
              <input
                type="checkbox"
                checked={draft.is_active}
                onChange={(e) => setDraft({ ...draft, is_active: e.target.checked })}
                className="size-4 accent-violet-500"
              />
              فعال باشد
            </label>

            <div className="flex gap-3 pt-2">
              <Button onClick={save} disabled={busy || !draft.value} className="flex-1">
                {busy ? "…" : "ذخیره"}
              </Button>
              <Button variant="outline" onClick={() => setDraft(null)}>
                انصراف
              </Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <Modal open={!!usage} title={`استفاده‌های ${usage?.coupon.code ?? ""}`} onClose={() => setUsage(null)}>
        {usage?.rows.length ? (
          <ul className="space-y-2">
            {usage.rows.map((use, index) => (
              <li key={index} className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/8 px-4 py-3 text-sm">
                <span className="min-w-0 flex-1">
                  <span className="block truncate font-medium">{use.user}</span>
                  <span className="block truncate text-xs text-mist-500" dir="ltr">
                    {use.email}
                  </span>
                </span>
                <span className="tnum text-xs text-mint-400">− {formatPrice(use.amount, locale, "—")}</span>
                <span className="tnum text-xs text-mist-500" dir="ltr">
                  {use.order_code}
                </span>
                <span className="text-xs text-mist-500">{formatDate(use.created_at, locale)}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-mist-500">هنوز کسی از این کد استفاده نکرده است.</p>
        )}
      </Modal>

      <Toast message={toast.message} tone={toast.tone} />
    </>
  );
}
