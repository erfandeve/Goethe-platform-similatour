"use client";

import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Field, Input } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminCourse, AdminPart, AdminVideo, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED } from "@/lib/admin";
import { formatNumber } from "@/lib/format";

import { VideoEditor, blankVideo, toDraft, type VideoDraft } from "./VideoEditor";
import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

interface PartDraft {
  id?: string;
  title: Translated;
  title_de: string;
  description: Translated;
}

const blankPart = (): PartDraft => ({
  title: { ...EMPTY_TRANSLATED },
  title_de: "",
  description: { ...EMPTY_TRANSLATED },
});

/** Chapters, their lessons, and the speaking prompt attached to each lesson. */
export function CourseBuilder({
  course,
  initialParts,
  locale,
}: {
  course: AdminCourse;
  initialParts: AdminPart[];
  locale: Locale;
}) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [parts, setParts] = useState(initialParts);
  const [partDraft, setPartDraft] = useState<PartDraft | null>(null);
  const [videoDraft, setVideoDraft] = useState<{ partId: string; draft: VideoDraft } | null>(null);

  // -- parts ---------------------------------------------------------------

  async function savePart() {
    if (!partDraft) return;
    const body = {
      title: partDraft.title,
      title_de: partDraft.title_de,
      description: partDraft.description,
    };

    const saved = partDraft.id
      ? await run(() => call<AdminPart>(`admin/parts/${partDraft.id}`, { method: "PATCH", body }),
          { success: "فصل بروزرسانی شد" })
      : await run(() => call<AdminPart>(`admin/courses/${course.id}/parts`, { method: "POST", body }),
          { success: "فصل ساخته شد" });

    if (!saved) return;
    setParts((current) =>
      partDraft.id
        ? current.map((part) => (part.id === saved.id ? { ...saved, videos: part.videos } : part))
        : [...current, { ...saved, videos: [], videos_count: 0 }],
    );
    setPartDraft(null);
  }

  async function removePart(part: AdminPart) {
    if (!confirm(`فصل «${part.title_de || part.slug}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/parts/${part.id}`, { method: "DELETE" }), {
      success: "فصل حذف شد",
    });
    if (done !== null) setParts((current) => current.filter((item) => item.id !== part.id));
  }

  async function movePart(index: number, direction: -1 | 1) {
    const target = index + direction;
    if (target < 0 || target >= parts.length) return;
    const next = [...parts];
    [next[index], next[target]] = [next[target], next[index]];
    setParts(next);
    await call("admin/parts/reorder", { method: "POST", body: { ids: next.map((p) => p.id) } });
  }

  // -- videos --------------------------------------------------------------

  async function saveVideo() {
    if (!videoDraft) return;
    const { partId, draft } = videoDraft;

    if (!draft.video_url) {
      notify("اول فایل ویدیو را آپلود کن", "error");
      return;
    }
    if (draft.hasQuestion && !draft.question.prompt_de.trim()) {
      notify("متن سؤال آلمانی را بنویس", "error");
      return;
    }

    const body = {
      title: draft.title,
      title_de: draft.title_de,
      scene_label: draft.scene_label,
      description: draft.description,
      video_url: draft.video_url,
      poster_url: draft.poster_url,
      duration_seconds: draft.duration_seconds,
      cefr_level: draft.cefr_level,
      is_published: draft.is_published,
      question: draft.hasQuestion ? draft.question : null,
    };

    const saved = draft.id
      ? await run(() => call<AdminVideo>(`admin/videos/${draft.id}`, { method: "PATCH", body }),
          { success: "ویدیو ذخیره شد" })
      : await run(() => call<AdminVideo>(`admin/parts/${partId}/videos`, { method: "POST", body }),
          { success: "ویدیو اضافه شد" });

    if (!saved) return;
    setParts((current) =>
      current.map((part) => {
        if (part.id !== partId) return part;
        const videos = draft.id
          ? part.videos.map((video) => (video.id === saved.id ? saved : video))
          : [...part.videos, saved];
        return { ...part, videos, videos_count: videos.length };
      }),
    );
    setVideoDraft(null);
  }

  async function removeVideo(partId: string, video: AdminVideo) {
    if (!confirm(`ویدیو «${video.title_de || video.slug}» حذف شود؟`)) return;
    const done = await run(() => call(`admin/videos/${video.id}`, { method: "DELETE" }), {
      success: "ویدیو حذف شد",
    });
    if (done === null) return;
    setParts((current) =>
      current.map((part) =>
        part.id === partId
          ? {
              ...part,
              videos: part.videos.filter((item) => item.id !== video.id),
              videos_count: part.videos.length - 1,
            }
          : part,
      ),
    );
  }

  async function moveVideo(partId: string, index: number, direction: -1 | 1) {
    const part = parts.find((item) => item.id === partId);
    if (!part) return;
    const target = index + direction;
    if (target < 0 || target >= part.videos.length) return;

    const videos = [...part.videos];
    [videos[index], videos[target]] = [videos[target], videos[index]];
    setParts((current) =>
      current.map((item) => (item.id === partId ? { ...item, videos } : item)),
    );
    await call("admin/videos/reorder", { method: "POST", body: { ids: videos.map((v) => v.id) } });
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div className="min-w-0">
          <Link href={`/${locale}/admin/courses`} className="text-xs text-mist-500 hover:text-mist-200">
            ← همه دوره‌ها
          </Link>
          <h1 className="font-display mt-2 truncate text-2xl font-semibold">
            {course.title.fa || course.title.en || course.slug}
          </h1>
          <p className="tnum mt-1 text-xs text-mist-500" dir="ltr">
            {course.slug} · {course.level} · {formatNumber(parts.length, locale)} فصل ·{" "}
            {formatNumber(parts.reduce((sum, part) => sum + part.videos.length, 0), locale)} ویدیو
          </p>
        </div>
        <div className="flex gap-2">
          <Link
            href={`/${locale}/learn/${course.slug}`}
            className="glass rounded-full px-5 py-2.5 text-sm"
          >
            پیش‌نمایش کلاس
          </Link>
          <Button onClick={() => setPartDraft(blankPart())}>+ فصل جدید</Button>
        </div>
      </header>

      {parts.length ? (
        <div className="space-y-4">
          {parts.map((part, partIndex) => (
            <Panel
              key={part.id}
              title={part.title_de || part.title.fa || part.slug}
              action={
                <div className="flex flex-wrap items-center gap-2">
                  <span className="tnum text-xs text-mist-500">
                    {formatNumber(part.videos.length, locale)} ویدیو
                  </span>
                  <button
                    type="button"
                    onClick={() => movePart(partIndex, -1)}
                    disabled={partIndex === 0}
                    className="glass grid size-8 place-items-center rounded-full text-xs disabled:opacity-30"
                    aria-label="بالا"
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    onClick={() => movePart(partIndex, 1)}
                    disabled={partIndex === parts.length - 1}
                    className="glass grid size-8 place-items-center rounded-full text-xs disabled:opacity-30"
                    aria-label="پایین"
                  >
                    ↓
                  </button>
                  <Button
                    size="sm"
                    variant="soft"
                    onClick={() =>
                      setVideoDraft({ partId: part.id, draft: blankVideo() })
                    }
                  >
                    + ویدیو
                  </Button>
                  <button
                    type="button"
                    onClick={() =>
                      setPartDraft({
                        id: part.id,
                        title: part.title,
                        title_de: part.title_de,
                        description: part.description,
                      })
                    }
                    className="glass rounded-full px-4 py-1.5 text-xs"
                  >
                    ویرایش
                  </button>
                  <button
                    type="button"
                    onClick={() => removePart(part)}
                    className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                  >
                    حذف
                  </button>
                </div>
              }
            >
              {part.videos.length ? (
                <ul className="space-y-2">
                  {part.videos.map((video, videoIndex) => (
                    <li
                      key={video.id}
                      className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/8 px-4 py-3"
                    >
                      <span className="tnum grid size-8 shrink-0 place-items-center rounded-lg bg-white/8 text-xs font-semibold">
                        {formatNumber(videoIndex + 1, locale)}
                      </span>

                      <span className="min-w-0 flex-1">
                        <span className="block truncate text-sm font-medium" dir="ltr">
                          {video.scene_label || video.title_de || video.slug}
                        </span>
                        <span className="block truncate text-xs text-mist-600" dir="ltr">
                          {video.question?.prompt_de || "بدون تمرین گفتاری"}
                        </span>
                      </span>

                      <span
                        className={`rounded-md px-2 py-0.5 text-[10px] font-semibold ${
                          video.has_speaking_task
                            ? "bg-cyan-400/15 text-cyan-400"
                            : "bg-white/8 text-mist-500"
                        }`}
                      >
                        {video.has_speaking_task ? "🎤 گفتاری" : "تماشا"}
                      </span>
                      {!video.is_published ? (
                        <span className="rounded-md bg-amber-400/15 px-2 py-0.5 text-[10px] text-amber-400">
                          پیش‌نویس
                        </span>
                      ) : null}

                      <button
                        type="button"
                        onClick={() => moveVideo(part.id, videoIndex, -1)}
                        disabled={videoIndex === 0}
                        className="glass grid size-7 place-items-center rounded-full text-[10px] disabled:opacity-30"
                        aria-label="بالا"
                      >
                        ↑
                      </button>
                      <button
                        type="button"
                        onClick={() => moveVideo(part.id, videoIndex, 1)}
                        disabled={videoIndex === part.videos.length - 1}
                        className="glass grid size-7 place-items-center rounded-full text-[10px] disabled:opacity-30"
                        aria-label="پایین"
                      >
                        ↓
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          setVideoDraft({ partId: part.id, draft: toDraft(video) })
                        }
                        className="glass rounded-full px-4 py-1.5 text-xs"
                      >
                        ویرایش
                      </button>
                      <button
                        type="button"
                        onClick={() => removeVideo(part.id, video)}
                        className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
                      >
                        حذف
                      </button>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-mist-500">
                  هنوز ویدیویی در این فصل نیست — با دکمه «+ ویدیو» اضافه کن.
                </p>
              )}
            </Panel>
          ))}
        </div>
      ) : (
        <Empty
          title="هنوز فصلی نساخته‌ای"
          body="اول یک فصل بساز، بعد ویدیوهایش را آپلود کن."
          icon="◇"
          action={<Button onClick={() => setPartDraft(blankPart())}>+ فصل جدید</Button>}
        />
      )}

      {/* -------------------------------------------------------- part modal */}
      <Modal
        open={!!partDraft}
        title={partDraft?.id ? "ویرایش فصل" : "فصل جدید"}
        onClose={() => setPartDraft(null)}
      >
        {partDraft ? (
          <div className="space-y-5">
            <Field label="عنوان آلمانی" hint="در کلاس نشان داده می‌شود، مثلاً Teil 2 – Grenzkontrolle">
              <Input
                value={partDraft.title_de}
                dir="ltr"
                lang="de"
                onChange={(event) => setPartDraft({ ...partDraft, title_de: event.target.value })}
              />
            </Field>
            <TranslatedField
              label="عنوان (سه‌زبانه)"
              required
              value={partDraft.title}
              onChange={(title) => setPartDraft({ ...partDraft, title })}
            />
            <TranslatedField
              label="توضیح فصل"
              multiline
              value={partDraft.description}
              onChange={(description) => setPartDraft({ ...partDraft, description })}
            />
            <div className="flex gap-3 pt-2">
              <Button onClick={savePart} disabled={busy} className="flex-1">
                {busy ? "…" : "ذخیره"}
              </Button>
              <Button variant="outline" onClick={() => setPartDraft(null)}>
                انصراف
              </Button>
            </div>
          </div>
        ) : null}
      </Modal>

      {/* ------------------------------------------------------- video modal */}
      <Modal
        open={!!videoDraft}
        wide
        title={videoDraft?.draft.id ? "ویرایش ویدیو" : "ویدیو جدید"}
        onClose={() => setVideoDraft(null)}
      >
        {videoDraft ? (
          <div className="space-y-6">
            <VideoEditor
              draft={videoDraft.draft}
              courseSlug={course.slug}
              onError={(message) => notify(message, "error")}
              onChange={(draft) => setVideoDraft({ ...videoDraft, draft })}
            />
            <div className="flex gap-3 border-t border-white/8 pt-5">
              <Button onClick={saveVideo} disabled={busy} className="flex-1">
                {busy ? "…" : "ذخیره ویدیو"}
              </Button>
              <Button variant="outline" onClick={() => setVideoDraft(null)}>
                انصراف
              </Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <Toast message={toast.message} tone={toast.tone} />
    </div>
  );
}
