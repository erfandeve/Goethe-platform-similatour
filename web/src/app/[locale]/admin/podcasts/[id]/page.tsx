import { notFound } from "next/navigation";

import { EpisodesManager } from "@/components/admin/EpisodesManager";
import { ButtonLink } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { isLocale } from "@/i18n/config";
import { apiFetchAuthed } from "@/lib/api";
import type { AdminEpisode, AdminPodcast } from "@/lib/admin";

export default async function AdminPodcastPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { locale, id } = await params;
  if (!isLocale(locale)) notFound();

  const data = await apiFetchAuthed<{ podcast: AdminPodcast; results: AdminEpisode[] }>(
    `/admin/podcasts/${id}/episodes/`,
    { locale },
  ).catch(() => null);

  if (!data) {
    return (
      <Empty
        title="پادکست پیدا نشد"
        icon="🔒"
        action={<ButtonLink href={`/${locale}/admin/podcasts`}>بازگشت</ButtonLink>}
      />
    );
  }

  return <EpisodesManager podcast={data.podcast} initial={data.results} locale={locale} />;
}
