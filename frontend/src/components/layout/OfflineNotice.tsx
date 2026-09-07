import type { Locale } from "@/i18n/config";
import { API_BASE } from "@/lib/api";

const COPY: Record<Locale, { title: string; body: string; hint: string }> = {
  fa: {
    title: "سرور محتوا در دسترس نیست",
    body: "طراحی سایت را می‌بینید، ولی دوره‌ها، آزمون‌ها و پادکست‌ها از API خوانده می‌شوند و آن آدرس الان جواب نمی‌دهد.",
    hint: "بک‌اند جنگو را بالا بیاورید و NEXT_PUBLIC_API_URL را به آن وصل کنید.",
  },
  en: {
    title: "The content server is unreachable",
    body: "The site itself is fine, but courses, exams and podcasts come from the API and that address is not responding.",
    hint: "Deploy the Django backend and point NEXT_PUBLIC_API_URL at it.",
  },
  de: {
    title: "Der Inhaltsserver ist nicht erreichbar",
    body: "Die Seite selbst läuft, aber Kurse, Prüfungen und Podcasts kommen aus der API, und diese Adresse antwortet nicht.",
    hint: "Django-Backend bereitstellen und NEXT_PUBLIC_API_URL darauf zeigen lassen.",
  },
};

export function OfflineNotice({ locale }: { locale: Locale }) {
  const copy = COPY[locale];
  return (
    <div className="border-b border-amber-400/30 bg-amber-400/10">
      <div className="mx-auto max-w-6xl px-4 py-3 text-sm">
        <p className="font-semibold text-amber-200">{copy.title}</p>
        <p className="mt-1 text-amber-100/80">{copy.body}</p>
        <p className="mt-1 text-amber-100/60">
          {copy.hint} <code className="text-amber-100/90">{API_BASE}</code>
        </p>
      </div>
    </div>
  );
}
