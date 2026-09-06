"use client";

import dynamic from "next/dynamic";

/** Keeps three.js out of the initial bundle so the hero text paints first. */
const HeroScene = dynamic(() => import("./HeroScene"), {
  ssr: false,
  loading: () => (
    <div aria-hidden className="absolute inset-[20%] rounded-full bg-violet-500/25 blur-3xl" />
  ),
});

export function SceneMount({ className }: { className?: string }) {
  return (
    <div className={className}>
      <HeroScene />
    </div>
  );
}
