"use client";

import { useState } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";
import type { CourseDetail } from "@/lib/types";
import { cn } from "@/lib/utils";

const KIND_ICONS: Record<string, string> = {
  video: "▶",
  audio: "♪",
  quiz: "✎",
  live: "◉",
  pdf: "▤",
};

export function Curriculum({
  sections,
  locale,
  dict,
}: {
  sections: CourseDetail["curriculum"];
  locale: Locale;
  dict: Dictionary;
}) {
  const [open, setOpen] = useState<number[]>([0]);

  function toggle(index: number) {
    setOpen((current) =>
      current.includes(index) ? current.filter((item) => item !== index) : [...current, index],
    );
  }

  return (
    <div className="space-y-3">
      {sections.map((section, index) => {
        const expanded = open.includes(index);
        const minutes = section.lessons.reduce((sum, lesson) => sum + lesson.duration_minutes, 0);

        return (
          <div key={section.title} className="glass overflow-hidden rounded-2xl">
            <button
              type="button"
              onClick={() => toggle(index)}
              className="flex w-full items-center gap-4 px-5 py-4 text-start transition hover:bg-white/4"
              aria-expanded={expanded}
            >
              <span
                className={cn(
                  "grid size-7 shrink-0 place-items-center rounded-lg bg-white/8 text-xs transition-transform",
                  expanded && "rotate-45",
                )}
                aria-hidden
              >
                +
              </span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-semibold">{section.title}</span>
                <span className="tnum mt-0.5 block text-xs text-mist-500">
                  {formatNumber(section.lessons.length, locale)} {dict.courses.card.lessons} ·{" "}
                  {formatNumber(minutes, locale)} {dict.common.minutes}
                </span>
              </span>
            </button>

            {expanded ? (
              <ul className="border-t border-white/8">
                {section.lessons.map((lesson) => (
                  <li
                    key={lesson.title}
                    className="flex items-center gap-3 px-5 py-3 text-sm transition hover:bg-white/3"
                  >
                    <span className="grid size-6 place-items-center rounded-md bg-white/6 text-[11px] text-mist-400">
                      {KIND_ICONS[lesson.kind] ?? "•"}
                    </span>
                    <span className="min-w-0 flex-1 truncate text-mist-200">{lesson.title}</span>
                    {lesson.is_preview ? (
                      <span className="rounded-md bg-mint-400/12 px-2 py-0.5 text-[10px] font-semibold text-mint-400 uppercase">
                        {dict.courses.detail.preview}
                      </span>
                    ) : null}
                    <span className="tnum text-xs text-mist-600">
                      {formatNumber(lesson.duration_minutes, locale)} {dict.common.minutes}
                    </span>
                  </li>
                ))}
              </ul>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
