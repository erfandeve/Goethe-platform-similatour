# GOTEH Academy

Trilingual (Deutsch / English / فارسی) language-learning platform: courses, exam
simulators, high-frequency exam banks and podcasts, with a personal student panel.

```
goteh/
├── api/   Django 5 + DRF + MongoEngine (MongoDB)          → http://localhost:8010
└── web/   Next.js 16 (App Router) + Tailwind 4 + three.js → http://localhost:3000
```

## Backend

```bash
cd api
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
cp .env.example .env
./.venv/bin/python manage.py seed --flush   # demo content in all three languages
./.venv/bin/python manage.py runserver 8010
```

Requires a running MongoDB (`brew services start mongodb-community`).

Demo student: `student@goteh.de` / `goteh1234` · demo coupon: `GOTEH15`

### Data model

Every content document embeds a `TranslatedText { fa, en, de }` for each
user-facing string, so one document serves all three languages and falls back
through a chain when a translation is missing. Prices are integer **Rial**;
the Persian UI renders them as Toman.

| Collection | Purpose |
| --- | --- |
| `users`, `wallet_transactions`, `notifications`, `messages` | account, balance, inbox |
| `categories`, `instructors`, `courses`, `enrollments`, `reviews` | catalogue + progress |
| `carts`, `orders` | commerce |
| `exams`, `exam_access`, `exam_attempts` | simulators (A1–C1) and high-frequency sets (B2, C1) |
| `podcasts`, `episodes`, `listen_progress`, `bookmarks` | podcast library |

### API surface

| Area | Endpoints |
| --- | --- |
| Auth | `POST /api/auth/register\|login\|refresh`, `GET\|PATCH /api/auth/me/`, `POST /api/auth/change-password/` |
| Panel | `GET /api/auth/dashboard/`, `/api/auth/wallet/` (+ `/topup/`), `/api/auth/notifications/`, `/api/auth/messages/` |
| Courses | `GET /api/courses/` (level, category, format, language, price, `q`, sort, pagination + facets), `/api/courses/<slug>/`, `/api/categories/`, `/api/instructors/` |
| Commerce | `GET /api/cart/`, `POST /api/cart/add\|remove\|coupon/`, `POST /api/checkout/`, `GET /api/orders/`, `GET /api/my/courses/` |
| Exams | `GET /api/exams/`, `/api/exams/<slug>/`, `POST /api/exams/<slug>/start/` (body `{"module": "lesen"}` for Goethe sets), `POST /api/attempts/<id>/answers\|submit/`, `GET /api/my/attempts/` |
| Podcasts | `GET /api/podcasts/`, `/api/podcasts/episodes/`, `/api/podcasts/episodes/<slug>/` (+ `play`, `progress`, `bookmark`), `/api/podcasts/library/` |
| SEO | `GET /api/home/`, `/api/sitemap-feed/` |

Localize any response with `?locale=fa|en|de` or an `X-Locale` header.
Answer keys are never sent while an attempt is open; essay questions are
excluded from the automatic score and flagged for teacher grading.

## Typography

Three faces, composed per glyph rather than per page:

| Variable | Face | Covers |
| --- | --- | --- |
| `--font-bricolage` | Bricolage Grotesque | Latin display / headings |
| `--font-manrope` | Manrope | Latin body, including `ä ö ü ß` |
| `--font-yekan` | Yekan Bakh (variable, `web/src/app/fonts/`) | Persian |

Yekan Bakh ships no accented Latin, and German words appear on every Persian
page, so its `@font-face` is scoped with `unicode-range` to the Arabic blocks.
A sentence like "پادکست Brötchen" therefore takes its Persian from Yekan Bakh
and every Latin glyph from Manrope, with no change of typeface mid-word. The
theme tokens (`--font-display`, `--font-sans`, `--font-persian`) compose those
three variables; none of them may reference itself.

The shipped file is the variable TTF converted to woff2 (113 KB → 47 KB), which
covers every weight from Thin to ExtraBlack in one request. Yekan Bakh is a
commercial face — check the web licence before deploying.

## Exam engine

Exams come in two shapes and the runner picks one automatically from
`exam.format`:

- **`simple`** — the original flat question bank (levels A1, A2, B1, C1 and the
  high-frequency B2/C1 sets). One list of questions per skill.
