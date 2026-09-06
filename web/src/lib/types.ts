export type Level = "A1" | "A2" | "B1" | "B2" | "C1" | "C2";
export type Skill = "listening" | "reading" | "writing" | "speaking" | "grammar";
export type CourseFormat = "self_paced" | "live" | "hybrid" | "private";

export interface Category {
  id: string;
  slug: string;
  kind: "course" | "podcast";
  title: string;
  description: string;
  icon: string;
  color: string;
  count?: number;
}

export interface Instructor {
  id: string;
  slug: string;
  name: string;
  avatar: string;
  headline: string;
  rating: number;
  students: number;
  bio?: string;
  languages?: string[];
}

export interface CourseCard {
  id: string;
  slug: string;
  title: string;
  subtitle: string;
  cover: string;
  accent: string;
  level: Level;
  language: string;
  format: CourseFormat;
  price: number;
  discount_price: number;
  effective_price: number;
  duration_minutes: number;
  lessons_count: number;
  sessions_count: number;
  rating: number;
  reviews_count: number;
  students_count: number;
  is_featured: boolean;
  is_bestseller: boolean;
  tags: string[];
  category: Category | null;
  instructor: Instructor | null;
}

export interface Lesson {
  title: string;
  duration_minutes: number;
  kind: "video" | "audio" | "quiz" | "live" | "pdf";
  is_preview: boolean;
}

export interface CourseDetail extends CourseCard {
  description: string;
  trailer_url: string;
  starts_at: string | null;
  created_at: string | null;
  outcomes: string[];
  requirements: string[];
  curriculum: { title: string; lessons: Lesson[] }[];
  reviews: { id: string; author_name: string; rating: number; body: string; created_at: string }[];
  related: CourseCard[];
  is_enrolled?: boolean;
}

export interface ExamCard {
  id: string;
  slug: string;
  title: string;
  subtitle: string;
  level: Level;
  kind: "simulator" | "frequent";
  language: string;
  exam_board: string;
  cover: string;
  accent: string;
  badge: string;
  duration_minutes: number;
  questions_count: number;
  sections_count: number;
  skills: Skill[];
  price: number;
  discount_price: number;
  effective_price: number;
  is_free: boolean;
  pass_score: number;
  rating: number;
  attempts_count: number;
  is_featured: boolean;
}

export interface ExamQuestion {
  key: string;
  prompt: string;
  passage: string;
  audio_url: string;
  image_url: string;
  kind: "single" | "multiple" | "true_false" | "gap" | "essay" | "audio_answer";
  points: number;
  options: string[];
}

export interface ExamSection {
  index: number;
  skill: Skill;
  title: string;
  instructions: string;
  duration_minutes: number;
  questions_count: number;
  questions?: ExamQuestion[];
}

export interface ExamModuleSummary {
  skill: "lesen" | "hoeren" | "schreiben" | "sprechen";
  title: string;
  intro: string;
  duration_minutes: number;
  max_points: number;
  parts_count: number;
  items_count: number;
}

export interface ExamSitting {
  id: string;
  code: string;
  label: string;
  description: string;
  order: number;
  extra_price: number;
  items_count: number;
  modules: string[];
  owned: boolean;
}

export interface ExamDetail extends ExamCard {
  description: string;
  highlights: string[];
  max_score: number;
  sections: ExamSection[];
  /** Present on exams built from a Goethe model set. */
  format?: "goethe" | "simple";
  modules?: ExamModuleSummary[];
  has_access: boolean;
  last_attempt: Attempt | null;
  /** Sittings the buyer chooses between; the first is covered by the price. */
  codes?: ExamSitting[];
  base_price?: number;
}

export interface Attempt {
  id: string;
  status: "in_progress" | "finished" | "abandoned";
  score: number;
  raw_score: number;
  max_score: number;
  correct_count: number;
  passed: boolean;
  cefr_estimate: string;
  started_at: string;
  finished_at: string | null;
  duration_seconds: number;
  section_results: { skill: Skill; score: number; max_score: number }[];
  exam: ExamCard | null;
  review?: AttemptReviewRow[];
}

