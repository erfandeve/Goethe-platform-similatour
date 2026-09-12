export type Answers = Record<string, string>;

export interface ExamOption {
  key: string;
  label: string;
  text?: string;
  author?: string;
  image?: string;
}

export interface ExamItem {
  key: string;
  number: number;
  prompt: string;
  points: number;
  audio_index: number | null;
  options: ExamOption[];
}

export interface AudioTrack {
  index: number;
  label: string;
  url: string;
  plays: number;
  pre_read_seconds: number;
  covers: number[];
}

export interface ExamPart {
  index: number;
  number: number;
  type:
    | "match_person"
    | "gap_drag"
    | "mcq"
    | "match_heading"
    | "match_paragraph"
    | "listening_mixed"
    | "writing";
  title: string;
  title_de: string;
  instructions: string;
  instructions_de: string;
  work_minutes: number;
  stimulus: {
    title: string;
    subtitle: string;
    image: string;
    intro: string;
    blocks: { kind: string; label: string; title: string; text: string; author: string; image: string }[];
  };
  options: ExamOption[];
  audio: AudioTrack[];
  example: { prompt: string; answer: string };
  min_words: number | null;
  items: ExamItem[];
}

export interface ExamModule {
  skill: "lesen" | "hoeren" | "schreiben" | "sprechen";
  title: string;
  intro: string;
  duration_minutes: number;
  max_points: number;
  parts_count: number;
  items_count: number;
  parts: ExamPart[];
}

/** One screen of the runner: a Teil, or one audio track inside Hören 1. */
export interface Page {
  part: ExamPart;
  trackIndex: number | null;
  items: ExamItem[];
}

export function buildPages(module: ExamModule): Page[] {
  const pages: Page[] = [];
  for (const part of module.parts) {
    // Any Teil with recordings is paged one recording at a time, whatever its
    // task type: A2 Hören 1 and 3 are plain a/b/c items over five tracks.
    if (part.audio.length) {
      // An item belongs to the track that names it in `covers`, then to its own
      // audio_index, and otherwise to the first track. Without that fallback a
      // part whose items carry no index renders every page empty.
      const trackOf = (item: ExamItem) => {
        const byCover = part.audio.findIndex((track) => (track.covers ?? []).includes(item.number));
        if (byCover >= 0) return byCover;
        if (item.audio_index != null && part.audio[item.audio_index]) return item.audio_index;
        return 0;
      };
      part.audio.forEach((_track, trackIndex) => {
        pages.push({
          part,
          trackIndex,
          items: part.items.filter((item) => trackOf(item) === trackIndex),
        });
      });
      continue;
    }
    pages.push({ part, trackIndex: part.audio.length ? 0 : null, items: part.items });
  }
  return pages;
}
