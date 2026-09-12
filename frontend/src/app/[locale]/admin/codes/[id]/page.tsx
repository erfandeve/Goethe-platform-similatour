import { notFound } from "next/navigation";

import { ExamBuilder } from "@/components/admin/ExamBuilder";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminExam, AdminExamCode } from "@/lib/admin";

/** The paper behind one exam code: its own modules, parts and answer keys. */
export default async function AdminExamCodePage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { locale, id } = await params;
  if (!isLocale(locale)) notFound();

  const code = await apiFetchAuthed<AdminExamCode>(`/admin/codes/${id}/`, { locale }).catch(
    () => null,
  );

  if (!code) {
    return (
      <Empty
        title="کد پیدا نشد"
        icon="🔒"
        action={<ButtonLink href={`/${locale}/admin/exams`}>بازگشت</ButtonLink>}
      />
    );
  }

  // The builder speaks the exam shape; a code carries the same modules.
  const asExam = {
    id: code.exam ?? "",
    slug: code.code,
    level: code.exam_level ?? "",
    title: code.label,
    questions_count: code.items_count,
    modules: code.modules,
  } as unknown as AdminExam;

  return (
    <ExamBuilder
      initial={asExam}
      locale={locale}
      codeId={code.id}
      title={`کد ${code.code}`}
      backHref={`/${locale}/admin/exams/${code.exam}`}
    />
  );
}