export interface AttemptReviewRow {
  key: string;
  skill: Skill;
  prompt: string;
  options: string[];
  kind: ExamQuestion["kind"];
  given: number | number[] | null;
  correct_index: number;
  correct_indices: number[];
  explanation: string;
  is_correct: boolean | null;
}

export interface Podcast {
  id: string;
  slug: string;
  title: string;
  tagline: string;
  cover: string;
  accent: string;
  host_name: string;
  host_avatar: string;
  level: Level;
  language: string;
  tags: string[];
  rating: number;
  plays: number;
  episodes_count: number;
  is_featured: boolean;
  category: Category | null;
  description?: string;
  episodes?: Episode[];
}

export interface Episode {
  id: string;
  slug: string;
  number: number;
  title: string;
  description: string;
  cover: string;
  duration_seconds: number;
  level: Level;
  plays: number;
  is_premium: boolean;
  published_at: string;
  podcast: { slug: string; title: string; accent: string; host_name: string } | null;
  position_seconds?: number;
}

export interface EpisodeDetail extends Episode {
  audio_url: string;
  transcript: { start: number; end: number; speaker: string; text: string; translation: string }[];
  vocabulary: { term: string; article: string; meaning: string; example: string }[];
  progress: { position_seconds: number; completed: boolean } | null;
  bookmarked: boolean;
  more_episodes: Episode[];
}

export interface User {
  id: string;
  email: string;
  phone: string;
  first_name: string;
  last_name: string;
  full_name: string;
  avatar: string;
  bio: string;
  birth_date: string;
  country: string;
  city: string;
  native_language: string;
  preferred_locale: "fa" | "en" | "de";
  current_level: Level;
  target_level: Level;
  wallet_balance: number;
  profile_completion: number;
  email_verified: boolean;
  is_staff?: boolean;
  prefs: { email: boolean; sms: boolean; product_news: boolean };
  created_at: string;
  last_login: string | null;
}

export interface Enrollment {
  id: string;
  progress: number;
  completed_lessons: number;
  minutes_spent: number;
  certificate_url: string;
  enrolled_at: string;
  last_activity: string;
  course: CourseCard | null;
}

export interface CartState {
  items: {
    item_type: "course" | "exam";
    item_id: string;
    slug: string;
    title: string;
    cover: string;
    price: number;
    quantity: number;
  }[];
  count: number;
  subtotal: number;
  discount: number;
  total: number;
  coupon: string;
}

export interface Notification {
  id: string;
  title: string;
  body: string;
  kind: "system" | "course" | "exam" | "payment" | "podcast";
  link: string;
  is_read: boolean;
  created_at: string;
}

export interface Message {
  id: string;
  sender_name: string;
  sender_role: "staff" | "teacher" | "student";
  sender_avatar: string;
  subject: string;
  body: string;
  thread: string;
  is_read: boolean;
  created_at: string;
}

export interface WalletTransaction {
  id: string;
  amount: number;
  balance_after: number;
  kind: "topup" | "purchase" | "refund" | "bonus" | "withdraw";
  title: string;
  reference: string;
  created_at: string;
}

export interface Order {
  id: string;
  code: string;
  items: { item_type: string; slug: string; title: string; price: number; quantity: number }[];
  subtotal: number;
  discount: number;
  total: number;
  status: "pending" | "paid" | "failed" | "refunded";
  payment_method: "wallet" | "gateway";
  created_at: string;
  paid_at: string | null;
}

export interface HomePayload {
  featured_courses: CourseCard[];
  newest_courses: CourseCard[];
  simulators: ExamCard[];
  frequent_exams: ExamCard[];
  podcasts: Podcast[];
  latest_episodes: Episode[];
  categories: Category[];
  instructors: Instructor[];
  stats: { students: number; courses: number; exams: number; episodes: number };
}

export interface Paginated<T> {
  results: T[];
  meta: { page: number; page_size: number; total: number; pages: number };
}
