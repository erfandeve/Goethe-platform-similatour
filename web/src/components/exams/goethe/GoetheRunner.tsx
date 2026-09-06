"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";

import { ExamShell } from "./ExamShell";
import { GoetheResult } from "./GoetheResult";
import {
  ArticleStimulus,
  GapDragOptions,
  GapDragStimulus,
  ItemBlock,
  ListeningStimulus,
  MatchPersonStimulus,
  StatementBoxes,
  WritingAnswer,
  WritingStimulus,
} from "./parts";
import { buildPages, type Answers, type ExamModule, type Page } from "./types";

interface StartResponse {
  attempt: { id: string; status: string };
  exam: { title: string; slug: string; level: string };
  module: ExamModule;
}

export interface ResultPayload {
  score: number;
  raw_score: number;
  max_score: number;
  correct_count: number;
  passed: boolean;
  cefr_estimate: string;
  duration_seconds: number;
  module: string;
  review: {
    key: string;
    number: number;
    part: number;
    type: string;
    prompt: string;
    given_label?: string;
    answer_label?: string;
    given_text?: string;
    explanation?: string;
    is_correct: boolean | null;
  }[];
}


/** A stable 12-digit session number, the way the exam player labels a sitting. */
function sessionNumber(attemptId: string) {
  let hash = 0;
  for (const char of attemptId) {
    hash = (hash * 31 + char.charCodeAt(0)) % 1_000_000_000_000;
  }
  return String(hash).padStart(12, "0");
}

