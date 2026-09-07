/** Article bodies are structured blocks, not HTML strings: the renderer keeps
 *  full control of the semantics search engines read (h2/h3, ol/ul, table). */
export type Block =
  | { type: "p"; text: string }
  | { type: "h2"; text: string; id: string }
  | { type: "h3"; text: string }
  | { type: "ul"; items: string[] }
  | { type: "ol"; items: string[] }
  | { type: "quote"; text: string }
  | { type: "table"; caption?: string; head: string[]; rows: string[][] }
  | { type: "callout"; title: string; text: string }
  | { type: "cta"; title: string; text: string; href: string; label: string };

export interface Faq {
  q: string;
  a: string;
}

export interface Article {
  slug: string;
  /** The language the body is written in. */
  lang: "fa";
  title: string;
  /** <title> — kept under ~60 characters so Google does not truncate it. */
  metaTitle: string;
  /** <meta name="description"> — 150–160 characters. */
  metaDescription: string;
  /** The phrase this page is meant to rank for. */
  focusKeyword: string;
  keywords: string[];
  excerpt: string;
  published: string;
  updated: string;
  readingMinutes: number;
  words: number;
  cover: string;
  body: Block[];
  faq: Faq[];
  related: string[];
}

/** Headings become the table of contents and the in-page anchor links. */
export function tableOfContents(body: Block[]) {
  return body.filter((b): b is Extract<Block, { type: "h2" }> => b.type === "h2");
}
