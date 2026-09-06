"use client";

import { useState } from "react";

import { alpha, cn, mediaUrl } from "@/lib/utils";

/**
 * The artwork slot. An uploaded cover wins; without one — or if the file is
 * missing — it falls back to a generated gradient in the item's accent, so a
 * catalogue with half its images filled in never looks broken.
 */
export function CoverArt({
  accent,
  label,
  caption,
  src,
  alt,
  className,
  ratio = "aspect-16/10",
}: {
  accent: string;
  label: string;
  caption?: string;
  src?: string;
  alt?: string;
  className?: string;
  ratio?: string;
}) {
  const [failed, setFailed] = useState(false);
  const image = src && !failed ? mediaUrl(src) : "";

  return (
    <div
      className={cn("relative w-full overflow-hidden", ratio, className)}
      style={{
        background: `radial-gradient(120% 120% at 15% 0%, ${alpha(accent, 0.85)} 0%, ${alpha(
          accent,
          0.25,
        )} 42%, rgba(8,8,20,0.96) 78%)`,
      }}
    >
      {image ? (
        <>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={image}
            alt={alt ?? ""}
            loading="lazy"
            className="absolute inset-0 size-full object-cover"
            onError={() => setFailed(true)}
          />
          <div
            className="absolute inset-0 bg-linear-to-t from-ink-950/85 via-ink-950/25 to-transparent"
            aria-hidden
          />
        </>
      ) : (
        <div aria-hidden>
          <div
            className="absolute -end-10 -top-16 size-56 rounded-full opacity-45 blur-2xl"
            style={{ background: alpha(accent, 0.55) }}
          />
          <svg viewBox="0 0 200 120" className="absolute inset-0 size-full opacity-30">
            <circle cx="150" cy="30" r="46" fill="none" stroke="white" strokeOpacity="0.22" />
            <circle cx="150" cy="30" r="70" fill="none" stroke="white" strokeOpacity="0.12" />
            <circle cx="30" cy="100" r="34" fill="none" stroke="white" strokeOpacity="0.14" />
          </svg>
        </div>
      )}

      <div className="absolute inset-0 flex flex-col justify-end p-5" aria-hidden>
        <span className="font-display text-4xl leading-none font-bold text-white/95 drop-shadow-sm">
          {label}
        </span>
        {caption ? (
          <span className="mt-1 text-[11px] tracking-[0.2em] text-white/60 uppercase">
            {caption}
          </span>
        ) : null}
      </div>
    </div>
  );
}
