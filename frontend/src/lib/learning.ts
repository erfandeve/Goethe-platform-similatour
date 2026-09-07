export type SpeakingState =
  | "VIDEO_PLAYING"
  | "VIDEO_PAUSED"
  | "VIDEO_COMPLETED"
  | "COUNTDOWN"
  | "READY_TO_SPEAK"
  | "RECORDING"
  | "UPLOADING"
  | "TRANSCRIBING"
  | "ANALYZING"
  | "SHOWING_RESULT"
  | "NEXT_VIDEO_COUNTDOWN"
  | "LOADING_NEXT_VIDEO"
  | "PART_COMPLETED"
  | "COURSE_COMPLETED"
  | "ERROR";

export interface LessonQuestion {
  prompt_de: string;
  prompt: string;
  hint: string;
  expected_points: string[];
  grammar_topics: string[];
  vocabulary: string[];
  min_words: number;
}

export interface VideoProgressState {
  position_seconds: number;
  completed: boolean;
  speaking_done: boolean;
  best_score: number;
  last_score: number;
  attempts: number;
  updated_at: string | null;
}

export interface LessonVideo {
  id: string;
  slug: string;
  order: number;
  title: string;
  title_de: string;
  scene_label: string;
  description: string;
  video_url: string;
  poster_url: string;
  duration_seconds: number;
  cefr_level: string;
  has_speaking_task: boolean;
  question: LessonQuestion | null;
  progress: VideoProgressState | null;
}

export interface LessonPart {
  id: string;
  slug: string;
  order: number;
  title: string;
  title_de: string;
  description: string;
  videos: LessonVideo[];
}

export interface Classroom {
  course: { id: string; slug: string; title: string; level: string; accent: string };
  parts: LessonPart[];
  stats: {
    total_videos: number;
    completed_videos: number;
    speaking_attempts: number;
    average_score: number;
    percent: number;
  };
}

export interface AnalysisMistake {
  original: string;
  correction: string;
  type: string;
  explanation: string;
}

export interface Analysis {
  overall_score: number;
  cefr_estimate: string;
  is_relevant: boolean;
  summary: string;
  corrected_answer: string;
  mistakes: AnalysisMistake[];
  categories: Record<string, number>;
  positive_feedback: string[];
  improvement_tips: string[];
  next_action: "retry" | "continue";
}

export interface SpeakingAttempt {
  id: string;
  video_id: string | null;
  question_de: string;
  transcript: string;
  score: number;
  cefr_estimate: string;
  processing_status: string;
  created_at: string;
  analysis: Analysis | null;
}

/** Flattens the parts into the running order the player walks through. */
export function flattenVideos(parts: LessonPart[]) {
  return parts.flatMap((part) => part.videos.map((video) => ({ part, video })));
}
