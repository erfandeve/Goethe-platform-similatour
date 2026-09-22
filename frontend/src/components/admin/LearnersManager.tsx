"use client";

import { useEffect, useRef, useState } from "react";

import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { Empty } from "@/components/ui/Empty";
import { Input, Select } from "@/components/ui/Field";
import type { Locale } from "@/i18n/config";
import type { AdminLearner, AdminLearnerPage, Translated } from "@/lib/admin";
import { EMPTY_TRANSLATED } from "@/lib/admin";
import { formatDate, formatNumber } from "@/lib/format";
import { cn } from "@/lib/utils";

import { useAdmin } from "./useAdmin";
import { Modal, Panel, Toast, TranslatedField } from "./ui";

const SORTS: { value: string; label: string }[] = [
  { value: "points", label: "امتیاز کلی" },
  { value: "exam_score", label: "میانگین نمره آزمون" },
  { value: "course_progress", label: "پیشرفت دوره‌ها" },
  { value: "lessons", label: "درس‌های تمام‌شده" },
  { value: "last_active", label: "آخرین فعالیت" },
  { value: "joined", label: "تازه‌ترین عضو" },
];

const MEDALS: Record<number, { label: string; tone: string; ring: string }> = {
  1: {
    label: "رتبه اول",
    tone: "text-amber-300",
    ring: "border-amber-300/50 bg-amber-300/10",
  },
  2: {
    label: "رتبه دوم",
    tone: "text-slate-200",
    ring: "border-slate-300/40 bg-slate-300/10",
  },
  3: {
    label: "رتبه سوم",
    tone: "text-orange-300",
    ring: "border-orange-400/40 bg-orange-400/10",
  },
};

function LearnerAvatar({ learner }: { learner: AdminLearner }) {
  return (
    <Avatar
      src={learner.avatar}
      name={learner.name}
      className="size-10 text-sm"
      fallbackClassName="bg-violet-500/15 text-violet-300"
    />
  );
}

