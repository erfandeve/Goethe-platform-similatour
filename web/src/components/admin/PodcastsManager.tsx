"use client";

import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input, Select } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminCategory, AdminPodcast, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED, LEVELS } from "@/lib/admin";
import { compact } from "@/lib/format";
import { alpha } from "@/lib/utils";

import { ImageUpload } from "./ImageUpload";
import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

interface Draft {
  id?: string;
  title: Translated;
  tagline: Translated;
  description: Translated;
  cover: string;
  accent: string;
  host_name: string;
  level: string;
  category: string;
  is_published: boolean;
  is_featured: boolean;
  slug: string;
}

const blank = (): Draft => ({
  title: { ...EMPTY_TRANSLATED },
  tagline: { ...EMPTY_TRANSLATED },
  description: { ...EMPTY_TRANSLATED },
  cover: "",
  accent: "#6d5efc",
  host_name: "",
  level: "A2",
  category: "",
  is_published: true,
  is_featured: false,
  slug: "",
});

export function PodcastsManager({
  initial,
  categories,
  locale,
}: {
  initial: AdminPodcast[];
  categories: AdminCategory[];
  locale: Locale;
}) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<Draft | null>(null);

  async function save() {
    if (!draft) return;
    const body = {
      title: draft.title,
      tagline: draft.tagline,
      description: draft.description,
      cover: draft.cover,
      accent: draft.accent,
      host_name: draft.host_name,
      level: draft.level,
      category: draft.category || null,
      is_published: draft.is_published,
      is_featured: draft.is_featured,
      ...(draft.slug ? { slug: draft.slug } : {}),
    };

    const saved = draft.id
      ? await run(() => call<AdminPodcast>(`admin/podcasts/${draft.id}`, { method: "PATCH", body }),
          { success: "پادکست بروزرسانی شد" })
      : await run(() => call<AdminPodcast>("admin/podcasts", { method: "POST", body }),
          { success: "پادکست ساخته شد" });

    if (!saved) return;
    setRows((current) =>
      draft.id ? current.map((row) => (row.id === saved.id ? saved : row)) : [...current, saved],
    );
    setDraft(null);
  }

  async function remove(row: AdminPodcast) {
    if (!confirm(`پادکست «${row.title.fa || row.slug}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/podcasts/${row.id}`, { method: "DELETE" }), {
      success: "حذف شد",
    });
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  return (
    <>
      <Panel title="پادکست‌ها" action={<Button onClick={() => setDraft(blank())}>+ پادکست جدید</Button>}>
        {rows.length ? (
          <ul className="space-y-2">
            {rows.map((row) => (
              <li
                key={row.id}
                className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/8 px-4 py-3"
              >
                <span
                  className="grid size-10 shrink-0 place-items-center rounded-xl text-[11px] font-bold"
                  style={{ background: alpha(row.accent, 0.16), color: row.accent }}
                >
                  {row.level}
                </span>

                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-semibold">
                    {row.title.fa || row.title.en || row.slug}
                  </span>
                  <span className="tnum block truncate text-xs text-mist-600" dir="ltr">
                    {row.slug} · {row.host_name || "—"} · {row.episodes_count} قسمت ·{" "}
                    {compact(row.plays, locale)} پخش
                  </span>
                </span>

                <span
                  className={`rounded-full px-3 py-1.5 text-[11px] font-semibold ${
                    row.is_published ? "bg-mint-400/15 text-mint-400" : "bg-white/8 text-mist-500"
                  }`}
                >
                  {row.is_published ? "منتشرشده" : "پیش‌نویس"}
                </span>

                <Link
                  href={`/${locale}/admin/podcasts/${row.id}`}
                  className="rounded-full bg-linear-to-r from-violet-500 to-cyan-400 px-4 py-1.5 text-xs font-semibold text-ink-950"
                >
                  قسمت‌ها
                </Link>
                <button
                  type="button"
                  onClick={() =>
                    setDraft({
                      id: row.id,
                      title: row.title,
                      tagline: row.tagline,
                      description: row.description,
                      cover: row.cover ?? "",
                      accent: row.accent,
                      host_name: row.host_name,
                      level: row.level,
                      category: row.category ?? "",
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
          <Empty title="هنوز پادکستی نساخته‌ای" icon="◇" />
        )}
      </Panel>

      <Modal open={!!draft} wide title={draft?.id ? "ویرایش پادکست" : "پادکست جدید"} onClose={() => setDraft(null)}>
        {draft ? (
          <div className="space-y-5">
            <TranslatedField
              label="عنوان"
              required
              value={draft.title}
              onChange={(title) => setDraft({ ...draft, title })}
            />
            <TranslatedField
              label="شعار کوتاه"
              value={draft.tagline}
              onChange={(tagline) => setDraft({ ...draft, tagline })}
            />
            <TranslatedField
              label="توضیحات"
              multiline
              value={draft.description}
              onChange={(description) => setDraft({ ...draft, description })}
            />

            <ImageUpload
              label="تصویر شاخص (کاور پادکست)"
              value={draft.cover}
              folder="podcasts"
              onChange={(cover) => setDraft({ ...draft, cover })}
              onError={(message) => notify(message, "error")}
              hint="مربعی بهتر است. JPG، PNG یا WebP تا ۸ مگابایت."
            />

            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="مجری">
                <Input
                  value={draft.host_name}
                  onChange={(e) => setDraft({ ...draft, host_name: e.target.value })}
                />
              </Field>
              <Field label="سطح">
                <Select value={draft.level} onChange={(e) => setDraft({ ...draft, level: e.target.value })}>
                  {LEVELS.map((level) => (
                    <option key={level} value={level} className="bg-ink-900">{level}</option>
                  ))}
                </Select>
              </Field>
              <Field label="دسته‌بندی">
                <Select
                  value={draft.category}
                  onChange={(e) => setDraft({ ...draft, category: e.target.value })}
                >
                  <option value="" className="bg-ink-900">—</option>
                  {categories
                    .filter((item) => item.kind === "podcast")
                    .map((item) => (
                      <option key={item.id} value={item.id} className="bg-ink-900">
                        {item.title.fa || item.slug}
                      </option>
                    ))}
                </Select>
              </Field>
              <Field label="رنگ شاخص">
                <Input
                  value={draft.accent}
                  dir="ltr"
                  onChange={(e) => setDraft({ ...draft, accent: e.target.value })}
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
