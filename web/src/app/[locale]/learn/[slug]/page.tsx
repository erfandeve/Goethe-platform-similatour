import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";

import { LearningExperience } from "@/components/learning/LearningExperience";
import { getDictionary } from "@/i18n/get-dictionary";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed, getAccessToken } from "@/lib/api";
import { ApiError } from "@/lib/api";
import type { Classroom } from "@/lib/learning";

export const metadata: Metadata = { robots: { index: false, follow: false } };

const MAX_AUDIO_SECONDS = Number(process.env.NEXT_PUBLIC_MAX_AUDIO_DURATION ?? 60);

export default async function LearnPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();

  const token = await getAccessToken();
  if (!token) redirect(`/${locale}/login?next=/${locale}/learn/${slug}`);

  const dict = await getDictionary(locale);

  let classroom: Classroom;
  try {
    classroom = await apiFetchAuthed<Classroom>(`/learning/${slug}/`, { locale });
  } catch (caught) {
    // Not enrolled yet: send them to the sales page rather than a dead end.
    if (caught instanceof ApiError && (caught.status === 403 || caught.status === 404)) {
      redirect(`/${locale}/courses/${slug}`);
    }
    throw caught;
  }

  return (
    <div className="container-page py-8">
      <LearningExperience
        classroom={classroom}
        locale={locale}
        dict={dict}
        maxAudioSeconds={MAX_AUDIO_SECONDS}
      />
    </div>
  );
}
