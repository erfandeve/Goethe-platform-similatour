"use client";

import { useState } from "react";

import { cn, mediaUrl } from "@/lib/utils";

/**
 * A cover that removes itself when the file is missing, so a stale path in the
 * database degrades to the card's own artwork instead of a broken-image icon.
 */
export function CoverImage({
  src,
  alt = "",
  className,
}: {
  src?: string;
  alt?: string;
  className?: string;
}) {
  const [failed, setFailed] = useState(false);
  if (!src || failed) return null;

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={mediaUrl(src)}
      alt={alt}
      loading="lazy"
      className={cn("pointer-events-none absolute inset-0 size-full object-cover", className)}
      onError={() => setFailed(true)}
    />
  );
}
