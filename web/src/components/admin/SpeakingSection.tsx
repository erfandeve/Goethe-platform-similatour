"use client";

import { useState, type ReactNode } from "react";

import { Button } from "@/components/ui/Button";
import type { Locale } from "@/i18n/config";
import type { AdminCategory, AdminCourse, AdminInstructor } from "@/lib/admin";

import {
  CourseFields,
  courseToDraft,
  draftToBody,
  type CourseDraft,
} from "./CourseForm";
import { SpeakingPicker } from "./SpeakingPicker";
import { useAdmin } from "./useAdmin";
import { Modal, Toast } from "./ui";

/**
 * Wraps the speaking builder so the course's own details — cover included — can
 * be edited here, instead of sending people to the courses screen and back.
 */
export function SpeakingSection({
  courses,
  course,
  categories,
  instructors,
  locale,
  children,
}: {
  courses: AdminCourse[];
  course: AdminCourse | null;
  categories: AdminCategory[];
  instructors: AdminInstructor[];
  locale: Locale;
  children: ReactNode;
}) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [draft, setDraft] = useState<CourseDraft | null>(null);
  const [current, setCurrent] = useState(course);

  async function save() {
    if (!draft?.id) return;
    const saved = await run(
      () =>
        call<AdminCourse>(`admin/courses/${draft.id}`, {
          method: "PATCH",
          body: draftToBody(draft),
        }),
      { success: "مشخصات دوره ذخیره شد" },
    );
    if (!saved) return;
    setCurrent(saved);
    setDraft(null);
  }

  return (
    <div className="space-y-6">
      <SpeakingPicker
        courses={courses}
        activeId={current?.id ?? ""}
        locale={locale}
        onEditCourse={current ? () => setDraft(courseToDraft(current)) : undefined}
      />

      {current?.cover ? (
        <p className="tnum truncate text-xs text-mist-600" dir="ltr">
          cover: {current.cover}
        </p>
      ) : null}

      {children}

      <Modal open={!!draft} wide title="مشخصات و تصویر شاخص دوره" onClose={() => setDraft(null)}>
        {draft ? (
          <div className="space-y-5">
            <CourseFields
              draft={draft}
              onChange={setDraft}
              categories={categories}
              instructors={instructors}
              onError={(message) => notify(message, "error")}
            />
            <div className="flex gap-3 pt-2">
              <Button onClick={save} disabled={busy} className="flex-1">
                {busy ? "…" : "ذخیره"}
              </Button>
              <Button variant="outline" onClick={() => setDraft(null)}>
                انصراف
              </Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <Toast message={toast.message} tone={toast.tone} />
    </div>
  );
}