- **`goethe`** — a full model set, modelled the way the real exam is built:
  `Exam.modules[] → ExamPart[] → ExamItem[]`. Each Teil declares its own
  `part_type`, which decides both how the material is shown and how it is
  scored:

  | `part_type` | Used by | Interaction |
  | --- | --- | --- |
  | `match_person` | Lesen 1 | statements → one of four forum posters |
  | `gap_drag` | Lesen 2 | drag sentences into numbered gaps in the article |
  | `mcq` | Lesen 3, Hören 2–4 | question with its own three options |
  | `match_heading` | Lesen 4 | headings → opinion boxes a–h |
  | `match_paragraph` | Lesen 5 | regulation paragraphs → headings a–h |
  | `listening_mixed` | Hören 1 | five tracks, richtig/falsch + 3-option pairs |
  | `writing` | Schreiben 1–2 | free text with a live word count |

`GOETHE-ZERTIFIKAT B2` is seeded from the published Modellsatz with
`manage.py seed_b2` (content in `api/apps/exams/content/`). Modules are sat one
at a time, exactly as in the real exam: Lesen 65 min / 30 items, Hören 40 min /
30 items, Schreiben 75 min / 2 tasks. Answer keys never reach the browser while
an attempt is open — the runner is served without them and they are only
returned in the review after submission. Writing tasks carry no automatic
points and are flagged for teacher grading.

The exam player (`web/src/components/exams/goethe/`) always renders
left-to-right, in every locale: the design it mirrors is LTR and the exam
material is entirely German. Persian interface labels inside it carry
`dir="auto"`. It reproduces the Goethe digital test layout: dark header with the session number and remaining time,
font-size/contrast/volume steppers, the time bar, the two-panel split with the
grey instruction band, the green edge navigation, per-Teil work time and page
counter, and the ring-shaped listening player that plays each track the allowed
number of times with the official reading time before it starts. It runs in its
own light theme with the site chrome hidden (`body[data-mode="exam"]`).

Listening audio in the demo is speech-synthesised from the Modellsatz
transcripts (`api/media/exams/b2/hoeren/`); replace it with the licensed
recordings before going live.

## AI speaking teacher

Video lessons with a spoken answer that OpenAI transcribes and a German teacher
persona grades. Lives in `api/apps/learning` and `web/src/components/learning`;
the classroom is at `/[locale]/learn/<course-slug>`.

```bash
cd api && ./.venv/bin/python manage.py seed_speaking_course
```

Needs `OPENAI_API_KEY` in `api/.env`. The key is server-side only — the browser
talks to Django, Django talks to OpenAI. Full write-up in
[AI_SPEAKING_SYSTEM.md](AI_SPEAKING_SYSTEM.md).

## Admin panel

`/[locale]/admin` — courses, categories, chapters, lesson videos and the AI
speaking prompts. Staff only:

```bash
cd api && ./.venv/bin/python manage.py make_staff you@example.com
```

## Frontend

```bash
cd web
npm install
npm run dev
```

Routes live under `/[locale]` (`fa`, `en`, `de`); `fa` renders RTL. A proxy
(`src/middleware.ts`) negotiates the locale from the cookie, then
`Accept-Language`, then falls back to Persian.

- **Session**: JWTs live in httpOnly cookies set by `/api/session/*` route
  handlers; browser calls reach Django through `/api/proxy/*` so the token is
  never exposed to page scripts.
- **SEO**: per-page `generateMetadata`, canonical + `hreflang` alternates for
  all three locales, OpenGraph/Twitter cards, JSON-LD
  (`EducationalOrganization`, `Course`, `Quiz`, `PodcastSeries`,
  `PodcastEpisode`, `BreadcrumbList`, `ItemList`), `sitemap.xml` built from the
  API feed, and `robots.txt` that keeps the panel, cart and exam runner out of
  the index.
- **3D**: the hero renders a react-three-fiber scene (distorting core, orbit
  rings, particle field) that is code-split, pointer-reactive, and swapped for a
  static gradient under `prefers-reduced-motion` or on small screens.

### Not yet real

Cover images are drawn procedurally from each item's accent colour, and every
episode points at one generated German demo track
(`api/media/podcasts/audio/demo.m4a`) — swap in real uploads when they exist.
The B2 exam text is the Goethe-Institut Modellsatz: fine for practice, but
licence it or replace it with in-house items before selling access. The exam
player deliberately carries GOTEH branding — the Goethe-Institut logo is their
trademark and must not appear here.
Checkout debits the wallet directly; a real payment gateway replaces
`POST /api/checkout/` and `POST /api/auth/wallet/topup/` in the payment phase.
