"use client";

import { useEffect, useState, type ReactNode } from "react";

import { cn } from "@/lib/utils";

/**
 * The exam chrome: a fixed dark header with the session id, remaining time and
 * the accessibility controls, a time bar, two content panels and the green edge
 * buttons that move between tasks — the layout of the Goethe digital player.
 */
export function ExamShell({
  sessionId,
  minutesLeft,
  elapsedRatio,
  page,
  pages,
  workMinutes,
  audioBadge,
  onPrev,
  onNext,
  canPrev,
  canNext,
  nextLabel,
  prevLabel,
  left,
  right,
  brand,
}: {
  sessionId: string;
  minutesLeft: number;
  elapsedRatio: number;
  page: number;
  pages: number;
  workMinutes?: number;
  audioBadge?: string;
  onPrev: () => void;
  onNext: () => void;
  canPrev: boolean;
  canNext: boolean;
  nextLabel: string;
  prevLabel: string;
  left: ReactNode;
  right: ReactNode;
  brand: string;
}) {
  const [scale, setScale] = useState(1);
  const [contrast, setContrast] = useState<"normal" | "high">("normal");
  const [volume, setVolume] = useState(1);
  const [stacked, setStacked] = useState(false);

  // Exam mode takes over the window: the site header and footer step aside.
  useEffect(() => {
    document.body.dataset.mode = "exam";
    return () => {
      delete document.body.dataset.mode;
    };
  }, []);

  useEffect(() => {
    document.querySelectorAll("audio").forEach((element) => {
      (element as HTMLAudioElement).volume = volume;
    });
  }, [volume]);

  return (
    <div
      dir="ltr"
      className="exam-root fixed inset-0 flex flex-col"
      data-contrast={contrast}
      style={{ ["--exam-scale" as string]: scale, background: "var(--exam-page)" }}
    >
      <header
        className="relative flex h-16 shrink-0 items-center px-5 text-white"
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
          <span className="hidden text-xs leading-tight font-semibold tracking-wide sm:block">
            {brand.toUpperCase()}
            <span className="block text-[10px] font-normal text-white/55">AKADEMIE</span>
          </span>
        </span>

        <span className="absolute start-1/2 -translate-x-1/2 text-center rtl:translate-x-1/2">
          <span className="tnum block text-sm font-semibold" dir="ltr">
            {sessionId}
          </span>
          <span className="block text-sm" dir="ltr">
            verbleibende Zeit | <b>{minutesLeft} Minuten</b>
          </span>
        </span>

        <span className="ms-auto flex items-center gap-2">
          {audioBadge ? (
            <span className="me-2 hidden items-center gap-2 text-xs text-white/85 lg:flex">
              <svg viewBox="0 0 24 24" className="size-4" fill="currentColor" aria-hidden>
                <path d="M4 9v6h4l5 4V5L8 9H4Zm12.5 3a4.5 4.5 0 0 0-2-3.7v7.4a4.5 4.5 0 0 0 2-3.7Z" />
              </svg>
              {audioBadge}
            </span>
          ) : null}

          <Stepper
            icon="A"
            label="Schriftgröße"
            onMinus={() => setScale((value) => Math.max(0.85, +(value - 0.1).toFixed(2)))}
            onPlus={() => setScale((value) => Math.min(1.5, +(value + 0.1).toFixed(2)))}
          />
          <Stepper
            icon="◐"
            label="Kontrast"
            onMinus={() => setContrast("normal")}
            onPlus={() => setContrast("high")}
          />
          <Stepper
            icon="🔊"
            label="Lautstärke"
            onMinus={() => setVolume((value) => Math.max(0, +(value - 0.2).toFixed(1)))}
            onPlus={() => setVolume((value) => Math.min(1, +(value + 0.2).toFixed(1)))}
          />
        </span>
      </header>

      {/* elapsed (grey) vs remaining (green) */}
      <div className="h-1.5 w-full shrink-0" style={{ background: "var(--exam-green)" }}>
        <div
          className="h-full transition-[width] duration-1000 ease-linear"
          style={{ width: `${Math.min(100, elapsedRatio * 100)}%`, background: "#6d7375" }}
        />
      </div>

      <div className="relative flex min-h-0 flex-1">
        <EdgeButton side="start" onClick={onPrev} disabled={!canPrev} label={prevLabel} />

        <div
          className={cn(
            "grid min-h-0 flex-1 gap-4 p-4",
            stacked ? "grid-rows-2" : "md:grid-cols-2",
          )}
        >
          <section
            className="exam-scroll min-h-0 rounded-sm p-6 md:p-8"
            style={{ background: "var(--exam-card)", border: "1px solid var(--exam-line)" }}
          >
            {left}
          </section>

          <section
            className="exam-scroll relative min-h-0 rounded-sm p-6 md:p-8"
            style={{ background: "var(--exam-card)", border: "1px solid var(--exam-line)" }}
          >
            <div className="mb-5 flex items-center justify-between border-b pb-3" style={{ borderColor: "var(--exam-line)" }}>
              {workMinutes ? (
                <span className="flex items-center gap-1.5 text-xs" style={{ color: "var(--exam-muted)" }}>
                  <svg viewBox="0 0 24 24" className="size-3.5" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden>
                    <circle cx="12" cy="12" r="8.5" />
                    <path d="M12 7.5V12l3 2" strokeLinecap="round" />
                  </svg>
                  <span dir="ltr">Arbeitszeit: {workMinutes} Minuten</span>
                </span>
              ) : (
                <span />
              )}
              <span className="tnum text-sm" dir="ltr">
                <b>{page}</b> <span style={{ color: "var(--exam-muted)" }}>| {pages}</span>
              </span>
            </div>
            {right}
          </section>
        </div>

        <EdgeButton side="end" onClick={onNext} disabled={!canNext} label={nextLabel} />

        <div className="absolute end-3 bottom-3 hidden flex-col gap-1 md:flex">
          <LayoutToggle active={!stacked} onClick={() => setStacked(false)} orientation="cols" />
          <LayoutToggle active={stacked} onClick={() => setStacked(true)} orientation="rows" />
        </div>
      </div>
    </div>
  );
}

