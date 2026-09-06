import { notFound } from "next/navigation";

import { WalletPanel } from "@/components/dashboard/WalletPanel";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { WalletTransaction } from "@/lib/types";

export default async function WalletPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const dict = await getDictionary(locale);
  const data = await apiFetchAuthed<{
    balance: number;
    transactions: WalletTransaction[];
  }>("/auth/wallet/", { locale });

  return (
    <div>
      <h1 className="font-display mb-8 text-2xl font-semibold">{dict.dashboard.wallet.title}</h1>
      <WalletPanel
        balance={data.balance}
        transactions={data.transactions}
        locale={locale}
        dict={dict}
      />
    </div>
  );
}
