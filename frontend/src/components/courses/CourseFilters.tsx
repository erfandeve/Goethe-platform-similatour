"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useState, useTransition } from "react";

import { Button } from "@/components/ui/Button";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { formatNumber } from "@/lib/format";
import type { Category } from "@/lib/types";
import { cn, levelColor } from "@/lib/utils";

interface Facets {
  levels: { value: string; count: number }[];
  languages: { value: string; count: number }[];
  formats: { value: string; count: number }[];
  categories: (Category & { count: number })[];
}

const LANGUAGE_NAMES: Record<string, Record<Locale, string>> = {
  de: { fa: "آلمانی", en: "German", de: "Deutsch" },
  en: { fa: "انگلیسی", en: "English", de: "Englisch" },
  fr: { fa: "فرانسوی", en: "French", de: "Französisch" },
  tr: { fa: "ترکی", en: "Turkish", de: "Türkisch" },
  es: { fa: "اسپانیایی", en: "Spanish", de: "Spanisch" },
};

export function CourseFilters({
  facets,
  locale,
  dict,
  total,
}: {
  facets: Facets;
  locale: Locale;
  dict: Dictionary;
  total: number;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const [pending, startTransition] = useTransition();
  const [openMobile, setOpenMobile] = useState(false);

  const push = useCallback(
    (next: URLSearchParams) => {
      next.delete("page");
      startTransition(() => {
        router.push(`${pathname}?${next.toString()}`, { scroll: false });
      });
    },
    [pathname, router],
  );

  const toggle = useCallback(
    (key: string, value: string) => {
      const next = new URLSearchParams(params.toString());
      const current = (next.get(key) ?? "").split(",").filter(Boolean);
      const updated = current.includes(value)
        ? current.filter((item) => item !== value)
        : [...current, value];
      if (updated.length) next.set(key, updated.join(","));
      else next.delete(key);
      push(next);
    },
    [params, push],
  );

  const isActive = (key: string, value: string) =>
    (params.get(key) ?? "").split(",").filter(Boolean).includes(value);

  const activeCount = ["level", "language", "format", "category", "free", "q"].filter((key) =>
    params.get(key),
  ).length;

  function clearAll() {
    const next = new URLSearchParams();
    const sort = params.get("sort");
    if (sort) next.set("sort", sort);
    push(next);
  }

  const groups = (
    <div className="space-y-8">
      <FilterGroup title={dict.courses.filters.level}>
        <div className="flex flex-wrap gap-2">
          {facets.levels.map((item) => (
            <button
              key={item.value}
              type="button"
              onClick={() => toggle("level", item.value)}
              className={cn(
                "tnum rounded-xl border px-3 py-2 text-xs font-semibold transition",
                isActive("level", item.value)
                  ? "border-transparent text-ink-950"
                  : "border-white/10 text-mist-300 hover:border-white/25",
              )}
              style={
                isActive("level", item.value)
                  ? { background: levelColor(item.value) }
                  : undefined
              }
            >
              {item.value}
              <span className="ms-1.5 opacity-60">({formatNumber(item.count, locale)})</span>
            </button>
          ))}
        </div>
      </FilterGroup>

      <FilterGroup title={dict.courses.filters.category}>
        <div className="space-y-1.5">
          {facets.categories.map((category) => (
            <CheckRow
              key={category.slug}
              label={category.title}
              count={formatNumber(category.count, locale)}
              checked={isActive("category", category.slug)}
              onClick={() => toggle("category", category.slug)}
              color={category.color}
            />
          ))}
        </div>
      </FilterGroup>

      <FilterGroup title={dict.courses.filters.format}>
        <div className="space-y-1.5">
          {facets.formats.map((item) => (
            <CheckRow
              key={item.value}
              label={
                dict.courses.formats[item.value as keyof typeof dict.courses.formats] ?? item.value
              }
              count={formatNumber(item.count, locale)}
              checked={isActive("format", item.value)}
              onClick={() => toggle("format", item.value)}
            />
          ))}
        </div>
      </FilterGroup>

      <FilterGroup title={dict.courses.filters.language}>
        <div className="space-y-1.5">
          {facets.languages.map((item) => (
            <CheckRow
              key={item.value}
              label={LANGUAGE_NAMES[item.value]?.[locale] ?? item.value}
              count={formatNumber(item.count, locale)}
              checked={isActive("language", item.value)}
              onClick={() => toggle("language", item.value)}
            />
          ))}
        </div>
      </FilterGroup>

      <FilterGroup title={dict.courses.filters.price}>
        <CheckRow
          label={dict.courses.filters.free}
          checked={params.get("free") === "true"}
          onClick={() => {
            const next = new URLSearchParams(params.toString());
            if (next.get("free") === "true") next.delete("free");
            else next.set("free", "true");
            push(next);
          }}
        />
      </FilterGroup>

      {activeCount > 0 ? (
        <Button variant="outline" size="sm" className="w-full" onClick={clearAll}>
          {dict.courses.filters.clear}
        </Button>
      ) : null}
    </div>
  );

  return (
    <>
      <div className="mb-6 flex items-center gap-3 lg:hidden">
        <Button variant="soft" size="sm" onClick={() => setOpenMobile((value) => !value)}>
          {dict.courses.filters.title}
          {activeCount ? (
            <span className="tnum grid size-5 place-items-center rounded-full bg-violet-500 text-[10px] text-ink-950">
              {activeCount}
            </span>
          ) : null}
        </Button>
        <span className="tnum text-xs text-mist-500">
          {formatNumber(total, locale)} {dict.courses.filters.results}
        </span>
      </div>

      <aside
        className={cn(
          "glass rounded-3xl p-6 transition-opacity lg:sticky lg:top-28 lg:block",
          pending && "opacity-60",
          openMobile ? "block" : "hidden",
        )}
      >
        <h2 className="font-display mb-6 hidden text-lg font-semibold lg:block">
          {dict.courses.filters.title}
        </h2>
        {groups}
      </aside>
    </>
  );
}

function FilterGroup({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="mb-3 text-xs font-semibold tracking-[0.2em] text-mist-500 uppercase">
        {title}
      </h3>
      {children}
    </div>
  );
}

function CheckRow({
  label,
  count,
  checked,
  onClick,
  color,
}: {
  label: string;
  count?: string;
  checked: boolean;
  onClick: () => void;
  color?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex w-full items-center gap-3 rounded-xl px-2 py-2 text-start text-sm transition hover:bg-white/5"
    >
      <span
        className={cn(
          "grid size-4.5 shrink-0 place-items-center rounded-md border transition",
          checked ? "border-transparent" : "border-white/20",
        )}
        style={checked ? { background: color ?? "#6d5efc" } : undefined}
      >
        {checked ? (
          <svg viewBox="0 0 12 12" className="size-3 text-ink-950" aria-hidden>
            <path d="m2.5 6 2.5 2.5 4.5-5" stroke="currentColor" strokeWidth="1.8" fill="none" strokeLinecap="round" />
          </svg>
        ) : null}
      </span>
      <span className={cn("flex-1 truncate", checked ? "text-mist-50" : "text-mist-300")}>
        {label}
      </span>
      {count ? <span className="tnum text-xs text-mist-600">{count}</span> : null}
    </button>
  );
}
