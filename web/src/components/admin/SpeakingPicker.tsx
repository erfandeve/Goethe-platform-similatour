"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/Button";
import { Select } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminCourse } from "@/lib/admin";

export function SpeakingPicker({
  courses,
  activeId,
  locale,
  onEditCourse,
}: {
  courses: AdminCourse[];
  activeId: string;
  locale: Locale;
  /** Opens the course details form without leaving this section. */
  onEditCourse?: () => void;
}) {
  const router = useRouter();

  return (
    <div className="glass flex flex-wrap items-center gap-4 rounded-3xl p-5">
      <div className="min-w-0 flex-1">
        <h1 className="font-display text-lg font-semibold">مکالمه با هوش مصنوعی</h1>
        <p className="text-muted mt-1 text-xs">
          فصل‌بندی کن، ویدیو آپلود کن و متن سؤالی که برای هوش مصنوعی می‌رود را بنویس.
        </p>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <Select
          value={activeId}
          onChange={(event) =>
            router.push(`/${locale}/admin/speaking?course=${event.target.value}`)
          }
          className="w-64"
          aria-label="انتخاب دوره"
        >
          {courses.map((course) => (
            <option key={course.id} value={course.id} className="bg-ink-900">
              {course.title.fa || course.title.en || course.slug}
              {course.videos_count ? ` (${course.videos_count})` : ""}
            </option>
          ))}
        </Select>
        {onEditCourse ? (
          <Button variant="soft" size="sm" onClick={onEditCourse}>
            مشخصات و تصویر شاخص
          </Button>
        ) : null}
      </div>
    </div>
  );
}
