"use client";

import { useRef, useState } from "react";

import { Button } from "@/components/ui/Button";
import { mediaUrl } from "@/lib/utils";

/**
 * Cover picker: uploads straight away and stores the returned path, so the
 * form only ever carries a URL. An existing cover is shown as-is.
 */
export function ImageUpload({
  label,
  value,
  folder,
  onChange,
  onError,
  hint,
}: {
  label: string;
  value: string;
  folder: string;
  onChange: (url: string) => void;
  onError: (message: string) => void;
  hint?: string;
}) {
  const input = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(0);

  function upload(file: File) {
    setBusy(true);
    setProgress(0);

    const form = new FormData();
    form.append("file", file);
    form.append("folder", folder);

    const request = new XMLHttpRequest();
    request.open("POST", "/api/admin/upload?kind=image");
    request.upload.onprogress = (event) => {
      if (event.lengthComputable) setProgress(Math.round((event.loaded / event.total) * 100));
    };
    request.onload = () => {
      setBusy(false);
      try {
        const body = JSON.parse(request.responseText);
        if (request.status >= 400) {
          onError(body.detail || "آپلود تصویر ناموفق بود");
          return;
        }
        onChange(body.url);
      } catch {
        onError("پاسخ آپلود نامعتبر بود");
      }
    };
    request.onerror = () => {
      setBusy(false);
      onError("ارتباط با سرور قطع شد");
    };
    request.send(form);
  }

  return (
    <div>
      <span className="mb-2 block text-xs font-medium tracking-wide text-mist-400">{label}</span>

      <div className="flex flex-wrap items-start gap-4 rounded-2xl border border-white/10 bg-white/3 p-4">
        <div className="relative aspect-16/10 w-44 shrink-0 overflow-hidden rounded-xl bg-ink-900 ring-1 ring-white/10">
          {value ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={mediaUrl(value)} alt="" className="size-full object-cover" />
          ) : (
            <span className="grid size-full place-items-center text-xs text-mist-600">
              بدون تصویر
            </span>
          )}
        </div>

        <div className="min-w-40 flex-1">
          <input
            ref={input}
            type="file"
            accept="image/jpeg,image/png,image/webp,image/avif"
            className="hidden"
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) upload(file);
              event.target.value = "";
            }}
          />

          <div className="flex flex-wrap gap-2">
            <Button
              type="button"
              size="sm"
              variant="soft"
              disabled={busy}
              onClick={() => input.current?.click()}
            >
              {busy ? `در حال آپلود… ${progress}%` : value ? "تعویض تصویر" : "انتخاب تصویر"}
            </Button>
            {value ? (
              <button
                type="button"
                onClick={() => onChange("")}
                className="rounded-full px-3 py-1.5 text-xs text-rose-400 transition hover:bg-rose-400/10"
              >
                حذف
              </button>
            ) : null}
          </div>

          {busy ? (
            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/10">
              <div
                className="h-full rounded-full bg-linear-to-r from-violet-500 to-cyan-400 transition-[width]"
                style={{ width: `${progress}%` }}
              />
            </div>
          ) : null}

          <p className="mt-2 text-xs text-mist-600">
            {hint ?? "JPG، PNG، WebP یا AVIF تا ۸ مگابایت. نسبت پیشنهادی ۱۶:۱۰."}
          </p>
          {value ? (
            <p className="tnum mt-1 truncate text-[11px] text-mist-600" dir="ltr">
              {value}
            </p>
          ) : null}
        </div>
      </div>
    </div>
  );
}
