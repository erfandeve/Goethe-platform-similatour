"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";

import { cn } from "@/lib/utils";

export function Pagination({ page, pages }: { page: number; pages: number }) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();

  if (pages <= 1) return null;

  function go(target: number) {
    const next = new URLSearchParams(params.toString());
    next.set("page", String(target));
    router.push(`${pathname}?${next.toString()}`);
  }

  const numbers = Array.from({ length: pages }, (_, index) => index + 1).filter(
    (value) => value === 1 || value === pages || Math.abs(value - page) <= 1,
  );

  return (
    <nav className="mt-12 flex items-center justify-center gap-2">
      <button
        type="button"
        onClick={() => go(page - 1)}
        disabled={page <= 1}
        className="glass flip-x grid size-10 place-items-center rounded-full disabled:opacity-40"
        aria-label="Previous"
      >
        ←
      </button>
      {numbers.map((value, index) => (
        <span key={value} className="flex items-center gap-2">
          {index > 0 && value - numbers[index - 1] > 1 ? (
            <span className="text-mist-600">…</span>
          ) : null}
          <button
            type="button"
            onClick={() => go(value)}
            className={cn(
              "tnum grid size-10 place-items-center rounded-full text-sm transition",
              value === page
                ? "bg-linear-to-r from-violet-500 to-cyan-400 font-semibold text-ink-950"
                : "glass hover:border-white/25",
            )}
          >
            {value}
          </button>
        </span>
      ))}
      <button
        type="button"
        onClick={() => go(page + 1)}
        disabled={page >= pages}
        className="glass flip-x grid size-10 place-items-center rounded-full disabled:opacity-40"
        aria-label="Next"
      >
        →
      </button>
    </nav>
  );
}
