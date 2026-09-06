"use client";

import { useMemo, useState, type ReactNode } from "react";

import { cn } from "@/lib/utils";

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
function Choice({
  name,
  checked,
  onChange,
  children,
}: {
  name: string;
  checked: boolean;
  onChange: () => void;
  children: ReactNode;
}) {
  return (
    <label className="flex cursor-pointer items-start gap-3 py-1.5" dir="ltr">
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
      <span className="exam-body leading-snug">{children}</span>
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
  options: { key: string; label: string; text?: string; author?: string }[];
  showNumber?: boolean;
}) {
  return (
    <div className="border-b py-5 first:pt-0 last:border-0" style={{ borderColor: "var(--exam-line)" }}>
      <p className="exam-lead mb-3 font-bold" dir="ltr">
        {showNumber ? `${item.number}. ` : ""}
        {item.prompt}
      </p>
      <div className="ps-1">
        {options.map((option) => (
          <Choice
            key={option.key}
            name={item.key}
            checked={answers[item.key] === option.key}
            onChange={() => setAnswer(item.key, option.key)}
          >
            {option.text ? (
              <>
                <b className="me-1.5">{option.key}</b>
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
      <div className="space-y-4">
        {part.stimulus.blocks.map((block, index) => (
          <p key={index} className="exam-body text-justify" dir="ltr">
            {block.label ? <b className="me-2">{block.label}</b> : null}
            {block.text}
          </p>
        ))}
      </div>
    </>
  );
}

/* ------------------------------------------- Lesen 4: opinions in boxes a–h */

export function StatementBoxes({ part }: { part: ExamPart }) {
  return (
    <>
      <PartHeading title={part.title_de || part.title} />
      <InstructionBand text={part.instructions_de} />
      <div className="grid gap-4 sm:grid-cols-2">
        {part.stimulus.blocks.map((block) => (
          <article
            key={block.label}
            className="rounded-md border p-4"
            style={{ borderColor: "var(--exam-line)" }}
            dir="ltr"
          >
            <p className="exam-body">
              <b className="me-2 text-base">{block.label}</b>
              {block.text}
            </p>
            <p className="mt-3 text-end text-xs italic" style={{ color: "var(--exam-muted)" }}>
              {block.author}
            </p>
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
  return (
    <>
      {/* The listening screens open straight with the instruction band. */}
      <InstructionBand text={part.instructions_de} />
      {track ? <AudioRing key={track.url} track={track} onPlay={onPlay} /> : null}
    </>
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
          src={part.stimulus.image}
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
      <ul className="mb-5 space-y-1.5 ps-6" dir="ltr">
        {part.stimulus.blocks.map((block, index) => (
          <li key={index} className="exam-body list-disc">
            {block.text}
          </li>
        ))}
      </ul>
      <p className="exam-body" dir="ltr">
        {part.stimulus.intro}
      </p>
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
