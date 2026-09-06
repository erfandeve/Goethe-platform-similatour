"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Input, Select } from "@/components/ui/Field";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";

export function CourseToolbar({
  dict,
  locale,
  total,
}: {
  dict: Dictionary;
  locale: Locale;
  total: number;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const [query, setQuery] = useState(params.get("q") ?? "");

  // Debounced search so every keystroke does not hit the API.
  useEffect(() => {
    const timer = setTimeout(() => {
      const next = new URLSearchParams(params.toString());
      if (query) next.set("q", query);
      else next.delete("q");
      next.delete("page");
      if ((params.get("q") ?? "") !== query) {
        router.push(`${pathname}?${next.toString()}`, { scroll: false });
      }
    }, 350);
    return () => clearTimeout(timer);
  }, [query, params, pathname, router]);

  function setSort(value: string) {
    const next = new URLSearchParams(params.toString());
    if (value) next.set("sort", value);
    else next.delete("sort");
    router.push(`${pathname}?${next.toString()}`, { scroll: false });
  }

  return (
    <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center">
      <div className="relative flex-1">
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={dict.courses.filters.search}
          aria-label={dict.courses.filters.search}
          className="ps-11"
        />
        <svg
          viewBox="0 0 24 24"
          className="pointer-events-none absolute start-4 top-1/2 size-4.5 -translate-y-1/2 text-mist-500"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          aria-hidden
        >
          <circle cx="11" cy="11" r="6.5" />
          <path d="m16 16 4 4" strokeLinecap="round" />
        </svg>
      </div>

      <div className="flex items-center gap-3">
        <span className="tnum hidden text-xs whitespace-nowrap text-mist-500 md:block">
          {formatNumber(total, locale)} {dict.courses.filters.results}
        </span>
        <Select
          value={params.get("sort") ?? "newest"}
          onChange={(event) => setSort(event.target.value)}
          aria-label={dict.courses.filters.sort}
          className="w-44"
        >
          {Object.entries(dict.courses.sort).map(([value, label]) => (
            <option key={value} value={value} className="bg-ink-900">
              {label}
            </option>
          ))}
        </Select>
      </div>
    </div>
  );
}