export function GoetheRunner({
  slug,
  moduleSkill,
  locale,
  dict,
  brand,
}: {
  slug: string;
  moduleSkill: string;
  locale: Locale;
  dict: Dictionary;
  brand: string;
}) {
  const [state, setState] = useState<"loading" | "running" | "done" | "error">("loading");
  const [error, setError] = useState("");
  const [module, setModule] = useState<ExamModule | null>(null);
  const [attemptId, setAttemptId] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [answers, setAnswers] = useState<Answers>({});
  const [pageIndex, setPageIndex] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(0);
  const [total, setTotal] = useState(1);
  const [confirm, setConfirm] = useState(false);
  const [result, setResult] = useState<ResultPayload | null>(null);
  const submitted = useRef(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await callApi<StartResponse>(`exams/${slug}/start`, {
          method: "POST",
          body: { module: moduleSkill },
          locale,
        });
        if (cancelled) return;
        setModule(data.module);
        setAttemptId(data.attempt.id);
        setSessionId(sessionNumber(data.attempt.id));
        const seconds = data.module.duration_minutes * 60;
        setSecondsLeft(seconds);
        setTotal(seconds);
        setState("running");
      } catch (caught) {
        if (cancelled) return;
        setError((caught as Error).message);
        setState("error");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [slug, moduleSkill, locale]);

  const submit = useCallback(async () => {
    if (submitted.current) return;
    submitted.current = true;
    try {
      const data = await callApi<ResultPayload>(`attempts/${attemptId}/submit`, {
        method: "POST",
        body: { answers },
        locale,
      });
      setResult(data);
      setState("done");
    } catch (caught) {
      setError((caught as Error).message);
      setState("error");
    }
  }, [attemptId, answers, locale]);

  useEffect(() => {
    if (state !== "running") return;
    const timer = setInterval(() => {
      setSecondsLeft((value) => {
        if (value <= 1) {
          clearInterval(timer);
          void submit();
          return 0;
        }
        return value - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [state, submit]);

  // Autosave: answers survive a reload or a dropped connection.
  useEffect(() => {
    if (state !== "running" || !attemptId || !Object.keys(answers).length) return;
    const timer = setTimeout(() => {
      void callApi(`attempts/${attemptId}/answers`, {
        method: "POST",
        body: { answers },
        locale,
      }).catch(() => {});
    }, 12000);
    return () => clearTimeout(timer);
  }, [answers, attemptId, state, locale]);

  const pages: Page[] = useMemo(() => (module ? buildPages(module) : []), [module]);
  const page = pages[pageIndex];

  const setAnswer = useCallback((key: string, value: string) => {
    setAnswers((current) => {
      if (!value) {
        const next = { ...current };
        delete next[key];
        return next;
      }
      return { ...current, [key]: value };
    });
  }, []);

  if (state === "loading" || (state === "running" && !page)) {
    return (
      <div dir="ltr" className="exam-root fixed inset-0 grid place-items-center" style={{ background: "var(--exam-page)" }}>
        <p className="text-sm" style={{ color: "var(--exam-muted)" }}>
          {dict.common.loading}
        </p>
      </div>
    );
  }

  if (state === "error") {
    return (
      <div dir="ltr" className="exam-root fixed inset-0 grid place-items-center p-8 text-center" style={{ background: "var(--exam-page)" }}>
        <div>
          <p className="text-lg font-bold">{dict.common.error}</p>
          <p className="mt-2 text-sm" style={{ color: "var(--exam-muted)" }}>
            {error}
          </p>
          <a
            href={`/${locale}/exams/${slug}`}
            className="mt-6 inline-block px-5 py-2.5 text-sm font-semibold text-white"
            style={{ background: "var(--exam-green)" }}
          >
            {dict.common.back}
          </a>
        </div>
      </div>
    );
  }

  if (state === "done" && result) {
    return <GoetheResult result={result} slug={slug} locale={locale} dict={dict} brand={brand} />;
  }

  if (!module || !page) return null;

  const { part, trackIndex, items } = page;
  const listening = module.skill === "hoeren";

  const left = (() => {
    switch (part.type) {
      case "match_person":
        return <MatchPersonStimulus part={part} />;
      case "gap_drag":
        return <GapDragStimulus part={part} answers={answers} setAnswer={setAnswer} />;
      case "match_heading":
        return <StatementBoxes part={part} />;
      case "writing":
        return <WritingStimulus part={part} />;
      case "listening_mixed":
      case "mcq":
        if (part.audio.length) {
          return (
            <ListeningStimulus part={part} trackIndex={trackIndex ?? 0} />
          );
        }
        return <ArticleStimulus part={part} />;
      default:
        return <ArticleStimulus part={part} />;
    }
  })();

  const right = (() => {
    if (part.type === "writing") {
      return <WritingAnswer part={part} answers={answers} setAnswer={setAnswer} />;
    }
    if (part.type === "gap_drag") {
      return <GapDragOptions part={part} answers={answers} setAnswer={setAnswer} />;
    }
    return (
      <div>
        {items.map((item) => (
          <ItemBlock
            key={item.key}
            item={item}
            answers={answers}
            setAnswer={setAnswer}
            options={item.options.length ? item.options : part.options}
          />
        ))}
      </div>
    );
  })();

  const answered = Object.keys(answers).filter((key) => answers[key]).length;
  const totalItems = module.items_count;

  return (
    <>
      <ExamShell
        brand={brand}
        sessionId={sessionId}
        minutesLeft={Math.ceil(secondsLeft / 60)}
        elapsedRatio={(total - secondsLeft) / total}
        page={pageIndex + 1}
        pages={pages.length}
        workMinutes={part.work_minutes}
        audioBadge={trackIndex !== null && part.audio[trackIndex] ? part.audio[trackIndex].label : undefined}
        onPrev={() => setPageIndex((value) => Math.max(0, value - 1))}
        onNext={() => {
          if (pageIndex + 1 < pages.length) setPageIndex(pageIndex + 1);
          else setConfirm(true);
        }}
        canPrev={pageIndex > 0 && !listening}
        canNext
        prevLabel="Zurück zur vorherigen Aufgabe"
        nextLabel={
          pageIndex + 1 < pages.length ? "Weiter zur nächsten Aufgabe" : dict.exams.runner.finish
        }
        left={left}
        right={right}
      />

      {confirm ? (
        <div dir="ltr" className="exam-root fixed inset-0 z-50 grid place-items-center bg-black/45 p-6">
          <div dir="auto" className="w-full max-w-md bg-white p-8 text-center">
            <h2 className="text-lg font-bold">{dict.exams.runner.confirmTitle}</h2>
            <p className="mt-3 text-sm" style={{ color: "var(--exam-muted)" }}>
              {dict.exams.runner.confirmBody}
            </p>
            <p className="tnum mt-4 text-sm font-semibold">
              {totalItems - answered} {dict.exams.runner.unanswered}
            </p>
            <div className="mt-7 flex gap-3">
              <button
                type="button"
                onClick={() => setConfirm(false)}
                className="flex-1 border px-4 py-2.5 text-sm font-semibold"
                style={{ borderColor: "var(--exam-line)" }}
              >
                {dict.exams.runner.cancel}
              </button>
              <button
                type="button"
                onClick={submit}
                className="flex-1 px-4 py-2.5 text-sm font-semibold text-white"
                style={{ background: "var(--exam-green)" }}
              >
                {dict.exams.runner.submit}
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
