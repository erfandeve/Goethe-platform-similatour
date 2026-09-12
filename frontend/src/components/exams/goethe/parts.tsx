"use client";

import { useMemo, useState, type ReactNode } from "react";

import { cn, mediaUrl } from "@/lib/utils";

import { AudioRing } from "./AudioRing";
import type { ExamItem, ExamPart, Answers } from "./types";

/* ------------------------------------------------------------------ atoms */

export function InstructionBand({ text }: { text: string }) {
  // The printed band puts the situation on one line and the task on the next.
  const [situation, ...rest] = text.split(/(?<=\.)\s+(?=[A-ZÄÖÜ])/);
  const task = rest.join(" ");

  return (
    <div
      className="exam-body mb-6 px-5 py-4 font-semibold text-white"
      style={{ background: "var(--exam-band)" }}
      dir="ltr"
    >
      <p>{situation}</p>
      {task ? <p className="mt-2">{task}</p> : null}
    </div>
  );
}

export function PartHeading({ title }: { title: string }) {
  return (
    <h1 className="mb-4 text-sm font-bold" dir="ltr">
      {title}
    </h1>
  );
}

/** Radio row styled like the exam player: blue dot, generous hit area. */
/** The situation line the paper prints above a task ("Sie nehmen an …"). */
function StimulusIntro({ text }: { text?: string }) {
  if (!text) return null;
  return (
    <p className="exam-body mb-5 italic" dir="ltr" style={{ color: "var(--exam-muted)" }}>
      {text}
    </p>
  );
}

/**
 * The worked example (Beispiel 0) that opens every Teil on the paper. Shown
 * already answered and greyed, so it reads as a model rather than a question.
 */
export function ExampleRow({ part }: { part: ExamPart }) {
  const prompt = part.example?.prompt?.trim();
  if (!prompt) return null;

  let line = prompt;
  if (!prompt.includes("→") && part.example.answer) {
    const pool = [...part.options, ...(part.items[0]?.options ?? [])];
    const option = pool.find((o) => o.key === part.example.answer);
    const shown =
      option?.text && option.text !== option.key
        ? `${option.key}) ${option.text}`
        : option?.label || part.example.answer;
    // "richtig" reads as "Richtig"; a lone letter stays a letter.
    line = `${prompt} → ${shown.length > 2 ? shown.charAt(0).toUpperCase() + shown.slice(1) : shown}`;
  }

  return (
    <div
      className="mb-5 rounded-sm border border-dashed px-4 py-3"
      style={{ borderColor: "var(--exam-line)", background: "var(--exam-page)", opacity: 0.85 }}
      dir="ltr"
    >
      <p className="mb-1 text-xs font-bold tracking-wide uppercase" style={{ color: "var(--exam-muted)" }}>
        Beispiel
      </p>
      <p className="exam-body">{line}</p>
    </div>
  );
}

/** A block's own picture — a sign, an advert, a photo the question is about. */
function BlockImage({ src, alt }: { src?: string; alt?: string }) {
  if (!src) return null;
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={mediaUrl(src)}
      alt={alt || ""}
      loading="lazy"
      className="mb-3 w-full rounded-sm object-contain"
      style={{ border: "1px solid var(--exam-line)" }}
    />
  );
}

function Choice({
  name,
  checked,
  onChange,
  children,
  /** Picture options put the radio under the image rather than beside it. */
  stacked = false,
}: {
  name: string;
  checked: boolean;
  onChange: () => void;
  children: ReactNode;
  stacked?: boolean;
}) {
  return (
    <label
      className={cn(
        "flex cursor-pointer gap-3 py-1.5",
        stacked ? "flex-col-reverse items-center text-center" : "items-start",
      )}
      dir="ltr"
    >
      <span className="relative mt-0.5 grid size-4 shrink-0 place-items-center">
        <input
          type="radio"
          name={name}
          checked={checked}
          onChange={onChange}
          className="peer sr-only"
        />
        <span
          className="size-4 rounded-full border transition"
          style={{
            borderColor: checked ? "var(--exam-radio)" : "#9a9a96",
            background: checked ? "var(--exam-radio)" : "#fff",
            boxShadow: checked ? "inset 0 0 0 2.5px #fff" : "none",
          }}
        />
      </span>
      <span className="exam-body w-full leading-snug">{children}</span>
    </label>
  );
}

