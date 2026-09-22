"use client";

import { useState } from "react";

import { cn, mediaUrl } from "@/lib/utils";

/** A round photo that falls back to the name's first letter if the file is missing. */
export function Avatar({
  src,
  name,
  className,
  fallbackClassName,
}: {
  src?: string;
  name: string;
  className?: string;
  fallbackClassName?: string;
}) {
  const [broken, setBroken] = useState(false);

  if (src && !broken) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={mediaUrl(src)}
        alt=""
        loading="lazy"
        onError={() => setBroken(true)}
        className={cn("shrink-0 rounded-full object-cover", className)}
      />
    );
  }
  return (
    <span
      aria-hidden
      className={cn("grid shrink-0 place-items-center rounded-full font-bold", className, fallbackClassName)}
    >
      {name.trim().slice(0, 1)}
    </span>
  );
}
