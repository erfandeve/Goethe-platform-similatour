"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useSession } from "@/components/layout/SessionProvider";
import { Button } from "@/components/ui/Button";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatNumber, formatPrice } from "@/lib/format";
import type { ExamSitting } from "@/lib/types";
import { alpha, cn } from "@/lib/utils";

/**
 * Pick which sittings to buy. Each code is priced on its own, so the running
 * total is simply the sum of what is ticked — visible while choosing rather
 * than at checkout.
 */
export function SittingPicker({
  slug,
  codes,
  accent,
  locale,
  dict,
}: {
  slug: string;
  codes: ExamSitting[];
  accent: string;
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();
  const { user, refreshCart } = useSession();
  const [picked, setPicked] = useState<string[]>(() => {
    const first = codes.find((code) => !code.owned);
    return first ? [first.id] : [];
  });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  const selectable = codes.filter((code) => !code.owned);
  const chosen = codes.filter((code) => picked.includes(code.id));
  const total = chosen.reduce((sum, code) => sum + code.price, 0);
  const allPicked = selectable.length > 0 && picked.length === selectable.length;

  function toggle(id: string) {
    setPicked((current) =>
      current.includes(id) ? current.filter((item) => item !== id) : [...current, id],
    );
  }

  async function addToCart() {
    if (!user) {
      router.push(`/${locale}/login?next=/${locale}/exams/${slug}`);
      return;
    }
    if (!picked.length) {
      setError(dict.exams.sittings.pickOne);
      return;
    }

    setBusy(true);
    setError("");
    try {
      // Sequential rather than parallel: the cart is one document, so
      // concurrent adds would race each other's writes.
      for (const id of picked) {
        await callApi("cart/add", {
          method: "POST",
          body: { item_type: "exam_code", id },
          locale,
        });
      }
      await refreshCart();
      setDone(true);
      router.refresh();
    } catch (caught) {
      const failure = caught as { message?: string; code?: string };
      if (failure.code === "duplicate_item") setDone(true);
      else setError(failure.message ?? dict.common.error);
    } finally {
      setBusy(false);
    }
  }

  if (!codes.length) return null;

  return (
    <div className="mt-6 border-t border-white/8 pt-5">
      <p className="mb-1 text-[11px] tracking-wider text-mist-500 uppercase">
        {dict.exams.sittings.title}
      </p>
      <p className="text-muted mb-3 text-xs">{dict.exams.sittings.hint}</p>

      {selectable.length > 1 ? (
        <button
          type="button"
          onClick={() => setPicked(allPicked ? [] : selectable.map((code) => code.id))}
          className="mb-3 rounded-full border border-white/15 px-3 py-1.5 text-[11px] text-mist-300 transition hover:border-white/30 hover:text-white"
        >
          {allPicked ? dict.exams.sittings.clearAll : dict.exams.sittings.selectAll}
        </button>
      ) : null}

      <ul className="space-y-2">
        {codes.map((code) => {
          const isPicked = picked.includes(code.id);
          const className = cn(
            "flex w-full items-center gap-3 rounded-2xl border px-4 py-3 text-start transition",
            code.owned
              ? "border-mint-400/30 bg-mint-400/8 hover:border-mint-400/60"
              : isPicked
                ? "border-transparent"
                : "border-white/10 hover:border-white/25",
          );
          const style = isPicked && !code.owned ? { background: alpha(accent, 0.14) } : undefined;

          const inner = (
            <>
              <span
                className={cn(
                  "grid size-5 shrink-0 place-items-center rounded-md border text-[10px]",
                  code.owned || isPicked ? "border-transparent text-ink-950" : "border-white/25",
                )}
                style={
                  code.owned
                    ? { background: "#34d399" }
                    : isPicked
                      ? { background: accent }
                      : undefined
                }
              >
                {code.owned || isPicked ? "✓" : ""}
              </span>

              <span className="min-w-0 flex-1">
                <span className="block text-sm font-medium" dir="ltr">
                  {code.code}
                </span>
                <span className="block truncate text-xs text-mist-500">
                  {code.label !== code.code ? code.label : ""}
                  {code.items_count
                    ? ` · ${formatNumber(code.items_count, locale)} ${dict.exams.card.questions}`
                    : ""}
                </span>
              </span>

              <span className="tnum shrink-0 text-xs">
                {code.owned ? (
                  <span className="text-mint-400">{dict.exams.card.start}</span>
                ) : (
                  <span className={isPicked ? "text-mist-300" : "text-mist-600"}>
                    {formatPrice(code.price, locale, dict.exams.card.free)}
                  </span>
                )}
              </span>
            </>
          );

          return (
            <li key={code.id}>
              {/* An owned sitting is no longer something to buy — it is
                  something to sit, and it carries its own code into the player. */}
              {code.owned ? (
                <Link
                  href={`/${locale}/exams/${slug}/attempt?code=${code.id}`}
                  className={className}
                >
                  {inner}
                </Link>
              ) : (
                <button
                  type="button"
                  onClick={() => toggle(code.id)}
                  className={className}
                  style={style}
                >
                  {inner}
                </button>
              )}
            </li>
          );
        })}
      </ul>

      {selectable.length ? (
        <>
          <div className="mt-4 flex items-center justify-between text-sm">
            <span className="text-mist-500">{dict.cart.total}</span>
            <span className="tnum font-display text-lg font-semibold">
              {formatPrice(total, locale, dict.exams.card.free)}
            </span>
          </div>

          <Button onClick={addToCart} disabled={busy} className="mt-4 w-full" size="lg">
            {busy
              ? dict.common.loading
              : done
                ? dict.courses.detail.inCart
                : dict.courses.detail.addToCart}
          </Button>

          {done ? (
            <a
              href={`/${locale}/cart`}
              className="mt-2 block text-center text-xs text-violet-400 underline-offset-4 hover:underline"
            >
              {dict.cart.title} →
            </a>
          ) : null}
          {error ? <p className="mt-2 text-center text-xs text-rose-400">{error}</p> : null}
        </>
      ) : null}
    </div>
  );
}
