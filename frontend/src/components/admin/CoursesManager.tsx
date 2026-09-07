"use client";

import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import type { Locale } from "@/i18n/config";
import type { AdminCategory, AdminCourse, AdminInstructor } from "@/lib/admin";
import { formatNumber, formatPrice } from "@/lib/format";

import {
  CourseFields,
  blankCourse,
  courseToDraft,
  draftToBody,
  type CourseDraft,
} from "./CourseForm";
import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast } from "./ui";

export function CoursesManager({
  initial,
  categories,
  instructors,
  locale,
}: {
  initial: AdminCourse[];
  categories: AdminCategory[];
  instructors: AdminInstructor[];
  locale: Locale;
}) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<CourseDraft | null>(null);

  async function save() {
    if (!draft) return;
    const body = draftToBody(draft);

    const saved = draft.id
      ? await run(() => call<AdminCourse>(`admin/courses/${draft.id}`, { method: "PATCH", body }),
          { success: "دوره بروزرسانی شد" })
      : await run(() => call<AdminCourse>("admin/courses", { method: "POST", body }),
          { success: "دوره ساخته شد" });

    if (!saved) return;
    setRows((current) =>
      draft.id ? current.map((row) => (row.id === saved.id ? saved : row)) : [saved, ...current],
    );
    setDraft(null);
  }

  async function togglePublished(row: AdminCourse) {
    const saved = await run(
      () =>
        call<AdminCourse>(`admin/courses/${row.id}`, {
          method: "PATCH",
          body: { is_published: !row.is_published },
        }),
      { success: row.is_published ? "از انتشار خارج شد" : "منتشر شد" },
    );
    if (saved) setRows((current) => current.map((item) => (item.id === saved.id ? saved : item)));
  }

  async function remove(row: AdminCourse) {
    if (!confirm(`«${row.title.fa || row.slug}» و همه فصل‌هایش حذف شوند؟`)) return;
    const done = await run(() => call(`admin/courses/${row.id}`, { method: "DELETE" }), {
      success: "حذف شد",
    });
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  return (
    <>
      <Panel title="دوره‌ها" action={<Button onClick={() => setDraft(blankCourse())}>+ دوره جدید</Button>}>
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
                    {row.slug} · {row.parts_count} فصل · {row.videos_count} ویدیو ·{" "}
                    {formatNumber(row.students_count, locale)} زبان‌آموز
                  </span>
                </span>

                <span className="tnum text-xs text-mist-400">
                  {formatPrice(row.discount_price || row.price, locale, "رایگان")}
                </span>

                <button
                  type="button"
                  onClick={() => togglePublished(row)}
                  className={`rounded-full px-3 py-1.5 text-[11px] font-semibold ${
                    row.is_published
                      ? "bg-mint-400/15 text-mint-400"
                      : "bg-white/8 text-mist-500"
                  }`}
                >
                  {row.is_published ? "منتشرشده" : "پیش‌نویس"}
                </button>

                <Link
                  href={`/${locale}/admin/courses/${row.id}`}
                  className="rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-4 py-1.5 text-xs font-semibold text-ink-950"
                >
                  فصل‌ها و ویدیوها
                </Link>

                <button
                  type="button"
                  onClick={() => setDraft(courseToDraft(row))}
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
          <Empty title="هنوز دوره‌ای نساخته‌ای" icon="◇" />
        )}
      </Panel>

      <Modal
        open={!!draft}
        wide
        title={draft?.id ? "ویرایش دوره" : "دوره جدید"}
        onClose={() => setDraft(null)}
      >
        {draft ? (
          <div className="space-y-5">
            <CourseFields
              draft={draft}
              onChange={setDraft}
              categories={categories}
              instructors={instructors}
              onError={(message) => notify(message, "error")}
            />

            <div className="flex gap-3 pt-2">
              <Button onClick={save} disabled={busy} className="flex-1">
                {busy ? "…" : "ذخیره"}
              </Button>
              <Button variant="outline" onClick={() => setDraft(null)}>
                انصراف
              </Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <Toast message={toast.message} tone={toast.tone} />
    </>
  );
}
