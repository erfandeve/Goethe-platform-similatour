import { notFound } from "next/navigation";

import { CartView } from "@/components/courses/CartView";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed, getAccessToken } from "@/lib/api";
import type { CartState, User } from "@/lib/types";

export const metadata = { robots: { index: false, follow: false } };

const EMPTY: CartState = {
  items: [],
  count: 0,
  subtotal: 0,
  discount: 0,
  total: 0,
  coupon: "",
};

export default async function CartPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const token = await getAccessToken();

  const [cart, user] = token
    ? await Promise.all([
        apiFetchAuthed<CartState>("/cart/", { locale }).catch(() => EMPTY),
        apiFetchAuthed<User>("/auth/me/", { locale }).catch(() => null),
      ])
    : [EMPTY, null];

  return (
    <div className="container-page py-12">
      <h1 className="font-display mb-10 text-4xl font-semibold md:text-5xl">{dict.cart.title}</h1>
      <CartView initialCart={cart} user={user} locale={locale} dict={dict} />
    </div>
  );
}
