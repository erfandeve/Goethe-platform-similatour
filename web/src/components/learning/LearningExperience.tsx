"use client";

import Link from "next/link";
import { useCallback, useMemo, useRef, useState } from "react";

import { useSpeakingTeacher } from "@/hooks/useSpeakingTeacher";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatNumber } from "@/lib/format";
import type { Classroom, SpeakingAttempt, SpeakingState } from "@/lib/learning";
import { flattenVideos } from "@/lib/learning";

import { AITeacher } from "./AITeacher";
import { CourseComplete, PartComplete } from "./Completion";
import { Countdown } from "./Countdown";
import { ProgressPanel } from "./ProgressPanel";
import { SpeakingRecorder } from "./SpeakingRecorder";
import { SpeakingResult } from "./SpeakingResult";
import { VideoPlayer, type VideoPlayerHandle } from "./VideoPlayer";

/**
 * Drives one course: which scene is on screen, what the learner may do next and
 * when the microphone opens. A single state value decides all of it, so the UI
 * can never end up in two moods at once.
 */
export function LearningExperience({
  classroom,
  locale,
  dict,
  maxAudioSeconds,
}: {
  classroom: Classroom;
  locale: Locale;
  dict: Dictionary;
  maxAudioSeconds: number;
}) {
  const accent = classroom.course.accent || "#22d3ee";
  const sequence = useMemo(() => flattenVideos(classroom.parts), [classroom.parts]);

  const firstUnfinished = Math.max(
    0,
    sequence.findIndex((entry) => !entry.video.progress?.completed),
  );
  const [index, setIndex] = useState(firstUnfinished === -1 ? 0 : firstUnfinished);
  const [completed, setCompleted] = useState<Set<string>>(
    () => new Set(sequence.filter((e) => e.video.progress?.completed).map((e) => e.video.id)),
  );
  const [attemptsCount, setAttemptsCount] = useState(classroom.stats.speaking_attempts);
  const [scores, setScores] = useState<number[]>([]);
  const [autoPlay, setAutoPlay] = useState(false);

  const player = useRef<VideoPlayerHandle>(null);
  const current = sequence[index];
  const isLastOfPart =
    index + 1 >= sequence.length || sequence[index + 1].part.id !== current.part.id;

  const [flow, setFlow] = useState<SpeakingState>("VIDEO_PLAYING");

  const teacher = useSpeakingTeacher({
    video: current.video,
    maxSeconds: maxAudioSeconds,
    locale,
    onFinished: (attempt: SpeakingAttempt) => {
      setAttemptsCount((value) => value + 1);
      if (attempt.analysis) setScores((value) => [...value, attempt.analysis!.overall_score]);
    },
  });

  const saveProgress = useCallback(
    (position: number, duration: number, done = false) => {
      void callApi("progress/video", {
        method: "POST",
        body: {
          video_id: current.video.id,
          position_seconds: position,
          duration_seconds: duration,
          completed: done,
        },
      }).catch(() => {
        // Progress is a convenience; a dropped save must not break the lesson.
      });
    },
    [current.video.id],
  );

  const handleProgress = useCallback(
    (position: number, duration: number) => saveProgress(position, duration),
    [saveProgress],
  );

  const handleAutoplayBlocked = useCallback(() => setFlow("VIDEO_PAUSED"), []);

  const goTo = useCallback(
    (nextIndex: number, { play = true } = {}) => {
      if (nextIndex < 0 || nextIndex >= sequence.length) return;
      teacher.reset();
      setIndex(nextIndex);
      setAutoPlay(play);
      setFlow("VIDEO_PLAYING");
    },
    [sequence.length, teacher],
  );

  const [manualStart, setManualStart] = useState(false);

  const handleEnded = useCallback(() => {
    setCompleted((current_) => new Set(current_).add(current.video.id));
    saveProgress(current.video.duration_seconds, current.video.duration_seconds, true);
    // Nothing should still be moving or playing while the learner speaks.
    player.current?.pause();

    if (current.video.has_speaking_task) {
      setManualStart(false);
      setFlow("COUNTDOWN");
      return;
    }
    // Watch-only scenes roll straight into the next one.
    setFlow(index + 1 < sequence.length ? "NEXT_VIDEO_COUNTDOWN" : "COURSE_COMPLETED");
  }, [current.video, index, sequence.length, saveProgress]);

  const advance = useCallback(() => {
    if (index + 1 >= sequence.length) {
      setFlow("COURSE_COMPLETED");
      return;
    }
    if (isLastOfPart) {
      setFlow("PART_COMPLETED");
      return;
    }
    goTo(index + 1);
  }, [index, sequence.length, isLastOfPart, goTo]);

  const averageScore = scores.length
    ? Math.round(scores.reduce((sum, value) => sum + value, 0) / scores.length)
    : classroom.stats.average_score;

  const partVideos = current.part.videos.length;

  // ---------------------------------------------------------------- panels ---

  const teacherPanel = (() => {
    if (flow === "COUNTDOWN") {
      return (
        <Countdown
          label={dict.learning.countdown.speak}
          hint={dict.learning.countdown.autoStart}
          accent={accent}
          cancelLabel={dict.learning.recorder.notReady}
          onCancel={() => {
            // Opting out hands control back: the mic waits for a deliberate press.
            setManualStart(true);
            setFlow("READY_TO_SPEAK");
          }}
          onDone={() => {
            setFlow("READY_TO_SPEAK");
            void teacher.start();
          }}
        />
      );
    }
    if (flow === "NEXT_VIDEO_COUNTDOWN") {
      return (
        <Countdown
          label={dict.learning.countdown.next}
          accent={accent}
          onDone={advance}
        />
      );
    }
    if (teacher.state === "SHOWING_RESULT" && teacher.attempt) {
      return (
        <SpeakingResult
          attempt={teacher.attempt}
          locale={locale}
          dict={dict}
          isLast={isLastOfPart}
          onRetry={() => {
            teacher.reset();
            setManualStart(true);
          }}
          onContinue={() => {
            teacher.reset();
            setFlow("NEXT_VIDEO_COUNTDOWN");
          }}
          onReplay={() => {
            teacher.reset();
            setFlow("VIDEO_PLAYING");
            void player.current?.replay();
          }}
        />
      );
    }
    if (flow === "READY_TO_SPEAK" || teacher.state !== "READY_TO_SPEAK") {
      return (
        <SpeakingRecorder
          state={teacher.state}
          waitingForLearner={manualStart}
          error={teacher.error}
          errorDetail={teacher.errorDetail}
          elapsed={teacher.elapsed}
          remaining={teacher.remaining}
          maxSeconds={maxAudioSeconds}
          accent={accent}
          locale={locale}
          dict={dict}
          onStart={teacher.start}
          onStop={teacher.stop}
          onCancel={teacher.cancel}
          onRetry={() => teacher.reset()}
        />
      );
    }
    return (
      <div className="glass rounded-3xl p-6 text-center text-sm text-mist-400">
        {current.video.has_speaking_task
          ? dict.learning.teacher.waiting
          : dict.learning.watchOnly}
      </div>
    );
  })();

  if (flow === "COURSE_COMPLETED") {
    return (
      <CourseComplete
        videos={completed.size}
        attempts={attemptsCount}
        average={averageScore}
        estimate={teacher.attempt?.analysis?.cefr_estimate ?? classroom.course.level}
        locale={locale}
        dict={dict}
      />
    );
  }

  if (flow === "PART_COMPLETED") {
    return (
      <PartComplete
        partTitle={current.part.title_de}
        videos={partVideos}
        attempts={attemptsCount}
        average={averageScore}
        accent={accent}
        locale={locale}
        dict={dict}
        onNext={() => goTo(index + 1)}
      />
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_25rem] xl:grid-cols-[1fr_28rem]">
      <div className="space-y-5">
        <div className="flex flex-wrap items-center gap-3">
          <span
            className="rounded-lg px-2.5 py-1 text-[11px] font-semibold"
            style={{ background: `${accent}22`, color: accent }}
            dir="ltr"
          >
            {current.part.title_de}
          </span>
          <span className="tnum text-xs text-mist-500">
            {dict.learning.lesson} {formatNumber(index + 1, locale)} /{" "}
            {formatNumber(sequence.length, locale)}
          </span>
        </div>

        <VideoPlayer
          ref={player}
          key={current.video.id}
          video={current.video}
          dict={dict}
          accent={accent}
          autoPlay={autoPlay}
          onEnded={handleEnded}
          onProgress={handleProgress}
          onAutoplayBlocked={handleAutoplayBlocked}
        />

        <div>
          <h1 className="font-display text-xl font-semibold" lang="de" dir="ltr">
            {current.video.scene_label || current.video.title_de}
          </h1>
          {current.video.description ? (
            <p className="text-muted mt-2 text-sm">{current.video.description}</p>
          ) : null}
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => goTo(index - 1)}
            disabled={index === 0}
            className="glass rounded-full px-5 py-2.5 text-sm disabled:opacity-40"
          >
            {dict.learning.actions.previous}
          </button>
          <button
            type="button"
            onClick={() => {
              setFlow("VIDEO_PLAYING");
              void player.current?.replay();
            }}
            className="glass rounded-full px-5 py-2.5 text-sm"
          >
            {dict.learning.actions.replay}
          </button>
          <button
            type="button"
            onClick={() => goTo(index + 1)}
            disabled={index + 1 >= sequence.length}
            className="glass rounded-full px-5 py-2.5 text-sm disabled:opacity-40"
          >
            {dict.learning.actions.next}
          </button>
          <Link
            href={`/${locale}/courses/${classroom.course.slug}`}
            className="ms-auto rounded-full px-5 py-2.5 text-sm text-mist-500 hover:text-mist-200"
          >
            {dict.learning.backToCourse}
          </Link>
        </div>

        <ProgressPanel
          parts={classroom.parts}
          current={current.video}
          accent={accent}
          locale={locale}
          dict={dict}
          completed={completed}
          onSelect={(video) => {
            const target = sequence.findIndex((entry) => entry.video.id === video.id);
            if (target >= 0) goTo(target, { play: false });
          }}
        />
      </div>

      <AITeacher video={current.video} accent={accent} dict={dict}>
        {teacherPanel}
      </AITeacher>
    </div>
  );
}
