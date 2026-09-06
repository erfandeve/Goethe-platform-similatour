# AI German Speaking Teacher

Video lessons paired with a spoken answer that an AI teacher transcribes, grades
and corrects. Built into the existing GOTEH platform — it reuses the current
accounts, course catalogue and purchase/enrolment logic rather than replacing
any of it.

---

## 1. Architecture

```
Browser (Next.js)                 Django                        OpenAI
─────────────────                 ──────                        ──────
MediaRecorder
   │ audio blob
   ├─ POST /api/ai/transcribe ──► POST /api/ai/transcribe/
   │  (Next route, multipart)        │
   │                                 ├─ POST https://api.openai.com/v1/audio/transcriptions
   │                                 │       model: gpt-transcribe
   │  ◄── { transcript } ────────────┘
   │
   ├─ POST /api/proxy/ai/analyze ─► POST /api/ai/analyze/
   │  (Next JSON proxy)              │
   │                                 ├─ POST https://api.openai.com/v1/responses
   │                                 │       model: gpt-5.4-mini
   │                                 │       strict json_schema output
   │  ◄── { attempt, analysis } ─────┘
   ▼
Result panel: score · corrections · grammar notes · feedback
```

**The browser never talks to OpenAI and never sees the API key.** Both Next.js
route handlers attach the learner's JWT from an httpOnly cookie; the OpenAI key
exists only in `api/.env`, read through `django.conf.settings`.

### OpenAI endpoints used

| Purpose | Endpoint | Model (configurable) |
| --- | --- | --- |
| Speech to text | `POST https://api.openai.com/v1/audio/transcriptions` | `gpt-transcribe` |
| Answer analysis | `POST https://api.openai.com/v1/responses` | `gpt-5.4-mini` |

Both were verified against the live API during implementation.

---

## 2. Learning flow

1. Learner opens `/[locale]/learn/<course-slug>` (redirects to the sales page if
   they have no enrolment).
2. The scene plays. Position is saved every five seconds and on completion.
3. On `ended`:
   * watch-only scene → 3-second countdown → next scene;
   * scene with a question → 3-second countdown → microphone unlocks.
4. The learner presses record, speaks, presses stop. Recording auto-stops at
   `MAX_AUDIO_DURATION`.
5. Upload → transcription → analysis → result.
6. Result offers **Retry**, **Continue** and **Replay video**. Continue runs a
   3-second countdown and loads the next scene.
7. Finishing a part shows **Teil abgeschlossen** with the part's statistics;
   finishing the course shows the completion screen.

### Front-end state machine

`VIDEO_PLAYING → VIDEO_PAUSED → VIDEO_COMPLETED → COUNTDOWN → READY_TO_SPEAK →
RECORDING → UPLOADING → TRANSCRIBING → ANALYZING → SHOWING_RESULT →
NEXT_VIDEO_COUNTDOWN → LOADING_NEXT_VIDEO → PART_COMPLETED → COURSE_COMPLETED`,
plus `ERROR`. One state variable drives the panel, so the UI cannot show two
moods at once.

---

## 3. Database (MongoEngine — no migrations)

Collections are created on first write. Existing `users`, `courses` and
`enrollments` are reused untouched.

| Document | Collection | Purpose |
| --- | --- | --- |
| `Part` | `parts` | ordered chapter of a course |
| `LessonVideo` | `lesson_videos` | one scene + its embedded `Question` |
| `VideoProgress` | `video_progress` | position, completion, attempts, best score |
| `SpeakingAttempt` | `speaking_attempts` | one spoken answer and its transcript |
| `AIAnalysis` | `ai_analyses` | the teacher's structured verdict |

`Question` is embedded on the video: `prompt_de`, localized `prompt`, `hint`,
`expected_points`, `grammar_topics`, `vocabulary`, `min_words`.

Scenes 1–3 of the seeded course carry no question and are watch-only; the
speaking task starts at scene 4, as specified.

---

## 4. API endpoints

