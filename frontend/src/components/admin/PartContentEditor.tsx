"use client";

import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Field, Input, Select, Textarea } from "@/components/ui/Field";
import type { ExamPart } from "@/lib/admin";
import { mediaUrl } from "@/lib/utils";
import { PART_TYPE_LABELS } from "@/lib/admin";

import { Modal, TranslatedField } from "./ui";

type Block = ExamPart["blocks"][number];
type Option = ExamPart["options"][number];
type Track = ExamPart["audio"][number];

/** What the left-hand panel shows for each block kind. */
const BLOCK_KINDS: Record<string, string> = {
  paragraph: "پاراگراف متن",
  person: "شخص (نام + متن)",
  statement: "اظهار نظر (نام + متن)",
  heading: "عنوان/آگهی (برچسب + متن)",
  section: "بند شماره‌دار (§ / جای خالی)",
  bullet: "مورد فهرست",
};

/** A one-line reminder of what each task type needs, shown above the form. */
const RECIPES: Record<string, string> = {
  match_person:
    "برای هر شخص یک بلوک از نوع «شخص» بساز (برچسب = a, b, c…) و همان حرف‌ها را در «گزینه‌های مشترک» تکرار کن. هر سؤال فقط یک جمله است و پاسخش حرف همان شخص.",
  match_heading:
    "متن‌ها یا آگهی‌ها را به‌صورت بلوک بنویس و عنوان‌ها را در «گزینه‌های مشترک» بگذار (a تا h). چند گزینه اضافه بگذار تا تسک واقعی شود.",
  match_paragraph:
    "هر پاراگراف مقاله یک بلوک است (برچسب = شماره پاراگراف) و عنوان‌های پیشنهادی در «گزینه‌های مشترک».",
  gap_drag:
    "متن اصلی را در بلوک‌ها بنویس و هر جای خالی را با [[شماره]] علامت بزن — مثلاً [[27]]. گزینه‌های قابل کشیدن در «گزینه‌های مشترک» می‌روند، و شماره داخل متن باید دقیقاً با شماره سؤال یکی باشد وگرنه آن جای خالی کار نمی‌کند.",
  mcq: "اگر متن خواندنی دارد در بلوک‌ها بنویس. گزینه‌ها را می‌توانی برای هر سؤال جدا بگذاری یا از «گزینه‌های مشترک» استفاده کنی.",
  listening_mixed:
    "فایل صوتی را در «صوت» اضافه کن و شماره سؤال‌هایی که به آن مربوط‌اند را بنویس. سؤال‌ها ترکیبی از درست/غلط و سه‌گزینه‌ای‌اند.",
  writing:
    "صورت تکلیف را در «متن مقدمه» بنویس و نکته‌هایی که باید پوشش داده شوند را به‌صورت بلوک «مورد فهرست» اضافه کن.",
};

const EMPTY_BLOCK: Block = { kind: "paragraph", label: "", title: "", text: "", author: "", image: "" };

/** Upload or clear one picture, with a thumbnail once it is set. */
function PictureField({
  label,
  value,
  onChange,
  onUpload,
}: {
  label: string;
  value: string;
  onChange: (url: string) => void;
  onUpload: (file: File) => Promise<string | null>;
}) {
  return (
    <div>
      <span className="mb-2 block text-xs font-medium tracking-wide text-mist-400">{label}</span>
      <div className="flex flex-wrap items-center gap-3">
        <label className="cursor-pointer rounded-full border border-white/15 px-4 py-2 text-xs transition hover:bg-white/5">
          {value ? "تغییر عکس" : "آپلود عکس"}
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={async (event) => {
              const file = event.target.files?.[0];
              if (!file) return;
              const url = await onUpload(file);
              if (url) onChange(url);
              event.target.value = "";
            }}
          />
        </label>
        {value ? (
          <>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={mediaUrl(value)}
              alt=""
              className="h-14 w-20 rounded-lg border border-white/10 object-cover"
            />
            <button
              type="button"
              onClick={() => onChange("")}
              className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
            >
              حذف عکس
            </button>
          </>
        ) : null}
      </div>
    </div>
  );
}

