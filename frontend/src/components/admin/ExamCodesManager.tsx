"use client";

import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminExam, AdminExamCode, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED } from "@/lib/admin";
import { formatNumber, formatPrice } from "@/lib/format";

import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

interface Draft {
  id?: string;
  code: string;
  label: Translated;
  description: Translated;
  extra_price: string;
  is_published: boolean;
}

const blank = (): Draft => ({
  code: "",
  label: { ...EMPTY_TRANSLATED },
  description: { ...EMPTY_TRANSLATED },
  extra_price: "0",
  is_published: true,
});

/**
 * The sittings of one exam. Buyers tick the codes they want and pay each one's
 * own price; a code left at zero sells at the exam's own price.
 */
export function ExamCodesManager({
  exam,
  initial,
  locale,
}: {
  exam: AdminExam;
  initial: AdminExamCode[];
  locale: Locale;
}) {
  const { busy, toast, run, call } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<Draft | null>(null);

  async function save() {
    if (!draft) return;
    if (!draft.code.trim()) return;

    const body = {
      code: draft.code.trim(),
      label: draft.label,
      description: draft.description,
      extra_price: Number(draft.extra_price) || 0,
      is_published: draft.is_published,
    };

    const saved = draft.id
      ? await run(() => call<AdminExamCode>(`admin/codes/${draft.id}`, { method: "PATCH", body }),
          { success: "کد بروزرسانی شد" })
      : await run(() => call<AdminExamCode>(`admin/exams/${exam.id}/codes`, { method: "POST", body }),
          { success: "کد ساخته شد" });

    if (!saved) return;
    setRows((current) =>
      draft.id ? current.map((row) => (row.id === saved.id ? saved : row)) : [...current, saved],
    );
    setDraft(null);
  }

  async function remove(row: AdminExamCode) {
    if (!confirm(`کد «${row.code}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/codes/${row.id}`, { method: "DELETE" }), {
      success: "حذف شد",
    });
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  return (
    <>
      <Panel
        title="کدهای آزمون"
        action={<Button onClick={() => setDraft(blank())}>+ کد جدید</Button>}
      >
        <p className="text-muted mb-4 text-xs">
          خریدار در صفحه محصول هر تعداد کد که بخواهد انتخاب می‌کند و قیمت هر کد جداگانه به فاکتور
          اضافه می‌شود. هر کدی که بخرد، هر چند بار که بخواهد می‌تواند بدهد. کدی که قیمتش صفر بماند
          با قیمت خود آزمون ({formatPrice(exam.price, locale, "رایگان")}) فروخته می‌شود.
        </p>

        {rows.length ? (
          <ul className="space-y-2">
            {rows.map((row) => (
              <li
                key={row.id}
                className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/8 px-4 py-3"
              >
                <span className="tnum grid size-9 shrink-0 place-items-center rounded-lg bg-white/8 text-[11px] font-bold">
                  {formatNumber(row.order, locale)}
                </span>

                <span className="min-w-0 flex-1">
                  <span className="block text-sm font-semibold" dir="ltr">
                    {row.code}
                  </span>
                  <span className="block truncate text-xs text-mist-600">
                    {row.label.fa || row.label.de || "—"} ·{" "}
                    {formatNumber(row.items_count, locale)} سؤال
                  </span>
                </span>

                <span className="tnum text-xs text-mist-400">
                  {row.extra_price
                    ? formatPrice(row.extra_price, locale, "رایگان")
                    : formatPrice(exam.price, locale, "رایگان")}
                </span>
                <span
                  className={`rounded-full px-3 py-1.5 text-[11px] font-semibold ${
                    row.is_published ? "bg-mint-400/15 text-mint-400" : "bg-white/8 text-mist-500"
                  }`}
                >
                  {row.is_published ? "فعال" : "غیرفعال"}
                </span>

                <Link
                  href={`/${locale}/admin/codes/${row.id}`}
                  className="rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-4 py-1.5 text-xs font-semibold text-ink-950"
                >
                  سؤال‌های این کد
                </Link>
                <button
                  type="button"
                  onClick={() =>
                    setDraft({
                      id: row.id,
                      code: row.code,
                      label: row.label,
                      description: row.description,
                      extra_price: String(row.extra_price),
                      is_published: row.is_published,
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
          <Empty
            title="این آزمون هنوز کدی ندارد"
            body="بدون کد، آزمون به‌صورت یکجا فروخته می‌شود."
            icon="◇"
          />
        )}
      </Panel>

      <Modal open={!!draft} title={draft?.id ? "ویرایش کد" : "کد جدید"} onClose={() => setDraft(null)}>
        {draft ? (
          <div className="space-y-5">
            <Field label="کد" hint="مثلاً B2-2026-01">
              <Input
                value={draft.code}
                dir="ltr"
                onChange={(e) => setDraft({ ...draft, code: e.target.value })}
              />
            </Field>
            <TranslatedField
              label="عنوان نمایشی"
              value={draft.label}
              onChange={(label) => setDraft({ ...draft, label })}
            />
            <TranslatedField
              label="توضیح"
              multiline
              value={draft.description}
              onChange={(description) => setDraft({ ...draft, description })}
            />
            <Field
              label="قیمت این کد (ریال)"
              hint="صفر بگذاری، با قیمت خود آزمون فروخته می‌شود"
            >
              <Input
                type="number"
                dir="ltr"
                className="tnum"
                value={draft.extra_price}
                onChange={(e) => setDraft({ ...draft, extra_price: e.target.value })}
              />
            </Field>
            <label className="flex items-center gap-3 text-sm text-mist-300">
              <input
                type="checkbox"
                checked={draft.is_published}
                onChange={(e) => setDraft({ ...draft, is_published: e.target.checked })}
                className="size-4 accent-violet-500"
              />
              فعال باشد
            </label>

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
