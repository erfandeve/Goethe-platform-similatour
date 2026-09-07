"use client";

import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input, Select, Textarea } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminExam, ExamItem, ExamModule, ExamPart } from "@/lib/admin";
import { MODULE_LABELS, PART_TYPE_LABELS } from "@/lib/admin";
import { formatNumber } from "@/lib/format";

import { PartContentEditor } from "./PartContentEditor";
import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

const SKILLS = ["lesen", "hoeren", "schreiben", "sprechen"] as const;
const LETTERS = "abcdefgh".split("");

/** Modules → Teile → questions, with the answer key set right on each question. */
export function ExamBuilder({
  initial,
  locale,
  /** When set, edits go to this code's paper rather than the exam's own. */
  codeId,
  title,
  backHref,
}: {
  initial: AdminExam;
  locale: Locale;
  codeId?: string;
  title?: string;
  backHref?: string;
}) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [exam, setExam] = useState(initial);
  const [editing, setEditing] = useState<{ module: number; part: number } | null>(null);
  // The same Teil, opened on its text rather than its questions.
  const [editingText, setEditingText] = useState<{ module: number; part: number } | null>(
    null,
  );
  const [items, setItems] = useState<ExamItem[]>([]);

  const modules = exam.modules ?? [];
  // One switch decides whether this builder edits an exam or one of its codes.
  const base = codeId ? `admin/codes/${codeId}` : `admin/exams/${exam.id}`;

  async function addModule(skill: string) {
    if (modules.some((module) => module.skill === skill)) {
      notify("این ماژول از قبل هست", "error");
      return;
    }
    const saved = await run(
      () =>
        call<AdminExam>(`${base}/modules`, {
          method: "POST",
          body: { skill, duration_minutes: 60, max_points: 30 },
        }),
      { success: "ماژول اضافه شد" },
    );
    if (saved) setExam(saved);
  }

  async function removeModule(module: ExamModule) {
    if (!confirm(`ماژول ${module.skill} و همه بخش‌هایش حذف شود؟`)) return;
    const saved = await run(
      () => call<AdminExam>(`${base}/modules/${module.index}`, { method: "DELETE" }),
      { success: "ماژول حذف شد" },
    );
    if (saved) setExam(saved);
  }

  async function addPart(module: ExamModule, type: string) {
    const saved = await run(
      () =>
        call<AdminExam>(`${base}/modules/${module.index}/parts`, {
          method: "POST",
          body: { type, number: module.parts.length + 1, work_minutes: 10 },
        }),
      { success: "بخش اضافه شد" },
    );
    if (saved) setExam(saved);
  }

  async function removePart(module: ExamModule, part: ExamPart) {
    if (!confirm(`Teil ${part.number} حذف شود؟`)) return;
    const saved = await run(
      () =>
        call<AdminExam>(`${base}/modules/${module.index}/parts/${part.index}`, {
          method: "DELETE",
        }),
      { success: "بخش حذف شد" },
    );
    if (saved) setExam(saved);
  }

  function openItems(module: ExamModule, part: ExamPart) {
    setEditing({ module: module.index, part: part.index });
    setItems(
      part.items.length
        ? part.items.map((item) => ({ ...item, options: item.options.map((o) => ({ ...o })) }))
        : [],
    );
  }

  const activePart =
    editing !== null ? modules[editing.module]?.parts[editing.part] : undefined;
  const textPart =
    editingText !== null ? modules[editingText.module]?.parts[editingText.part] : undefined;

  async function savePartContent(payload: Record<string, unknown>) {
    if (!editingText) return;
    const saved = await run(
      () =>
        call<AdminExam>(
          `${base}/modules/${editingText.module}/parts/${editingText.part}`,
          { method: "PATCH", body: payload },
        ),
      { success: "متن بخش ذخیره شد" },
    );
    if (saved) {
      setExam(saved);
      setEditingText(null);
    }
  }

  /** Upload one listening file and hand back the URL the player will use. */
  async function uploadTrack(file: File) {
    const body = new FormData();
    body.append("file", file);
    try {
      const response = await fetch("/api/admin/upload?kind=audio", { method: "POST", body });
      const payload = (await response.json()) as { url?: string; detail?: string };
      if (!response.ok || !payload.url) throw new Error(payload.detail || "آپلود نشد");
      return payload.url;
    } catch (caught) {
      notify((caught as Error).message, "error");
      return null;
    }
  }

  function addItem() {
    if (!activePart) return;
    const usesSharedPool = activePart.options.length > 0;
    const nextNumber = (items.at(-1)?.number ?? 0) + 1;
    setItems([
      ...items,
      {
        number: nextNumber,
        prompt: "",
        answer: "",
        points: 1,
        audio_index: null,
        explanation: { fa: "", en: "", de: "" },
        options: usesSharedPool
          ? []
          : ["a", "b", "c"].map((key) => ({ key, label: key, text: "" })),
      },
    ]);
  }

  function patchItem(index: number, patch: Partial<ExamItem>) {
    setItems(items.map((item, i) => (i === index ? { ...item, ...patch } : item)));
  }

  async function saveItems() {
    if (editing === null) return;
    const invalid = items.find(
      (item) => !item.prompt.trim() || (!item.answer && activePart?.type !== "writing"),
    );
    if (invalid) {
      notify(`سؤال ${invalid.number}: متن و پاسخ درست را کامل کن`, "error");
      return;
    }
    const saved = await run(
      () =>
        call<AdminExam>(`${base}/modules/${editing.module}/parts/${editing.part}/items`, {
          method: "PUT",
          body: { items },
        }),
      { success: "سؤال‌ها ذخیره شد" },
    );
    if (saved) {
      setExam(saved);
      setEditing(null);
    }
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div className="min-w-0">
          <Link
            href={backHref ?? `/${locale}/admin/exams`}
            className="text-xs text-mist-500 hover:text-mist-200"
          >
            ← {backHref ? "بازگشت به آزمون" : "همه آزمون‌ها"}
          </Link>
          <h1 className="font-display mt-2 truncate text-2xl font-semibold">
            {title ?? exam.title.fa ?? exam.title.en ?? exam.slug}
          </h1>
          <p className="tnum mt-1 text-xs text-mist-500" dir="ltr">
            {exam.slug} · {exam.level} · {formatNumber(exam.questions_count, locale)} سؤال
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {SKILLS.filter((skill) => !modules.some((module) => module.skill === skill)).map(
            (skill) => (
              <Button key={skill} size="sm" variant="soft" onClick={() => addModule(skill)}>
                + {MODULE_LABELS[skill].split(" — ")[0]}
              </Button>
            ),
          )}
        </div>
      </header>

      {modules.length ? (
        modules.map((module) => (
          <Panel
            key={module.skill}
            title={MODULE_LABELS[module.skill] ?? module.skill}
            action={
              <div className="flex flex-wrap items-center gap-2">
                <span className="tnum text-xs text-mist-500">
                  {formatNumber(module.duration_minutes, locale)} دقیقه
                </span>
                <Select
                  value=""
                  onChange={(event) => event.target.value && addPart(module, event.target.value)}
                  className="w-44"
                  aria-label="افزودن بخش"
                >
                  <option value="" className="bg-ink-900">+ بخش جدید…</option>
                  {Object.entries(PART_TYPE_LABELS).map(([type, label]) => (
                    <option key={type} value={type} className="bg-ink-900">{label}</option>
                  ))}
                </Select>
                <button
                  type="button"
                  onClick={() => removeModule(module)}
                  className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                >
                  حذف ماژول
                </button>
              </div>
            }
          >
            {module.parts.length ? (
              <ul className="space-y-2">
                {module.parts.map((part) => (
                  <li
                    key={part.index}
                    className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/8 px-4 py-3"
                  >
                    <span className="tnum grid size-8 shrink-0 place-items-center rounded-lg bg-white/8 text-xs font-semibold">
                      {formatNumber(part.number, locale)}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block truncate text-sm font-medium">
                        {part.title.fa || part.title.de || `Teil ${part.number}`}
                      </span>
                      <span className="block truncate text-xs text-mist-600">
                        {PART_TYPE_LABELS[part.type] ?? part.type} ·{" "}
                        {formatNumber(part.items.length, locale)} سؤال
                        {part.blocks.length
                          ? ` · ${formatNumber(part.blocks.length, locale)} بلوک متن`
                          : ""}
                        {part.options.length
                          ? ` · ${formatNumber(part.options.length, locale)} گزینه مشترک`
                          : ""}
                        {part.audio.length
                          ? ` · ${formatNumber(part.audio.length, locale)} فایل صوتی`
                          : ""}
                      </span>
                    </span>
                    <Button
                      size="sm"
                      variant="soft"
                      onClick={() =>
                        setEditingText({ module: module.index, part: part.index })
                      }
                    >
                      متن
                    </Button>
                    <Button size="sm" variant="soft" onClick={() => openItems(module, part)}>
                      سؤال‌ها
                    </Button>
                    <button
                      type="button"
                      onClick={() => removePart(module, part)}
                      className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                    >
                      حذف
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-mist-500">
                هنوز بخشی ندارد — از منوی «+ بخش جدید» یکی اضافه کن.
              </p>
            )}
          </Panel>
        ))
      ) : (
        <Empty
          title="این آزمون هنوز ماژول ندارد"
          body="با دکمه‌های بالا ماژول Lesen یا Hören اضافه کن."
          icon="◇"
        />
      )}

      <PartContentEditor
        open={editingText !== null}
        part={textPart}
        busy={busy}
        onClose={() => setEditingText(null)}
        onSave={savePartContent}
        onUpload={uploadTrack}
      />

      {/* ------------------------------------------------------ item editor */}
      <Modal
        open={editing !== null}
        wide
        title={`سؤال‌های ${activePart ? PART_TYPE_LABELS[activePart.type] ?? activePart.type : ""}`}
        onClose={() => setEditing(null)}
      >
        {activePart ? (
          <div className="space-y-5">
            {activePart.options.length ? (
              <p className="rounded-2xl border border-cyan-400/25 bg-cyan-400/5 px-4 py-3 text-xs text-mist-300">
                این بخش گزینه‌های مشترک دارد ({activePart.options.map((o) => o.key).join("، ")}) —
                برای هر سؤال فقط کافی است حرف پاسخ درست را انتخاب کنی.
              </p>
            ) : null}

            {items.length ? (
              <ul className="space-y-4">
                {items.map((item, index) => {
                  const pool = item.options.length ? item.options : activePart.options;
                  return (
                    <li key={index} className="rounded-2xl border border-white/10 p-4">
                      <div className="mb-3 flex items-center gap-3">
                        <Input
                          type="number"
                          dir="ltr"
                          className="tnum w-20"
                          value={item.number}
                          onChange={(e) =>
                            patchItem(index, { number: Number(e.target.value) || index + 1 })
                          }
                          aria-label="شماره"
                        />
                        <span className="text-xs text-mist-500">شماره سؤال</span>
                        <button
                          type="button"
                          onClick={() => setItems(items.filter((_, i) => i !== index))}
                          className="ms-auto rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                        >
                          حذف سؤال
                        </button>
                      </div>

                      <Field label="متن سؤال (آلمانی)">
                        <Textarea
                          value={item.prompt}
                          dir="ltr"
                          lang="de"
                          onChange={(e) => patchItem(index, { prompt: e.target.value })}
                        />
                      </Field>

                      {item.options.length ? (
                        <div className="mt-4 space-y-2">
                          <span className="block text-xs text-mist-400">
                            گزینه‌ها — روی دایره بزن تا پاسخ درست مشخص شود
                          </span>
                          {item.options.map((option, optionIndex) => (
                            <div key={optionIndex} className="flex items-center gap-3">
                              <button
                                type="button"
                                onClick={() => patchItem(index, { answer: option.key })}
                                className="grid size-6 shrink-0 place-items-center rounded-full border transition"
                                style={{
                                  borderColor:
                                    item.answer === option.key ? "#34d399" : "rgba(255,255,255,0.2)",
                                  background: item.answer === option.key ? "#34d399" : "transparent",
                                }}
                                aria-label={`پاسخ درست: ${option.key}`}
                              >
                                {item.answer === option.key ? (
                                  <span className="text-[10px] text-ink-950">✓</span>
                                ) : null}
                              </button>
                              <span className="w-5 text-xs font-bold text-mist-500">
                                {option.key}
                              </span>
                              <Input
                                value={option.text}
                                dir="ltr"
                                lang="de"
                                onChange={(e) => {
                                  const options = item.options.map((o, i) =>
                                    i === optionIndex ? { ...o, text: e.target.value } : o,
                                  );
                                  patchItem(index, { options });
                                }}
                              />
                              <button
                                type="button"
                                onClick={() =>
                                  patchItem(index, {
                                    options: item.options.filter((_, i) => i !== optionIndex),
                                    answer: item.answer === option.key ? "" : item.answer,
                                  })
                                }
                                className="text-xs text-mist-600 hover:text-rose-400"
                                aria-label="حذف گزینه"
                              >
                                ✕
                              </button>
                            </div>
                          ))}
                          <button
                            type="button"
                            onClick={() => {
                              const used = item.options.map((o) => o.key);
                              const key = LETTERS.find((letter) => !used.includes(letter));
                              if (!key) return;
                              patchItem(index, {
                                options: [...item.options, { key, label: key, text: "" }],
                              });
                            }}
                            className="glass rounded-full px-4 py-1.5 text-xs"
                          >
                            + گزینه
                          </button>
                        </div>
                      ) : (
                        <Field label="پاسخ درست" hint="یکی از گزینه‌های مشترک این بخش">
                          <Select
                            value={item.answer}
                            onChange={(e) => patchItem(index, { answer: e.target.value })}
                          >
                            <option value="" className="bg-ink-900">—</option>
                            {pool.map((option) => (
                              <option key={option.key} value={option.key} className="bg-ink-900">
                                {option.key} — {option.label || option.text.slice(0, 40)}
                              </option>
                            ))}
                          </Select>
                        </Field>
                      )}

                      <div className="mt-4">
                        <TranslatedField
                          label="توضیح پاسخ (در کارنامه نشان داده می‌شود)"
                          value={item.explanation}
                          onChange={(explanation) => patchItem(index, { explanation })}
                        />
                      </div>
                    </li>
                  );
                })}
              </ul>
            ) : (
              <p className="text-sm text-mist-500">هنوز سؤالی ندارد.</p>
            )}

            <div className="flex flex-wrap gap-3 border-t border-white/8 pt-5">
              <Button variant="soft" onClick={addItem}>+ سؤال جدید</Button>
              <Button onClick={saveItems} disabled={busy} className="flex-1">
                {busy ? "…" : "ذخیره سؤال‌ها"}
              </Button>
              <Button variant="outline" onClick={() => setEditing(null)}>انصراف</Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <Toast message={toast.message} tone={toast.tone} />
    </div>
  );
}
