import { notFound } from "next/navigation";

import { CoursesManager } from "@/components/admin/CoursesManager";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminCategory, AdminCourse, AdminInstructor } from "@/lib/admin";

export default async function AdminCoursesPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const [courses, categories, instructors] = await Promise.all([
    apiFetchAuthed<{ results: AdminCourse[] }>("/admin/courses/", { locale }).catch(() => ({
      results: [] as AdminCourse[],
    })),
    apiFetchAuthed<{ results: AdminCategory[] }>("/admin/categories/", { locale }).catch(() => ({
      results: [] as AdminCategory[],
    })),
    apiFetchAuthed<{ results: AdminInstructor[] }>("/admin/instructors/", { locale }).catch(
      () => ({ results: [] as AdminInstructor[] }),
    ),
  ]);

  return (
    <CoursesManager
      initial={courses.results}
      categories={categories.results}
      instructors={instructors.results}
      locale={locale}
    />
  );
}
