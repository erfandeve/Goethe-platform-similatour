"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useSession } from "@/components/layout/SessionProvider";
import { Button, ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Input } from "@/components/ui/Field";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatPrice } from "@/lib/format";
import type { CartState, Order, User } from "@/lib/types";

export function CartView({
  initialCart,
  user,
  locale,
  dict,
}: {
  initialCart: CartState;
  user: User | null;
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();
  const { refreshCart } = useSession();
  const [cart, setCart] = useState(initialCart);
  const [coupon, setCoupon] = useState(initialCart.coupon);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [order, setOrder] = useState<Order | null>(null);

  async function remove(itemId: string) {
    setBusy(true);
    try {
      const next = await callApi<CartState>("cart/remove", {
        method: "POST",
        body: { item_id: itemId },
        locale,
      });
      setCart(next);
      await refreshCart();
      router.refresh();
    } finally {
      setBusy(false);
    }
  }

  async function applyCoupon() {
    setBusy(true);
    setError("");
    try {
      const next = await callApi<CartState>("cart/coupon", {
        method: "POST",
        body: { coupon },
        locale,
      });
      setCart(next);
    } catch {
      setError(dict.cart.couponInvalid);
    } finally {
      setBusy(false);
    }
  }

  async function checkout() {
    setBusy(true);
    setError("");
    try {
      const created = await callApi<Order>("checkout", {
        method: "POST",
        body: { payment_method: "wallet" },
        locale,
      });
      setOrder(created);
      setCart({ ...cart, items: [], count: 0, subtotal: 0, discount: 0, total: 0 });
      await refreshCart();
      router.refresh();
    } catch (caught) {
      const failure = caught as { code?: string; message?: string };
      setError(
        failure.code === "insufficient_funds" ? dict.cart.insufficient : (failure.message ?? ""),
      );
    } finally {
      setBusy(false);
    }
  }

  if (order) {
    return (
      <div className="glass mx-auto max-w-lg rounded-3xl p-10 text-center">
        <span className="mx-auto grid size-14 place-items-center rounded-2xl bg-mint-400/15 text-2xl text-mint-400">
          ✓
        </span>
        <h2 className="font-display mt-5 text-2xl font-semibold">{dict.cart.success.title}</h2>
        <p className="text-muted mt-3 text-sm">{dict.cart.success.body}</p>
        <p className="tnum mt-4 text-xs text-mist-500">{order.code}</p>
        <ButtonLink href={`/${locale}/dashboard`} className="mt-7">
          {dict.cart.success.cta}
        </ButtonLink>
      </div>
    );
  }

  if (!user) {
    return (
      <Empty
        title={dict.exams.access.loginFirst}
        action={<ButtonLink href={`/${locale}/login?next=/${locale}/cart`}>{dict.nav.login}</ButtonLink>}
        icon="→"
      />
    );
  }

  if (!cart.items.length) {
    return (
      <Empty
        title={dict.cart.empty.title}
        body={dict.cart.empty.body}
        action={<ButtonLink href={`/${locale}/courses`}>{dict.cart.empty.cta}</ButtonLink>}
        icon="◇"
      />
    );
  }

  const enough = (user.wallet_balance ?? 0) >= cart.total;

  return (
    <div className="grid gap-8 lg:grid-cols-[1.6fr_1fr]">
      <ul className="space-y-3">
        {cart.items.map((item) => (
          <li key={item.item_id} className="glass flex items-center gap-4 rounded-2xl p-4">
            <span className="grid size-14 shrink-0 place-items-center rounded-xl bg-violet-500/15 text-xs font-semibold text-violet-400 uppercase">
              {item.item_type === "exam" ? "EXAM" : "KURS"}
            </span>
            <div className="min-w-0 flex-1">
              <Link
                href={`/${locale}/${item.item_type}s/${item.slug}`}
                className="block truncate text-sm font-semibold hover:text-violet-400"
              >
                {item.title}
              </Link>
              <span className="tnum mt-1 block text-xs text-mist-500">
                {formatPrice(item.price, locale, dict.common.free)}
              </span>
            </div>
            <button
              type="button"
              onClick={() => remove(item.item_id)}
              disabled={busy}
              className="rounded-lg px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
            >
              {dict.cart.remove}
            </button>
          </li>
        ))}
      </ul>

      <aside className="glass h-fit rounded-3xl p-6 lg:sticky lg:top-28">
        <div className="flex gap-2">
          <Input
            value={coupon}
            onChange={(event) => setCoupon(event.target.value.toUpperCase())}
            placeholder={dict.cart.coupon}
            aria-label={dict.cart.coupon}
          />
          <Button variant="soft" onClick={applyCoupon} disabled={busy}>
            {dict.cart.applyCoupon}
          </Button>
        </div>

        <dl className="mt-6 space-y-3 border-t border-white/8 pt-5 text-sm">
          <div className="flex justify-between">
            <dt className="text-mist-500">{dict.cart.subtotal}</dt>
            <dd className="tnum">{formatPrice(cart.subtotal, locale, dict.common.free)}</dd>
          </div>
          {cart.discount ? (
            <div className="flex justify-between text-mint-400">
              <dt>{dict.cart.discount}</dt>
              <dd className="tnum">− {formatPrice(cart.discount, locale, dict.common.free)}</dd>
            </div>
          ) : null}
          <div className="flex justify-between border-t border-white/8 pt-3">
            <dt className="font-semibold">{dict.cart.total}</dt>
            <dd className="tnum font-display text-lg font-semibold">
              {formatPrice(cart.total, locale, dict.common.free)}
            </dd>
          </div>
        </dl>

        <div className="mt-5 flex items-center justify-between rounded-2xl bg-white/4 px-4 py-3 text-xs">
          <span className="text-mist-500">{dict.cart.walletBalance}</span>
          <span className="tnum font-semibold">
            {formatPrice(user.wallet_balance, locale, dict.common.free)}
          </span>
        </div>

        <Button className="mt-5 w-full" size="lg" onClick={checkout} disabled={busy || !enough}>
          {dict.cart.checkout}
        </Button>

        {!enough ? (
          <Link
            href={`/${locale}/dashboard/wallet`}
            className="mt-3 block text-center text-xs text-amber-400 underline-offset-4 hover:underline"
          >
            {dict.cart.topup}
          </Link>
        ) : null}
        {error ? <p className="mt-3 text-center text-xs text-rose-400">{error}</p> : null}
      </aside>
    </div>
  );
}
