"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useSession } from "@/components/layout/SessionProvider";
import { Button } from "@/components/ui/Button";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";

export function AddToCartButton({
  slug,
  itemType,
  locale,
  dict,
  isFree = false,
  isOwned = false,
  size = "lg",
}: {
  slug: string;
  itemType: "course" | "exam";
  locale: Locale;
  dict: Dictionary;
  isFree?: boolean;
  isOwned?: boolean;
  size?: "sm" | "md" | "lg";
}) {
  const router = useRouter();
  const { user, refreshCart } = useSession();
  const [state, setState] = useState<"idle" | "loading" | "added">("idle");
  const [error, setError] = useState("");

  async function handleClick() {
    if (!user) {
      router.push(`/${locale}/login?next=/${locale}/${itemType}s/${slug}`);
      return;
    }
    if (isOwned) {
      router.push(
        itemType === "course" ? `/${locale}/learn/${slug}` : `/${locale}/dashboard/exams`,
      );
      return;
    }

    setState("loading");
    setError("");
    try {
      if (isFree && itemType === "course") {
        await callApi(`courses/${slug}/enroll`, { method: "POST", locale });
        router.push(`/${locale}/dashboard/courses`);
        router.refresh();
        return;
      }
      await callApi("cart/add", { method: "POST", body: { item_type: itemType, slug }, locale });
      await refreshCart();
      setState("added");
      router.refresh();
    } catch (caught) {
      const failure = caught as { code?: string; message?: string };
      if (failure.code === "duplicate_item") setState("added");
      else if (failure.code === "already_enrolled") router.push(`/${locale}/learn/${slug}`);
      else setError(failure.message ?? dict.common.error);
      if (failure.code !== "duplicate_item") setState("idle");
    }
  }

  const label = isOwned
    ? dict.courses.detail.enrolled
    : state === "added"
      ? dict.courses.detail.inCart
      : isFree
        ? dict.courses.detail.startFree
        : itemType === "exam"
          ? dict.exams.card.buy
          : dict.courses.detail.addToCart;

  return (
    <div className="w-full">
      <Button
        onClick={handleClick}
        size={size}
        disabled={state === "loading"}
        variant={state === "added" ? "soft" : "primary"}
        className="w-full"
      >
        {state === "loading" ? dict.common.loading : label}
      </Button>
      {state === "added" ? (
        <a
          href={`/${locale}/cart`}
          className="mt-2 block text-center text-xs text-violet-400 underline-offset-4 hover:underline"
        >
          {dict.cart.title} →
        </a>
      ) : null}
      {error ? <p className="mt-2 text-center text-xs text-rose-400">{error}</p> : null}
    </div>
  );
}
