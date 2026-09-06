import { notFound } from "next/navigation";

import { ExamBuilder } from "@/components/admin/ExamBuilder";
import { ExamCodesManager } from "@/components/admin/ExamCodesManager";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminExam, AdminExamCode } from "@/lib/admin";

export default async function AdminExamPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { locale, id } = await params;
  if (!isLocale(locale)) notFound();

  const exam = await apiFetchAuthed<AdminExam>(`/admin/exams/${id}/`, { locale }).catch(
    () => null,
  );

  if (!exam) {
    return (
      <Empty
        title="آزمون پیدا نشد"
        icon="🔒"
        action={<ButtonLink href={`/${locale}/admin/exams`}>بازگشت</ButtonLink>}
      />
    );
  }

  const codes = await apiFetchAuthed<{ results: AdminExamCode[] }>(
    `/admin/exams/${id}/codes/`,
    { locale },
  ).catch(() => ({ results: [] as AdminExamCode[] }));

  return (
    <div className="space-y-6">
      <ExamCodesManager exam={exam} initial={codes.results} locale={locale} />
      <ExamBuilder initial={exam} locale={locale} />
    </div>
  );
}
