"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { Button, ButtonLink } from "@/components/ui/Button";
import { LevelBadge } from "@/components/ui/Badge";
import { Progress } from "@/components/ui/Progress";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatClock, formatNumber } from "@/lib/format";
import type { Attempt, ExamDetail, ExamQuestion } from "@/lib/types";
import { alpha, cn } from "@/lib/utils";

import { ExamResult } from "./ExamResult";

type Answers = Record<string, number>;

interface StartResponse {
  attempt: Attempt;
  exam: ExamDetail;
}

export function ExamRunner({
  slug,
  locale,
  dict,
}: {
  slug: string;
  locale: Locale;
  dict: Dictionary;
}) {
  const [state, setState] = useState<"loading" | "running" | "finished" | "error">("loading");
  const [error, setError] = useState("");
  const [exam, setExam] = useState<ExamDetail | null>(null);
  const [attemptId, setAttemptId] = useState("");
  const [answers, setAnswers] = useState<Answers>({});
  const [sectionIndex, setSectionIndex] = useState(0);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(0);
  const [confirm, setConfirm] = useState(false);
  const [result, setResult] = useState<Attempt | null>(null);
  const [saving, setSaving] = useState(false);
  const submitted = useRef(false);

  // --- start the attempt --------------------------------------------------
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await callApi<StartResponse>(`exams/${slug}/start`, {
          method: "POST",
          locale,
        });
        if (cancelled) return;
        setExam(data.exam);
        setAttemptId(data.attempt.id);
        setSecondsLeft(data.exam.duration_minutes * 60);
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
  }, [slug, locale]);

  const submit = useCallback(async () => {
    if (submitted.current) return;
    submitted.current = true;
    try {
      const data = await callApi<Attempt>(`attempts/${attemptId}/submit`, {
        method: "POST",
        body: { answers },
        locale,
      });
      setResult(data);
      setState("finished");
    } catch (caught) {
      setError((caught as Error).message);
      setState("error");
    }
  }, [attemptId, answers, locale]);

  // --- countdown ----------------------------------------------------------
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

  // --- autosave every 15s -------------------------------------------------
  useEffect(() => {
    if (state !== "running" || !attemptId || !Object.keys(answers).length) return;
    const timer = setTimeout(async () => {
      setSaving(true);
      try {
        await callApi(`attempts/${attemptId}/answers`, {
          method: "POST",
          body: { answers },
          locale,
        });
      } catch {
        // A failed autosave is recoverable: the final submit sends everything.
      } finally {
        setSaving(false);
      }
    }, 15000);
    return () => clearTimeout(timer);
  }, [answers, attemptId, state, locale]);

  const sections = useMemo(() => exam?.sections ?? [], [exam]);
  const section = sections[sectionIndex];
  const questions: ExamQuestion[] = useMemo(() => section?.questions ?? [], [section]);
  const question = questions[questionIndex];

  const totals = useMemo(() => {
    const all = sections.flatMap((item) => item.questions ?? []);
    return { count: all.length, answered: all.filter((item) => item.key in answers).length };
  }, [sections, answers]);

  if (state === "loading") {
    return (
      <div className="container-page py-32 text-center">
        <div className="glass mx-auto max-w-sm rounded-3xl p-10">
          <div className="mx-auto size-10 animate-spin rounded-full border-2 border-white/15 border-t-violet-400" />
          <p className="text-muted mt-5 text-sm">{dict.common.loading}</p>
        </div>
      </div>
    );
  }

  if (state === "error") {
    return (
      <div className="container-page py-32 text-center">
        <div className="glass mx-auto max-w-md rounded-3xl p-10">
          <p className="font-display text-xl font-semibold">{dict.common.error}</p>
          <p className="text-muted mt-3 text-sm">{error}</p>
          <div className="mt-7 flex justify-center gap-3">
            <ButtonLink href={`/${locale}/exams/${slug}`} variant="soft">
              {dict.common.back}
            </ButtonLink>
            <ButtonLink href={`/${locale}/login`}>{dict.nav.login}</ButtonLink>
          </div>
        </div>
      </div>
    );
  }

  if (state === "finished" && result) {
    return <ExamResult attempt={result} locale={locale} dict={dict} slug={slug} />;
  }

  if (!exam || !section || !question) return null;

  const accent = exam.accent;
  const lowTime = secondsLeft < 300;

  return (
    <div className="container-page pb-24">
      {/* ------------------------------------------------------- topbar --- */}
      <div className="glass-strong sticky top-24 z-30 mb-8 flex flex-wrap items-center gap-4 rounded-2xl px-5 py-3.5">
        <div className="flex items-center gap-3">
          <LevelBadge level={exam.level} />
          <span className="hidden text-sm font-semibold sm:block">{exam.title}</span>
        </div>

        <div className="ms-auto flex items-center gap-4">
          <span className="tnum text-xs text-mist-500">
            {formatNumber(totals.answered, locale)} / {formatNumber(totals.count, locale)}
          </span>
          {saving ? (
            <span className="text-xs text-mist-500">{dict.exams.runner.saving}</span>
          ) : null}
          <span
            className={cn(
              "tnum rounded-xl px-3 py-1.5 text-sm font-semibold",
              lowTime ? "bg-rose-400/15 text-rose-400" : "bg-white/8 text-mist-100",
            )}
          >
            {formatClock(secondsLeft)}
          </span>
          <Button size="sm" onClick={() => setConfirm(true)}>
            {dict.exams.runner.finish}
          </Button>
        </div>

        <Progress value={(totals.answered / Math.max(totals.count, 1)) * 100} color={accent} className="w-full" />
      </div>

      <div className="grid gap-8 lg:grid-cols-[1fr_17rem]">
        {/* ------------------------------------------------- question --- */}
        <div>
          <div className="mb-5 flex flex-wrap gap-2">
            {sections.map((item, index) => (
              <button
                key={item.index}
                type="button"
                onClick={() => {
                  setSectionIndex(index);
                  setQuestionIndex(0);
                }}
                className={cn(
                  "rounded-xl px-4 py-2 text-xs font-semibold transition",
                  index === sectionIndex
                    ? "text-ink-950"
                    : "glass text-mist-300 hover:border-white/25",
                )}
                style={index === sectionIndex ? { background: accent } : undefined}
              >
                {dict.exams.skills[item.skill]}
              </button>
            ))}
          </div>

          <article className="glass rounded-3xl p-7 md:p-9">
            <header className="mb-6 flex items-center justify-between gap-4">
              <span className="text-xs tracking-[0.2em] text-mist-500 uppercase">
                {dict.exams.runner.question} {formatNumber(questionIndex + 1, locale)}{" "}
                {dict.exams.runner.of} {formatNumber(questions.length, locale)}
              </span>
              <span className="tnum rounded-lg bg-white/6 px-2.5 py-1 text-xs text-mist-400">
                +{formatNumber(question.points, locale)}
              </span>
            </header>

            {question.passage ? (
              <p className="mb-5 rounded-2xl border border-white/8 bg-white/3 p-5 text-sm leading-relaxed text-mist-200">
                {question.passage}
              </p>
            ) : null}

            {question.audio_url ? (
              <audio controls className="mb-6 w-full" src={question.audio_url}>
                <track kind="captions" />
              </audio>
            ) : null}

            <h2
              lang="de"
              dir="ltr"
              className="font-display text-start text-xl leading-relaxed font-semibold text-balance md:text-2xl"
            >
              {question.prompt}
            </h2>

            {question.kind === "essay" ? (
              <textarea
                value={String(answers[question.key] ?? "")}
                onChange={(event) =>
                  setAnswers((current) => ({
                    ...current,
                    [question.key]: event.target.value as unknown as number,
                  }))
                }
                className="mt-6 min-h-48 w-full rounded-2xl border border-white/10 bg-white/4 p-5 text-sm outline-none focus:border-violet-400/60"
                placeholder="…"
              />
            ) : (
              <ul className="mt-7 space-y-3">
                {question.options.map((option, index) => {
                  const selected = answers[question.key] === index;
                  return (
                    <li key={`${question.key}-${index}`}>
                      <button
                        type="button"
                        onClick={() =>
                          setAnswers((current) => ({ ...current, [question.key]: index }))
                        }
                        className={cn(
                          "flex w-full items-center gap-4 rounded-2xl border px-5 py-4 text-start text-sm transition",
                          selected
                            ? "border-transparent"
                            : "border-white/10 hover:border-white/25 hover:bg-white/4",
                        )}
                        style={
                          selected
                            ? { background: alpha(accent, 0.16), borderColor: alpha(accent, 0.5) }
                            : undefined
                        }
                      >
                        <span
                          className={cn(
                            "grid size-7 shrink-0 place-items-center rounded-lg text-xs font-bold",
                            selected ? "text-ink-950" : "bg-white/8 text-mist-400",
                          )}
                          style={selected ? { background: accent } : undefined}
                        >
                          {String.fromCharCode(65 + index)}
                        </span>
                        <span lang="de" dir="ltr" className={selected ? "text-mist-50" : "text-mist-200"}>
                          {option}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            )}

            <footer className="mt-8 flex items-center justify-between gap-3 border-t border-white/8 pt-6">
              <Button
                variant="outline"
                onClick={() => setQuestionIndex((value) => Math.max(0, value - 1))}
                disabled={questionIndex === 0}
              >
                {dict.exams.runner.previous}
              </Button>
              {questionIndex < questions.length - 1 ? (
                <Button onClick={() => setQuestionIndex((value) => value + 1)}>
                  {dict.exams.runner.next}
                </Button>
              ) : sectionIndex < sections.length - 1 ? (
                <Button
                  onClick={() => {
                    setSectionIndex((value) => value + 1);
                    setQuestionIndex(0);
                  }}
                >
                  {dict.exams.runner.next} · {dict.exams.skills[sections[sectionIndex + 1].skill]}
                </Button>
              ) : (
                <Button onClick={() => setConfirm(true)}>{dict.exams.runner.finish}</Button>
              )}
            </footer>
          </article>
        </div>

        {/* ------------------------------------------------- navigator --- */}
        <aside className="glass h-fit rounded-3xl p-5 lg:sticky lg:top-48">
          <h2 className="mb-4 text-xs font-semibold tracking-[0.2em] text-mist-500 uppercase">
            {dict.exams.runner.section} {formatNumber(sectionIndex + 1, locale)}
          </h2>
          <div className="grid grid-cols-6 gap-2 lg:grid-cols-5">
            {questions.map((item, index) => {
              const answered = item.key in answers;
              const active = index === questionIndex;
              return (
                <button
                  key={item.key}
                  type="button"
                  onClick={() => setQuestionIndex(index)}
                  className={cn(
                    "tnum grid aspect-square place-items-center rounded-xl text-xs font-semibold transition",
                    active
                      ? "text-ink-950"
                      : answered
                        ? "bg-white/14 text-mist-50"
                        : "bg-white/5 text-mist-500 hover:bg-white/10",
                  )}
                  style={active ? { background: accent } : undefined}
                >
                  {index + 1}
                </button>
              );
            })}
          </div>
          <p className="tnum mt-5 border-t border-white/8 pt-4 text-xs text-mist-500">
            {formatNumber(totals.count - totals.answered, locale)} {dict.exams.runner.unanswered}
          </p>
        </aside>
      </div>

      {/* -------------------------------------------------- confirm ------ */}
      {confirm ? (
        <div className="fixed inset-0 z-100 grid place-items-center bg-ink-950/80 p-6 backdrop-blur-sm">
          <div className="glass-strong w-full max-w-md rounded-3xl p-8 text-center">
            <h2 className="font-display text-xl font-semibold">{dict.exams.runner.confirmTitle}</h2>
            <p className="text-muted mt-3 text-sm">{dict.exams.runner.confirmBody}</p>
            <p className="tnum mt-4 text-sm text-amber-400">
              {formatNumber(totals.count - totals.answered, locale)} {dict.exams.runner.unanswered}
            </p>
            <div className="mt-7 flex gap-3">
              <Button variant="outline" className="flex-1" onClick={() => setConfirm(false)}>
                {dict.exams.runner.cancel}
              </Button>
              <Button className="flex-1" onClick={submit}>
                {dict.exams.runner.submit}
              </Button>
            </div>
          </div>
        </div>
      ) : null}

      <p className="mt-8 text-center text-xs text-mist-600">
        <Link href={`/${locale}/exams`} className="hover:text-mist-300">
          {dict.exams.result.backToExams}
        </Link>
      </p>
    </div>
  );
}
