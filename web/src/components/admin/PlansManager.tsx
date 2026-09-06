"use client";

import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminPlan, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED, PERK_LABELS } from "@/lib/admin";
import { formatNumber, formatPrice } from "@/lib/format";
import { alpha } from "@/lib/utils";

import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

interface Draft {
  id?: string;
  title: Translated;
  description: Translated;
  perks: string[];
  price: string;
  duration_days: string;
  accent: string;
  badge: string;
  is_published: boolean;
  is_featured: boolean;
  slug: string;
}

const blank = (): Draft => ({
  title: { ...EMPTY_TRANSLATED },
  description: { ...EMPTY_TRANSLATED },
  perks: [],
  price: "0",
  duration_days: "365",
  accent: "#6d5efc",
  badge: "",
  is_published: true,
  is_featured: false,
  slug: "",
});

export function PlansManager({
  initial,
  perks,
  locale,
}: {
  initial: AdminPlan[];
  perks: string[];
  locale: Locale;
}) {
  const { busy, toast, run, call } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<Draft | null>(null);

  async function save() {
    if (!draft) return;
    const body = {
      title: draft.title,
      description: draft.description,
      perks: draft.perks,
      price: Number(draft.price) || 0,
      duration_days: Number(draft.duration_days) || 365,
      accent: draft.accent,
      badge: draft.badge,
      is_published: draft.is_published,
      is_featured: draft.is_featured,
      ...(draft.slug ? { slug: draft.slug } : {}),
    };

    const saved = draft.id
      ? await run(() => call<AdminPlan>(`admin/plans/${draft.id}`, { method: "PATCH", body }),
          { success: "اشتراک بروزرسانی شد" })
      : await run(() => call<AdminPlan>("admin/plans", { method: "POST", body }),
          { success: "اشتراک ساخته شد" });

    if (!saved) return;
    setRows((current) =>
      draft.id ? current.map((row) => (row.id === saved.id ? saved : row)) : [...current, saved],
    );
    setDraft(null);
  }

  async function remove(row: AdminPlan) {
    if (!confirm(`اشتراک «${row.title.fa || row.slug}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/plans/${row.id}`, { method: "DELETE" }), {
      success: "حذف شد",
    });
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  return (
    <>
      <Panel title="اشتراک‌ها" action={<Button onClick={() => setDraft(blank())}>+ اشتراک جدید</Button>}>
        {rows.length ? (
          <ul className="space-y-2">
            {rows.map((row) => (
              <li
                key={row.id}
                className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/8 px-4 py-3"
              >
                <span
                  className="grid size-10 shrink-0 place-items-center rounded-xl text-xs font-bold"
                  style={{ background: alpha(row.accent, 0.16), color: row.accent }}
                  aria-hidden
                >
                  ★
                </span>

                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-semibold">
                    {row.title.fa || row.title.en || row.slug}
                  </span>
                  <span className="block truncate text-xs text-mist-600">
                    {row.perks.map((perk) => PERK_LABELS[perk] ?? perk).join(" · ")}
                  </span>
                </span>

                <span className="tnum text-xs text-mist-400">
                  {formatPrice(row.price, locale, "—")} / {formatNumber(row.duration_days, locale)} روز
                </span>
                <span className="tnum text-xs text-mist-500">
                  {formatNumber(row.subscribers, locale)} مشترک
                </span>
                <span
                  className={`rounded-full px-3 py-1.5 text-[11px] font-semibold ${
                    row.is_published ? "bg-mint-400/15 text-mint-400" : "bg-white/8 text-mist-500"
                  }`}
                >
                  {row.is_published ? "منتشرشده" : "پیش‌نویس"}
                </span>

                <button
                  type="button"
                  onClick={() =>
                    setDraft({
                      id: row.id,
                      title: row.title,
                      description: row.description,
                      perks: row.perks,
                      price: String(row.price),
                      duration_days: String(row.duration_days),
                      accent: row.accent,
                      badge: row.badge,
                      is_published: row.is_published,
                      is_featured: row.is_featured,
                      slug: row.slug,
                    })
                  }
                  className="glass rounded-full px-4 py-1.5 text-xs"
                >
                  ویرایش
                </button>
                <button
                  type="button"
                  onClick={() => remove(row)}
                  className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                >
                  حذف
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <Empty title="هنوز اشتراکی نساخته‌ای" icon="◇" />
        )}
      </Panel>

      <Modal open={!!draft} wide title={draft?.id ? "ویرایش اشتراک" : "اشتراک جدید"} onClose={() => setDraft(null)}>
        {draft ? (
          <div className="space-y-5">
            <TranslatedField
              label="عنوان"
              required
              value={draft.title}
              onChange={(title) => setDraft({ ...draft, title })}
            />
            <TranslatedField
              label="توضیح"
              multiline
              value={draft.description}
              onChange={(description) => setDraft({ ...draft, description })}
            />

            <div>
              <span className="mb-2 block text-xs text-mist-400">
                این اشتراک چه چیزی را باز می‌کند
              </span>
              <div className="space-y-1.5">
                {perks.map((perk) => (
                  <label
                    key={perk}
                    className="flex cursor-pointer items-center gap-3 rounded-xl px-3 py-2 text-sm transition hover:bg-white/5"
                  >
                    <input
                      type="checkbox"
                      checked={draft.perks.includes(perk)}
                      onChange={(event) =>
                        setDraft({
                          ...draft,
                          perks: event.target.checked
                            ? [...draft.perks, perk]
                            : draft.perks.filter((item) => item !== perk),
                        })
                      }
                      className="size-4 accent-violet-500"
                    />
                    <span className="text-mist-200">{PERK_LABELS[perk] ?? perk}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="قیمت (ریال)" hint="در فارسی به تومان نمایش داده می‌شود">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  value={draft.price}
                  onChange={(e) => setDraft({ ...draft, price: e.target.value })}
                />
              </Field>
              <Field label="مدت اعتبار (روز)">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  value={draft.duration_days}
                  onChange={(e) => setDraft({ ...draft, duration_days: e.target.value })}
                />
              </Field>
              <Field label="رنگ شاخص">
                <Input
                  value={draft.accent}
                  dir="ltr"
                  onChange={(e) => setDraft({ ...draft, accent: e.target.value })}
                />
              </Field>
              <Field label="برچسب" hint="مثلاً پرفروش">
                <Input
                  value={draft.badge}
                  onChange={(e) => setDraft({ ...draft, badge: e.target.value })}
                />
              </Field>
            </div>

            <div className="flex flex-wrap gap-5">
              <label className="flex items-center gap-3 text-sm text-mist-300">
                <input
                  type="checkbox"
                  checked={draft.is_published}
                  onChange={(e) => setDraft({ ...draft, is_published: e.target.checked })}
                  className="size-4 accent-violet-500"
                />
                منتشر شود
              </label>
              <label className="flex items-center gap-3 text-sm text-mist-300">
                <input
                  type="checkbox"
                  checked={draft.is_featured}
                  onChange={(e) => setDraft({ ...draft, is_featured: e.target.checked })}
                  className="size-4 accent-violet-500"
                />
                برجسته شود
              </label>
            </div>

            <div className="flex gap-3 pt-2">
              <Button onClick={save} disabled={busy} className="flex-1">
                {busy ? "…" : "ذخیره"}
              </Button>
              <Button variant="outline" onClick={() => setDraft(null)}>انصراف</Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <Toast message={toast.message} tone={toast.tone} />
    </>
  );
}
