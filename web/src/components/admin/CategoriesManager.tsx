"use client";

import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input, Select } from "@/components/ui/Field";
import type { AdminCategory, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED } from "@/lib/admin";
import { alpha } from "@/lib/utils";

import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

const ICONS = ["layers", "target", "chat", "book", "briefcase", "heart", "sun", "globe", "radio", "book-open"];
const COLORS = ["#6d5efc", "#22d3ee", "#f59e0b", "#ff6b6b", "#34d399", "#e879f9", "#38bdf8", "#fbbf24"];

interface Draft {
  id?: string;
  kind: "course" | "podcast";
  title: Translated;
  description: Translated;
  icon: string;
  color: string;
  slug: string;
}

const blank = (): Draft => ({
  kind: "course",
  title: { ...EMPTY_TRANSLATED },
  description: { ...EMPTY_TRANSLATED },
  icon: "layers",
  color: COLORS[0],
  slug: "",
});

export function CategoriesManager({ initial }: { initial: AdminCategory[] }) {
  const { busy, toast, run, call } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<Draft | null>(null);

  async function save() {
    if (!draft) return;
    const body = {
      kind: draft.kind,
      title: draft.title,
      description: draft.description,
      icon: draft.icon,
      color: draft.color,
      ...(draft.slug ? { slug: draft.slug } : {}),
    };

    const saved = draft.id
      ? await run(() => call<AdminCategory>(`admin/categories/${draft.id}`, { method: "PATCH", body }),
          { success: "دسته‌بندی بروزرسانی شد" })
      : await run(() => call<AdminCategory>("admin/categories", { method: "POST", body }),
          { success: "دسته‌بندی ساخته شد" });

    if (!saved) return;
    setRows((current) =>
      draft.id
        ? current.map((row) => (row.id === saved.id ? saved : row))
        : [...current, saved],
    );
    setDraft(null);
  }

  async function remove(row: AdminCategory) {
    if (!confirm(`«${row.title.fa || row.slug}» حذف شود؟`)) return;
    const done = await run(
      () => call(`admin/categories/${row.id}`, { method: "DELETE" }),
      { success: "حذف شد" },
    );
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  return (
    <>
      <Panel
        title="دسته‌بندی‌ها"
        action={<Button onClick={() => setDraft(blank())}>+ دسته‌بندی جدید</Button>}
      >
        {rows.length ? (
          <ul className="space-y-2">
            {rows.map((row) => (
              <li
                key={row.id}
                className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/8 px-4 py-3"
              >
                <span
                  className="grid size-9 shrink-0 place-items-center rounded-xl text-xs font-bold"
                  style={{ background: alpha(row.color, 0.16), color: row.color }}
                  aria-hidden
                >
                  {row.kind === "podcast" ? "P" : "C"}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block text-sm font-semibold">
                    {row.title.fa || row.title.en || row.slug}
                  </span>
                  <span className="block text-xs text-mist-600" dir="ltr">
                    {row.slug} · {row.kind}
                  </span>
                </span>
                <span className="tnum text-xs text-mist-500">{row.course_count} دوره</span>
                <button
                  type="button"
                  onClick={() =>
                    setDraft({
                      id: row.id,
                      kind: row.kind,
                      title: row.title,
                      description: row.description,
                      icon: row.icon,
                      color: row.color,
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
          <Empty title="هنوز دسته‌بندی نساخته‌ای" icon="◇" />
        )}
      </Panel>

      <Modal
        open={!!draft}
        title={draft?.id ? "ویرایش دسته‌بندی" : "دسته‌بندی جدید"}
        onClose={() => setDraft(null)}
      >
        {draft ? (
          <div className="space-y-5">
            <TranslatedField
              label="عنوان"
              required
              value={draft.title}
              onChange={(title) => setDraft({ ...draft, title })}
            />
            <TranslatedField
              label="توضیح کوتاه"
              multiline
              value={draft.description}
              onChange={(description) => setDraft({ ...draft, description })}
            />

            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="نوع">
                <Select
                  value={draft.kind}
                  onChange={(event) =>
                    setDraft({ ...draft, kind: event.target.value as Draft["kind"] })
                  }
                >
                  <option value="course" className="bg-ink-900">دوره</option>
                  <option value="podcast" className="bg-ink-900">پادکست</option>
                </Select>
              </Field>
              <Field label="نشانی (slug)" hint="خالی بگذار تا خودکار ساخته شود">
                <Input
                  value={draft.slug}
                  dir="ltr"
                  onChange={(event) => setDraft({ ...draft, slug: event.target.value })}
                />
              </Field>
            </div>

            <div>
              <span className="mb-2 block text-xs text-mist-400">رنگ</span>
              <div className="flex flex-wrap gap-2">
                {COLORS.map((color) => (
                  <button
                    key={color}
                    type="button"
                    onClick={() => setDraft({ ...draft, color })}
                    className="size-8 rounded-lg ring-2 transition"
                    style={{
                      background: color,
                      boxShadow: draft.color === color ? `0 0 0 2px ${color}` : "none",
                    }}
                    aria-label={color}
                  />
                ))}
              </div>
            </div>

            <Field label="آیکون">
              <Select
                value={draft.icon}
                onChange={(event) => setDraft({ ...draft, icon: event.target.value })}
              >
                {ICONS.map((icon) => (
                  <option key={icon} value={icon} className="bg-ink-900">
                    {icon}
                  </option>
                ))}
              </Select>
            </Field>

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
