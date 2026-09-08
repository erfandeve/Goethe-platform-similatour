"use client";

import Link from "next/link";
import { useEffect } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";

interface ModuleSummary {
  skill: string;
  title: string;
  intro: string;
  duration_minutes: number;
  max_points: number;
  parts_count: number;
  items_count: number;
}

const GERMAN_NAME: Record<string, string> = {
  lesen: "Lesen",
  hoeren: "Hören",
  schreiben: "Schreiben",
  sprechen: "Sprechen",
};

/** The lobby: pick a module, read the rules, start the clock. */
export function ExamStart({
  slug,
  title,
  level,
  board,
  modules,
  codeId = "",
  codeLabel = "",
  locale,
  dict,
  brand,
}: {
  slug: string;
  title: string;
  level: string;
  board: string;
  modules: ModuleSummary[];
  /** The sitting being taken; its questions differ per code. */
  codeId?: string;
  codeLabel?: string;
  locale: Locale;
  dict: Dictionary;
  brand: string;
}) {
  useEffect(() => {
    document.body.dataset.mode = "exam";
    return () => {
      delete document.body.dataset.mode;
    };
  }, []);

  return (
    <div
      dir="ltr"
      className="exam-root fixed inset-0 flex flex-col"
      style={{ background: "var(--exam-page)" }}
    >
      <header
        className="flex h-16 shrink-0 items-center justify-between px-6 text-white"
        style={{ background: "var(--exam-bar)" }}
      >
        <span className="flex items-center gap-3">
          <span
            className="grid size-9 place-items-center rounded-full border-2 text-[13px] font-bold"
            style={{ borderColor: "var(--exam-green)", color: "var(--exam-green)" }}
            aria-hidden
          >
            G
          </span>
          <span className="text-xs leading-tight font-semibold tracking-wide">
            {brand.toUpperCase()}
            <span className="block text-[10px] font-normal text-white/55">AKADEMIE</span>
          </span>
        </span>
        <Link href={`/${locale}/exams/${slug}`} className="text-sm text-white/75 hover:text-white">
          {dict.common.back}
        </Link>
      </header>
      <div className="h-1.5 w-full shrink-0" style={{ background: "var(--exam-green)" }} />

      <div className="exam-scroll flex-1 p-6">
        <div className="mx-auto max-w-4xl">
          <div className="bg-white p-8 md:p-12" style={{ border: "1px solid var(--exam-line)" }}>
            <p className="text-xs tracking-[0.2em] uppercase" style={{ color: "var(--exam-muted)" }} dir="ltr">
              {board}
            </p>
            <h1 className="mt-3 text-3xl font-bold" dir="ltr">
              {title}
            </h1>
            <p className="exam-body mt-4 max-w-2xl" dir="auto" style={{ color: "var(--exam-muted)" }}>
              {dict.exams.simulators.body}
            </p>

            <div className="mt-10 space-y-3">
              {modules.map((module) => {
                const offline = module.skill === "sprechen";
                return (
                  <div
                    key={module.skill}
                    className="flex flex-wrap items-center gap-4 border p-5"
                    style={{ borderColor: "var(--exam-line)" }}
                  >
                    <span
                      className="grid size-12 shrink-0 place-items-center text-sm font-bold text-white"
                      style={{ background: offline ? "#b6bcbe" : "var(--exam-green)" }}
                      aria-hidden
                    >
                      {GERMAN_NAME[module.skill]?.slice(0, 2)}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block font-bold" dir="ltr">
                        {GERMAN_NAME[module.skill] ?? module.skill}
                        {module.title && module.title !== GERMAN_NAME[module.skill] ? (
                          <span
                            className="ms-2 font-normal"
                            dir="auto"
                            style={{ color: "var(--exam-muted)" }}
                          >
                            {module.title}
                          </span>
                        ) : null}
                      </span>
                      <span className="tnum mt-1 block text-xs" style={{ color: "var(--exam-muted)" }} dir="ltr">
                        {module.duration_minutes} Minuten · {module.parts_count} Teile ·{" "}
                        {module.items_count} Aufgaben
                      </span>
                    </span>
                    {offline ? (
                      <span className="text-xs" dir="auto" style={{ color: "var(--exam-muted)" }}>
                        {dict.exams.result.teacherGraded}
                      </span>
                    ) : (
                      <Link
                        href={`/${locale}/exams/${slug}/attempt?module=${module.skill}${
                          codeId ? `&code=${codeId}` : ""
                        }`}
                        className="px-6 py-2.5 text-sm font-semibold text-white transition"
                        style={{ background: "var(--exam-green)" }}
                      >
                        {dict.exams.card.start}
                      </Link>
                    )}
                  </div>
                );
              })}
            </div>

            <ul className="mt-10 space-y-2 border-t pt-6 text-xs" style={{ borderColor: "var(--exam-line)", color: "var(--exam-muted)" }}>
              <li>· Die Uhr läuft ab dem Start des Moduls und stoppt nicht.</li>
              <li>· Hörtexte werden automatisch abgespielt; ein Zurückspringen ist nicht möglich.</li>
              <li>· Ihre Antworten werden während der Prüfung automatisch gespeichert.</li>
              <li>· {level} · Bestehensgrenze: 60 %</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