export function ItemBlock({
  item,
  answers,
  setAnswer,
  options,
  showNumber = true,
}: {
  item: ExamItem;
  answers: Answers;
  setAnswer: (key: string, value: string) => void;
  options: { key: string; label: string; text?: string; author?: string; image?: string }[];
  showNumber?: boolean;
}) {
  // A1 answers a picture as often as a sentence, so picture options lay out
  // side by side instead of as a stacked list.
  const pictorial = options.some((option) => option.image);
  // Matching tasks offer a–j plus 0: eleven radio lines per question would
  // bury the page, so single-letter pools become a row of keys.
  const compact =
    !pictorial && options.length > 5 && options.every((option) => (option.label || option.key).length <= 2);

  if (compact) {
    return (
      <div className="border-b py-4 first:pt-0 last:border-0" style={{ borderColor: "var(--exam-line)" }}>
        <p className="exam-lead mb-3 font-bold" dir="ltr">
          {showNumber ? `${item.number}. ` : ""}
          {item.prompt}
        </p>
        <div className="flex flex-wrap gap-2" dir="ltr" role="radiogroup" aria-label={item.prompt}>
          {options.map((option) => {
            const checked = answers[item.key] === option.key;
            return (
              <label
                key={option.key}
                className="grid size-10 cursor-pointer place-items-center rounded-sm border text-sm font-bold transition"
                style={{
                  borderColor: checked ? "var(--exam-radio)" : "#b9b9b5",
                  background: checked ? "var(--exam-radio)" : "#fff",
                  color: checked ? "#fff" : "inherit",
                }}
              >
                <input
                  type="radio"
                  name={item.key}
                  checked={checked}
                  onChange={() => setAnswer(item.key, option.key)}
                  className="sr-only"
                />
                {option.label || option.key}
              </label>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="border-b py-5 first:pt-0 last:border-0" style={{ borderColor: "var(--exam-line)" }}>
      <p className="exam-lead mb-3 font-bold" dir="ltr">
        {showNumber ? `${item.number}. ` : ""}
        {item.prompt}
      </p>
      <div className={pictorial ? "grid grid-cols-1 gap-3 sm:grid-cols-3" : "ps-1"}>
        {options.map((option) => (
          <Choice
            key={option.key}
            name={item.key}
            checked={answers[item.key] === option.key}
            onChange={() => setAnswer(item.key, option.key)}
            stacked={pictorial}
          >
            {option.image ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={mediaUrl(option.image)}
                alt={option.text || option.label || option.key}
                loading="lazy"
                // contain, not cover: these are line drawings, and cropping a
                // clock face or a price tag changes the answer.
                className="mb-2 aspect-4/3 w-full rounded-sm bg-white object-contain"
                style={{ border: "1px solid var(--exam-line)" }}
              />
            ) : null}
            {option.text ? (
              <>
                {/* a/b/c lead their sentence; "richtig"/"ja" are the answer itself. */}
                {option.key.toLowerCase() !== option.text.toLowerCase() ? (
                  <b className="me-1.5">{option.key}</b>
                ) : null}
                {option.text}
              </>
            ) : (
              option.label
            )}
            {option.author ? (
              <span className="ms-1" style={{ color: "var(--exam-muted)" }}>
                , {option.author}
              </span>
            ) : null}
          </Choice>
        ))}
      </div>
    </div>
  );
}

/* --------------------------------------------------- Lesen 1: forum posts */

export function MatchPersonStimulus({ part }: { part: ExamPart }) {
  return (
    <>
      <PartHeading title={part.title_de || part.title} />
      <InstructionBand text={part.instructions_de} />
      <h2 className="exam-lead mb-6 text-center font-bold" dir="ltr">
        {part.stimulus.title}
      </h2>
      <div className="space-y-7">
        {part.stimulus.blocks.map((block) => (
          <article key={block.label}>
            <h3 className="mb-2 text-sm font-bold" dir="ltr">
              {block.title}
            </h3>
            <div className="flex gap-4" dir="ltr">
              <span
                className="grid size-24 shrink-0 place-items-center rounded-sm text-2xl font-semibold text-white"
                style={{ background: "#b6bcbe" }}
                aria-hidden
              >
                {block.title.slice(0, 1)}
              </span>
              <p className="exam-body text-justify">{block.text}</p>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}

/* ------------------------------------------------- Lesen 2: drag the gaps */

export function GapDragStimulus({
  part,
  answers,
  setAnswer,
}: {
  part: ExamPart;
  answers: Answers;
  setAnswer: (key: string, value: string) => void;
}) {
  const [over, setOver] = useState<number | null>(null);
  const byNumber = useMemo(
    () => new Map(part.items.map((item) => [item.number, item])),
    [part.items],
  );
  const options = useMemo(
    () => new Map(part.options.map((option) => [option.key, option])),
    [part.options],
  );

  function drop(gap: number, key: string) {
    const item = byNumber.get(gap);
    if (item) setAnswer(item.key, key);
    setOver(null);
  }

  function renderParagraph(text: string, paragraphIndex: number) {
    // Paragraphs carry [[n]] markers where a sentence has been removed.
    const pieces = text.split(/(\[\[\d+\]\])/g);
    return (
      <p key={paragraphIndex} className="exam-body mb-4 text-justify" dir="ltr">
        {pieces.map((piece, index) => {
          const match = piece.match(/^\[\[(\d+)\]\]$/);
          if (!match) return <span key={index}>{piece}</span>;
          const gap = Number(match[1]);
          if (gap === 0) {
            return (
              <span key={index} className="exam-gap-slot" style={{ opacity: 0.75 }}>
                <span className="exam-gap-number">0</span>
                {part.example.answer}
              </span>
            );
          }
          const item = byNumber.get(gap);
          const chosen = item ? answers[item.key] : undefined;
          return (
            <span
              key={index}
              className="exam-gap-slot"
              data-over={over === gap}
              onDragOver={(event) => {
                event.preventDefault();
                setOver(gap);
              }}
              onDragLeave={() => setOver((value) => (value === gap ? null : value))}
              onDrop={(event) => {
                event.preventDefault();
                drop(gap, event.dataTransfer.getData("text/plain"));
              }}
              onClick={() => {
                if (chosen && item) setAnswer(item.key, "");
              }}
              role="button"
              tabIndex={0}
              onKeyDown={(event) => {
                if ((event.key === "Backspace" || event.key === "Delete") && item) {
                  setAnswer(item.key, "");
                }
              }}
            >
              <span className="exam-gap-number">{gap}</span>
              {chosen ? options.get(chosen)?.text : ""}
            </span>
          );
        })}
      </p>
    );
  }

  return (
    <>
      <PartHeading title={part.title_de || part.title} />
      <InstructionBand text={part.instructions_de} />
      <h2 className="exam-lead mb-1 text-center font-bold" dir="ltr">
        {part.stimulus.title}
      </h2>
      <p className="mb-5 text-center text-sm font-semibold" dir="ltr">
        {part.stimulus.subtitle}
      </p>
      {part.stimulus.blocks.map((block, index) => renderParagraph(block.text, index))}
    </>
  );
}

export function GapDragOptions({
  part,
  answers,
  setAnswer,
}: {
  part: ExamPart;
  answers: Answers;
  setAnswer: (key: string, value: string) => void;
}) {
  const used = new Set(part.items.map((item) => answers[item.key]).filter(Boolean));
  const [picked, setPicked] = useState<string | null>(null);

  return (
    <div className="space-y-3">
      {part.options.map((option) => {
        const isUsed = used.has(option.key);
        return (
          <div
            key={option.key}
            className="exam-option-tile"
            data-used={isUsed}
            draggable={!isUsed}
            onDragStart={(event) => event.dataTransfer.setData("text/plain", option.key)}
            onClick={() => {
              if (isUsed) {
                // Clicking a placed sentence sends it back to the pool.
                const item = part.items.find((entry) => answers[entry.key] === option.key);
                if (item) setAnswer(item.key, "");
                return;
              }
              setPicked((value) => (value === option.key ? null : option.key));
              const empty = part.items.find((entry) => !answers[entry.key]);
              if (picked === option.key && empty) setAnswer(empty.key, option.key);
            }}
            dir="ltr"
          >
            <span aria-hidden style={{ color: "var(--exam-muted)" }}>
              ✥
            </span>
            <span className="exam-body">{option.text}</span>
          </div>
        );
      })}
      <p className="pt-2 text-xs" style={{ color: "var(--exam-muted)" }} dir="ltr">
        Ziehen Sie die Sätze in die Lücken. Ein Klick auf eine Lücke leert sie wieder.
      </p>
    </div>
  );
}

/* ------------------------------------------- Lesen 3 / Hören: plain article */

export function ArticleStimulus({ part }: { part: ExamPart }) {
  return (
    <>
      <PartHeading title={part.title_de || part.title} />
      <InstructionBand text={part.instructions_de} />
      {part.stimulus.title ? (
        <h2 className="exam-lead mb-1 text-center font-bold" dir="ltr">
          {part.stimulus.title}
        </h2>
      ) : null}
      {part.stimulus.subtitle ? (
        <p className="mb-5 text-center text-sm font-semibold" dir="ltr">
          {part.stimulus.subtitle}
        </p>
      ) : null}
      <StimulusIntro text={part.stimulus.intro} />
      <div className="space-y-4">
        {part.stimulus.blocks.map((block, index, blocks) =>
          block.kind === "row" ? (
            // A run of rows is one board (a store directory, a timetable); it is
            // drawn once, at its first row.
            blocks[index - 1]?.kind === "row" ? null : (
              <DirectoryBoard key={index} rows={blocks.slice(index)} />
            )
          ) : block.kind === "statement" ? (
            // reader comments and posts sit in their own boxes, signed
            <article
              key={index}
              className="rounded-md border p-4"
              style={{ borderColor: "var(--exam-line)" }}
              dir="ltr"
            >
              <BlockImage src={block.image} alt={block.title || block.label} />
              <p className="exam-body whitespace-pre-line">
                {block.label ? <b className="me-2">{block.label}</b> : null}
                {block.text}
              </p>
              {block.title || block.author ? (
                <p className="mt-2 text-end text-xs italic" style={{ color: "var(--exam-muted)" }}>
                  {block.title || block.author}
                </p>
              ) : null}
            </article>
          ) : (
            <div key={index} dir="ltr">
              <BlockImage src={block.image} alt={block.title || block.label} />
              {block.label && block.label.length > 3 ? (
                <p className="mb-1 text-xs font-bold tracking-wide" style={{ color: "var(--exam-muted)" }}>
                  {block.label}
                </p>
              ) : null}
              {block.title ? <p className="exam-body mb-1 font-bold">{block.title}</p> : null}
              <p className="exam-body text-justify whitespace-pre-line">
                {block.label && block.label.length <= 3 ? <b className="me-2">{block.label}</b> : null}
                {block.text}
              </p>
            </div>
          ),
        )}
      </div>
    </>
  );
}

/** Label-and-text rows read as a sign board: floor on the left, what's there on the right. */
function DirectoryBoard({ rows }: { rows: ExamPart["stimulus"]["blocks"] }) {
  const end = rows.findIndex((block) => block.kind !== "row");
  const run = end === -1 ? rows : rows.slice(0, end);
  return (
    <table className="exam-body w-full border-collapse" dir="ltr" style={{ border: "2px solid var(--exam-band)" }}>
      <tbody>
        {run.map((row, index) => (
          <tr key={index} className="border-b last:border-0" style={{ borderColor: "var(--exam-line)" }}>
            <th
              scope="row"
              className="w-24 px-3 py-2.5 text-start align-top font-bold whitespace-nowrap text-white"
              style={{ background: "var(--exam-band)" }}
            >
              {row.label}
            </th>
            <td className="px-3 py-2.5 align-top">
              {row.title ? <b className="me-1">{row.title}</b> : null}
              {row.text}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

/* ------------------------------------------- Lesen 4: opinions in boxes a–h */

export function StatementBoxes({ part }: { part: ExamPart }) {
  return (
    <>
      <PartHeading title={part.title_de || part.title} />
      <InstructionBand text={part.instructions_de} />
      <StimulusIntro text={part.stimulus.intro} />
      <div className="grid gap-4 sm:grid-cols-2">
        {part.stimulus.blocks.map((block) => (
          <article
            key={block.label}
            className="rounded-md border p-4"
            style={{ borderColor: "var(--exam-line)" }}
            dir="ltr"
          >
            <BlockImage src={block.image} alt={block.title || block.label} />
            {block.title ? (
              <p className="exam-body mb-1 font-bold">{block.title}</p>
            ) : null}
            <p className="exam-body">
              {block.label ? <b className="me-2 text-base">{block.label}</b> : null}
              {block.text}
            </p>
            {block.author ? (
              <p className="mt-3 text-end text-xs italic" style={{ color: "var(--exam-muted)" }}>
                {block.author}
              </p>
            ) : null}
          </article>
        ))}
      </div>
    </>
  );
}

/* ----------------------------------------- Hören: tracks with ring player */

export function ListeningStimulus({
  part,
  trackIndex,
  onPlay,
}: {
  part: ExamPart;
  trackIndex: number;
  onPlay?: () => void;
}) {
  const track = part.audio[trackIndex];
  const pictures = part.stimulus.blocks.filter((block) => block.kind === "picture");
  return (
    <>
      {/* The listening screens open straight with the instruction band. */}
      <InstructionBand text={part.instructions_de} />
      <StimulusIntro text={part.stimulus.intro} />
      {track?.url ? (
        <AudioRing
          key={track.url}
          track={track}
          onPlay={onPlay}
          prompt={pictures.length ? "Sehen Sie sich jetzt die Bilder an." : undefined}
        />
      ) : track ? (
        <p className="exam-body mt-6 text-center" dir="ltr" style={{ color: "var(--exam-muted)" }}>
          Für diesen Teil ist noch keine Aufnahme vorhanden.
        </p>
      ) : null}
      {pictures.length ? <PictureGallery part={part} pictures={pictures} /> : null}
    </>
  );
}

/**
 * The lettered pictures a matching task answers with (A2 Hören 2: which
 * picture goes with which day). The example's letter is struck through, as on
 * the paper, because it can't be chosen again.
 */
function PictureGallery({
  part,
  pictures,
}: {
  part: ExamPart;
  pictures: ExamPart["stimulus"]["blocks"];
}) {
  return (
    <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-3" dir="ltr">
      {pictures.map((block) => {
        const used = block.label === part.example?.answer;
        return (
          <figure
            key={block.label}
            className="relative overflow-hidden rounded-sm border bg-white"
            style={{ borderColor: "var(--exam-line)" }}
          >
            <span
              className={cn(
                "absolute top-1.5 left-1.5 grid size-6 place-items-center border bg-white text-xs font-bold",
                used && "line-through",
              )}
              style={{ borderColor: "var(--exam-line)", color: used ? "var(--exam-muted)" : undefined }}
            >
              {block.label}
            </span>
            {block.image ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={mediaUrl(block.image)}
                alt={block.title || block.label}
                loading="lazy"
                className={cn("aspect-[12/11] w-full object-contain", used && "opacity-45")}
              />
            ) : (
              <div className="grid aspect-[12/11] place-items-center text-xs" style={{ color: "var(--exam-muted)" }}>
                {block.title || "Bild fehlt"}
              </div>
            )}
          </figure>
        );
      })}
    </div>
  );
}

/* -------------------------------------------------- Schreiben: writing task */

export function WritingStimulus({ part }: { part: ExamPart }) {
  return (
    <>
      <PartHeading title={part.title_de || part.title} />
      {part.stimulus.image ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={mediaUrl(part.stimulus.image)}
          alt=""
          className="mx-auto mb-6 max-h-72 w-auto"
          onError={(event) => {
            event.currentTarget.style.display = "none";
          }}
        />
      ) : null}
      <p className="exam-body mb-4" dir="ltr">
        {part.instructions_de}
      </p>
      {part.stimulus.intro ? (
        <p className="exam-body mb-4" dir="ltr">
          {part.stimulus.intro}
        </p>
      ) : null}
      {part.stimulus.blocks.some((block) => block.kind !== "statement") ? (
        <ul className="mb-5 space-y-1.5 ps-6" dir="ltr">
          {part.stimulus.blocks
            .filter((block) => block.kind !== "statement")
            .map((block, index) => (
              <li key={index} className="exam-body list-disc">
                {block.text}
              </li>
            ))}
        </ul>
      ) : null}
      {part.stimulus.blocks
        .filter((block) => block.kind === "statement")
        .map((block, index) => (
          // a guestbook post or message the learner is answering
          <blockquote
            key={index}
            className="mb-4 rounded-md border p-4"
            style={{ borderColor: "var(--exam-line)", background: "var(--exam-page)" }}
            dir="ltr"
          >
            <p className="exam-body whitespace-pre-line">{block.text}</p>
            {block.title ? (
              <p className="mt-2 text-end text-xs italic" style={{ color: "var(--exam-muted)" }}>
                {block.title}
              </p>
            ) : null}
          </blockquote>
        ))}
    </>
  );
}

export function WritingAnswer({
  part,
  answers,
  setAnswer,
}: {
  part: ExamPart;
  answers: Answers;
  setAnswer: (key: string, value: string) => void;
}) {
  const item = part.items[0];
  const value = answers[item.key] ?? "";
  const words = value.trim() ? value.trim().split(/\s+/).length : 0;

  return (
    <div>
      <p className="exam-lead mb-4 font-bold" dir="ltr">
        {part.number}. Schreiben Sie Ihren Text in dieses Feld.
      </p>
      <textarea
        value={value}
        onChange={(event) => setAnswer(item.key, event.target.value)}
        dir="ltr"
        lang="de"
        spellCheck={false}
        className={cn(
          "exam-body h-[26rem] w-full resize-y border p-4 outline-none",
          "focus:border-[color:var(--exam-radio)]",
        )}
        style={{ borderColor: "var(--exam-line)" }}
      />
      <p className="mt-2 text-xs" dir="ltr">
        Wortanzahl: {words}
        {part.min_words ? (
          <span style={{ color: words >= part.min_words ? "var(--exam-green-dark)" : "var(--exam-muted)" }}>
            {" "}· mindestens {part.min_words}
          </span>
        ) : null}
      </p>
    </div>
  );
}
