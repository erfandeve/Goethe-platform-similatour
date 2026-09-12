"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/Button";
import { Select } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminExam } from "@/lib/admin";
import { MODULE_LABELS, PART_TYPE_LABELS } from "@/lib/admin";
import { formatNumber } from "@/lib/format";

import { Panel } from "./ui";

interface Outline {
  level: string;
  modules: {
    skill: string;
    duration_minutes: number;
    parts: { number: number; type: string; title: string; work_minutes: number; items: number[]; tracks: number }[];
  }[];
}

const LEVELS = ["A1", "A2", "B1", "B2", "C1"];

/**
 * Start a paper from the official shape of its level: every Teil, task type,
 * working time, item number and replay rule is laid out, and only the
 * material is left to write.
 */
export function TemplatePicker({
  base,
  defaultLevel,
  hasModules,
  busy,
  locale,
  run,
  call,
  onApplied,
}: {
  base: string;
  defaultLevel?: string;
  hasModules: boolean;
  busy: boolean;
  locale: Locale;
  run: <T>(request: () => Promise<T>, messages?: { success?: string; failure?: string }) => Promise<T | null>;
  call: <T>(path: string, init?: { method?: string; body?: unknown }) => Promise<T>;
  onApplied: (saved: AdminExam) => void;
}) {
  const [outlines, setOutlines] = useState<Outline[]>([]);
  const [level, setLevel] = useState(
    defaultLevel && LEVELS.includes(defaultLevel.toUpperCase()) ? defaultLevel.toUpperCase() : "B1",
  );
  const [open, setOpen] = useState(!hasModules);

  useEffect(() => {
    let alive = true;
    call<{ results: Outline[] }>("admin/exam-templates")
      .then((data) => alive && setOutlines(data.results))
      .catch(() => {});
    return () => {
      alive = false;
    };
  }, [call]);

  const outline = outlines.find((entry) => entry.level === level);

  async function apply() {
    if (
      hasModules &&
      !confirm(
        `همه ماژول‌ها و سؤال‌های فعلی این آزمون پاک و با ساختار استاندارد ${level} جایگزین می‌شوند. ادامه می‌دهید؟`,
      )
    ) {
      return;
    }
    const saved = await run(
      () =>
        call<AdminExam>(`${base}/template`, {
          method: "POST",
          body: { level, replace: hasModules },
        }),
      { success: `ساختار استاندارد ${level} ساخته شد — حالا متن‌ها و جواب‌ها را پر کن` },
    );
    if (saved) {
      onApplied(saved);
      setOpen(false);
    }
  }

  if (!open) {
    return (
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="text-xs text-mist-500 underline-offset-4 transition hover:text-mist-200 hover:underline"
      >
        ساخت دوباره از ساختار استاندارد گوته…
      </button>
    );
  }

  return (
    <Panel
      title="ساختار استاندارد آزمون"
      description="همه تایل‌ها، نوع تسک‌ها، زمان‌ها، شماره سؤال‌ها و دفعات پخش صوت طبق Modellsatz رسمی ساخته می‌شوند؛ فقط متن‌ها، فایل‌های صوتی و جواب‌ها را پر می‌کنی."
      action={
        <div className="flex items-center gap-2">
          <Select value={level} onChange={(event) => setLevel(event.target.value)} className="w-24">
            {LEVELS.map((code) => (
              <option key={code} value={code}>
                {code}
              </option>
            ))}
          </Select>
          <Button size="sm" onClick={apply} disabled={busy || !outline}>
            {hasModules ? "جایگزینی با این ساختار" : `ساخت ساختار ${level}`}
          </Button>
          {hasModules ? (
            <Button size="sm" variant="ghost" onClick={() => setOpen(false)}>
              بستن
            </Button>
          ) : null}
        </div>
      }
    >
      {outline ? (
        <div className="grid gap-4 md:grid-cols-3">
          {outline.modules.map((module) => (
            <div key={module.skill} className="rounded-2xl border border-white/8 p-4">
              <p className="mb-3 flex items-baseline justify-between text-sm font-semibold">
                <span>{MODULE_LABELS[module.skill] ?? module.skill}</span>
                <span className="tnum text-xs font-normal text-mist-500">
                  {formatNumber(module.duration_minutes, locale)} دقیقه
                </span>
              </p>
              <ol className="space-y-1.5">
                {module.parts.map((part) => (
                  <li key={part.number} className="flex items-baseline gap-2 text-xs text-mist-400">
                    <span className="tnum w-5 shrink-0 text-mist-600">{part.number}</span>
                    <span className="min-w-0 flex-1 truncate">
                      {PART_TYPE_LABELS[part.type] ?? part.type}
                      {part.tracks ? ` · ${formatNumber(part.tracks, locale)} صوت` : ""}
                    </span>
                    <span className="tnum shrink-0 text-mist-500" dir="ltr">
                      {part.items.length ? `${part.items[0]}–${part.items[1]}` : ""}
                    </span>
                  </li>
                ))}
              </ol>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-mist-500">در حال خواندن ساختارها…</p>
      )}
    </Panel>
  );
}
