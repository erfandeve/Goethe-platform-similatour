"use client";

import { useEffect } from "react";
import { useParams } from "next/navigation";

const COPY = {
  fa: {
    title: "این صفحه بارگذاری نشد",
    body: "محتوای این صفحه از سرور API خوانده می‌شود و آن آدرس الان جواب نمی‌دهد.",
    retry: "تلاش دوباره",
    home: "بازگشت به خانه",
  },
  en: {
    title: "This page could not load",
    body: "Its content comes from the API server, and that address is not responding right now.",
    retry: "Try again",
    home: "Back to home",
  },
  de: {
    title: "Diese Seite konnte nicht geladen werden",
    body: "Ihre Inhalte kommen vom API-Server, und diese Adresse antwortet gerade nicht.",
    retry: "Erneut versuchen",
    home: "Zur Startseite",
  },
} as const;

export default function LocaleError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const params = useParams<{ locale?: string }>();
  const locale = (params?.locale ?? "fa") as keyof typeof COPY;
  const copy = COPY[locale] ?? COPY.fa;

  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <main className="mx-auto flex min-h-[60vh] max-w-xl flex-col items-center justify-center gap-4 px-6 text-center">
      <h1 className="text-2xl font-bold">{copy.title}</h1>
      <p className="text-sm opacity-70">{copy.body}</p>
      {error.digest && <code className="text-xs opacity-40">digest: {error.digest}</code>}
      <div className="mt-2 flex gap-3">
        <button
          onClick={reset}
          className="rounded-full bg-white/10 px-5 py-2 text-sm font-medium hover:bg-white/20"
        >
          {copy.retry}
        </button>
        <a
          href={`/${locale}`}
          className="rounded-full border border-white/20 px-5 py-2 text-sm font-medium hover:bg-white/10"
        >
          {copy.home}
        </a>
      </div>
    </main>
  );
}
