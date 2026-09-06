"use client";

import type { ReactNode } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { LessonVideo } from "@/lib/learning";
import { alpha } from "@/lib/utils";

/** The panel that frames the exercise: who is asking, and what they asked. */
export function AITeacher({
  video,
  accent,
  dict,
  children,
}: {
  video: LessonVideo;
  accent: string;
  dict: Dictionary;
  children: ReactNode;
}) {
  return (
    <section className="flex flex-col gap-4">
      <header className="glass flex items-center gap-4 rounded-3xl p-5">
        <span
          className="grid size-12 shrink-0 place-items-center rounded-2xl"
          style={{ background: alpha(accent, 0.16), color: accent }}
          aria-hidden
        >
          <svg viewBox="0 0 24 24" className="size-6" fill="none" stroke="currentColor" strokeWidth="1.6">
            <rect x="4" y="7" width="16" height="12" rx="3" />
            <path d="M12 3v4M9 12.5h.01M15 12.5h.01M9.5 16h5" strokeLinecap="round" />
          </svg>
        </span>
        <div className="min-w-0">
          <p className="font-display text-sm font-semibold">{dict.learning.teacher.name}</p>
          <p className="text-xs text-mist-500">{dict.learning.teacher.role}</p>
        </div>
        <span
          className="tnum ms-auto rounded-lg px-2.5 py-1 text-[11px] font-semibold"
          style={{ background: alpha(accent, 0.12), color: accent }}
        >
          {video.cefr_level}
        </span>
      </header>

      {video.question ? (
        <div className="glass rounded-3xl p-6">
          <p className="mb-2 text-[11px] tracking-wider text-mist-500 uppercase">
            {dict.learning.teacher.question}
          </p>
          <p className="font-display text-lg leading-snug font-semibold" lang="de" dir="ltr">
            {video.question.prompt_de}
          </p>
          {video.question.prompt && video.question.prompt !== video.question.prompt_de ? (
            <p className="mt-2 text-sm text-mist-400">{video.question.prompt}</p>
          ) : null}

          {video.question.vocabulary.length ? (
            <div className="mt-4 flex flex-wrap gap-1.5" dir="ltr">
              {video.question.vocabulary.map((word) => (
                <span
                  key={word}
                  className="rounded-lg bg-white/6 px-2.5 py-1 text-xs text-mist-300"
                  lang="de"
                >
                  {word}
                </span>
              ))}
            </div>
          ) : null}

          {video.question.hint ? (
            <p className="mt-4 border-s-2 border-white/12 ps-3 text-xs text-mist-500">
              {dict.learning.teacher.hint}: {video.question.hint}
            </p>
          ) : null}
        </div>
      ) : (
        <div className="glass rounded-3xl p-6 text-center">
          <p className="text-sm text-mist-400">{dict.learning.teacher.waiting}</p>
        </div>
      )}

      {children}
    </section>
  );
}
