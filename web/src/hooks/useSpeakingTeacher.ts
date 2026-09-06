"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { callApi } from "@/lib/client";
import type { LessonVideo, SpeakingAttempt, SpeakingState } from "@/lib/learning";

const MIME_CANDIDATES = [
  "audio/webm;codecs=opus",
  "audio/webm",
  "audio/mp4",
  "audio/ogg;codecs=opus",
];

const MIN_RECORDING_MS = 700;

export type SpeakingError =
  | "unsupported"
  | "denied"
  | "too_short"
  | "empty"
  | "upload"
  | "analysis";

interface Options {
  video: LessonVideo | null;
  maxSeconds: number;
  /** Drives the language the teacher writes its explanations in. */
  locale: string;
  onFinished?: (attempt: SpeakingAttempt) => void;
}

/**
 * Owns the microphone and the request chain for one spoken answer.
 *
 * The chain is deliberately linear — record → upload → transcribe → analyse —
 * and a run in flight blocks a second one, so a double click or a re-render can
 * never buy two analyses.
 */
export function useSpeakingTeacher({ video, maxSeconds, locale, onFinished }: Options) {
  const [state, setState] = useState<SpeakingState>("READY_TO_SPEAK");
  const [error, setError] = useState<SpeakingError | null>(null);
  const [errorDetail, setErrorDetail] = useState("");
  const [attempt, setAttempt] = useState<SpeakingAttempt | null>(null);
  const [elapsed, setElapsed] = useState(0);

  const recorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<BlobPart[]>([]);
  const stream = useRef<MediaStream | null>(null);
  const startedAt = useRef(0);
  const busy = useRef(false);
  const cancelled = useRef(false);

  const cleanup = useCallback(() => {
    stream.current?.getTracks().forEach((track) => track.stop());
    stream.current = null;
    recorder.current = null;
    chunks.current = [];
  }, []);

  useEffect(() => cleanup, [cleanup]);

  const reset = useCallback(() => {
    cancelled.current = true;
    busy.current = false;
    cleanup();
    setAttempt(null);
    setError(null);
    setErrorDetail("");
    setElapsed(0);
    setState("READY_TO_SPEAK");
  }, [cleanup]);

  const run = useCallback(
    async (blob: Blob, seconds: number) => {
      if (!video) return;
      try {
        setState("UPLOADING");
        const form = new FormData();
        const extension = blob.type.includes("mp4") ? "mp4" : blob.type.includes("ogg") ? "ogg" : "webm";
        form.append("audio", blob, `answer.${extension}`);
        form.append("video_id", video.id);
        form.append("language", "de");

        setState("TRANSCRIBING");
        const upload = await fetch("/api/ai/transcribe", { method: "POST", body: form });
        const transcribed = await upload.json().catch(() => ({}));
        if (cancelled.current) return;

        if (!upload.ok || !transcribed.success) {
          setError("upload");
          setErrorDetail(transcribed.error ?? transcribed.detail ?? "");
          setState("ERROR");
          return;
        }
        if (transcribed.is_empty || !transcribed.transcript?.trim()) {
          setError("empty");
          setState("ERROR");
          return;
        }

        setState("ANALYZING");
        const analysed = await callApi<{ success: boolean; attempt: SpeakingAttempt }>(
          "ai/analyze",
          {
            method: "POST",
            locale,
            body: {
              transcript: transcribed.transcript,
              video_id: video.id,
              audio_path: transcribed.audio_path ?? "",
              audio_seconds: seconds,
            },
          },
        );
        if (cancelled.current) return;

        setAttempt(analysed.attempt);
        setState("SHOWING_RESULT");
        onFinished?.(analysed.attempt);
      } catch (caught) {
        if (cancelled.current) return;
        const failure = caught as { code?: string; message?: string };
        setError(failure.code === "empty_transcript" ? "empty" : "analysis");
        setErrorDetail(failure.message ?? "");
        setState("ERROR");
      } finally {
        busy.current = false;
      }
    },
    [video, locale, onFinished],
  );

  const stop = useCallback(() => {
    const active = recorder.current;
    if (!active || active.state === "inactive") return;
    active.stop();
  }, []);

  const start = useCallback(async () => {
    if (busy.current || !video) return;
    if (typeof MediaRecorder === "undefined" || !navigator.mediaDevices?.getUserMedia) {
      setError("unsupported");
      setState("ERROR");
      return;
    }

    cancelled.current = false;
    setError(null);
    setErrorDetail("");
    setAttempt(null);

    let media: MediaStream;
    try {
      media = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch {
      setError("denied");
      setState("ERROR");
      return;
    }

    busy.current = true;
    stream.current = media;
    chunks.current = [];

    const mime = MIME_CANDIDATES.find((type) => MediaRecorder.isTypeSupported(type));
    const active = new MediaRecorder(media, mime ? { mimeType: mime } : undefined);
    recorder.current = active;

    active.ondataavailable = (event) => {
      if (event.data.size) chunks.current.push(event.data);
    };
    active.onstop = () => {
      const seconds = (Date.now() - startedAt.current) / 1000;
      const blob = new Blob(chunks.current, { type: active.mimeType || "audio/webm" });
      cleanup();

      if (cancelled.current) {
        busy.current = false;
        return;
      }
      if (Date.now() - startedAt.current < MIN_RECORDING_MS || blob.size < 1024) {
        busy.current = false;
        setError("too_short");
        setState("ERROR");
        return;
      }
      void run(blob, seconds);
    };

    startedAt.current = Date.now();
    setElapsed(0);
    active.start();
    setState("RECORDING");
  }, [video, cleanup, run]);

  // Recording clock, with the hard stop the server also enforces.
  useEffect(() => {
    if (state !== "RECORDING") return;
    const timer = setInterval(() => {
      const seconds = (Date.now() - startedAt.current) / 1000;
      setElapsed(seconds);
      if (seconds >= maxSeconds) stop();
    }, 200);
    return () => clearInterval(timer);
  }, [state, maxSeconds, stop]);

  const cancel = useCallback(() => {
    cancelled.current = true;
    const active = recorder.current;
    if (active && active.state !== "inactive") active.stop();
    cleanup();
    busy.current = false;
    setState("READY_TO_SPEAK");
  }, [cleanup]);

  return {
    state,
    setState,
    error,
    errorDetail,
    attempt,
    elapsed,
    remaining: Math.max(0, maxSeconds - elapsed),
    start,
    stop,
    cancel,
    reset,
  };
}
