"use client";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";
import type { LessonPart, LessonVideo } from "@/lib/learning";
import { alpha, cn } from "@/lib/utils";

export function ProgressPanel({
  parts,
  current,
  accent,
  locale,
  dict,
  completed,
  onSelect,
}: {
  parts: LessonPart[];
  current: LessonVideo;
  accent: string;
  locale: Locale;
  dict: Dictionary;
  completed: Set<string>;
  onSelect: (video: LessonVideo) => void;
}) {
  return (
    <aside className="glass rounded-3xl p-5">
      <h2 className="mb-4 text-[11px] tracking-wider text-mist-500 uppercase">
        {dict.learning.progress.title}
      </h2>
      <div className="space-y-5">
        {parts.map((part) => (
          <div key={part.id}>
            <p className="mb-2 text-xs font-semibold text-mist-300" dir="ltr">
              {part.title_de}
            </p>
            <ul className="space-y-1">
              {part.videos.map((video) => {
                const active = video.id === current.id;
                const done = completed.has(video.id);
                return (
                  <li key={video.id}>
                    <button
                      type="button"
                      onClick={() => onSelect(video)}
                      className={cn(
                        "flex w-full items-center gap-2.5 rounded-xl px-3 py-2 text-start text-xs transition",
                        active ? "text-mist-50" : "text-mist-400 hover:bg-white/5",
                      )}
                      style={active ? { background: alpha(accent, 0.14) } : undefined}
                    >
                      <span
                        className={cn(
                          "tnum grid size-5 shrink-0 place-items-center rounded-md text-[10px] font-bold",
                          done ? "text-ink-950" : "bg-white/8 text-mist-500",
                        )}
                        style={done ? { background: "#34d399" } : undefined}
                      >
                        {done ? "✓" : formatNumber(video.order, locale)}
                      </span>
                      <span className="min-w-0 flex-1 truncate" dir="ltr">
                        {video.title_de}
                      </span>
                      {video.has_speaking_task ? (
                        <span aria-hidden style={{ color: accent }}>
                          🎤
                        </span>
                      ) : (
                        <span className="text-[10px] text-mist-600">
                          {dict.learning.watchOnly}
                        </span>
                      )}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>
    </aside>
  );
}
