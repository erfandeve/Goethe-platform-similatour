export interface Translated {
  fa: string;
  en: string;
  de: string;
}

export interface AdminCategory {
  id: string;
  slug: string;
  kind: "course" | "podcast";
  title: Translated;
  description: Translated;
  icon: string;
  color: string;
  order: number;
  course_count: number;
}

export interface AdminInstructor {
  id: string;
  slug: string;
  name: string;
  headline: Translated;
  avatar: string;
  is_featured: boolean;
}

export interface AdminCourse {
  id: string;
  slug: string;
  title: Translated;
  subtitle: Translated;
  description?: Translated;
  level: string;
  language: string;
  format: string;
  accent: string;
  cover: string;
  price: number;
  discount_price: number;
  duration_minutes: number;
  students_count: number;
  is_published: boolean;
  is_featured: boolean;
  is_bestseller: boolean;
  category: string | null;
  category_slug: string;
  instructor: string | null;
  parts_count: number;
  videos_count: number;
  tags?: string[];
  created_at: string | null;
}

export interface AdminQuestion {
  prompt_de: string;
  prompt: Translated;
  hint: Translated;
  expected_points: string[];
  grammar_topics: string[];
  vocabulary: string[];
  min_words: number;
}

export interface AdminVideo {
  id: string;
  slug: string;
  order: number;
  title: Translated;
  title_de: string;
  scene_label: string;
  description: Translated;
  video_url: string;
  poster_url: string;
  duration_seconds: number;
  cefr_level: string;
  is_published: boolean;
  has_speaking_task: boolean;
  question: AdminQuestion | null;
  part: string | null;
}

export interface AdminPart {
  id: string;
  slug: string;
  order: number;
  title: Translated;
  title_de: string;
  description: Translated;
  is_published: boolean;
  course: string | null;
  videos: AdminVideo[];
  videos_count: number;
}

export const EMPTY_TRANSLATED: Translated = { fa: "", en: "", de: "" };

export const LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"] as const;

export const emptyQuestion = (): AdminQuestion => ({
  prompt_de: "",
  prompt: { ...EMPTY_TRANSLATED },
  hint: { ...EMPTY_TRANSLATED },
  expected_points: [],
  grammar_topics: [],
  vocabulary: [],
  min_words: 2,
});

/** Textarea ⇄ list, so staff can type one item per line. */
export const linesToList = (value: string) =>
  value.split("\n").map((line) => line.trim()).filter(Boolean);

export const listToLines = (value: string[] | undefined) => (value ?? []).join("\n");

// --- exams -------------------------------------------------------------------

export interface ExamOption {
  key: string;
  label: string;
  text: string;
  author?: string;
  /** A1 tasks answer with a picture as often as with a sentence. */
  image?: string;
}

export interface ExamItem {
  number: number;
  prompt: string;
  answer: string;
  points: number;
  audio_index: number | null;
  explanation: Translated;
  options: ExamOption[];
}

export interface ExamPart {
  index: number;
  number: number;
  type: string;
  title: Translated;
  instructions: Translated;
  work_minutes: number;
  stimulus_title: string;
  stimulus_subtitle: string;
  stimulus_intro: string;
  stimulus_image: string;
  blocks: {
    kind: string;
    label: string;
    title: string;
    text: string;
    author: string;
    image: string;
  }[];
  options: ExamOption[];
  audio: {
    label: string;
    url: string;
    plays: number;
    pre_read_seconds: number;
    covers: number[];
  }[];
  items: ExamItem[];
  example_prompt: string;
  example_answer: string;
  min_words: number | null;
}

export interface ExamModule {
  index: number;
  skill: "lesen" | "hoeren" | "schreiben" | "sprechen";
  title: Translated;
  intro: Translated;
  duration_minutes: number;
  max_points: number;
  parts: ExamPart[];
}

export interface AdminExam {
  id: string;
  slug: string;
  title: Translated;
  subtitle: Translated;
  description?: Translated;
  level: string;
  kind: "simulator" | "frequent";
  exam_board: string;
  accent: string;
  badge: string;
  cover: string;
  duration_minutes: number;
  pass_score: number;
  price: number;
  discount_price: number;
  is_published: boolean;
  is_featured: boolean;
  questions_count: number;
  modules_count: number;
  attempts_count: number;
  modules?: ExamModule[];
}

export const MODULE_LABELS: Record<string, string> = {
  lesen: "Lesen — درک مطلب",
  hoeren: "Hören — شنیداری",
  schreiben: "Schreiben — نگارش",
  sprechen: "Sprechen — گفتاری",
};

export const PART_TYPE_LABELS: Record<string, string> = {
  mcq: "چندگزینه‌ای",
  match_person: "تطبیق با اشخاص",
  gap_drag: "جای خالی (کشیدنی)",
  match_heading: "تطبیق عنوان",
  match_paragraph: "تطبیق بند",
  listening_mixed: "شنیداری ترکیبی",
  writing: "نگارش",
};

// --- podcasts, exam codes and plans ------------------------------------------

export interface AdminPodcast {
  id: string;
  slug: string;
  title: Translated;
  tagline: Translated;
  description: Translated;
  cover: string;
  accent: string;
  host_name: string;
  level: string;
  language: string;
  tags: string[];
  category: string | null;
  is_published: boolean;
  is_featured: boolean;
  plays: number;
  episodes_count: number;
}

export interface AdminEpisode {
  id: string;
  slug: string;
  number: number;
  title: Translated;
  description: Translated;
  audio_url: string;
  cover: string;
  duration_seconds: number;
  level: string;
  is_premium: boolean;
  is_published: boolean;
  podcast: string | null;
  transcript: {
    start: number;
    end: number;
    speaker: string;
    text: string;
    translation: Translated;
  }[];
  vocabulary: { term: string; article: string; meaning: Translated; example: string }[];
}

export interface AdminExamCode {
  id: string;
  code: string;
  label: Translated;
  description: Translated;
  order: number;
  extra_price: number;
  is_published: boolean;
  items_count: number;
  modules: ExamModule[];
  exam: string | null;
}

export interface AdminPlan {
  id: string;
  slug: string;
  title: Translated;
  description: Translated;
  highlights: Translated[];
  perks: string[];
  price: number;
  duration_days: number;
  accent: string;
  badge: string;
  order: number;
  is_published: boolean;
  is_featured: boolean;
  subscribers: number;
}

export const PERK_LABELS: Record<string, string> = {
  exam_codes: "همه کدهای آزمون",
  exams: "همه آزمون‌ها",
  courses: "همه دوره‌ها",
  speaking: "مکالمه با هوش مصنوعی",
  podcasts: "پادکست‌های ویژه",
};
