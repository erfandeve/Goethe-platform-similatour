import { notFound } from "next/navigation";

import { CourseBuilder } from "@/components/admin/CourseBuilder";
import { SpeakingSection } from "@/components/admin/SpeakingSection";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminCategory, AdminCourse, AdminInstructor, AdminPart } from "@/lib/admin";

/**
 * The speaking section opens the builder for the AI course directly, because
 * that is the one people come here to edit. Any other course is one pick away,
 * and the course's own details are editable without leaving.
 */
export default async function AdminSpeakingPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: string }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const query = await searchParams;

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

  const requested = typeof query.course === "string" ? query.course : "";
  const selected =
    courses.results.find((course) => course.id === requested) ??
    courses.results.find((course) => course.slug === "einreise-nach-deutschland") ??
    courses.results.find((course) => course.parts_count > 0) ??
    courses.results[0] ??
    null;

  const data = selected
    ? await apiFetchAuthed<{ course: AdminCourse; results: AdminPart[] }>(
        `/admin/courses/${selected.id}/parts/`,
        { locale },
      ).catch(() => null)
    : null;

  return (
    <SpeakingSection
      courses={courses.results}
      course={data?.course ?? selected}
      categories={categories.results}
      instructors={instructors.results}
      locale={locale}
    >
      {data ? (
        <CourseBuilder course={data.course} initialParts={data.results} locale={locale} />
      ) : null}
    </SpeakingSection>
  );
}
