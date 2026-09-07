"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";

import { cn } from "@/lib/utils";

/**
 * Scroll-reveal wrapper.
 *
 * Deliberately CSS-driven and visible by default: content that is already on
 * screen (or rendered before hydration) never depends on JavaScript to become
 * readable. Only elements that start below the fold are hidden and then eased
 * in when they scroll into view.
 */
export function Reveal({
  children,
  delay = 0,
  className,
}: {
  children: ReactNode;
  delay?: number;
  /** Kept for call-site symmetry; the travel distance lives in CSS. */
  y?: number;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node || typeof IntersectionObserver === "undefined") return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const viewport = window.innerHeight || document.documentElement.clientHeight;
    if (!viewport || node.getBoundingClientRect().top < viewport * 0.92) return;

    setHidden(true);
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          setHidden(false);
          observer.disconnect();
        }
      },
      { rootMargin: "0px 0px -8% 0px" },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={cn("reveal-item", hidden && "is-hidden", className)}
      style={delay ? { transitionDelay: `${delay}s` } : undefined}
    >
      {children}
    </div>
  );
}
