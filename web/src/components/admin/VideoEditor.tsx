"use client";

import { useRef, useState } from "react";

import { Button } from "@/components/ui/Button";
import { Field, Input, Select, Textarea } from "@/components/ui/Field";
import type { AdminQuestion, AdminVideo, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED, LEVELS, emptyQuestion, linesToList, listToLines } from "@/lib/admin";
import { mediaUrl } from "@/lib/utils";

import { ImageUpload } from "./ImageUpload";
import { TranslatedField } from "./ui";

export interface VideoDraft {
  id?: string;
  title: Translated;
  title_de: string;
  scene_label: string;
  description: Translated;
  video_url: string;
  poster_url: string;
  duration_seconds: number;
  cefr_level: string;
  is_published: boolean;
  hasQuestion: boolean;
  question: AdminQuestion;
}

export const blankVideo = (): VideoDraft => ({
  title: { ...EMPTY_TRANSLATED },
  title_de: "",
  scene_label: "",
  description: { ...EMPTY_TRANSLATED },
  video_url: "",
  poster_url: "",
  duration_seconds: 0,
  cefr_level: "A2",
  is_published: true,
  hasQuestion: true,
  question: emptyQuestion(),
});

export const toDraft = (video: AdminVideo): VideoDraft => ({
  id: video.id,
  title: video.title,
  title_de: video.title_de,
  scene_label: video.scene_label,
  description: video.description,
  video_url: video.video_url,
  poster_url: video.poster_url,
  duration_seconds: video.duration_seconds,
  cefr_level: video.cefr_level,
  is_published: video.is_published,
  hasQuestion: !!video.question,
  question: video.question ?? emptyQuestion(),
});

/**
 * The lesson form. The lower half is the speaking prompt — exactly the text and
 * hints that get sent to the AI teacher — so it is labelled as such rather than
 * hidden among the metadata.
 */