All require a signed-in learner **and** an enrolment in the course that owns the
lesson. Ids sent by the client are never trusted: the course is re-derived from
the video, and a mismatched `course_id`/`part_id` is rejected with 403.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/learning/<course-slug>/` | whole classroom: parts, videos, progress, stats |
| GET | `/api/courses/<course_id>/parts/` | parts of a course |
| GET | `/api/parts/<part_id>/videos/` | videos of a part |
| GET | `/api/progress/` | the learner's recent progress rows |
| POST | `/api/progress/video/` | save position / completion |
| GET | `/api/speaking-attempts/` | attempt history |
| GET | `/api/speaking-attempts/<video_id>/` | attempts for one lesson |
| POST | `/api/ai/transcribe/` | multipart audio → German transcript |
| POST | `/api/ai/analyze/` | transcript + lesson context → analysis |

### `POST /api/ai/transcribe/`

Request `multipart/form-data`: `audio` (required), `video_id`, `language`
(default `de`).

```json
{ "success": true, "transcript": "Ich habe ein Visum.", "audio_path": "", "is_empty": false }
```

Errors: `{"success": false, "error": "Unable to transcribe audio."}`

### `POST /api/ai/analyze/`

```json
{ "transcript": "...", "video_id": "...", "course_id": "...", "part_id": "...", "audio_seconds": 6 }
```

```json
{
  "success": true,
  "attempt": {
    "id": "...", "transcript": "...", "score": 96, "cefr_estimate": "A2",
    "processing_status": "completed",
    "analysis": {
      "overall_score": 96, "cefr_estimate": "A2", "is_relevant": true,
      "summary": "...", "corrected_answer": "...",
      "mistakes": [{"original": "...", "correction": "...", "type": "verb", "explanation": "..."}],
      "categories": {"grammar": 100, "vocabulary": 95, "sentence_structure": 98,
                     "word_order": 100, "naturalness": 100, "relevance": 100},
      "positive_feedback": ["..."], "improvement_tips": ["..."], "next_action": "continue"
    }
  }
}
```

---

## 5. The teacher prompt

Lives in `api/apps/learning/services/prompts.py`, versioned by `PROMPT_VERSION`.
It instructs the model to:

* grade **relative to the CEFR level** of the lesson;
* treat a correct alternative phrasing as **not a mistake**, separating real
  grammar errors from stylistic or vocabulary suggestions;
* judge short answers on content, not length alone;
* flag an off-topic answer with `is_relevant: false` but still grade the language;
* answer in German, constructively, with at most five key mistakes.

Output is forced through a **strict `json_schema`** on the Responses API.

---

## 6. Validation and error handling

Nothing from the model reaches the browser unchecked
(`services/speaking_teacher.py`):

* the payload is re-parsed and re-typed field by field;
* scores are clamped to 0–100 and mistakes capped;
* category scores are rescaled when the model answers on a 0–10 scale — a real
  failure observed in testing that the JSON schema cannot prevent;
* a malformed response is retried up to `AI_MAX_RETRIES`, then returned as a
  controlled error.

Handled cases: microphone denied, `MediaRecorder` unsupported, recording too
short, upload failure, transcription failure, analysis failure, timeout, empty
transcript (returns 422 **without** spending a model call), over-long answer
(truncated), unauthorised course, autoplay blocked, duplicate submissions.

**Duplicate protection.** An identical transcript for the same lesson within
eight seconds returns the existing attempt instead of buying a second analysis;
if the first is still running, the second gets `409 in_progress`. The recorder
also refuses to start while a run is in flight and disables its buttons.

**Audio limits.** `MAX_AUDIO_DURATION` (default 60s) stops the recorder client
side; the server rejects anything above 12 MB or below 1 KB. Format is taken
from the MIME type with the filename extension as fallback, so Safari's
`audio/mp4a-latm` and Chrome's `audio/webm;codecs=opus` both pass.

---

## 7. Security

* `OPENAI_API_KEY` is server-only. It is not in any `NEXT_PUBLIC_*` variable, not
  in the client bundle, and never logged — failures log the status code only.
* Every AI endpoint requires authentication **and** enrolment; route protection
  in the client is a convenience, not the control.
* Audio is not stored by default (`STORE_AUDIO=false`). When enabled, files go to
  `MEDIA_ROOT/speaking/<user-id>/` under a random name.
* CORS keeps its existing explicit allow-list; `CORS_ALLOW_ALL_ORIGINS` is not
  used. The browser only ever calls same-origin Next.js routes.

---

## 8. Environment variables (`api/.env`)

```
OPENAI_API_KEY=...              # server-side only
OPENAI_TEXT_MODEL=gpt-5.4-mini
OPENAI_TRANSCRIPTION_MODEL=gpt-transcribe
MAX_AUDIO_DURATION=60
STORE_AUDIO=false
AI_MAX_RETRIES=2
```

`.env.local` holds only the harmless `NEXT_PUBLIC_MAX_AUDIO_DURATION=60`.

---

## 9. Running locally

```bash
# backend
cd api
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python manage.py seed                    # catalogue, if not seeded yet
./.venv/bin/python manage.py seed_speaking_course    # course, parts, 12 scenes, 9 questions
./.venv/bin/python manage.py runserver 8010

