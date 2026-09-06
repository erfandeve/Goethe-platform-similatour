import { notFound } from "next/navigation";

import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import { formatDate, formatPrice } from "@/lib/format";
import type { Order, Paginated } from "@/lib/types";

const STATUS_TONE: Record<string, string> = {
  paid: "text-mint-400 bg-mint-400/12",
  pending: "text-amber-400 bg-amber-400/12",
  failed: "text-rose-400 bg-rose-400/12",
  refunded: "text-mist-400 bg-white/8",
};

export default async function OrdersPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetchAuthed<Paginated<Order>>("/orders/", { locale });

  return (
    <div>
      <h1 className="font-display mb-8 text-2xl font-semibold">{dict.dashboard.nav.orders}</h1>

      {data.results.length ? (
        <div className="space-y-3">
          {data.results.map((order) => (
            <article key={order.id} className="glass rounded-2xl p-5">
              <header className="flex flex-wrap items-center gap-3">
                <span className="tnum font-display text-sm font-semibold" dir="ltr">
                  {order.code}
                </span>
                <span
                  className={`rounded-lg px-2.5 py-1 text-[11px] font-semibold uppercase ${STATUS_TONE[order.status]}`}
                >
                  {dict.dashboard.orders.statuses[order.status]}
                </span>
                <span className="text-xs text-mist-600">{formatDate(order.created_at, locale)}</span>
                <span className="tnum ms-auto font-semibold">
                  {formatPrice(order.total, locale, dict.common.free)}
                </span>
              </header>
              <ul className="mt-4 space-y-1.5 border-t border-white/8 pt-4">
                {order.items.map((item) => (
                  <li key={item.slug} className="flex items-center justify-between text-xs">
                    <span className="truncate text-mist-300">{item.title}</span>
                    <span className="tnum text-mist-500">
                      {formatPrice(item.price, locale, dict.common.free)}
                    </span>
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      ) : (
        <Empty
          title={dict.dashboard.orders.empty}
          action={<ButtonLink href={`/${locale}/courses`}>{dict.nav.courses}</ButtonLink>}
        />
      )}
    </div>
  );
}
