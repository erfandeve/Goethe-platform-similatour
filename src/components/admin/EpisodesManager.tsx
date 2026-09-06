"use client";

import Link from "next/link";
import { useRef, useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input, Select, Textarea } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminEpisode, AdminPodcast, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED, LEVELS } from "@/lib/admin";
import { formatClock, formatNumber } from "@/lib/format";
import { mediaUrl } from "@/lib/utils";

import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

interface Draft {
  id?: string;
  number: string;
  title: Translated;
  description: Translated;
  audio_url: string;
  duration_seconds: string;
  level: string;
  is_premium: boolean;
  is_published: boolean;
  transcript: string;
  vocabulary: string;
}

const blank = (next: number): Draft => ({
  number: String(next),
  title: { ...EMPTY_TRANSLATED },
  description: { ...EMPTY_TRANSLATED },
  audio_url: "",
  duration_seconds: "0",
  level: "A2",
  is_premium: false,
  is_published: true,
  transcript: "",
  vocabulary: "",
});

/**
 * Transcript and vocabulary are edited as plain lines rather than a nested
 * form: one line per cue is far quicker to paste and correct than a table.
 *   transcript →  0:12 | Anna | Guten Morgen! | صبح بخیر
 *   vocabulary →  das | Brötchen | نان کوچک | Ich kaufe zwei Brötchen.
 */
function parseTranscript(text: string) {
  return text
    .split("\n")
    .map((line) => line.split("|").map((part) => part.trim()))
    .filter((parts) => parts.length >= 3 && parts[2])
    .map((parts, index, all) => {
      const [stamp, speaker, german, translation = ""] = parts;
      const [minutes, seconds] = stamp.split(":").map(Number);
      const start = (Number.isFinite(minutes) ? minutes : 0) * 60 + (seconds || 0);
      const nextStamp = all[index + 1]?.[0];
      let end = start + 5;
      if (nextStamp) {
        const [m, s] = nextStamp.split(":").map(Number);
        end = (Number.isFinite(m) ? m : 0) * 60 + (s || 0);
      }
      return { start, end, speaker, text: german, translation: { fa: translation, en: "", de: "" } };
    });
}

function parseVocabulary(text: string) {
  return text
    .split("\n")
    .map((line) => line.split("|").map((part) => part.trim()))
    .filter((parts) => parts.length >= 2)
    .map(([article, term, meaning = "", example = ""]) => ({
      article,
      term,
      meaning: { fa: meaning, en: "", de: "" },
      example,
    }));
}

const transcriptToText = (episode: AdminEpisode) =>
  episode.transcript
    .map(
      (line) =>
        `${formatClock(line.start)} | ${line.speaker} | ${line.text} | ${line.translation.fa}`,
    )
    .join("\n");

const vocabularyToText = (episode: AdminEpisode) =>
  episode.vocabulary
    .map((item) => `${item.article} | ${item.term} | ${item.meaning.fa} | ${item.example}`)
    .join("\n");