function Stepper({
  icon,
  label,
  onMinus,
  onPlus,
}: {
  icon: string;
  label: string;
  onMinus: () => void;
  onPlus: () => void;
}) {
  return (
    <span
      className="flex items-center gap-1 rounded-sm px-1.5 py-1"
      style={{ background: "var(--exam-bar-soft)" }}
      role="group"
      aria-label={label}
    >
      <button type="button" onClick={onMinus} className="px-1.5 text-lg leading-none text-white/85 hover:text-white" aria-label={`${label} verkleinern`}>
        −
      </button>
      <span className="w-4 text-center text-sm" style={{ color: "var(--exam-green)" }} aria-hidden>
        {icon}
      </span>
      <button type="button" onClick={onPlus} className="px-1.5 text-lg leading-none text-white/85 hover:text-white" aria-label={`${label} vergrößern`}>
        +
      </button>
    </span>
  );
}

function EdgeButton({
  side,
  onClick,
  disabled,
  label,
}: {
  side: "start" | "end";
  onClick: () => void;
  disabled: boolean;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      title={label}
      aria-label={label}
      className={cn(
        "group absolute top-1/2 z-20 grid h-24 w-11 -translate-y-1/2 place-items-center text-white transition-colors",
        side === "start" ? "start-0 rounded-e-md" : "end-0 rounded-s-md",
        disabled && "pointer-events-none opacity-0",
      )}
      style={{ background: "var(--exam-green)" }}
    >
      <span
        className={cn("text-xl leading-none", side === "start" ? "rtl:rotate-180" : "rtl:rotate-180")}
        aria-hidden
      >
        {side === "start" ? "←" : "→"}
      </span>
    </button>
  );
}

function LayoutToggle({
  active,
  onClick,
  orientation,
}: {
  active: boolean;
  onClick: () => void;
  orientation: "cols" | "rows";
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={orientation === "cols" ? "Nebeneinander" : "Untereinander"}
      className={cn("grid h-7 w-10 place-items-center rounded-sm border bg-white transition")}
      style={{ borderColor: active ? "var(--exam-green-dark)" : "var(--exam-line)" }}
    >
      <svg viewBox="0 0 24 16" className="h-3.5 w-6" aria-hidden>
        {orientation === "cols" ? (
          <>
            <rect x="1" y="1" width="10" height="14" rx="1" fill="none" stroke="currentColor" strokeWidth="1.5" />
            <rect x="13" y="1" width="10" height="14" rx="1" fill="none" stroke="currentColor" strokeWidth="1.5" />
          </>
        ) : (
          <>
            <rect x="1" y="1" width="22" height="6" rx="1" fill="none" stroke="currentColor" strokeWidth="1.5" />
            <rect x="1" y="9" width="22" height="6" rx="1" fill="none" stroke="currentColor" strokeWidth="1.5" />
          </>
        )}
      </svg>
    </button>
  );
}
