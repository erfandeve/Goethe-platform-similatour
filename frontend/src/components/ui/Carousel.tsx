"use client";

import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";

import { cn } from "@/lib/utils";

/**
 * A horizontal, snap-scrolling rail.
 *
 * Arrow keys and a drag both work because it is a real scroll container; the
 * buttons only nudge it. Direction is read from the document so the "next"
 * button moves the same way the language reads.
 *
 * With `grid`, the rail only exists on small screens: from md up the same
 * items lay out as that grid. One set of markup, so nothing is duplicated for
 * search engines and nothing is rendered twice.
 *
 * With `autoplay`, the rail advances one card at a time and loops. It holds
 * still while it is being touched, hovered or focused, while it is off screen
 * or the tab is hidden, whenever there is nothing to scroll (the desktop
 * grid), and for anyone who has asked their system for reduced motion.
 */
export function Carousel({
  children,
  className,
  itemClassName = "w-[19rem] sm:w-[21rem] lg:w-[23rem]",
  label,
  grid,
  autoplay,
}: {
  children: ReactNode[];
  className?: string;
  itemClassName?: string;
  label?: string;
  /** Grid classes to switch to from md up, e.g. "md:grid-cols-2 lg:grid-cols-3". */
  grid?: string;
  /** Milliseconds between automatic steps. */
  autoplay?: number;
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

  /** One card's width plus the gap, so a step lands on the next snap point. */
  const stepSize = useCallback((node: HTMLDivElement) => {
    const first = node.firstElementChild as HTMLElement | null;
    const gap = parseFloat(getComputedStyle(node).columnGap) || 0;
    return first ? first.getBoundingClientRect().width + gap : node.clientWidth * 0.8;
  }, []);

  function nudge(direction: -1 | 1) {
    const node = track.current;
    if (!node) return;
    const rtl = getComputedStyle(node).direction === "rtl";
    const step = node.clientWidth * 0.8;
    node.scrollBy({ left: step * direction * (rtl ? -1 : 1), behavior: "smooth" });
  }

  useEffect(() => {
    const node = track.current;
    if (!autoplay || !node) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    let held = false;
    let visible = false;
    let release: ReturnType<typeof setTimeout> | undefined;

    const hold = () => {
      held = true;
      clearTimeout(release);
    };
    // After a touch or a hover, wait one full interval before moving again,
    // so the card someone just reached does not slide away under them.
    const letGo = () => {
      clearTimeout(release);
      release = setTimeout(() => {
        held = false;
      }, autoplay);
    };

    const events: [string, () => void][] = [
      ["pointerenter", hold],
      ["pointerleave", letGo],
      ["pointerdown", hold],
      ["pointerup", letGo],
      ["touchstart", hold],
      ["touchend", letGo],
      ["focusin", hold],
      ["focusout", letGo],
    ];
    events.forEach(([name, handler]) => node.addEventListener(name, handler, { passive: true }));

    const seen = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
    });
    seen.observe(node);

    const tick = setInterval(() => {
      if (held || !visible || document.hidden) return;
      const max = node.scrollWidth - node.clientWidth;
      if (max < 8) return; // laid out as a grid, or everything already fits
      const offset = Math.abs(node.scrollLeft);
      if (max - offset < 8) {
        node.scrollTo({ left: 0, behavior: "smooth" });
        return;
      }
      const rtl = getComputedStyle(node).direction === "rtl";
      node.scrollBy({ left: stepSize(node) * (rtl ? -1 : 1), behavior: "smooth" });
    }, autoplay);

    return () => {
      clearInterval(tick);
      clearTimeout(release);
      seen.disconnect();
      events.forEach(([name, handler]) => node.removeEventListener(name, handler));
    };
  }, [autoplay, stepSize]);

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
          grid && cn("md:grid md:snap-none md:overflow-visible md:pb-0", grid),
        )}
      >
        {children.map((child, index) => (
          <div
            key={index}
            className={cn(
              "shrink-0 snap-start",
              grid ? "w-[84%] sm:w-[62%] md:w-auto" : itemClassName,
            )}
          >
            {child}
          </div>
        ))}
      </div>

      {/* A grid needs no arrows; a phone scrolls the rail with a thumb. */}
      {grid ? null : (
        <>
          <RailButton side="start" onClick={() => nudge(-1)} disabled={atStart} />
          <RailButton side="end" onClick={() => nudge(1)} disabled={atEnd} />
        </>
      )}
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
