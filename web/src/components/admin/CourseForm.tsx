"use client";

import { Field, Input, Select } from "@/components/ui/Field";
import type { AdminCategory, AdminCourse, AdminInstructor, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED, LEVELS } from "@/lib/admin";

import { ImageUpload } from "./ImageUpload";
import { TranslatedField } from "./ui";

/** One definition of "a course's details", shared by every screen that edits them. */
export interface CourseDraft {
  id?: string;
  title: Translated;
  subtitle: Translated;
  description: Translated;
  level: string;
  category: string;
  instructor: string;
  price: string;
  discount_price: string;
  accent: string;
  format: string;
  cover: string;
  is_published: boolean;
  slug: string;
}

export const blankCourse = (): CourseDraft => ({
  title: { ...EMPTY_TRANSLATED },
  subtitle: { ...EMPTY_TRANSLATED },
  description: { ...EMPTY_TRANSLATED },
  level: "A1",
  category: "",
  instructor: "",
  price: "0",
  discount_price: "0",
  accent: "#6d5efc",
  format: "self_paced",
  cover: "",
  is_published: true,
  slug: "",
});

export const courseToDraft = (course: AdminCourse): CourseDraft => ({
  id: course.id,
  title: course.title,
  subtitle: course.subtitle,
  description: course.description ?? { ...EMPTY_TRANSLATED },
  level: course.level,
  category: course.category ?? "",
  instructor: course.instructor ?? "",
  price: String(course.price),
  discount_price: String(course.discount_price),
  accent: course.accent,
  format: course.format,
  cover: course.cover ?? "",
  is_published: course.is_published,
  slug: course.slug,
});

export const draftToBody = (draft: CourseDraft) => ({
  title: draft.title,
  subtitle: draft.subtitle,
  description: draft.description,
  level: draft.level,
  category: draft.category || null,
  instructor: draft.instructor || null,
  price: Number(draft.price) || 0,
  discount_price: Number(draft.discount_price) || 0,
  accent: draft.accent,
  format: draft.format,
  cover: draft.cover,
  is_published: draft.is_published,
  ...(draft.slug ? { slug: draft.slug } : {}),
});

export function CourseFields({
  draft,
  onChange,
  categories,
  instructors,
  onError,
}: {
  draft: CourseDraft;
  onChange: (next: CourseDraft) => void;
  categories: AdminCategory[];
  instructors: AdminInstructor[];
  onError: (message: string) => void;
}) {
  return (
    <div className="space-y-5">
      <TranslatedField
        label="عنوان دوره"
        required
        value={draft.title}
        onChange={(title) => onChange({ ...draft, title })}
      />
      <TranslatedField
        label="زیرعنوان"
        value={draft.subtitle}
        onChange={(subtitle) => onChange({ ...draft, subtitle })}
      />
      <TranslatedField
        label="توضیحات"
        multiline
        value={draft.description}
        onChange={(description) => onChange({ ...draft, description })}
      />

      <ImageUpload
        label="تصویر شاخص (کاور دوره)"
        value={draft.cover}
        folder="courses"
        onChange={(cover) => onChange({ ...draft, cover })}
        onError={onError}
      />

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="سطح">
          <Select value={draft.level} onChange={(e) => onChange({ ...draft, level: e.target.value })}>
            {LEVELS.map((level) => (
              <option key={level} value={level} className="bg-ink-900">{level}</option>
            ))}
          </Select>
        </Field>
        <Field label="دسته‌بندی">
          <Select
            value={draft.category}
            onChange={(e) => onChange({ ...draft, category: e.target.value })}
          >
            <option value="" className="bg-ink-900">—</option>
            {categories
              .filter((item) => item.kind === "course")
              .map((item) => (
                <option key={item.id} value={item.id} className="bg-ink-900">
                  {item.title.fa || item.slug}
                </option>
              ))}
          </Select>
        </Field>
        <Field label="مدرس">
          <Select
            value={draft.instructor}
            onChange={(e) => onChange({ ...draft, instructor: e.target.value })}
          >
            <option value="" className="bg-ink-900">—</option>
            {instructors.map((item) => (
              <option key={item.id} value={item.id} className="bg-ink-900">
                {item.name}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="نوع برگزاری">
          <Select value={draft.format} onChange={(e) => onChange({ ...draft, format: e.target.value })}>
            <option value="self_paced" className="bg-ink-900">غیرحضوری</option>
            <option value="live" className="bg-ink-900">کلاس زنده</option>
            <option value="hybrid" className="bg-ink-900">ترکیبی</option>
            <option value="private" className="bg-ink-900">خصوصی</option>
          </Select>
        </Field>
        <Field label="قیمت (ریال)">
          <Input
            type="number"
            dir="ltr"
            className="tnum"
            value={draft.price}
            onChange={(e) => onChange({ ...draft, price: e.target.value })}
          />
        </Field>
        <Field label="قیمت با تخفیف (ریال)" hint="صفر یعنی بدون تخفیف">
          <Input
            type="number"
            dir="ltr"
            className="tnum"
            value={draft.discount_price}
            onChange={(e) => onChange({ ...draft, discount_price: e.target.value })}
          />
        </Field>
        <Field label="رنگ شاخص">
          <Input
            value={draft.accent}
            dir="ltr"
            onChange={(e) => onChange({ ...draft, accent: e.target.value })}
          />
        </Field>
        <Field label="نشانی (slug)" hint="خالی بگذار تا خودکار ساخته شود">
          <Input
            value={draft.slug}
            dir="ltr"
            onChange={(e) => onChange({ ...draft, slug: e.target.value })}
          />
        </Field>
      </div>

      <label className="flex items-center gap-3 text-sm text-mist-300">
        <input
          type="checkbox"
          checked={draft.is_published}
          onChange={(e) => onChange({ ...draft, is_published: e.target.checked })}
          className="size-4 accent-violet-500"
        />
        منتشر شود
      </label>
    </div>
  );
}
