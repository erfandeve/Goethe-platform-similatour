import Link from "next/link";
import { notFound } from "next/navigation";

import { StatCard } from "@/components/dashboard/StatCard";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import { formatNumber } from "@/lib/format";

interface Overview {
  courses: { total: number; published: number };
  categories: number;
  instructors: number;
  parts: number;
  videos: number;
  speaking_videos: number;
  students: number;
  enrollments: number;
  speaking_attempts: number;
}

export default async function AdminHome({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<Overview>("/admin/overview/", { locale }).catch(
    () => null,
  );

  if (!data) {
    return (
      <Empty
        title="دسترسی مدیریت ندارید"
        body="این حساب هنوز staff نیست. با دستور make_staff دسترسی بدهید."
        icon="🔒"
        action={<ButtonLink href={`/${locale}/dashboard`}>بازگشت به پنل</ButtonLink>}
      />
    );
  }

  const cards = [
    { label: "دوره‌ها", value: data.courses.total, hint: `${data.courses.published} منتشرشده` },
    { label: "دسته‌بندی‌ها", value: data.categories, accent: "#22d3ee" },
    { label: "فصل‌ها", value: data.parts, accent: "#f59e0b" },
    { label: "ویدیوها", value: data.videos, hint: `${data.speaking_videos} با تمرین گفتاری`, accent: "#34d399" },
    { label: "زبان‌آموزان", value: data.students, accent: "#e879f9" },
    { label: "ثبت‌نام‌ها", value: data.enrollments },
    { label: "تلاش‌های گفتاری", value: data.speaking_attempts, accent: "#ff6b6b" },
    { label: "مدرسان", value: data.instructors, accent: "#22d3ee" },
  ];

  return (
    <div className="space-y-8">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="font-display text-2xl font-semibold">پنل مدیریت</h1>
          <p className="text-muted mt-1 text-sm">
            دوره‌ها، دسته‌بندی‌ها، فصل‌ها و ویدیوهای تمرین گفتاری
          </p>
        </div>
        <ButtonLink href={`/${locale}/admin/courses`}>مدیریت دوره‌ها</ButtonLink>
      </header>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map((card) => (
          <StatCard
            key={card.label}
            label={card.label}
            value={formatNumber(card.value, locale)}
            hint={card.hint}
            accent={card.accent}
          />
        ))}
      </div>

      <div className="glass rounded-3xl p-6">
        <h2 className="font-display mb-3 text-lg font-semibold">شروع سریع</h2>
        <ul className="space-y-2 text-sm text-mist-300">
          <li>
            ۱.{" "}
            <Link href={`/${locale}/admin/categories`} className="text-violet-400 hover:underline">
              دسته‌بندی
            </Link>{" "}
            بساز تا دوره‌ها را زیرش بچینی.
          </li>
          <li>
            ۲.{" "}
            <Link href={`/${locale}/admin/courses`} className="text-violet-400 hover:underline">
              دوره
            </Link>{" "}
            بساز و قیمت و سطحش را مشخص کن.
          </li>
          <li>۳. داخل دوره فصل اضافه کن، ویدیو آپلود کن و متن سؤال هر ویدیو را بنویس.</li>
          <li>۴. متن سؤال همان چیزی است که برای هوش مصنوعی فرستاده می‌شود.</li>
        </ul>
      </div>
    </div>
  );
}
