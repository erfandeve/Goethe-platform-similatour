"use client";

import { useState } from "react";

import { ImageUpload } from "@/components/admin/ImageUpload";
import { Modal, Panel, Toast, TranslatedField } from "@/components/admin/ui";
import { useAdmin } from "@/components/admin/useAdmin";
import { Button } from "@/components/ui/Button";
import { Input, Select } from "@/components/ui/Field";
import type { Translated } from "@/lib/admin";

interface Item {
  title: Translated;
  body: Translated;
  icon: string;
}

interface Section {
  id: string;
  key: string;
  kind: string;
  eyebrow: Translated;
  title: Translated;
  subtitle: Translated;
  body: Translated;
  items: Item[];
  image: string;
  image_alt: Translated;
  image_side: "start" | "end";
  cta_label: Translated;
  cta_href: string;
  accent: string;
  order: number;
  is_published: boolean;
}

const EMPTY: Translated = { fa: "", en: "", de: "" };

/** What each kind reads, so the form can hide the fields it ignores. */
const KIND_LABELS: Record<string, string> = {
  text_image: "متن + تصویر",
  rich_text: "متن بلند",
  features: "شبکه‌ی کارت‌ها",
  stats: "آمار",
  faq: "پرسش و پاسخ",
  cta: "بنر دعوت به اقدام",
};

const USES_ITEMS = new Set(["features", "stats", "faq"]);
const USES_IMAGE = new Set(["text_image"]);

function blank(): Section {
  return {
    id: "",
    key: "",
    kind: "text_image",
    eyebrow: { ...EMPTY },
    title: { ...EMPTY },
    subtitle: { ...EMPTY },
    body: { ...EMPTY },
    items: [],
    image: "",
    image_alt: { ...EMPTY },
    image_side: "end",
    cta_label: { ...EMPTY },
    cta_href: "",
    accent: "#8b7dff",
    order: 0,
    is_published: true,
  };
}

