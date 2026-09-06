"use client";

import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input, Select } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminExam, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED, LEVELS } from "@/lib/admin";
import { formatPrice } from "@/lib/format";

import { ImageUpload } from "./ImageUpload";
import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

interface Draft {
  id?: string;
  title: Translated;
  subtitle: Translated;
  level: string;
  kind: "simulator" | "frequent";
  exam_board: string;
  duration_minutes: string;
  pass_score: string;
  price: string;
  cover: string;
  is_published: boolean;
  slug: string;
}

const blank = (): Draft => ({
  title: { ...EMPTY_TRANSLATED },
  subtitle: { ...EMPTY_TRANSLATED },
  level: "B1",
  kind: "simulator",
  exam_board: "Goethe-Zertifikat",
  duration_minutes: "60",
  pass_score: "60",
  price: "0",
  cover: "",
  is_published: true,
  slug: "",
});

export function ExamsManager({
  initial,
  locale,
}: {
  initial: AdminExam[];
  locale: Locale;
}) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<Draft | null>(null);

  async function save() {
    if (!draft) return;
    const body = {
      title: draft.title,
      subtitle: draft.subtitle,
      level: draft.level,
      kind: draft.kind,
      exam_board: draft.exam_board,
      duration_minutes: Number(draft.duration_minutes) || 60,
      pass_score: Number(draft.pass_score) || 60,
      price: Number(draft.price) || 0,
      cover: draft.cover,
      is_published: draft.is_published,
      ...(draft.slug ? { slug: draft.slug } : {}),
    };

    const saved = draft.id
      ? await run(() => call<AdminExam>(`admin/exams/${draft.id}`, { method: "PATCH", body }),
          { success: "آزمون بروزرسانی شد" })
      : await run(() => call<AdminExam>("admin/exams", { method: "POST", body }),
          { success: "آزمون ساخته شد" });

    if (!saved) return;
    setRows((current) =>
      draft.id ? current.map((row) => (row.id === saved.id ? saved : row)) : [...current, saved],
    );
    setDraft(null);
  }

  async function remove(row: AdminExam) {
    if (!confirm(`آزمون «${row.title.fa || row.slug}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/exams/${row.id}`, { method: "DELETE" }), {
      success: "حذف شد",
    });
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  return (
    <>
      <Panel title="آزمون‌ها" action={<Button onClick={() => setDraft(blank())}>+ آزمون جدید</Button>}>
        {rows.length ? (
          <ul className="space-y-2">
            {rows.map((row) => (
              <li
                key={row.id}
                className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/8 px-4 py-3"
              >
                <span
                  className="grid size-10 shrink-0 place-items-center rounded-xl text-[11px] font-bold"
                  style={{ background: `${row.accent}22`, color: row.accent }}
                >
                  {row.level}
                </span>

                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-semibold">
                    {row.title.fa || row.title.en || row.slug}
                  </span>
                  <span className="tnum block text-xs text-mist-600" dir="ltr">
                    {row.slug} · {row.kind === "frequent" ? "پرتکرار" : "شبیه‌ساز"} ·{" "}
                    {row.modules_count} ماژول · {row.questions_count} سؤال
                  </span>
                </span>

                <span className="tnum text-xs text-mist-400">
                  {formatPrice(row.discount_price || row.price, locale, "رایگان")}
                </span>

                <span
                  className={`rounded-full px-3 py-1.5 text-[11px] font-semibold ${
                    row.is_published ? "bg-mint-400/15 text-mint-400" : "bg-white/8 text-mist-500"
                  }`}
                >
                  {row.is_published ? "منتشرشده" : "پیش‌نویس"}
                </span>

                <Link
                  href={`/${locale}/admin/exams/${row.id}`}
                  className="rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-4 py-1.5 text-xs font-semibold text-ink-950"
                >
                  سؤال‌ها
                </Link>

                <button
                  type="button"
                  onClick={() =>
                    setDraft({
                      id: row.id,
                      title: row.title,
                      subtitle: row.subtitle,
                      level: row.level,
                      kind: row.kind,
                      exam_board: row.exam_board,
                      duration_minutes: String(row.duration_minutes),
                      pass_score: String(row.pass_score),
                      price: String(row.price),
                      cover: row.cover ?? "",
                      is_published: row.is_published,
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
          <Empty title="هنوز آزمونی نساخته‌ای" icon="◇" />
        )}
      </Panel>

      <Modal open={!!draft} wide title={draft?.id ? "ویرایش آزمون" : "آزمون جدید"} onClose={() => setDraft(null)}>
        {draft ? (
          <div className="space-y-5">
            <TranslatedField
              label="عنوان آزمون"
              required
              value={draft.title}
              onChange={(title) => setDraft({ ...draft, title })}
            />
            <TranslatedField
              label="زیرعنوان"
              value={draft.subtitle}
              onChange={(subtitle) => setDraft({ ...draft, subtitle })}
            />

            <ImageUpload
              label="تصویر شاخص (کاور آزمون)"
              value={draft.cover}
              folder="exams"
              onChange={(cover) => setDraft({ ...draft, cover })}
              onError={(message) => notify(message, "error")}
            />

            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="سطح">
                <Select value={draft.level} onChange={(e) => setDraft({ ...draft, level: e.target.value })}>
                  {LEVELS.map((level) => (
                    <option key={level} value={level} className="bg-ink-900">{level}</option>
                  ))}
                </Select>
              </Field>
              <Field label="نوع">
                <Select
                  value={draft.kind}
                  onChange={(e) => setDraft({ ...draft, kind: e.target.value as Draft["kind"] })}
                >
                  <option value="simulator" className="bg-ink-900">شبیه‌ساز کامل</option>
                  <option value="frequent" className="bg-ink-900">سؤالات پرتکرار</option>
                </Select>
              </Field>
              <Field label="مرجع آزمون">
                <Input
                  value={draft.exam_board}
                  dir="ltr"
                  onChange={(e) => setDraft({ ...draft, exam_board: e.target.value })}
                />
              </Field>
              <Field label="مدت (دقیقه)">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  value={draft.duration_minutes}
                  onChange={(e) => setDraft({ ...draft, duration_minutes: e.target.value })}
                />
              </Field>
              <Field label="حد نصاب قبولی (٪)">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  value={draft.pass_score}
                  onChange={(e) => setDraft({ ...draft, pass_score: e.target.value })}
                />
              </Field>
              <Field label="قیمت (ریال)" hint="صفر یعنی رایگان">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  value={draft.price}
                  onChange={(e) => setDraft({ ...draft, price: e.target.value })}
                />
              </Field>
            </div>

            <label className="flex items-center gap-3 text-sm text-mist-300">
              <input
                type="checkbox"
                checked={draft.is_published}
                onChange={(e) => setDraft({ ...draft, is_published: e.target.checked })}
                className="size-4 accent-violet-500"
              />
              منتشر شود
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
