"use client";

import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";

import { cn } from "@/lib/utils";

/**
 * A horizontal, snap-scrolling rail.
 *
 * Arrow keys and a drag both work because it is a real scroll container; the
 * buttons only nudge it. Direction is read from the document so the "next"
 * button moves the same way the language reads.
 */
export function Carousel({
  children,
  className,
  itemClassName = "w-[19rem] sm:w-[21rem] lg:w-[23rem]",
  label,
}: {
  children: ReactNode[];
  className?: string;
  itemClassName?: string;
  label?: string;
}) {
  const track = useRef<HTMLDivElement>(null);
  const [atStart, setAtStart] = useState(true);
  const [atEnd, setAtEnd] = useState(false);

  const sync = useCallback(() => {
    const node = track.current;
    if (!node) return;
    // In RTL browsers report negative scrollLeft; distance is what matters.
    const offset = Math.abs(node.scrollLeft);
    const max = node.scrollWidth - node.clientWidth;
    setAtStart(offset < 8);
    setAtEnd(max - offset < 8);
  }, []);

  useEffect(() => {
    sync();
    const node = track.current;
    if (!node) return;
    const observer = new ResizeObserver(sync);
    observer.observe(node);
    return () => observer.disconnect();
  }, [sync, children.length]);

  function nudge(direction: -1 | 1) {
    const node = track.current;
    if (!node) return;
    const rtl = getComputedStyle(node).direction === "rtl";
    const step = node.clientWidth * 0.8;
    node.scrollBy({ left: step * direction * (rtl ? -1 : 1), behavior: "smooth" });
  }

  return (
    <div className={cn("relative", className)}>
      <div
        ref={track}
        onScroll={sync}
        role="region"
        aria-label={label}
        tabIndex={0}
        className={cn(
          "flex snap-x snap-mandatory gap-5 overflow-x-auto scroll-smooth pb-3",
          // The scrollbar would fight the card shadows; the buttons replace it.
          "[-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden",
        )}
      >
        {children.map((child, index) => (
          <div key={index} className={cn("shrink-0 snap-start", itemClassName)}>
            {child}
          </div>
        ))}
      </div>

      <RailButton side="start" onClick={() => nudge(-1)} disabled={atStart} />
      <RailButton side="end" onClick={() => nudge(1)} disabled={atEnd} />
    </div>
  );
}

function RailButton({
  side,
  onClick,
  disabled,
}: {
  side: "start" | "end";
  onClick: () => void;
  disabled: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={side === "start" ? "قبلی" : "بعدی"}
      className={cn(
        "glass-strong absolute top-1/2 z-10 hidden size-11 -translate-y-1/2 place-items-center rounded-full text-lg transition md:grid",
        side === "start" ? "-start-4" : "-end-4",
        disabled ? "pointer-events-none opacity-0" : "opacity-100 hover:border-white/30",
      )}
    >
      <span className="flip-x" aria-hidden>
        {side === "start" ? "←" : "→"}
      </span>
    </button>
  );
}