export function EpisodesManager({
  podcast,
  initial,
  locale,
}: {
  podcast: AdminPodcast;
  initial: AdminEpisode[];
  locale: Locale;
}) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [rows, setRows] = useState(initial);
  const [draft, setDraft] = useState<Draft | null>(null);
  const audioInput = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  function uploadAudio(file: File) {
    if (!draft) return;
    setUploading(true);
    setProgress(0);

    const form = new FormData();
    form.append("file", file);
    form.append("folder", podcast.slug);

    const request = new XMLHttpRequest();
    request.open("POST", "/api/admin/upload?kind=audio");
    request.upload.onprogress = (event) => {
      if (event.lengthComputable) setProgress(Math.round((event.loaded / event.total) * 100));
    };
    request.onload = () => {
      setUploading(false);
      try {
        const body = JSON.parse(request.responseText);
        if (request.status >= 400) {
          notify(body.detail || "آپلود ناموفق بود", "error");
          return;
        }
        setDraft((current) => (current ? { ...current, audio_url: body.url } : current));
      } catch {
        notify("پاسخ آپلود نامعتبر بود", "error");
      }
    };
    request.onerror = () => {
      setUploading(false);
      notify("ارتباط با سرور قطع شد", "error");
    };
    request.send(form);
  }

  async function save() {
    if (!draft) return;
    if (!draft.audio_url) {
      notify("اول فایل صوتی را آپلود کن", "error");
      return;
    }

    const body = {
      number: Number(draft.number) || 1,
      title: draft.title,
      description: draft.description,
      audio_url: draft.audio_url,
      duration_seconds: Number(draft.duration_seconds) || 0,
      level: draft.level,
      is_premium: draft.is_premium,
      is_published: draft.is_published,
      transcript: parseTranscript(draft.transcript),
      vocabulary: parseVocabulary(draft.vocabulary),
    };

    const saved = draft.id
      ? await run(() => call<AdminEpisode>(`admin/episodes/${draft.id}`, { method: "PATCH", body }),
          { success: "قسمت ذخیره شد" })
      : await run(
          () => call<AdminEpisode>(`admin/podcasts/${podcast.id}/episodes`, { method: "POST", body }),
          { success: "قسمت اضافه شد" },
        );

    if (!saved) return;
    setRows((current) =>
      draft.id ? current.map((row) => (row.id === saved.id ? saved : row)) : [...current, saved],
    );
    setDraft(null);
  }

  async function remove(row: AdminEpisode) {
    if (!confirm(`قسمت «${row.title.fa || row.slug}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/episodes/${row.id}`, { method: "DELETE" }), {
      success: "حذف شد",
    });
    if (done !== null) setRows((current) => current.filter((item) => item.id !== row.id));
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div className="min-w-0">
          <Link href={`/${locale}/admin/podcasts`} className="text-xs text-mist-500 hover:text-mist-200">
            ← همه پادکست‌ها
          </Link>
          <h1 className="font-display mt-2 truncate text-2xl font-semibold">
            {podcast.title.fa || podcast.title.en || podcast.slug}
          </h1>
          <p className="tnum mt-1 text-xs text-mist-500" dir="ltr">
            {podcast.slug} · {formatNumber(rows.length, locale)} قسمت
          </p>
        </div>
        <Button onClick={() => setDraft(blank(rows.length + 1))}>+ قسمت جدید</Button>
      </header>

      <Panel title="قسمت‌ها">
        {rows.length ? (
          <ul className="space-y-2">
            {rows.map((row) => (
              <li
                key={row.id}
                className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/8 px-4 py-3"
              >
                <span className="tnum grid size-8 shrink-0 place-items-center rounded-lg bg-white/8 text-xs font-semibold">
                  {formatNumber(row.number, locale)}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-medium">
                    {row.title.fa || row.title.de || row.slug}
                  </span>
                  <span className="tnum block truncate text-xs text-mist-600" dir="ltr">
                    {formatClock(row.duration_seconds)} · {row.transcript.length} خط متن ·{" "}
                    {row.vocabulary.length} واژه
                  </span>
                </span>
                {row.is_premium ? (
                  <span className="rounded-md bg-amber-400/15 px-2 py-0.5 text-[10px] text-amber-400">
                    ویژه
                  </span>
                ) : null}
                <button
                  type="button"
                  onClick={() =>
                    setDraft({
                      id: row.id,
                      number: String(row.number),
                      title: row.title,
                      description: row.description,
                      audio_url: row.audio_url,
                      duration_seconds: String(row.duration_seconds),
                      level: row.level,
                      is_premium: row.is_premium,
                      is_published: row.is_published,
                      transcript: transcriptToText(row),
                      vocabulary: vocabularyToText(row),
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
          <Empty title="هنوز قسمتی ندارد" icon="◇" />
        )}
      </Panel>

      <Modal open={!!draft} wide title={draft?.id ? "ویرایش قسمت" : "قسمت جدید"} onClose={() => setDraft(null)}>
        {draft ? (
          <div className="space-y-5">
            <div className="rounded-2xl border border-white/10 bg-white/3 p-5">
              <p className="mb-3 text-xs font-semibold tracking-wider text-mist-400 uppercase">
                فایل صوتی
              </p>
              {draft.audio_url ? (
                <audio
                  controls
                  src={mediaUrl(draft.audio_url)}
                  className="w-full"
                  onLoadedMetadata={(event) =>
                    setDraft((current) =>
                      current && !Number(current.duration_seconds)
                        ? {
                            ...current,
                            duration_seconds: String(Math.round(event.currentTarget.duration || 0)),
                          }
                        : current,
                    )
                  }
                >
                  <track kind="captions" />
                </audio>
              ) : (
                <p className="text-sm text-mist-500">هنوز فایلی انتخاب نشده است.</p>
              )}

              <input
                ref={audioInput}
                type="file"
                accept="audio/*"
                className="hidden"
                onChange={(event) => {
                  const file = event.target.files?.[0];
                  if (file) uploadAudio(file);
                  event.target.value = "";
                }}
              />
              <div className="mt-4 flex flex-wrap items-center gap-3">
                <Button
                  type="button"
                  size="sm"
                  variant="soft"
                  disabled={uploading}
                  onClick={() => audioInput.current?.click()}
                >
                  {uploading
                    ? `در حال آپلود… ${progress}%`
                    : draft.audio_url
                      ? "تعویض فایل"
                      : "انتخاب فایل"}
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

            <TranslatedField
              label="عنوان قسمت"
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

            <div className="grid gap-4 sm:grid-cols-3">
              <Field label="شماره قسمت">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  value={draft.number}
                  onChange={(e) => setDraft({ ...draft, number: e.target.value })}
                />
              </Field>
              <Field label="مدت (ثانیه)" hint="هنگام آپلود پر می‌شود">
                <Input
                  type="number"
                  dir="ltr"
                  className="tnum"
                  value={draft.duration_seconds}
                  onChange={(e) => setDraft({ ...draft, duration_seconds: e.target.value })}
                />
              </Field>
              <Field label="سطح">
                <Select value={draft.level} onChange={(e) => setDraft({ ...draft, level: e.target.value })}>
                  {LEVELS.map((level) => (
                    <option key={level} value={level} className="bg-ink-900">{level}</option>
                  ))}
                </Select>
              </Field>
            </div>

            <Field
              label="متن قسمت"
              hint="هر خط: زمان | گوینده | جمله آلمانی | ترجمه فارسی — مثلاً  0:12 | Anna | Guten Morgen! | صبح بخیر"
            >
              <Textarea
                dir="ltr"
                className="min-h-40"
                value={draft.transcript}
                onChange={(e) => setDraft({ ...draft, transcript: e.target.value })}
              />
            </Field>

            <Field
              label="واژه‌نامه"
              hint="هر خط: حرف تعریف | واژه | معنی فارسی | مثال — مثلاً  das | Brötchen | نان کوچک | Ich kaufe zwei Brötchen."
            >
              <Textarea
                dir="ltr"
                className="min-h-28"
                value={draft.vocabulary}
                onChange={(e) => setDraft({ ...draft, vocabulary: e.target.value })}
              />
            </Field>

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
                  checked={draft.is_premium}
                  onChange={(e) => setDraft({ ...draft, is_premium: e.target.checked })}
                  className="size-4 accent-amber-400"
                />
                قسمت ویژه (نیازمند اشتراک)
              </label>
            </div>

            <div className="flex gap-3 pt-2">
              <Button onClick={save} disabled={busy} className="flex-1">
                {busy ? "…" : "ذخیره قسمت"}
              </Button>
              <Button variant="outline" onClick={() => setDraft(null)}>انصراف</Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <Toast message={toast.message} tone={toast.tone} />
    </div>
  );
}
