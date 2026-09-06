"use client";

import { useEffect, useState } from "react";

/** The three-beat pause between a scene and the next thing that happens. */
export function Countdown({
  from = 3,
  label,
  hint,
  accent,
  onDone,
  onCancel,
  cancelLabel,
}: {
  from?: number;
  label: string;
  hint?: string;
  accent: string;
  onDone: () => void;
  onCancel?: () => void;
  cancelLabel?: string;
}) {
  const [value, setValue] = useState(from);

  useEffect(() => {
    if (value <= 0) {
      onDone();
      return;
    }
    const timer = setTimeout(() => setValue((current) => current - 1), 1000);
    return () => clearTimeout(timer);
  }, [value, onDone]);

  return (
    <div className="glass flex flex-col items-center gap-4 rounded-3xl p-10 text-center">
      <span
        key={value}
        className="font-display grid size-20 place-items-center rounded-full text-4xl font-bold text-ink-950"
        style={{ background: accent, animation: "rise 0.4s ease-out" }}
        aria-live="polite"
      >
        {Math.max(1, value)}
      </span>
      <p className="text-sm text-mist-300">{label}</p>
      {hint ? <p className="-mt-2 text-xs text-mist-500">{hint}</p> : null}
      {onCancel && cancelLabel ? (
        <button
          type="button"
          onClick={onCancel}
          className="glass rounded-full px-5 py-2 text-xs text-mist-300 transition hover:text-mist-50"
        >
          {cancelLabel}
        </button>
      ) : null}
    </div>
  );
}