export function SectionsManager({ initial }: { initial: Section[] }) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [sections, setSections] = useState(initial);
  const [draft, setDraft] = useState<Section | null>(null);

  const reload = async () => {
    const data = await run(() => call<{ results: Section[] }>("/admin/sections/"));
    if (data) setSections(data.results);
  };

  const save = async () => {
    if (!draft) return;
    const payload = { ...draft } as Record<string, unknown>;
    delete payload.id;

    const result = draft.id
      ? await run(() => call(`/admin/sections/${draft.id}/`, { method: "PATCH", body: payload }), {
          success: "بخش ذخیره شد.",
        })
      : await run(() => call("/admin/sections/", { method: "POST", body: payload }), {
          success: "بخش ساخته شد.",
        });

    if (result) {
      setDraft(null);
      await reload();
    }
  };

  const remove = async (section: Section) => {
    if (!confirm(`بخش «${section.title.fa || section.key}» حذف شود؟`)) return;
    const done = await run(
      () => call(`/admin/sections/${section.id}/`, { method: "DELETE" }),
      { success: "بخش حذف شد." },
    );
    if (done !== null) await reload();
  };

  const move = async (index: number, delta: number) => {
    const next = [...sections];
    const target = index + delta;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    setSections(next);
    await run(() =>
      call("/admin/sections/reorder/", { method: "POST", body: { ids: next.map((s) => s.id) } }),
    );
  };

  const patchItem = (index: number, patch: Partial<Item>) => {
    if (!draft) return;
    const items = draft.items.map((item, i) => (i === index ? { ...item, ...patch } : item));
    setDraft({ ...draft, items });
  };

  return (
    <div className="space-y-6">
      <Toast {...toast} />

      <Panel
        title="بخش‌های صفحه اصلی"
        description="هر بخش را می‌توانی اضافه، ویرایش، جابه‌جا یا حذف کنی. متن‌ها در هر سه زبان ذخیره می‌شوند."
        action={
          <Button onClick={() => setDraft(blank())} disabled={busy}>
            بخش جدید
          </Button>
        }
      >
        <ul className="space-y-2">
          {sections.map((section, index) => (
            <li
              key={section.id}
              className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.02] p-4"
            >
              <div className="flex flex-col gap-1">
                <button
                  onClick={() => move(index, -1)}
                  disabled={busy || index === 0}
                  className="rounded px-1.5 text-xs text-mist-500 hover:text-white disabled:opacity-30"
                  aria-label="بالا"
                >
                  ▲
                </button>
                <button
                  onClick={() => move(index, 1)}
                  disabled={busy || index === sections.length - 1}
                  className="rounded px-1.5 text-xs text-mist-500 hover:text-white disabled:opacity-30"
                  aria-label="پایین"
                >
                  ▼
                </button>
              </div>

              <div className="min-w-0 flex-1">
                <p className="truncate font-medium text-white">
                  {section.title.fa || section.key}
                </p>
                <p className="mt-1 text-xs text-mist-500">
                  {KIND_LABELS[section.kind] ?? section.kind} · {section.key}
                  {!section.is_published && " · پنهان"}
                </p>
              </div>

              <Button variant="ghost" onClick={() => setDraft(section)} disabled={busy}>
                ویرایش
              </Button>
              <Button variant="ghost" onClick={() => remove(section)} disabled={busy}>
                حذف
              </Button>
            </li>
          ))}
          {sections.length === 0 && (
            <li className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-mist-500">
              هنوز بخشی ساخته نشده.
            </li>
          )}
        </ul>
      </Panel>

      <Modal
        open={Boolean(draft)}
        title={draft?.id ? "ویرایش بخش" : "بخش جدید"}
        onClose={() => setDraft(null)}
      >
        {draft && (
          <div className="space-y-5">
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="mb-2 block text-xs text-mist-400">نوع چیدمان</span>
                <Select
                  value={draft.kind}
                  onChange={(e) => setDraft({ ...draft, kind: e.target.value })}
                >
                  {Object.entries(KIND_LABELS).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </Select>
              </label>
              <label className="block">
                <span className="mb-2 block text-xs text-mist-400">رنگ تأکید</span>
                <Input
                  value={draft.accent}
                  onChange={(e) => setDraft({ ...draft, accent: e.target.value })}
                />
              </label>
            </div>

            <TranslatedField
              label="برچسب بالای عنوان"
              value={draft.eyebrow}
              onChange={(eyebrow) => setDraft({ ...draft, eyebrow })}
            />
            <TranslatedField
              label="عنوان"
              required
              value={draft.title}
              onChange={(title) => setDraft({ ...draft, title })}
            />
            <TranslatedField
              label="زیرعنوان"
              value={draft.subtitle}
              onChange={(subtitle) => setDraft({ ...draft, subtitle })}
            />
            <TranslatedField
              label="متن (هر پاراگراف را با یک خط خالی جدا کن)"
              multiline
              value={draft.body}
              onChange={(body) => setDraft({ ...draft, body })}
            />

            {USES_IMAGE.has(draft.kind) && (
              <div className="space-y-4 rounded-2xl border border-white/10 p-4">
                <ImageUpload
                  label="تصویر بخش"
                  value={draft.image}
                  folder="sections"
                  onChange={(image) => setDraft({ ...draft, image })}
                  onError={(message) => notify(message, "error")}
                />
                <label className="block">
                  <span className="mb-2 block text-xs text-mist-400">تصویر در کدام سمت</span>
                  <Select
                    value={draft.image_side}
                    onChange={(e) =>
                      setDraft({ ...draft, image_side: e.target.value as "start" | "end" })
                    }
                  >
                    <option value="end">بعد از متن</option>
                    <option value="start">قبل از متن</option>
                  </Select>
                </label>
                <TranslatedField
                  label="متن جایگزین تصویر (alt)"
                  value={draft.image_alt}
                  onChange={(image_alt) => setDraft({ ...draft, image_alt })}
                />
              </div>
            )}

            {USES_ITEMS.has(draft.kind) && (
              <div className="space-y-3 rounded-2xl border border-white/10 p-4">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-white">
                    {draft.kind === "faq" ? "پرسش‌ها" : "کارت‌ها"}
                  </p>
                  <Button
                    variant="ghost"
                    onClick={() =>
                      setDraft({
                        ...draft,
                        items: [...draft.items, { title: { ...EMPTY }, body: { ...EMPTY }, icon: "" }],
                      })
                    }
                  >
                    افزودن
                  </Button>
                </div>
                {draft.items.map((item, index) => (
                  <div key={index} className="space-y-3 rounded-xl bg-white/[0.03] p-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-mist-500">#{index + 1}</span>
                      <Button
                        variant="ghost"
                        onClick={() =>
                          setDraft({
                            ...draft,
                            items: draft.items.filter((_, i) => i !== index),
                          })
                        }
                      >
                        حذف
                      </Button>
                    </div>
                    <TranslatedField
                      label={draft.kind === "faq" ? "پرسش" : draft.kind === "stats" ? "عدد" : "عنوان"}
                      value={item.title}
                      onChange={(title) => patchItem(index, { title })}
                    />
                    <TranslatedField
                      label={draft.kind === "faq" ? "پاسخ" : draft.kind === "stats" ? "برچسب" : "متن"}
                      multiline
                      value={item.body}
                      onChange={(body) => patchItem(index, { body })}
                    />
                  </div>
                ))}
              </div>
            )}

            <div className="grid gap-4 sm:grid-cols-2">
              <TranslatedField
                label="متن دکمه"
                value={draft.cta_label}
                onChange={(cta_label) => setDraft({ ...draft, cta_label })}
              />
              <label className="block">
                <span className="mb-2 block text-xs text-mist-400">
                  مقصد دکمه (مثل /exams — بدون کد زبان)
                </span>
                <Input
                  value={draft.cta_href}
                  dir="ltr"
                  onChange={(e) => setDraft({ ...draft, cta_href: e.target.value })}
                />
              </label>
            </div>

            <label className="flex items-center gap-3 text-sm text-mist-300">
              <input
                type="checkbox"
                checked={draft.is_published}
                onChange={(e) => setDraft({ ...draft, is_published: e.target.checked })}
                className="size-4 accent-violet-500"
              />
              نمایش در صفحه اصلی
            </label>

            <div className="flex justify-end gap-3 pt-2">
              <Button variant="ghost" onClick={() => setDraft(null)}>
                انصراف
              </Button>
              <Button onClick={save} disabled={busy}>
                ذخیره
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
