"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Field";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import { formatDate, formatPrice } from "@/lib/format";
import type { WalletTransaction } from "@/lib/types";

const PRESETS = [1_000_000, 5_000_000, 10_000_000];

export function WalletPanel({
  balance,
  transactions,
  locale,
  dict,
}: {
  balance: number;
  transactions: WalletTransaction[];
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();
  const [amount, setAmount] = useState(5_000_000);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [current, setCurrent] = useState(balance);
  const [rows, setRows] = useState(transactions);

  async function topup() {
    setBusy(true);
    setError("");
    try {
      const data = await callApi<{ balance: number; transaction: WalletTransaction }>(
        "auth/wallet/topup",
        { method: "POST", body: { amount }, locale },
      );
      setCurrent(data.balance);
      setRows([data.transaction, ...rows]);
      router.refresh();
    } catch (caught) {
      setError((caught as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-8">
      <div className="glass relative overflow-hidden rounded-3xl p-7">
        <div
          className="pointer-events-none absolute -top-20 end-0 size-64 rounded-full bg-mint-400/20 blur-3xl"
          aria-hidden
        />
        <p className="relative text-xs tracking-wider text-mist-600 uppercase">
          {dict.dashboard.wallet.balance}
        </p>
        <p className="tnum font-display relative mt-2 text-4xl font-semibold">
          {formatPrice(current, locale, dict.common.free)}
        </p>

        <div className="relative mt-7 flex flex-wrap items-end gap-3">
          <label className="min-w-40 flex-1">
            <span className="mb-2 block text-xs text-mist-500">{dict.dashboard.wallet.amount}</span>
            <Input
              type="number"
              value={amount}
              min={100000}
              step={100000}
              onChange={(event) => setAmount(Number(event.target.value))}
              dir="ltr"
              className="tnum"
            />
          </label>
          <Button onClick={topup} disabled={busy}>
            {busy ? dict.common.loading : dict.dashboard.wallet.topup}
          </Button>
        </div>

        <div className="relative mt-3 flex flex-wrap gap-2">
          {PRESETS.map((preset) => (
            <button
              key={preset}
              type="button"
              onClick={() => setAmount(preset)}
              className="glass tnum rounded-full px-3.5 py-1.5 text-xs transition hover:border-white/25"
            >
              + {formatPrice(preset, locale, dict.common.free)}
            </button>
          ))}
        </div>

        {error ? <p className="relative mt-3 text-xs text-rose-400">{error}</p> : null}
      </div>

      <section>
        <h2 className="font-display mb-4 text-lg font-semibold">
          {dict.dashboard.wallet.history}
        </h2>
        {rows.length ? (
          <ul className="space-y-2.5">
            {rows.map((tx) => (
              <li key={tx.id} className="glass flex items-center gap-4 rounded-2xl p-4">
                <span
                  className={`grid size-10 shrink-0 place-items-center rounded-xl text-sm ${
                    tx.amount >= 0
                      ? "bg-mint-400/12 text-mint-400"
                      : "bg-rose-400/12 text-rose-400"
                  }`}
                  aria-hidden
                >
                  {tx.amount >= 0 ? "↓" : "↑"}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm">{tx.title}</p>
                  <p className="text-xs text-mist-600">
                    {dict.dashboard.wallet.kinds[tx.kind]} · {formatDate(tx.created_at, locale)}
                  </p>
                </div>
                <span
                  className={`tnum text-sm font-semibold ${
                    tx.amount >= 0 ? "text-mint-400" : "text-rose-400"
                  }`}
                >
                  {tx.amount >= 0 ? "+" : "−"}{" "}
                  {formatPrice(Math.abs(tx.amount), locale, dict.common.free)}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-muted text-sm">{dict.dashboard.wallet.empty}</p>
        )}
      </section>
    </div>
  );
}
