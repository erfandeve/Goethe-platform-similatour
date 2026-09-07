import Link from "next/link";

import type { Locale } from "@/i18n/config";
import type { ArticleBlock } from "@/lib/types";

/** Renders article blocks as semantic HTML — the structure search engines read. */
export function ArticleBody({ body, locale }: { body: ArticleBlock[]; locale: Locale }) {
  return (
    <div className="flex flex-col gap-6">
      {body.map((block, index) => {
        switch (block.type) {
          case "h2":
            return (
              <h2
                key={index}
                id={block.id}
                className="font-display mt-8 scroll-mt-28 text-2xl font-bold text-white md:text-3xl"
              >
                {block.text}
              </h2>
            );

          case "h3":
            return (
              <h3 key={index} className="font-display mt-4 text-xl font-semibold text-white/95">
                {block.text}
              </h3>
            );

          case "p":
            return (
              <p key={index} className="text-[17px] leading-9 text-mist-300">
                {block.text}
              </p>
            );

          case "ul":
            return (
              <ul key={index} className="flex flex-col gap-3 ps-1">
                {block.items.map((item, i) => (
                  <li key={i} className="flex gap-3 text-[17px] leading-8 text-mist-300">
                    <span aria-hidden className="mt-3 size-1.5 shrink-0 rounded-full bg-violet-400" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            );

          case "ol":
            return (
              <ol key={index} className="flex flex-col gap-3">
                {block.items.map((item, i) => (
                  <li key={i} className="flex gap-3 text-[17px] leading-8 text-mist-300">
                    <span className="mt-1 grid size-6 shrink-0 place-items-center rounded-lg bg-violet-500/15 text-xs font-semibold text-violet-300">
                      {(i + 1).toLocaleString(locale)}
                    </span>
                    <span>{item}</span>
                  </li>
                ))}
              </ol>
            );

          case "quote":
            return (
              <blockquote
                key={index}
                className="border-s-2 border-violet-400/60 bg-white/[0.03] px-6 py-5 text-lg leading-9 text-white/90 italic"
              >
                {block.text}
              </blockquote>
            );

          case "callout":
            return (
              <aside
                key={index}
                className="rounded-2xl border border-cyan-400/20 bg-cyan-400/[0.06] p-6"
              >
                <p className="font-display mb-2 font-semibold text-cyan-200">{block.title}</p>
                <p className="text-[16px] leading-8 text-mist-300">{block.text}</p>
              </aside>
            );

          case "table":
            return (
              <figure key={index} className="my-2">
                <div className="overflow-x-auto rounded-2xl border border-white/10">
                  <table className="w-full border-collapse text-start text-sm">
                    <thead>
                      <tr className="bg-white/[0.04]">
                        {block.head.map((cell, i) => (
                          <th
                            key={i}
                            scope="col"
                            className="px-4 py-3 text-start font-semibold whitespace-nowrap text-white"
                          >
                            {cell}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {block.rows.map((row, r) => (
                        <tr key={r} className="border-t border-white/[0.07]">
                          {row.map((cell, c) => (
                            <td key={c} className="px-4 py-3 leading-7 text-mist-300">
                              {cell}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {block.caption && (
                  <figcaption className="mt-2 text-xs text-mist-500">{block.caption}</figcaption>
                )}
              </figure>
            );

          case "cta":
            return (
              <div
                key={index}
                className="my-4 flex flex-col gap-4 rounded-2xl border border-violet-400/25 bg-linear-to-br from-violet-500/10 to-cyan-400/[0.06] p-6 sm:flex-row sm:items-center sm:justify-between"
              >
                <div>
                  <p className="font-display text-lg font-semibold text-white">{block.title}</p>
                  <p className="mt-1 text-sm leading-7 text-mist-300">{block.text}</p>
                </div>
                <Link
                  href={`/${locale}${block.href}`}
                  className="shrink-0 rounded-full bg-white px-5 py-2.5 text-sm font-semibold text-ink-950 transition hover:bg-white/90"
                >
                  {block.label}
                </Link>
              </div>
            );

          default:
            return null;
        }
      })}
    </div>
  );
}
