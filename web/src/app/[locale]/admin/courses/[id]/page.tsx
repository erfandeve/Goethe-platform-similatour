import { notFound } from "next/navigation";

import { CourseBuilder } from "@/components/admin/CourseBuilder";
import { Empty } from "@/components/ui/Empty";
import { ButtonLink } from "@/components/ui/Button";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminCourse, AdminPart } from "@/lib/admin";

export default async function AdminCoursePage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { locale, id } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ course: AdminCourse; results: AdminPart[] }>(
    `/admin/courses/${id}/parts/`,
    { locale },
  ).catch(() => null);

  if (!data) {
    return (
      <Empty
        title="دوره پیدا نشد"
        body="ممکن است حذف شده باشد یا دسترسی مدیریت نداشته باشید."
        icon="🔒"
        action={<ButtonLink href={`/${locale}/admin/courses`}>بازگشت</ButtonLink>}
      />
    );
  }

  return <CourseBuilder course={data.course} initialParts={data.results} locale={locale} />;
}