export function LearnersManager({
  initial,
  locale,
}: {
  initial: AdminLearnerPage;
  locale: Locale;
}) {
  const { busy, toast, run, call } = useAdmin();
  const [data, setData] = useState(initial);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState(initial.sort || "points");
  const [page, setPage] = useState(1);
  const [placing, setPlacing] = useState<{
    learner: AdminLearner;
    rank: number;
    note: Translated;
  } | null>(null);
  const first = useRef(true);

  const n = (value: number) => formatNumber(value, locale);

  // Reload on search/sort/page; the search waits for typing to pause.
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    const timer = setTimeout(
      async () => {
        const params = new URLSearchParams({ sort, page: String(page) });
        if (query.trim()) params.set("q", query.trim());
        const next = await run(() =>
          call<AdminLearnerPage>(`admin/learners?${params}`),
        );
        if (next) setData(next);
      },
      query ? 350 : 0,
    );
    return () => clearTimeout(timer);
  }, [query, sort, page, run, call]);

  async function place(learner: AdminLearner, rank: number, note?: Translated) {
    const saved = await run(
      () =>
        call<AdminLearner>(`admin/learners/${learner.id}/showcase`, {
          method: "PATCH",
          body: { rank, ...(note ? { note } : {}) },
        }),
      {
        success: rank
          ? `${learner.name} در ${MEDALS[rank].label} قرار گرفت`
          : "از سکو برداشته شد",
      },
    );
    if (!saved) return;
    // The previous holder of this rank was moved off by the server.
    setData((current) => {
      const rows = current.results.map((row) => {
        if (row.id === saved.id) return saved;
        if (rank && row.showcase_rank === rank)
          return { ...row, showcase_rank: 0 };
        return row;
      });
      const podium = [
        ...current.podium.filter(
          (row) => row.id !== saved.id && row.showcase_rank !== rank,
        ),
        ...(rank ? [saved] : []),
      ].sort((a, b) => a.showcase_rank - b.showcase_rank);
      return { ...current, results: rows, podium };
    });
    setPlacing(null);
  }

  const slots = [1, 2, 3].map((rank) =>
    data.podium.find((row) => row.showcase_rank === rank),
  );

  return (
    <div className="space-y-6">
      <Panel
        title="زبان‌آموزان برتر"
        description="سه نفری که این‌جا می‌گذاری، به همین ترتیب در صفحه اصلی سایت نمایش داده می‌شوند. از سایت فقط نام کوچک و حرف اول نام خانوادگی دیده می‌شود، نه ایمیل یا شماره."
      >
        <div className="grid gap-3 md:grid-cols-3">
          {slots.map((learner, index) => {
            const rank = index + 1;
            const medal = MEDALS[rank];
            return (
              <div
                key={rank}
                className={cn("rounded-2xl border p-4", medal.ring)}
              >
                <p className={cn("mb-3 text-xs font-bold", medal.tone)}>
                  {["🥇", "🥈", "🥉"][index]} {medal.label}
                </p>
                {learner ? (
                  <>
                    <div className="flex items-center gap-3">
                      <LearnerAvatar learner={learner} />
                      <div className="min-w-0">
                        <p className="truncate text-sm font-semibold">
                          {learner.name}
                        </p>
                        <p className="tnum text-xs text-mist-500">
                          {learner.level} · {n(learner.stats.points)} امتیاز
                        </p>
                      </div>
                    </div>
                    <p className="mt-3 line-clamp-2 min-h-8 text-xs text-mist-400">
                      {learner.showcase_note.fa || "بدون توضیح"}
                    </p>
                    <div className="mt-3 flex gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          setPlacing({
                            learner,
                            rank,
                            note: learner.showcase_note,
                          })
                        }
                        className="glass rounded-full px-3 py-1 text-xs"
                      >
                        ویرایش متن
                      </button>
                      <button
                        type="button"
                        onClick={() => place(learner, 0)}
                        disabled={busy}
                        className="rounded-full px-3 py-1 text-xs text-rose-400 transition hover:bg-rose-400/10"
                      >
                        برداشتن
                      </button>
                    </div>
                  </>
                ) : (
                  <p className="py-6 text-center text-xs text-mist-500">
                    خالی — از فهرست پایین انتخاب کن
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </Panel>

      <Panel
        title={`همه کاربرها (${n(data.meta.total)})`}
        description="امتیاز کلی = هر درس تمام‌شده ۱۰ + هر بخش آزمون قبول‌شده ۲۵ + میانگین نمره آزمون + میانگین نمره مکالمه + میانگین پیشرفت دوره‌ها."
      >
        <div className="mb-4 flex flex-wrap gap-3">
          <Input
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            placeholder="جستجو با نام، ایمیل یا شماره…"
            className="min-w-56 flex-1"
          />
          <div className="w-full sm:w-56">
            <Select
              value={sort}
              onChange={(e) => {
                setSort(e.target.value);
                setPage(1);
              }}
              aria-label="مرتب‌سازی"
            >
              {SORTS.map((option) => (
                <option key={option.value} value={option.value}>
                  مرتب بر اساس {option.label}
                </option>
              ))}
            </Select>
          </div>
        </div>

        {data.results.length ? (
          <ul
            className={cn("space-y-2 transition-opacity", busy && "opacity-60")}
          >
            {data.results.map((learner, index) => {
              const s = learner.stats;
              const position =
                (data.meta.page - 1) * data.meta.size + index + 1;
              return (
                <li
                  key={learner.id}
                  className="rounded-2xl border border-white/8 px-4 py-3"
                >
                  <div className="flex flex-wrap items-center gap-3">
                    <span className="tnum w-6 text-center text-xs text-mist-600">
                      {n(position)}
                    </span>
                    <LearnerAvatar learner={learner} />
                    <div className="min-w-0 flex-1">
                      <p className="flex items-center gap-2 truncate text-sm font-semibold">
                        {learner.name}
                        {learner.showcase_rank ? (
                          <span
                            className={cn(
                              "text-xs",
                              MEDALS[learner.showcase_rank].tone,
                            )}
                          >
                            {["🥇", "🥈", "🥉"][learner.showcase_rank - 1]}
                          </span>
                        ) : null}
                        {learner.is_staff ? (
                          <span className="rounded-full bg-white/8 px-2 py-0.5 text-[10px] font-normal text-mist-400">
                            ادمین
                          </span>
                        ) : null}
                        {!learner.is_active ? (
                          <span className="rounded-full bg-rose-400/12 px-2 py-0.5 text-[10px] font-normal text-rose-300">
                            مسدود
                          </span>
                        ) : null}
                      </p>
                      <p className="truncate text-xs text-mist-500" dir="ltr">
                        {learner.email}
                      </p>
                    </div>
                    <span className="tnum rounded-full bg-violet-500/12 px-3 py-1 text-xs font-semibold text-violet-200">
                      {n(s.points)} امتیاز
                    </span>
                    <span
                      className="flex items-center gap-1"
                      role="group"
                      aria-label="رتبه در سکو"
                    >
                      {[1, 2, 3].map((rank) => (
                        <button
                          key={rank}
                          type="button"
                          disabled={busy}
                          onClick={() =>
                            learner.showcase_rank === rank
                              ? place(learner, 0)
                              : setPlacing({
                                  learner,
                                  rank,
                                  note: learner.showcase_note ?? {
                                    ...EMPTY_TRANSLATED,
                                  },
                                })
                          }
                          aria-pressed={learner.showcase_rank === rank}
                          title={
                            learner.showcase_rank === rank
                              ? "برداشتن از سکو"
                              : MEDALS[rank].label
                          }
                          className={cn(
                            "tnum grid size-8 place-items-center rounded-full border text-xs font-bold transition",
                            learner.showcase_rank === rank
                              ? cn(MEDALS[rank].ring, MEDALS[rank].tone)
                              : "border-white/12 text-mist-500 hover:bg-white/5 hover:text-mist-100",
                          )}
                        >
                          {n(rank)}
                        </button>
                      ))}
                    </span>
                  </div>

                  <dl className="mt-3 grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs sm:grid-cols-3 lg:grid-cols-6">
                    <Stat
                      label="سطح"
                      value={`${learner.level} → ${learner.target_level}`}
                    />
                    <Stat
                      label="دوره‌ها"
                      value={`${n(s.courses)} · ${n(s.course_progress)}٪`}
                      bar={s.course_progress}
                    />
                    <Stat label="درس تمام‌شده" value={n(s.lessons_done)} />
                    <Stat
                      label="آزمون (قبولی)"
                      value={`${n(s.exams_taken)} (${n(s.exams_passed)}) · ${n(s.exam_score)}٪`}
                      bar={s.exam_score}
                    />
                    <Stat
                      label="مکالمه با AI"
                      value={`${n(s.speaking_answers)} · ${n(s.speaking_score)}٪`}
                      bar={s.speaking_score}
                    />
                    <Stat
                      label="آخرین فعالیت"
                      value={formatDate(s.last_active, locale)}
                    />
                  </dl>
                </li>
              );
            })}
          </ul>
        ) : (
          <Empty title="کاربری پیدا نشد" icon="☺" />
        )}

        {data.meta.pages > 1 ? (
          <div className="mt-5 flex items-center justify-center gap-3 text-sm">
            <Button
              size="sm"
              variant="outline"
              disabled={page <= 1 || busy}
              onClick={() => setPage(page - 1)}
            >
              قبلی
            </Button>
            <span className="tnum text-mist-400">
              {n(data.meta.page)} از {n(data.meta.pages)}
            </span>
            <Button
              size="sm"
              variant="outline"
              disabled={page >= data.meta.pages || busy}
              onClick={() => setPage(page + 1)}
            >
              بعدی
            </Button>
          </div>
        ) : null}
      </Panel>

      <Modal
        open={!!placing}
        title={
          placing
            ? `${placing.learner.name} — ${MEDALS[placing.rank].label}`
            : ""
        }
        onClose={() => setPlacing(null)}
      >
        {placing ? (
          <div className="space-y-5">
            {slots[placing.rank - 1] &&
            slots[placing.rank - 1]?.id !== placing.learner.id ? (
              <p className="rounded-2xl border border-amber-300/30 bg-amber-300/10 px-4 py-3 text-xs text-amber-200">
                الان {slots[placing.rank - 1]?.name} در این رتبه است و با ذخیره
                از سکو برداشته می‌شود.
              </p>
            ) : null}
            <TranslatedField
              label="جمله زیر اسمش در سایت (مثلاً «قبولی B1 با نمره ۹۲ در سه ماه»)"
              value={placing.note}
              onChange={(note) => setPlacing({ ...placing, note })}
            />
            <div className="flex gap-3">
              <Button
                className="flex-1"
                disabled={busy}
                onClick={() =>
                  place(placing.learner, placing.rank, placing.note)
                }
              >
                {busy ? "…" : "ذخیره و نمایش در سایت"}
              </Button>
              <Button variant="outline" onClick={() => setPlacing(null)}>
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

function Stat({
  label,
  value,
  bar,
}: {
  label: string;
  value: string;
  bar?: number;
}) {
  return (
    <div className="min-w-0">
      <dt className="text-mist-600">{label}</dt>
      <dd className="tnum truncate text-mist-200">{value}</dd>
      {bar !== undefined ? (
        <div className="mt-1 h-1 overflow-hidden rounded-full bg-white/8">
          <div
            className="h-full rounded-full bg-linear-to-r from-violet-500 to-cyan-400"
            style={{ width: `${Math.min(100, bar)}%` }}
          />
        </div>
      ) : null}
    </div>
  );
}
