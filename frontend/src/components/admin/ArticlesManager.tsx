"use client";

import { useState } from "react";

import { ImageUpload } from "@/components/admin/ImageUpload";
import { Modal, Panel, Toast, TranslatedField } from "@/components/admin/ui";
import { useAdmin } from "@/components/admin/useAdmin";
import { Button } from "@/components/ui/Button";
import { Input, Select } from "@/components/ui/Field";
import type { Translated } from "@/lib/admin";

const EMPTY: Translated = { fa: "", en: "", de: "" };

interface Block {
  type: string;
  text: Translated;
  anchor: string;
  items: Translated[];
  head: Translated[];
  rows: Translated[][];
  caption: Translated;
  title: Translated;
  label: Translated;
  href: string;
}

interface Faq {
  question: Translated;
  answer: Translated;
}

interface Article {
  id: string;
  slug: string;
  title: Translated;
  meta_title: Translated;
  meta_description: Translated;
  excerpt: Translated;
  focus_keyword: Translated;
  keywords: Translated;
  cover: string;
  related: string[];
  reading_minutes: number;
  is_published: boolean;
  order: number;
  blocks: number;
  words: { fa: number; en: number; de: number };
  body?: Block[];
  faq?: Faq[];
}

/** Only the block types an editor realistically writes by hand. Tables are
 *  editable but created through the seed; the form keeps them intact. */
const BLOCK_LABELS: Record<string, string> = {
  h2: "عنوان اصلی (H2)",
  h3: "عنوان فرعی (H3)",
  p: "پاراگراف",
  ul: "فهرست نقطه‌ای",
  ol: "فهرست شماره‌دار",
  quote: "نقل قول",
  callout: "کادر تأکید",
  cta: "دکمه دعوت",
  table: "جدول",
};

function blankBlock(type: string): Block {
  return {
    type,
    text: { ...EMPTY },
    anchor: "",
    items: [],
    head: [],
    rows: [],
    caption: { ...EMPTY },
    title: { ...EMPTY },
    label: { ...EMPTY },
    href: "",
  };
}

function blankArticle(): Article {
  return {
    id: "",
    slug: "",
    title: { ...EMPTY },
    meta_title: { ...EMPTY },
    meta_description: { ...EMPTY },
    excerpt: { ...EMPTY },
    focus_keyword: { ...EMPTY },
    keywords: { ...EMPTY },
    cover: "",
    related: [],
    reading_minutes: 8,
    is_published: true,
    order: 0,
    blocks: 0,
    words: { fa: 0, en: 0, de: 0 },
    body: [],
    faq: [],
  };
}