export function PartContentEditor({
  open,
  part,
  onClose,
  onSave,
  busy,
  onUpload,
  onUploadImage,
}: {
  open: boolean;
  part: ExamPart | undefined;
  onClose: () => void;
  onSave: (payload: Record<string, unknown>) => void;
  busy: boolean;
  onUpload: (file: File) => Promise<string | null>;
  onUploadImage: (file: File) => Promise<string | null>;
}) {
  const [draft, setDraft] = useState<ExamPart | null>(() => (part ? structuredClone(part) : null));
  const [loaded, setLoaded] = useState(part);

  // Reload whenever a different Teil is opened, so edits never leak across parts.
  if (part !== loaded) {
    setLoaded(part);
    setDraft(part ? structuredClone(part) : null);
  }

  if (!draft) return null;

  const patch = (next: Partial<ExamPart>) => setDraft({ ...draft, ...next });
  const patchBlock = (index: number, next: Partial<Block>) =>
    patch({ blocks: draft.blocks.map((b, i) => (i === index ? { ...b, ...next } : b)) });
  const patchOption = (index: number, next: Partial<Option>) =>
    patch({ options: draft.options.map((o, i) => (i === index ? { ...o, ...next } : o)) });
  const patchTrack = (index: number, next: Partial<Track>) =>
    patch({ audio: draft.audio.map((t, i) => (i === index ? { ...t, ...next } : t)) });

  const move = (list: "blocks" | "options", index: number, delta: number) => {
    const next = [...draft[list]];
    const target = index + delta;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    patch({ [list]: next } as Partial<ExamPart>);
  };

  const label = PART_TYPE_LABELS[draft.type] ?? draft.type;

  return (
    <Modal open={open} wide title={`متن و محتوای ${label}`} onClose={onClose}>
      <div className="space-y-6">
        {RECIPES[draft.type] ? (
          <p className="rounded-2xl border border-cyan-400/25 bg-cyan-400/5 px-4 py-3 text-xs leading-6 text-mist-300">
            {RECIPES[draft.type]}
          </p>
        ) : null}

        {/* ------------------------------------------------ Teil settings */}
        <section className="space-y-4 rounded-2xl border border-white/10 p-4">
          <p className="text-sm font-medium text-white">مشخصات بخش</p>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="نوع تسک">
              <Select value={draft.type} onChange={(e) => patch({ type: e.target.value })}>
                {Object.entries(PART_TYPE_LABELS).map(([value, text]) => (
                  <option key={value} value={value}>
                    {text}
                  </option>
                ))}
              </Select>
            </Field>
            <Field label="زمان کار (دقیقه)">
              <Input
                type="number"
                value={draft.work_minutes}
                onChange={(e) => patch({ work_minutes: Number(e.target.value) || 1 })}
              />
            </Field>
          </div>
          <TranslatedField
            label="عنوان بخش"
            value={draft.title}
            onChange={(title) => patch({ title })}
          />
          <TranslatedField
            label="صورت تسک (Anweisung)"
            multiline
            value={draft.instructions}
            onChange={(instructions) => patch({ instructions })}
          />
        </section>

        {/* --------------------------------------------- stimulus heading */}
        <section className="space-y-4 rounded-2xl border border-white/10 p-4">
          <p className="text-sm font-medium text-white">سربرگ متن</p>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="عنوان متن (بالای پنل راست)">
              <Input
                dir="ltr"
                value={draft.stimulus_title}
                onChange={(e) => patch({ stimulus_title: e.target.value })}
              />
            </Field>
            <Field label="زیرعنوان">
              <Input
                dir="ltr"
                value={draft.stimulus_subtitle}
                onChange={(e) => patch({ stimulus_subtitle: e.target.value })}
              />
            </Field>
          </div>
          <PictureField
            label="عکس کل بخش (بالای متن نمایش داده می‌شود)"
            value={draft.stimulus_image ?? ""}
            onChange={(stimulus_image) => patch({ stimulus_image })}
            onUpload={onUploadImage}
          />
          <Field label="متن مقدمه (اختیاری — بالای بلوک‌ها می‌آید)">
            <Textarea
              dir="ltr"
              rows={3}
              value={draft.stimulus_intro}
              onChange={(e) => patch({ stimulus_intro: e.target.value })}
            />
          </Field>
        </section>

        {/* ------------------------------------------------------- blocks */}
        <section className="space-y-3 rounded-2xl border border-white/10 p-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-sm font-medium text-white">متن‌ها و بلوک‌ها</p>
              <p className="mt-1 text-xs text-mist-600">
                همان چیزی که در پنل سمت راست آزمون دیده می‌شود.
              </p>
            </div>
            <Button
              size="sm"
              variant="soft"
              onClick={() => patch({ blocks: [...draft.blocks, { ...EMPTY_BLOCK }] })}
            >
              + بلوک
            </Button>
          </div>

          {draft.blocks.map((block, index) => (
            <div key={index} className="space-y-3 rounded-xl bg-white/[0.03] p-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs text-mist-600">#{index + 1}</span>
                <Select
                  className="max-w-48"
                  value={block.kind}
                  onChange={(e) => patchBlock(index, { kind: e.target.value })}
                >
                  {Object.entries(BLOCK_KINDS).map(([value, text]) => (
                    <option key={value} value={value}>
                      {text}
                    </option>
                  ))}
                </Select>
                <span className="flex-1" />
                <button
                  type="button"
                  onClick={() => move("blocks", index, -1)}
                  className="px-2 text-xs text-mist-500 hover:text-white"
                  aria-label="بالا"
                >
                  ▲
                </button>
                <button
                  type="button"
                  onClick={() => move("blocks", index, 1)}
                  className="px-2 text-xs text-mist-500 hover:text-white"
                  aria-label="پایین"
                >
                  ▼
                </button>
                <button
                  type="button"
                  onClick={() => patch({ blocks: draft.blocks.filter((_, i) => i !== index) })}
                  className="rounded-full px-3 py-1 text-xs text-rose-400 transition hover:bg-rose-400/10"
                >
                  حذف
                </button>
              </div>

              <div className="grid gap-3 sm:grid-cols-2">
                <Field label="برچسب (a، b، ۱، § 28…)">
                  <Input
                    dir="ltr"
                    value={block.label}
                    onChange={(e) => patchBlock(index, { label: e.target.value })}
                  />
                </Field>
                <Field label="عنوان / نام شخص">
                  <Input
                    dir="ltr"
                    value={block.title}
                    onChange={(e) => patchBlock(index, { title: e.target.value })}
                  />
                </Field>
              </div>
              <Field
                label="متن آلمانی"
                hint={
                  draft.type === "gap_drag"
                    ? "جای خالی را این‌طور بنویس: [[27]] — شماره باید با شماره سؤال یکی باشد."
                    : undefined
                }
              >
                <Textarea
                  dir="ltr"
                  rows={6}
                  value={block.text}
                  onChange={(e) => patchBlock(index, { text: e.target.value })}
                />
              </Field>
              <Field label="امضا / منبع (اختیاری — مثلاً «Amelie, Bonn»)">
                <Input
                  dir="ltr"
                  value={block.author}
                  onChange={(e) => patchBlock(index, { author: e.target.value })}
                />
              </Field>
              <PictureField
                label="عکس این بلوک (تابلو، آگهی، تصویر)"
                value={block.image ?? ""}
                onChange={(image) => patchBlock(index, { image })}
                onUpload={onUploadImage}
              />
            </div>
          ))}

          {draft.blocks.length === 0 ? (
            <p className="text-xs text-mist-600">هنوز بلوکی ندارد.</p>
          ) : null}
        </section>

        {/* ------------------------------------------------- shared pool */}
        <section className="space-y-3 rounded-2xl border border-white/10 p-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-sm font-medium text-white">گزینه‌های مشترک</p>
              <p className="mt-1 text-xs text-mist-600">
                برای تسک‌های تطبیقی و جای خالی — همه سؤال‌ها از همین فهرست انتخاب می‌کنند.
              </p>
            </div>
            <Button
              size="sm"
              variant="soft"
              onClick={() =>
                patch({
                  options: [
                    ...draft.options,
                    {
                      key: "abcdefghij"[draft.options.length] ?? "",
                      label: "abcdefghij"[draft.options.length] ?? "",
                      text: "",
                      author: "",
                    },
                  ],
                })
              }
            >
              + گزینه
            </Button>
          </div>

          {draft.options.map((option, index) => (
            <div key={index} className="flex flex-wrap items-end gap-2 rounded-xl bg-white/[0.03] p-3">
              <div className="w-16">
                <Field label="کلید">
                  <Input
                    dir="ltr"
                    value={option.key}
                    onChange={(e) => patchOption(index, { key: e.target.value })}
                  />
                </Field>
              </div>
              <div className="w-24">
                <Field label="برچسب">
                  <Input
                    dir="ltr"
                    value={option.label}
                    onChange={(e) => patchOption(index, { label: e.target.value })}
                  />
                </Field>
              </div>
              <div className="min-w-56 flex-1">
                <Field label="متن گزینه">
                  <Input
                    dir="ltr"
                    value={option.text}
                    onChange={(e) => patchOption(index, { text: e.target.value })}
                  />
                </Field>
              </div>
              <button
                type="button"
                onClick={() => patch({ options: draft.options.filter((_, i) => i !== index) })}
                className="rounded-full px-3 py-2 text-xs text-rose-400 transition hover:bg-rose-400/10"
              >
                حذف
              </button>
              <div className="w-full">
                <PictureField
                  label="عکس گزینه (برای تسک‌های تصویری A1)"
                  value={option.image ?? ""}
                  onChange={(image) => patchOption(index, { image })}
                  onUpload={onUploadImage}
                />
              </div>
            </div>
          ))}
        </section>

        {/* ------------------------------------------------------- audio */}
        <section className="space-y-3 rounded-2xl border border-white/10 p-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-sm font-medium text-white">فایل‌های صوتی</p>
              <p className="mt-1 text-xs text-mist-600">
                تعداد دفعات پخش و ثانیه‌های پیش‌مطالعه، دقیقاً مثل آزمون واقعی.
              </p>
            </div>
            <Button
              size="sm"
              variant="soft"
              onClick={() =>
                patch({
                  audio: [
                    ...draft.audio,
                    { label: "", url: "", plays: 1, pre_read_seconds: 20, covers: [] },
                  ],
                })
              }
            >
              + فایل صوتی
            </Button>
          </div>

          {draft.audio.map((track, index) => (
            <div key={index} className="space-y-3 rounded-xl bg-white/[0.03] p-3">
              <div className="grid gap-3 sm:grid-cols-2">
                <Field label="برچسب">
                  <Input
                    dir="ltr"
                    value={track.label}
                    onChange={(e) => patchTrack(index, { label: e.target.value })}
                  />
                </Field>
                <Field label="آدرس فایل">
                  <Input
                    dir="ltr"
                    value={track.url}
                    onChange={(e) => patchTrack(index, { url: e.target.value })}
                  />
                </Field>
              </div>
              <div className="grid gap-3 sm:grid-cols-3">
                <Field label="دفعات مجاز پخش">
                  <Select
                    value={String(track.plays)}
                    onChange={(e) => patchTrack(index, { plays: Number(e.target.value) })}
                  >
                    <option value="1">یک بار</option>
                    <option value="2">دو بار</option>
                    <option value="3">سه بار</option>
                  </Select>
                </Field>
                <Field label="پیش‌مطالعه (ثانیه)">
                  <Input
                    type="number"
                    value={track.pre_read_seconds}
                    onChange={(e) =>
                      patchTrack(index, { pre_read_seconds: Number(e.target.value) || 0 })
                    }
                  />
                </Field>
                <Field label="شماره سؤال‌ها (با ویرگول)">
                  <Input
                    dir="ltr"
                    value={track.covers.join(", ")}
                    onChange={(e) =>
                      patchTrack(index, {
                        covers: e.target.value
                          .split(",")
                          .map((n) => Number(n.trim()))
                          .filter((n) => Number.isFinite(n) && n > 0),
                      })
                    }
                  />
                </Field>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <label className="cursor-pointer rounded-full border border-white/15 px-4 py-2 text-xs transition hover:bg-white/5">
                  آپلود فایل
                  <input
                    type="file"
                    accept="audio/*"
                    className="hidden"
                    onChange={async (event) => {
                      const file = event.target.files?.[0];
                      if (!file) return;
                      const url = await onUpload(file);
                      if (url) patchTrack(index, { url });
                      event.target.value = "";
                    }}
                  />
                </label>
                {track.url ? (
                  // eslint-disable-next-line jsx-a11y/media-has-caption
                  <audio controls src={track.url} className="h-9 max-w-72" />
                ) : null}
                <span className="flex-1" />
                <button
                  type="button"
                  onClick={() => patch({ audio: draft.audio.filter((_, i) => i !== index) })}
                  className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                >
                  حذف
                </button>
              </div>
            </div>
          ))}
        </section>

        {/* ------------------------------------------- example and writing */}
        <section className="grid gap-4 rounded-2xl border border-white/10 p-4 sm:grid-cols-2">
          <Field label="نمونه (صورت)">
            <Input
              dir="ltr"
              value={draft.example_prompt}
              onChange={(e) => patch({ example_prompt: e.target.value })}
            />
          </Field>
          <Field label="نمونه (پاسخ)">
            <Input
              dir="ltr"
              value={draft.example_answer}
              onChange={(e) => patch({ example_answer: e.target.value })}
            />
          </Field>
          {draft.type === "writing" ? (
            <Field label="حداقل تعداد کلمه">
              <Input
                type="number"
                value={draft.min_words ?? 0}
                onChange={(e) => patch({ min_words: Number(e.target.value) || 0 })}
              />
            </Field>
          ) : null}
        </section>

        <div className="flex justify-end gap-3">
          <Button variant="ghost" onClick={onClose}>
            انصراف
          </Button>
          <Button
            disabled={busy}
            onClick={() =>
              onSave({
                type: draft.type,
                title: draft.title,
                instructions: draft.instructions,
                work_minutes: draft.work_minutes,
                stimulus_title: draft.stimulus_title,
                stimulus_subtitle: draft.stimulus_subtitle,
                stimulus_intro: draft.stimulus_intro,
                stimulus_image: draft.stimulus_image,
                blocks: draft.blocks,
                options: draft.options,
                audio: draft.audio,
                example_prompt: draft.example_prompt,
                example_answer: draft.example_answer,
                min_words: draft.min_words,
              })
            }
          >
            ذخیره متن
          </Button>
        </div>
      </div>
    </Modal>
  );
}
