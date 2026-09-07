"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useSession } from "@/components/layout/SessionProvider";
import { Button } from "@/components/ui/Button";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatPrice } from "@/lib/format";
import { alpha } from "@/lib/utils";

export interface Plan {
  id: string;
  slug: string;
  title: string;
  description: string;
  highlights: string[];
  perks: string[];
  price: number;
  duration_days: number;
  accent: string;
  badge: string;
  is_featured: boolean;
  owned: boolean;
}

/** The tiers, with the running "what this opens" list a buyer compares on. */
export function PlanCards({
  plans,
  locale,
  dict,
}: {
  plans: Plan[];
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();
  const { user, refreshCart } = useSession();
  const [pending, setPending] = useState("");
  const [added, setAdded] = useState<string[]>([]);
  const [error, setError] = useState("");

  async function subscribe(plan: Plan) {
    if (!user) {
      router.push(`/${locale}/login?next=/${locale}/plans`);
      return;
    }
    setPending(plan.id);
    setError("");
    try {
      await callApi("cart/add", {
        method: "POST",
        body: { item_type: "plan", slug: plan.slug },
        locale,
      });
      await refreshCart();
      setAdded((current) => [...current, plan.id]);
      router.refresh();
    } catch (caught) {
      const failure = caught as { message?: string; code?: string };
      if (failure.code === "duplicate_item") setAdded((current) => [...current, plan.id]);
      else setError(failure.message ?? dict.common.error);
    } finally {
      setPending("");
    }
  }

  return (
    <>
      <div className="grid gap-5 lg:grid-cols-3">
        {plans.map((plan) => (
          <article
            key={plan.id}
            className="glass relative flex flex-col overflow-hidden rounded-3xl p-7"
            style={
              plan.is_featured
                ? {
                    borderColor: alpha(plan.accent, 0.45),
                    boxShadow: `0 0 60px -30px ${plan.accent}`,
                  }
                : undefined
            }
          >
            <div
              className="pointer-events-none absolute -top-24 end-0 size-56 rounded-full opacity-30 blur-3xl"
              style={{ background: plan.accent }}
              aria-hidden
            />

            <div className="relative">
              {plan.badge ? (
                <span
                  className="mb-3 inline-block rounded-full px-3 py-1 text-[11px] font-semibold"
                  style={{ background: alpha(plan.accent, 0.16), color: plan.accent }}
                >
                  {plan.badge}
                </span>
              ) : null}

              <h2 className="font-display text-xl font-semibold">{plan.title}</h2>
              <p className="text-muted mt-2 min-h-10 text-sm">{plan.description}</p>

              <p className="mt-5 flex items-end gap-2">
                <span className="tnum font-display text-3xl font-semibold">
                  {formatPrice(plan.price, locale, "—")}
                </span>
                <span className="pb-1 text-xs text-mist-500">{dict.plans.perYear}</span>
              </p>

              <p className="mt-6 mb-3 text-[11px] tracking-wider text-mist-500 uppercase">
                {dict.plans.includes}
              </p>
              <ul className="space-y-2">
                {plan.perks.map((perk) => (
                  <li key={perk} className="flex items-start gap-2.5 text-sm text-mist-200">
                    <span style={{ color: plan.accent }} aria-hidden>
                      ✓
                    </span>
                    {dict.plans.perks[perk as keyof typeof dict.plans.perks] ?? perk}
                  </li>
                ))}
              </ul>

              {plan.highlights.length ? (
                <ul className="mt-4 space-y-1.5 border-t border-white/8 pt-4">
                  {plan.highlights.map((item) => (
                    <li key={item} className="text-xs text-mist-500">
                      · {item}
                    </li>
                  ))}
                </ul>
              ) : null}
            </div>

            <div className="relative mt-auto pt-6">
              {plan.owned ? (
                <p
                  className="rounded-full py-3 text-center text-sm font-semibold"
                  style={{ background: alpha("#34d399", 0.14), color: "#34d399" }}
                >
                  {dict.plans.owned}
                </p>
              ) : (
                <Button
                  onClick={() => subscribe(plan)}
                  disabled={pending === plan.id}
                  className="w-full"
                  size="lg"
                  variant={plan.is_featured ? "primary" : "soft"}
                >
                  {pending === plan.id
                    ? dict.common.loading
                    : added.includes(plan.id)
                      ? dict.plans.inCart
                      : dict.plans.choose}
                </Button>
              )}
            </div>
          </article>
        ))}
      </div>

      {error ? <p className="mt-4 text-center text-sm text-rose-400">{error}</p> : null}
    </>
  );
}