export function ArticlesManager({ initial }: { initial: Article[] }) {
  const { busy, toast, notify, run, call } = useAdmin();
  const [articles, setArticles] = useState(initial);
  const [draft, setDraft] = useState<Article | null>(null);

  const reload = async () => {
    const data = await run(() => call<{ results: Article[] }>("/admin/articles/"));
    if (data) setArticles(data.results);
  };

  const open = async (article: Article) => {
    const full = await run(() => call<Article>(`/admin/articles/${article.id}/`));
    if (full) setDraft(full);
  };

  const save = async () => {
    if (!draft) return;
    const payload = { ...draft } as Record<string, unknown>;
    delete payload.id;
    delete payload.blocks;
    delete payload.words;

    const result = draft.id
      ? await run(() => call(`/admin/articles/${draft.id}/`, { method: "PATCH", body: payload }), {
          success: "مقاله ذخیره شد.",
        })
      : await run(() => call("/admin/articles/", { method: "POST", body: payload }), {
          success: "مقاله ساخته شد.",
        });

    if (result) {
      setDraft(null);
      await reload();
    }
  };

  const remove = async (article: Article) => {
    if (!confirm(`مقاله «${article.title.fa || article.slug}» حذف شود؟`)) return;
    const done = await run(
      () => call(`/admin/articles/${article.id}/`, { method: "DELETE" }),
      { success: "مقاله حذف شد." },
    );
    if (done !== null) await reload();
  };

  const patchBlock = (index: number, patch: Partial<Block>) => {
    if (!draft?.body) return;
    setDraft({
      ...draft,
      body: draft.body.map((block, i) => (i === index ? { ...block, ...patch } : block)),
    });
  };

  const moveBlock = (index: number, delta: number) => {
    if (!draft?.body) return;
    const next = [...draft.body];
    const target = index + delta;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    setDraft({ ...draft, body: next });
  };

  return (
    <div className="space-y-6">
      <Toast {...toast} />

      <Panel
        title="مقالات"
        description="هر مقاله در سه زبان ذخیره می‌شود. عنوان سئو، توضیح متا و کلمات کلیدی برای هر زبان جداگانه‌اند."
        action={
          <Button onClick={() => setDraft(blankArticle())} disabled={busy}>
            مقاله جدید
          </Button>
        }
      >
        <ul className="space-y-2">
          {articles.map((article) => (
            <li
              key={article.id}
              className="flex flex-wrap items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.02] p-4"
            >
              <div className="min-w-0 flex-1">
                <p className="truncate font-medium text-white">
                  {article.title.fa || article.slug}
                </p>
                <p className="mt-1 text-xs text-mist-500" dir="ltr">
                  /{article.slug} · {article.blocks} بلوک · fa {article.words.fa} / en{" "}
                  {article.words.en} / de {article.words.de}
                  {!article.is_published && " · پیش‌نویس"}
                </p>
              </div>
              <Button variant="ghost" onClick={() => open(article)} disabled={busy}>
                ویرایش
              </Button>
              <Button variant="ghost" onClick={() => remove(article)} disabled={busy}>
                حذف
              </Button>
            </li>
          ))}
          {articles.length === 0 && (
            <li className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-mist-500">
              هنوز مقاله‌ای ساخته نشده.
            </li>
          )}
        </ul>
      </Panel>

      <Modal
        open={Boolean(draft)}
        title={draft?.id ? "ویرایش مقاله" : "مقاله جدید"}
        onClose={() => setDraft(null)}
      >
        {draft && (
          <div className="space-y-5">
            <TranslatedField
              label="عنوان مقاله"
              required
              value={draft.title}
              onChange={(title) => setDraft({ ...draft, title })}
            />
            <TranslatedField
              label="عنوان سئو (زیر ۶۰ نویسه)"
              value={draft.meta_title}
              onChange={(meta_title) => setDraft({ ...draft, meta_title })}
            />
            <TranslatedField
              label="توضیح متا (۱۵۰ تا ۱۶۰ نویسه)"
              multiline
              value={draft.meta_description}
              onChange={(meta_description) => setDraft({ ...draft, meta_description })}
            />
            <TranslatedField
              label="کلمه کلیدی اصلی"
              value={draft.focus_keyword}
              onChange={(focus_keyword) => setDraft({ ...draft, focus_keyword })}
            />
            <TranslatedField
              label="کلمات کلیدی (با ویرگول جدا کن)"
              multiline
              value={draft.keywords}
              onChange={(keywords) => setDraft({ ...draft, keywords })}
            />
            <TranslatedField
              label="چکیده"
              multiline
              value={draft.excerpt}
              onChange={(excerpt) => setDraft({ ...draft, excerpt })}
            />

            <ImageUpload
              label="تصویر شاخص"
              value={draft.cover}
              folder="articles"
              onChange={(cover) => setDraft({ ...draft, cover })}
              onError={(message) => notify(message, "error")}
            />

            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block">
                <span className="mb-2 block text-xs text-mist-400">زمان مطالعه (دقیقه)</span>
                <Input
                  type="number"
                  value={draft.reading_minutes}
                  onChange={(e) =>
                    setDraft({ ...draft, reading_minutes: Number(e.target.value) || 0 })
                  }
                />
              </label>
              <label className="block">
                <span className="mb-2 block text-xs text-mist-400">
                  مقالات مرتبط (slug، با ویرگول)
                </span>
                <Input
                  dir="ltr"
                  value={draft.related.join(", ")}
                  onChange={(e) =>
                    setDraft({
                      ...draft,
                      related: e.target.value
                        .split(",")
                        .map((s) => s.trim())
                        .filter(Boolean),
                    })
                  }
                />
              </label>
            </div>

            <div className="space-y-3 rounded-2xl border border-white/10 p-4">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <p className="text-sm font-medium text-white">متن مقاله</p>
                <div className="flex items-center gap-2">
                  <Select
                    defaultValue=""
                    onChange={(e) => {
                      if (!e.target.value) return;
                      setDraft({
                        ...draft,
                        body: [...(draft.body ?? []), blankBlock(e.target.value)],
                      });
                      e.target.value = "";
                    }}
                  >
                    <option value="">افزودن بلوک…</option>
                    {Object.entries(BLOCK_LABELS)
                      .filter(([type]) => type !== "table")
                      .map(([type, label]) => (
                        <option key={type} value={type}>
                          {label}
                        </option>
                      ))}
                  </Select>
                </div>
              </div>

              {(draft.body ?? []).map((block, index) => (
                <div key={index} className="space-y-3 rounded-xl bg-white/[0.03] p-3">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs text-mist-500">
                      #{index + 1} · {BLOCK_LABELS[block.type] ?? block.type}
                    </span>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => moveBlock(index, -1)}
                        className="px-1.5 text-xs text-mist-500 hover:text-white"
                        aria-label="بالا"
                      >
                        ▲
                      </button>
                      <button
                        onClick={() => moveBlock(index, 1)}
                        className="px-1.5 text-xs text-mist-500 hover:text-white"
                        aria-label="پایین"
                      >
                        ▼
                      </button>
                      <Button
                        variant="ghost"
                        onClick={() =>
                          setDraft({
                            ...draft,
                            body: (draft.body ?? []).filter((_, i) => i !== index),
                          })
                        }
                      >
                        حذف
                      </Button>
                    </div>
                  </div>

                  {block.type === "table" ? (
                    <p className="text-xs text-mist-500">
                      جدول {block.head.length} ستونی با {block.rows.length} ردیف — ساختارش دست
                      نمی‌خورد و همان‌طور ذخیره می‌شود.
                    </p>
                  ) : block.type === "ul" || block.type === "ol" ? (
                    <div className="space-y-2">
                      {block.items.map((item, i) => (
                        <TranslatedField
                          key={i}
                          label={`مورد ${i + 1}`}
                          multiline
                          value={item}
                          onChange={(next) =>
                            patchBlock(index, {
                              items: block.items.map((old, j) => (j === i ? next : old)),
                            })
                          }
                        />
                      ))}
                      <Button
                        variant="ghost"
                        onClick={() =>
                          patchBlock(index, { items: [...block.items, { ...EMPTY }] })
                        }
                      >
                        افزودن مورد
                      </Button>
                    </div>
                  ) : (
                    <>
                      {(block.type === "callout" || block.type === "cta") && (
                        <TranslatedField
                          label="عنوان"
                          value={block.title}
                          onChange={(title) => patchBlock(index, { title })}
                        />
                      )}
                      <TranslatedField
                        label="متن"
                        multiline={block.type !== "h2" && block.type !== "h3"}
                        value={block.text}
                        onChange={(text) => patchBlock(index, { text })}
                      />
                      {block.type === "cta" && (
                        <div className="grid gap-3 sm:grid-cols-2">
                          <TranslatedField
                            label="متن دکمه"
                            value={block.label}
                            onChange={(label) => patchBlock(index, { label })}
                          />
                          <label className="block">
                            <span className="mb-2 block text-xs text-mist-400">مقصد دکمه</span>
                            <Input
                              dir="ltr"
                              value={block.href}
                              onChange={(e) => patchBlock(index, { href: e.target.value })}
                            />
                          </label>
                        </div>
                      )}
                      {block.type === "h2" && (
                        <label className="block">
                          <span className="mb-2 block text-xs text-mist-400">
                            لنگر (برای فهرست مطالب — خالی بگذاری خودکار ساخته می‌شود)
                          </span>
                          <Input
                            dir="ltr"
                            value={block.anchor}
                            onChange={(e) => patchBlock(index, { anchor: e.target.value })}
                          />
                        </label>
                      )}
                    </>
                  )}
                </div>
              ))}
            </div>

            <div className="space-y-3 rounded-2xl border border-white/10 p-4">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-white">پرسش‌های پرتکرار</p>
                <Button
                  variant="ghost"
                  onClick={() =>
                    setDraft({
                      ...draft,
                      faq: [...(draft.faq ?? []), { question: { ...EMPTY }, answer: { ...EMPTY } }],
                    })
                  }
                >
                  افزودن
                </Button>
              </div>
              {(draft.faq ?? []).map((item, index) => (
                <div key={index} className="space-y-3 rounded-xl bg-white/[0.03] p-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-mist-500">#{index + 1}</span>
                    <Button
                      variant="ghost"
                      onClick={() =>
                        setDraft({
                          ...draft,
                          faq: (draft.faq ?? []).filter((_, i) => i !== index),
                        })
                      }
                    >
                      حذف
                    </Button>
                  </div>
                  <TranslatedField
                    label="پرسش"
                    value={item.question}
                    onChange={(question) =>
                      setDraft({
                        ...draft,
                        faq: (draft.faq ?? []).map((old, i) =>
                          i === index ? { ...old, question } : old,
                        ),
                      })
                    }
                  />
                  <TranslatedField
                    label="پاسخ"
                    multiline
                    value={item.answer}
                    onChange={(answer) =>
                      setDraft({
                        ...draft,
                        faq: (draft.faq ?? []).map((old, i) =>
                          i === index ? { ...old, answer } : old,
                        ),
                      })
                    }
                  />
                </div>
              ))}
            </div>

            <label className="flex items-center gap-3 text-sm text-mist-300">
              <input
                type="checkbox"
                checked={draft.is_published}
                onChange={(e) => setDraft({ ...draft, is_published: e.target.checked })}
                className="size-4 accent-violet-500"
              />
              منتشر شود
            </label>

            <div className="flex justify-end gap-3 pt-2">
              <Button variant="ghost" onClick={() => setDraft(null)}>
                انصراف
              </Button>
              <Button onClick={save} disabled={busy}>
                ذخیره
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