export function VideoEditor({
  draft,
  onChange,
  courseSlug,
  onError,
}: {
  draft: VideoDraft;
  onChange: (next: VideoDraft) => void;
  courseSlug: string;
  onError: (message: string) => void;
}) {
  const fileInput = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const patchQuestion = (patch: Partial<AdminQuestion>) =>
    onChange({ ...draft, question: { ...draft.question, ...patch } });

  function upload(file: File) {
    setUploading(true);
    setProgress(0);

    // XHR rather than fetch: a 300 MB lesson needs a real progress bar.
    const form = new FormData();
    form.append("file", file);
    form.append("course_slug", courseSlug);

    const request = new XMLHttpRequest();
    request.open("POST", "/api/admin/upload");
    request.upload.onprogress = (event) => {
      if (event.lengthComputable) setProgress(Math.round((event.loaded / event.total) * 100));
    };
    request.onload = () => {
      setUploading(false);
      try {
        const body = JSON.parse(request.responseText);
        if (request.status >= 400) {
          onError(body.detail || "آپلود ناموفق بود");
          return;
        }
        onChange({
          ...draft,
          video_url: body.url,
          duration_seconds: body.duration_seconds || draft.duration_seconds,
        });
      } catch {
        onError("پاسخ آپلود نامعتبر بود");
      }
    };
    request.onerror = () => {
      setUploading(false);
      onError("ارتباط با سرور قطع شد");
    };
    request.send(form);
  }

  return (
    <div className="space-y-6">
      {/* ------------------------------------------------------------ file */}
      <div className="rounded-2xl border border-white/10 bg-white/3 p-5">
        <p className="mb-3 text-xs font-semibold tracking-wider text-mist-400 uppercase">
          فایل ویدیو
        </p>

        {draft.video_url ? (
          <div className="space-y-3">
            <video
              src={mediaUrl(draft.video_url)}
              controls
              className="max-h-56 w-full rounded-xl bg-black"
            >
              <track kind="captions" />
            </video>
            <p className="tnum text-xs text-mist-500" dir="ltr">
              {draft.video_url} · {draft.duration_seconds}s
            </p>
          </div>
        ) : (
          <p className="text-sm text-mist-500">هنوز فایلی انتخاب نشده است.</p>
        )}

        <input
          ref={fileInput}
          type="file"
          accept="video/mp4,video/webm,video/quicktime"
          className="hidden"
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) upload(file);
            event.target.value = "";
          }}
        />

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <Button
            type="button"
            variant="soft"
            size="sm"
            disabled={uploading}
            onClick={() => fileInput.current?.click()}
          >
            {uploading ? `در حال آپلود… ${progress}%` : draft.video_url ? "تعویض فایل" : "انتخاب فایل"}
          </Button>
          {uploading ? (
            <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/10">
              <div
                className="h-full rounded-full bg-linear-to-r from-violet-500 to-cyan-400 transition-[width]"
                style={{ width: `${progress}%` }}
              />
            </div>
          ) : null}
        </div>
      </div>

      {/* -------------------------------------------------------- metadata */}
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="عنوان آلمانی" hint="در پخش‌کننده نشان داده می‌شود">
          <Input
            value={draft.title_de}
            dir="ltr"
            lang="de"
            onChange={(event) => onChange({ ...draft, title_de: event.target.value })}
          />
        </Field>
        <Field label="برچسب صحنه" hint="مثلاً SZENE 4 – ANKUNFT">
          <Input
            value={draft.scene_label}
            dir="ltr"
            onChange={(event) => onChange({ ...draft, scene_label: event.target.value })}
          />
        </Field>
        <Field label="سطح زبانی">
          <Select
            value={draft.cefr_level}
            onChange={(event) => onChange({ ...draft, cefr_level: event.target.value })}
          >
            {LEVELS.map((level) => (
              <option key={level} value={level} className="bg-ink-900">
                {level}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="مدت (ثانیه)" hint="هنگام آپلود خودکار پر می‌شود">
          <Input
            type="number"
            dir="ltr"
            className="tnum"
            value={draft.duration_seconds}
            onChange={(event) =>
              onChange({ ...draft, duration_seconds: Number(event.target.value) || 0 })
            }
          />
        </Field>
      </div>

      <TranslatedField
        label="عنوان (سه‌زبانه)"
        value={draft.title}
        onChange={(title) => onChange({ ...draft, title })}
      />

      <ImageUpload
        label="تصویر شاخص ویدیو (پوستر)"
        value={draft.poster_url}
        folder="lessons"
        onChange={(poster_url) => onChange({ ...draft, poster_url })}
        onError={onError}
        hint="قبل از شروع پخش نشان داده می‌شود. اختیاری است."
      />

      <label className="flex items-center gap-3 text-sm text-mist-300">
        <input
          type="checkbox"
          checked={draft.is_published}
          onChange={(event) => onChange({ ...draft, is_published: event.target.checked })}
          className="size-4 accent-violet-500"
        />
        منتشر شود
      </label>

      {/* --------------------------------------------------- speaking task */}
      <div className="rounded-2xl border border-cyan-400/25 bg-cyan-400/5 p-5">
        <label className="flex items-center gap-3 text-sm font-semibold">
          <input
            type="checkbox"
            checked={draft.hasQuestion}
            onChange={(event) => onChange({ ...draft, hasQuestion: event.target.checked })}
            className="size-4 accent-cyan-400"
          />
          این ویدیو تمرین گفتاری دارد
        </label>
        <p className="mt-1.5 ps-7 text-xs text-mist-500">
          اگر خاموش باشد، بعد از ویدیو میکروفون باز نمی‌شود (مثل صحنه‌های ۱ تا ۳).
        </p>

        {draft.hasQuestion ? (
          <div className="mt-5 space-y-4">
            <Field
              label="متن سؤال (آلمانی)"
              hint="همین متن برای هوش مصنوعی فرستاده می‌شود"
            >
              <Textarea
                value={draft.question.prompt_de}
                dir="ltr"
                lang="de"
                onChange={(event) => patchQuestion({ prompt_de: event.target.value })}
              />
            </Field>

            <TranslatedField
              label="ترجمه سؤال (اختیاری)"
              value={draft.question.prompt}
              onChange={(prompt) => patchQuestion({ prompt })}
            />
            <TranslatedField
              label="راهنمایی برای زبان‌آموز"
              value={draft.question.hint}
              onChange={(hint) => patchQuestion({ hint })}
            />

            <div className="grid gap-4 sm:grid-cols-3">
              <Field label="نکات مورد انتظار" hint="هر خط یک مورد">
                <Textarea
                  value={listToLines(draft.question.expected_points)}
                  onChange={(event) =>
                    patchQuestion({ expected_points: linesToList(event.target.value) })
                  }
                />
              </Field>
              <Field label="موضوعات گرامری" hint="هر خط یک مورد">
                <Textarea
                  value={listToLines(draft.question.grammar_topics)}
                  dir="ltr"
                  onChange={(event) =>
                    patchQuestion({ grammar_topics: linesToList(event.target.value) })
                  }
                />
              </Field>
              <Field label="واژگان پیشنهادی" hint="هر خط یک واژه">
                <Textarea
                  value={listToLines(draft.question.vocabulary)}
                  dir="ltr"
                  lang="de"
                  onChange={(event) =>
                    patchQuestion({ vocabulary: linesToList(event.target.value) })
                  }
                />
              </Field>
            </div>

            <Field label="حداقل تعداد کلمه">
              <Input
                type="number"
                dir="ltr"
                className="tnum w-32"
                value={draft.question.min_words}
                onChange={(event) =>
                  patchQuestion({ min_words: Math.max(1, Number(event.target.value) || 1) })
                }
              />
            </Field>
          </div>
        ) : null}
      </div>
    </div>
  );
}