# frontend
npm run dev
```

Sign in as `student@goteh.de` / `goteh1234` and open
`/fa/learn/einreise-nach-deutschland` (also `/de/...` and `/en/...`).

`seed_speaking_course` is idempotent and enrols the demo student. Videos live in
`api/media/courses/einreise-nach-deutschland/videos/`.

---

## 10. Production notes

* Serve `MEDIA_ROOT` from nginx or object storage — Django only serves it in
  `DEBUG`.
* Videos are static assets; put them behind a CDN with range requests.
* Requests to OpenAI time out at 90s (transcription) and 120s (analysis).
* Consider a per-user rate limit on `/api/ai/analyze/` before opening signups.
* Rotate the API key if it has ever been shared outside the server.

---

## 11. Admin panel

Back-office at `/[locale]/admin`, reachable from the account menu for staff.

### Access

```bash
cd api && ./.venv/bin/python manage.py make_staff you@example.com
# revoke with --revoke
```

`is_staff` on the user document is the only gate, and it is enforced by
`IsStaff` on **every** admin endpoint — the client route only decides whether to
show the door.

### What it manages

| Screen | Does |
| --- | --- |
| Overview | counts for courses, categories, parts, videos, learners, attempts |
| Categories | create / edit / delete course and podcast categories (colour, icon, order) |
| Courses | create / edit / publish / delete, price, level, category, instructor |
| Course builder | chapters (Parts), lesson videos, upload, ordering, and the speaking prompt |

Every text field is edited in all three languages at once — the editor writes
the raw `{fa, en, de}` object, so saving one language never wipes the others.

### The speaking prompt

Inside a lesson the lower half of the form is the AI teacher's brief:

* **متن سؤال (آلمانی)** — `prompt_de`, the question the teacher grades against;
* translation and hint shown to the learner;
* **expected points**, **grammar topics**, **vocabulary** — one per line, passed
  to the model as lesson context;
* **min words**.

Unticking “this video has a speaking task” stores `question = null`, and the
classroom then rolls straight to the next scene — the behaviour scenes 1–3 use.

### Uploads

`POST /api/admin/upload/video/` (staff only) accepts MP4/WebM/MOV up to 512 MB,
stores it under `MEDIA_ROOT/courses/<course-slug>/videos/` with a random suffix,
and reads the duration out of the MP4 `mvhd` atom so the form prefills it. The
browser sends the file to the same-origin Next route `/api/admin/upload`, which
attaches the session cookie — the JSON proxy cannot carry multipart.

### Admin endpoints

```
GET                /api/admin/overview/
GET  POST          /api/admin/categories/
PATCH DELETE       /api/admin/categories/<id>/
GET  POST          /api/admin/instructors/
GET  POST          /api/admin/courses/
GET  PATCH DELETE  /api/admin/courses/<id>/
GET  POST          /api/admin/courses/<id>/parts/
PATCH DELETE       /api/admin/parts/<id>/
POST               /api/admin/parts/<id>/videos/
PATCH DELETE       /api/admin/videos/<id>/
POST               /api/admin/parts/reorder/   /api/admin/videos/reorder/
POST               /api/admin/upload/video/
```

### Deletes that refuse

The panel will not let a delete silently destroy learner data:

* a category still used by a course → **409**;
* a course with enrolments → **409** (unpublish instead);
* a part that still holds lessons → **409**;
* a lesson with speaking attempts → **409** (unpublish instead).

Only a lesson with no attempts is removed, and its watch progress goes with it.
