"""Populate MongoDB with a full demo dataset: python manage.py seed --flush"""

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from apps.accounts.models import Message, Notification, User, WalletTransaction
from apps.core.i18n import tt
from apps.courses.models import (
    Cart,
    Category,
    Course,
    Enrollment,
    Instructor,
    Lesson,
    Order,
    Review,
    Section,
)
from apps.exams.models import Exam, ExamAccess, ExamAttempt, ExamSection, Question
from apps.podcasts.models import (
    Bookmark,
    Episode,
    ListenProgress,
    Podcast,
    TranscriptLine,
    VocabItem,
)

M = 1_000_000  # one million Rial, prices read better this way


class Command(BaseCommand):
    help = "Seed the GOTEH database with demo content."

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true", help="Drop existing data first.")

    def handle(self, *args, **options):
        if options["flush"]:
            for model in (
                Bookmark, ListenProgress, Episode, Podcast,
                ExamAttempt, ExamAccess, Exam,
                Review, Enrollment, Order, Cart, Course, Instructor, Category,
                WalletTransaction, Notification, Message, User,
            ):
                model.drop_collection()
            self.stdout.write(self.style.WARNING("Collections dropped."))

        categories = self.seed_categories()
        instructors = self.seed_instructors()
        courses = self.seed_courses(categories, instructors)
        exams = self.seed_exams()
        episodes = self.seed_podcasts(categories)
        self.seed_demo_user(courses, exams, episodes)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(courses)} courses, {len(exams)} exams, "
                f"{len(episodes)} episodes. Demo login: student@goteh.de / goteh1234"
            )
        )

    # -- taxonomy -------------------------------------------------------------

    def seed_categories(self):
        data = [
            ("general-german", "course", "آلمانی عمومی", "General German", "Allgemeines Deutsch", "#6d5efc", "layers"),
            ("exam-prep", "course", "آمادگی آزمون", "Exam Preparation", "Prüfungsvorbereitung", "#ff6b6b", "target"),
            ("conversation", "course", "مکالمه", "Conversation", "Konversation", "#22d3ee", "chat"),
            ("grammar", "course", "گرامر", "Grammar", "Grammatik", "#f59e0b", "book"),
            ("business", "course", "آلمانی تجاری", "Business German", "Wirtschaftsdeutsch", "#34d399", "briefcase"),
            ("medical", "course", "آلمانی پزشکی", "Medical German", "Medizinisches Deutsch", "#e879f9", "heart"),
            ("daily-life", "podcast", "زندگی روزمره", "Daily Life", "Alltag", "#6d5efc", "sun"),
            ("culture", "podcast", "فرهنگ و جامعه", "Culture & Society", "Kultur & Gesellschaft", "#f472b6", "globe"),
            ("news-slow", "podcast", "اخبار آهسته", "Slow News", "Nachrichten langsam", "#38bdf8", "radio"),
            ("stories", "podcast", "داستان کوتاه", "Short Stories", "Kurzgeschichten", "#fbbf24", "book-open"),
        ]
        result = {}
        for order, (slug, kind, fa, en, de, color, icon) in enumerate(data):
            cat = Category.objects(slug=slug, kind=kind).first() or Category(slug=slug, kind=kind)
            cat.title = tt(fa, en, de)
            cat.color = color
            cat.icon = icon
            cat.order = order
            cat.save()
            result[slug] = cat
        return result

    def seed_instructors(self):
        data = [
            ("lena-hoffmann", "Lena Hoffmann", "مدرس ارشد آلمانی، گوته C2",
             "Senior German Trainer, Goethe C2", "Senior-Deutschtrainerin, Goethe C2", 4.9, 12400),
            ("dr-sara-ahmadi", "Dr. Sara Ahmadi", "دکترای زبان‌شناسی، متخصص آزمون",
             "PhD Linguistics, Exam Specialist", "Dr. Linguistik, Prüfungsexpertin", 4.8, 9800),
            ("markus-weber", "Markus Weber", "مدرس بومی، مکالمه و تلفظ",
             "Native Coach, Speaking & Pronunciation", "Muttersprachlicher Coach, Sprechen", 4.9, 15200),
            ("nima-rasouli", "Nima Rasouli", "مدرس آلمانی پزشکی و FSP",
             "Medical German & FSP Trainer", "Trainer für Medizindeutsch & FSP", 4.7, 5400),
        ]
        result = {}
        for slug, name, fa, en, de, rating, students in data:
            ins = Instructor.objects(slug=slug).first() or Instructor(slug=slug)
            ins.name = name
            ins.headline = tt(fa, en, de)
            ins.bio = tt(
                f"{name} بیش از ده سال است که زبان‌آموزان فارسی‌زبان را تا سطح C1 همراهی می‌کند.",
                f"{name} has guided Persian-speaking learners up to C1 for over a decade.",
                f"{name} begleitet seit über zehn Jahren Lernende bis zum Niveau C1.",
            )
            ins.avatar = f"/media/instructors/{slug}.jpg"
            ins.languages = ["de", "en", "fa"]
            ins.rating = rating
            ins.students = students
            ins.is_featured = True
            ins.save()
            result[slug] = ins
        return result

    # -- courses --------------------------------------------------------------

    def seed_courses(self, categories, instructors):
        blueprint = [
            dict(slug="deutsch-a1-komplett", level="A1", cat="general-german", ins="lena-hoffmann",
                 fa="آلمانی A1 — دوره کامل از صفر", en="German A1 — Complete Course from Zero",
                 de="Deutsch A1 — Komplettkurs von Null",
                 sub_fa="اولین قدم مطمئن شما به دنیای زبان آلمانی",
                 sub_en="Your first confident step into German",
                 sub_de="Ihr erster sicherer Schritt ins Deutsche",
                 price=9*M, discount=6*M, minutes=1840, sessions=48, accent="#6d5efc",
                 featured=True, best=True, fmt="self_paced"),
            dict(slug="deutsch-a2-aufbau", level="A2", cat="general-german", ins="lena-hoffmann",
                 fa="آلمانی A2 — تثبیت پایه", en="German A2 — Building the Base",
                 de="Deutsch A2 — Grundlagen festigen",
                 sub_fa="از جملات ساده تا گفتگوی روزمره", sub_en="From simple sentences to real conversation",
                 sub_de="Von einfachen Sätzen zum echten Gespräch",
                 price=11*M, discount=0, minutes=2100, sessions=52, accent="#22d3ee", fmt="self_paced"),
            dict(slug="deutsch-b1-intensiv", level="B1", cat="general-german", ins="markus-weber",
                 fa="آلمانی B1 — دوره فشرده", en="German B1 — Intensive Course",
                 de="Deutsch B1 — Intensivkurs",
                 sub_fa="سطحی که درِ مهاجرت را باز می‌کند", sub_en="The level that opens the migration door",
                 sub_de="Das Niveau, das Türen öffnet",
                 price=14*M, discount=10*M, minutes=2600, sessions=60, accent="#f59e0b",
                 featured=True, fmt="hybrid"),
            dict(slug="deutsch-b2-pruefung", level="B2", cat="exam-prep", ins="dr-sara-ahmadi",
                 fa="آمادگی آزمون B2 گوته", en="Goethe B2 Exam Preparation",
                 de="Goethe B2 Prüfungsvorbereitung",
                 sub_fa="چهار مهارت + تکنیک‌های آزمون", sub_en="Four skills plus exam technique",
                 sub_de="Vier Fertigkeiten plus Prüfungstechnik",
                 price=18*M, discount=13*M, minutes=2200, sessions=44, accent="#ff6b6b",
                 featured=True, best=True, fmt="live"),
            dict(slug="deutsch-c1-meisterkurs", level="C1", cat="exam-prep", ins="dr-sara-ahmadi",
                 fa="C1 — دوره تسلط دانشگاهی", en="C1 — Academic Mastery",
                 de="C1 — Akademischer Meisterkurs",
                 sub_fa="برای تحصیل و کار حرفه‌ای در آلمان", sub_en="For study and professional work in Germany",
                 sub_de="Für Studium und Beruf in Deutschland",
                 price=22*M, discount=0, minutes=2400, sessions=40, accent="#e879f9", fmt="live"),
            dict(slug="sprechen-konversation", level="B1", cat="conversation", ins="markus-weber",
                 fa="کارگاه مکالمه با مدرس بومی", en="Speaking Lab with a Native Coach",
                 de="Sprechlabor mit Muttersprachler",
                 sub_fa="هفته‌ای دو جلسه زنده، گروه‌های ۶ نفره",
                 sub_en="Two live sessions a week, groups of six",
                 sub_de="Zwei Live-Sitzungen pro Woche, Sechsergruppen",
                 price=8*M, discount=0, minutes=900, sessions=24, accent="#34d399", fmt="live"),
            dict(slug="grammatik-master", level="B2", cat="grammar", ins="lena-hoffmann",
                 fa="گرامر آلمانی از A تا Z", en="German Grammar from A to Z",
                 de="Deutsche Grammatik von A bis Z",
                 sub_fa="تمام ساختارها با تمرین تعاملی", sub_en="Every structure with interactive drills",
                 sub_de="Alle Strukturen mit interaktiven Übungen",
                 price=7*M, discount=4*M, minutes=1500, sessions=38, accent="#fbbf24", fmt="self_paced"),
            dict(slug="wirtschaftsdeutsch", level="B2", cat="business", ins="lena-hoffmann",
                 fa="آلمانی تجاری و مکاتبات اداری", en="Business German & Office Writing",
                 de="Wirtschaftsdeutsch & Korrespondenz",
                 sub_fa="ایمیل، جلسه، مذاکره", sub_en="Emails, meetings, negotiation",
                 sub_de="E-Mails, Meetings, Verhandlung",
                 price=12*M, discount=0, minutes=1100, sessions=28, accent="#38bdf8", fmt="self_paced"),
            dict(slug="medizinisches-deutsch-fsp", level="C1", cat="medical", ins="nima-rasouli",
                 fa="آلمانی پزشکی و آمادگی FSP", en="Medical German & FSP Prep",
                 de="Medizinisches Deutsch & FSP",
                 sub_fa="برای پزشکان و پرستاران مهاجر", sub_en="For migrating doctors and nurses",
                 sub_de="Für zuwandernde Ärzte und Pflegekräfte",
                 price=26*M, discount=19*M, minutes=1800, sessions=36, accent="#f472b6", fmt="hybrid"),
            dict(slug="deutsch-schnellstart-gratis", level="A1", cat="general-german", ins="markus-weber",
                 fa="شروع سریع آلمانی — رایگان", en="German Quick Start — Free",
                 de="Deutsch Schnellstart — Kostenlos",
                 sub_fa="۱۰ درس رایگان برای شروع امروز", sub_en="Ten free lessons to start today",
                 sub_de="Zehn kostenlose Lektionen für den Start",
                 price=0, discount=0, minutes=180, sessions=10, accent="#a78bfa", fmt="self_paced"),
        ]

        courses = []
        for index, b in enumerate(blueprint):
            course = Course.objects(slug=b["slug"]).first() or Course(slug=b["slug"])
            course.title = tt(b["fa"], b["en"], b["de"])
            course.subtitle = tt(b["sub_fa"], b["sub_en"], b["sub_de"])
            course.description = tt(
                "این دوره با تمرکز بر مهارت‌های چهارگانه طراحی شده و هر درس شامل ویدیو، تمرین تعاملی و آزمون کوتاه است. "
                "پشتیبانی مدرس، تصحیح تکالیف نوشتاری و جلسات پرسش‌وپاسخ زنده در طول دوره همراه شماست.",
                "Built around the four core skills, every lesson combines video, interactive drills and a short quiz. "
                "Tutor support, written homework correction and live Q&A sessions run throughout the course.",
                "Der Kurs ist auf die vier Fertigkeiten ausgerichtet: Video, interaktive Übungen und ein kurzes Quiz pro Lektion. "
                "Betreuung, Korrektur der schriftlichen Aufgaben und Live-Fragestunden begleiten Sie durchgehend.",
            )
            course.category = categories[b["cat"]]
            course.instructor = instructors[b["ins"]]
            course.level = b["level"]
            course.format = b["fmt"]
            course.language = "de"
            course.cover = f"/media/courses/{b['slug']}.jpg"
            course.accent = b["accent"]
            course.price = b["price"]
            course.discount_price = b["discount"]
            course.duration_minutes = b["minutes"]
            course.sessions_count = b["sessions"]
            course.tags = [b["level"], b["cat"], "deutsch"]
            course.rating = round(4.4 + (index % 6) * 0.1, 1)
            course.reviews_count = 40 + index * 17
            course.students_count = 320 + index * 214
            course.is_featured = b.get("featured", False)
            course.is_bestseller = b.get("best", False)
            course.starts_at = datetime.utcnow() + timedelta(days=7 + index)
            course.outcomes = [
                tt("درک مطمئن مکالمات روزمره", "Confidently follow everyday conversations",
                   "Alltagsgespräche sicher verstehen"),
                tt("نوشتن ایمیل و نامه رسمی", "Write emails and formal letters",
                   "E-Mails und formelle Briefe schreiben"),
                tt(f"آمادگی کامل برای آزمون {b['level']}", f"Full readiness for the {b['level']} exam",
                   f"Volle Bereitschaft für die {b['level']}-Prüfung"),
                tt("تسلط بر ۲۰۰۰ واژه پرکاربرد", "Master 2,000 high-frequency words",
                   "2.000 häufige Wörter beherrschen"),
            ]
            course.requirements = [
                tt("بدون پیش‌نیاز برای سطح A1", "No prerequisites for A1", "Keine Vorkenntnisse für A1"),
                tt("روزی ۳۰ دقیقه تمرین", "Thirty minutes of practice a day", "Täglich 30 Minuten Übung"),
            ]
            course.curriculum = self.build_curriculum(b["level"])
            course.is_published = True
            course.save()
            courses.append(course)

            if not Review.objects(course=course).first():
                for name, rating, body in (
                    ("Parisa M.", 5, "بهترین دوره‌ای که تا حالا دیدم، ساختار درس‌ها فوق‌العاده منظمه."),
                    ("Amir R.", 5, "Die Erklärungen sind klar und die Übungen wirklich praxisnah."),
                    ("Hannah K.", 4, "Great pacing. I passed my exam on the first try."),
                ):
                    Review(course=course, author_name=name, rating=rating, body=body).save()
        return courses

    def build_curriculum(self, level):
        modules = [
            ("مقدمه و تلفظ", "Orientation & Pronunciation", "Einstieg & Aussprache"),
            ("واژگان پایه", "Core Vocabulary", "Grundwortschatz"),
            ("ساختار جمله", "Sentence Structure", "Satzbau"),
            ("مهارت شنیداری", "Listening Skills", "Hörverstehen"),
            ("نوشتار و تصحیح", "Writing & Correction", "Schreiben & Korrektur"),
            ("مرور و آزمون پایانی", "Review & Final Test", "Wiederholung & Abschlusstest"),
        ]
        kinds = ("video", "video", "quiz", "audio", "pdf")
        sections = []
        for m_index, (fa, en, de) in enumerate(modules):
            lessons = []
            for l_index in range(4):
                lessons.append(
                    Lesson(
                        title=tt(
                            f"{fa} — درس {l_index + 1}",
                            f"{en} — Lesson {l_index + 1}",
                            f"{de} — Lektion {l_index + 1}",
                        ),
                        duration_minutes=8 + (l_index * 5),
                        kind=kinds[(m_index + l_index) % len(kinds)],
                        is_preview=(m_index == 0 and l_index < 2),
                    )
                )
            sections.append(
                Section(title=tt(f"بخش {m_index + 1}: {fa}", f"Module {m_index + 1}: {en}",
                                 f"Modul {m_index + 1}: {de}"), lessons=lessons)
            )
        return sections

    # -- exams ----------------------------------------------------------------

    def seed_exams(self):
        simulators = [
            ("A1", "Goethe-Zertifikat A1: Start Deutsch 1", 65, 0, "#34d399",
             "اولین گواهی رسمی آلمانی شما", "Your first official German certificate",
             "Ihr erstes offizielles Deutschzertifikat"),
            ("A2", "Goethe-Zertifikat A2", 80, 2*M, "#22d3ee",
             "سنجش کامل چهار مهارت در سطح A2", "Full four-skill assessment at A2",
             "Vollständige Vier-Fertigkeiten-Prüfung auf A2"),
            ("B1", "Goethe-Zertifikat B1", 165, 3*M, "#f59e0b",
             "سطح کلیدی برای اقامت و کار", "The key level for residence and work",
             "Das Schlüsselniveau für Aufenthalt und Arbeit"),
            ("B2", "Goethe-Zertifikat B2", 190, 4*M, "#ff6b6b",
             "شبیه‌ساز کامل آزمون B2", "Complete B2 exam simulator",
             "Vollständiger B2-Prüfungssimulator"),
            ("C1", "Goethe-Zertifikat C1", 190, 5*M, "#e879f9",
             "بالاترین سطح آمادگی دانشگاهی", "Top-tier academic readiness",
             "Höchste akademische Vorbereitung"),
        ]
        frequent = [
            ("B2", "پرتکرارهای B2", "B2 High-Frequency Set", "B2 Häufigkeitsset", 90, 3*M, "#ff6b6b"),
            ("C1", "پرتکرارهای C1", "C1 High-Frequency Set", "C1 Häufigkeitsset", 90, 4*M, "#e879f9"),
        ]

        exams = []
        for level, board, minutes, price, accent, fa, en, de in simulators:
            slug = f"simulator-{level.lower()}"
            exam = Exam.objects(slug=slug).first() or Exam(slug=slug)
            exam.title = tt(f"آزمون شبیه‌ساز {level}", f"{level} Exam Simulator",
                            f"{level} Prüfungssimulator")
            exam.subtitle = tt(fa, en, de)
            exam.description = tt(
                "این شبیه‌ساز دقیقاً با ساختار، زمان‌بندی و سطح دشواری آزمون رسمی طراحی شده است. "
                "در پایان، کارنامه تفکیکی هر مهارت به همراه پاسخ تشریحی هر سؤال را دریافت می‌کنید.",
                "The simulator mirrors the official exam in structure, timing and difficulty. "
                "At the end you get a per-skill score report plus a full explanation for every question.",
                "Der Simulator entspricht der offiziellen Prüfung in Aufbau, Timing und Schwierigkeit. "
                "Am Ende erhalten Sie eine Auswertung pro Fertigkeit und Erklärungen zu jeder Aufgabe.",
            )
            exam.level = level
            exam.kind = "simulator"
            exam.exam_board = board
            exam.cover = f"/media/exams/{slug}.jpg"
            exam.accent = accent
            exam.badge = "GRATIS" if price == 0 else level
            exam.duration_minutes = minutes
            exam.pass_score = 60
            exam.price = price
            exam.highlights = [
                tt("چهار مهارت کامل", "All four skills", "Alle vier Fertigkeiten"),
                tt("زمان‌بندی واقعی آزمون", "Real exam timing", "Echtes Prüfungstiming"),
                tt("کارنامه تفکیکی مهارت‌ها", "Per-skill score report", "Auswertung pro Fertigkeit"),
                tt("پاسخ تشریحی همه سؤالات", "Explanations for every question", "Erklärungen zu allen Aufgaben"),
            ]
            exam.sections = self.build_sections(level)
            exam.rating = 4.8
            exam.attempts_count = 1200 + len(exams) * 340
            exam.is_featured = level in ("B1", "B2")
            exam.save()
            exams.append(exam)

        for level, fa, en, de, minutes, price, accent in frequent:
            slug = f"frequent-{level.lower()}"
            exam = Exam.objects(slug=slug).first() or Exam(slug=slug)
            exam.title = tt(fa, en, de)
            exam.subtitle = tt(
                "سؤالاتی که در دوره‌های اخیر بیشترین تکرار را داشته‌اند",
                "The questions that repeat most often in recent sittings",
                "Die Aufgaben, die zuletzt am häufigsten wiederkehrten",
            )
            exam.description = tt(
                "بانک سؤالات پرتکرار از آزمون‌های واقعی دو سال اخیر، دسته‌بندی‌شده بر اساس مهارت و موضوع. "
                "بهترین ابزار برای مرور نهایی یک هفته پیش از آزمون.",
                "A bank of high-frequency questions from real sittings of the last two years, grouped by skill and topic. "
                "The best tool for a final review one week before the exam.",
                "Eine Sammlung häufiger Aufgaben aus echten Prüfungen der letzten zwei Jahre, nach Fertigkeit und Thema sortiert. "
                "Ideal für die Endwiederholung eine Woche vor der Prüfung.",
            )
            exam.level = level
            exam.kind = "frequent"
            exam.exam_board = f"Goethe-Zertifikat {level}"
            exam.cover = f"/media/exams/{slug}.jpg"
            exam.accent = accent
            exam.badge = "TOP"
            exam.duration_minutes = minutes
            exam.pass_score = 70
            exam.price = price
            exam.highlights = [
                tt("برگرفته از آزمون‌های واقعی", "Taken from real sittings", "Aus echten Prüfungen"),
                tt("دسته‌بندی موضوعی", "Grouped by topic", "Nach Themen sortiert"),
                tt("به‌روزرسانی فصلی", "Updated every quarter", "Vierteljährlich aktualisiert"),
            ]
            exam.sections = self.build_sections(level, frequent=True)
            exam.rating = 4.9
            exam.attempts_count = 2400
            exam.is_featured = True
            exam.save()
            exams.append(exam)
        return exams

    def build_sections(self, level, frequent=False):
        skills = ("listening", "reading", "grammar", "writing") if not frequent else ("reading", "grammar")
        titles = {
            "listening": ("شنیداری", "Listening", "Hören"),
            "reading": ("درک مطلب", "Reading", "Lesen"),
            "grammar": ("گرامر و واژگان", "Grammar & Vocabulary", "Grammatik & Wortschatz"),
            "writing": ("نوشتار", "Writing", "Schreiben"),
        }
        bank = [
            ("Wie ___ du?", ["heißt", "heißen", "heiße", "heißen Sie"], 0,
             "دوم شخص مفرد فعل heißen می‌شود heißt.",
             "The second-person singular of heißen is heißt.",
             "Die 2. Person Singular von heißen lautet heißt."),
            ("Ich fahre ___ dem Bus zur Arbeit.", ["mit", "auf", "in", "an"], 0,
             "برای وسیله نقلیه از حرف اضافه mit + Dativ استفاده می‌شود.",
             "Means of transport take mit + dative.",
             "Verkehrsmittel stehen mit mit + Dativ."),
            ("Der Termin wurde ___ verschoben.", ["kurzfristig", "kurzfristige", "kurzfristigen", "kurzfristiger"], 0,
             "قید حالت بدون پسوند صرفی می‌آید.",
             "Used adverbially, the adjective takes no ending.",
             "Adverbial gebraucht bleibt das Adjektiv endungslos."),
            ("___ des schlechten Wetters fand das Fest statt.", ["Trotz", "Wegen", "Während", "Statt"], 0,
             "trotz به معنی «با وجودِ» و با Genitiv می‌آید.",
             "trotz means 'despite' and governs the genitive.",
             "trotz bedeutet „ungeachtet“ und steht mit Genitiv."),
            ("Sie legt großen Wert ___ Pünktlichkeit.", ["auf", "an", "über", "für"], 0,
             "ترکیب ثابت: Wert legen auf + Akkusativ.",
             "Fixed collocation: Wert legen auf + accusative.",
             "Feste Wendung: Wert legen auf + Akkusativ."),
            ("Das Projekt ist ___ gescheitert.", ["letztendlich", "letztendliche", "letztendlichen", "letztendlicher"], 0,
             "قید است و صرف نمی‌شود.", "It is an adverb and stays uninflected.",
             "Es ist ein Adverb und bleibt unverändert."),
        ]
        count = {"A1": 4, "A2": 5, "B1": 6, "B2": 6, "C1": 6}[level]
        sections = []
        for skill in skills:
            fa, en, de = titles[skill]
            questions = []
            for index in range(count):
                prompt, options, correct, e_fa, e_en, e_de = bank[index % len(bank)]
                if skill == "writing":
                    questions.append(
                        Question(
                            prompt=tt(
                                "یک ایمیل ۸۰ کلمه‌ای بنویسید و قرار ملاقات را جابه‌جا کنید.",
                                "Write an 80-word email to reschedule an appointment.",
                                "Schreiben Sie eine E-Mail (80 Wörter) zur Terminverschiebung.",
                            ),
                            kind="essay",
                            points=5,
                        )
                    )
                    continue
                questions.append(
                    Question(
                        prompt=tt(prompt, prompt, prompt),
                        audio_url=f"/media/exams/audio/{level.lower()}-{index + 1}.mp3" if skill == "listening" else "",
                        kind="single",
                        options=[tt(o, o, o) for o in options],
                        correct_index=correct,
                        explanation=tt(e_fa, e_en, e_de),
                        points=1,
                    )
                )
            sections.append(
                ExamSection(
                    skill=skill,
                    title=tt(fa, en, de),
                    instructions=tt(
                        "برای هر سؤال یک گزینه را انتخاب کنید. زمان این بخش محدود است.",
                        "Choose one option per question. This section is timed.",
                        "Wählen Sie pro Aufgabe eine Option. Dieser Teil ist zeitbegrenzt.",
                    ),
                    duration_minutes=20 if skill != "writing" else 30,
                    questions=questions,
                )
            )
        return sections

    # -- podcasts -------------------------------------------------------------

    def seed_podcasts(self, categories):
        shows = [
            dict(slug="alltag-auf-deutsch", cat="daily-life", level="A2", accent="#6d5efc",
                 host="Markus Weber",
                 fa="روزمرگی به آلمانی", en="Everyday German", de="Alltag auf Deutsch",
                 t_fa="گفتگوهای واقعی از خیابان‌های برلین",
                 t_en="Real conversations from the streets of Berlin",
                 t_de="Echte Gespräche aus Berlins Straßen"),
            dict(slug="langsame-nachrichten", cat="news-slow", level="B1", accent="#38bdf8",
                 host="Lena Hoffmann",
                 fa="اخبار آهسته", en="Slow News", de="Langsame Nachrichten",
                 t_fa="اخبار هفته با سرعت قابل فهم",
                 t_en="The week's news at an understandable pace",
                 t_de="Die Wochennachrichten in verständlichem Tempo"),
            dict(slug="kultur-kompakt", cat="culture", level="B2", accent="#f472b6",
                 host="Dr. Sara Ahmadi",
                 fa="فرهنگ فشرده", en="Culture Compact", de="Kultur kompakt",
                 t_fa="جامعه، هنر و تاریخ آلمان در ۱۵ دقیقه",
                 t_en="German society, art and history in fifteen minutes",
                 t_de="Gesellschaft, Kunst und Geschichte in 15 Minuten"),
            dict(slug="kurzgeschichten", cat="stories", level="A2", accent="#fbbf24",
                 host="Nima Rasouli",
                 fa="داستان‌های کوتاه", en="Short Stories", de="Kurzgeschichten",
                 t_fa="هر هفته یک داستان با متن کامل",
                 t_en="One story a week with a full transcript",
                 t_de="Jede Woche eine Geschichte mit Transkript"),
        ]

        episode_titles = [
            ("در نانوایی", "At the Bakery", "In der Bäckerei"),
            ("قرار پزشک", "At the Doctor's", "Beim Arzt"),
            ("جستجوی خانه", "Flat Hunting", "Wohnungssuche"),
            ("گفتگوی شغلی", "Job Interview", "Vorstellungsgespräch"),
            ("سفر با قطار", "Travelling by Train", "Mit dem Zug unterwegs"),
            ("خرید هفتگی", "Weekly Shopping", "Wocheneinkauf"),
        ]
        transcript_bank = [
            ("Anna", "Guten Morgen! Ich hätte gern zwei Brötchen, bitte.",
             "صبح بخیر! لطفاً دو تا نان کوچک می‌خواستم.",
             "Good morning! I'd like two rolls, please.",
             "Guten Morgen! Ich hätte gern zwei Brötchen, bitte."),
            ("Verkäufer", "Gerne. Möchten Sie noch etwas dazu?",
             "با کمال میل. چیز دیگری هم میل دارید؟",
             "Of course. Would you like anything else?",
             "Gerne. Möchten Sie noch etwas dazu?"),
            ("Anna", "Ja, einen Kaffee zum Mitnehmen, bitte.",
             "بله، یک قهوه بیرون‌بر لطفاً.",
             "Yes, one coffee to go, please.",
             "Ja, einen Kaffee zum Mitnehmen, bitte."),
            ("Verkäufer", "Das macht dann vier Euro zwanzig.",
             "می‌شود چهار یورو و بیست سنت.",
             "That comes to four euros twenty.",
             "Das macht dann vier Euro zwanzig."),
        ]
        vocab_bank = [
            ("Brötchen", "das", "نان کوچک", "bread roll", "kleines Brot",
             "Ich kaufe jeden Morgen zwei Brötchen."),
            ("mitnehmen", "", "با خود بردن", "to take away", "etwas mit sich nehmen",
             "Einen Kaffee zum Mitnehmen, bitte."),
            ("Wohnungssuche", "die", "جستجوی خانه", "flat hunting", "Suche nach einer Wohnung",
             "Die Wohnungssuche in Berlin ist schwierig."),
            ("Vorstellungsgespräch", "das", "مصاحبه شغلی", "job interview", "Gespräch bei einer Bewerbung",
             "Morgen habe ich ein Vorstellungsgespräch."),
        ]

        episodes = []
        for show_data in shows:
            podcast = Podcast.objects(slug=show_data["slug"]).first() or Podcast(slug=show_data["slug"])
            podcast.title = tt(show_data["fa"], show_data["en"], show_data["de"])
            podcast.tagline = tt(show_data["t_fa"], show_data["t_en"], show_data["t_de"])
            podcast.description = tt(
                "هر قسمت شامل فایل صوتی، متن کامل دوزبانه، واژه‌نامه و تمرین درک مطلب است. "
                "می‌توانید سرعت پخش را تغییر دهید و همزمان متن را دنبال کنید.",
                "Every episode ships with audio, a bilingual transcript, a vocabulary list and comprehension practice. "
                "Change the playback speed and follow the transcript line by line.",
                "Jede Folge enthält Audio, ein zweisprachiges Transkript, eine Vokabelliste und Verständnisübungen. "
                "Sie können das Tempo anpassen und dem Text Zeile für Zeile folgen.",
            )
            podcast.category = categories[show_data["cat"]]
            podcast.host_name = show_data["host"]
            podcast.host_avatar = f"/media/hosts/{show_data['slug']}.jpg"
            podcast.cover = f"/media/podcasts/{show_data['slug']}.jpg"
            podcast.accent = show_data["accent"]
            podcast.level = show_data["level"]
            podcast.tags = [show_data["level"], show_data["cat"]]
            podcast.rating = 4.8
            podcast.plays = 18400
            podcast.is_featured = show_data["slug"] in ("alltag-auf-deutsch", "langsame-nachrichten")
            podcast.save()

            for number, (fa, en, de) in enumerate(episode_titles, start=1):
                slug = f"{show_data['slug']}-{number:02d}"
                episode = Episode.objects(slug=slug).first() or Episode(slug=slug)
                episode.podcast = podcast
                episode.number = number
                episode.title = tt(f"قسمت {number}: {fa}", f"Episode {number}: {en}",
                                   f"Folge {number}: {de}")
                episode.description = tt(
                    "در این قسمت یک موقعیت واقعی روزمره را می‌شنوید، سپس واژگان کلیدی آن را مرور می‌کنیم.",
                    "This episode walks through a real everyday situation, then reviews its key vocabulary.",
                    "In dieser Folge hören Sie eine echte Alltagssituation und wiederholen den Schlüsselwortschatz.",
                )
                # Shared demo track until real recordings are uploaded per episode.
                episode.audio_url = "/media/podcasts/audio/demo.m4a"
                episode.cover = podcast.cover
                episode.duration_seconds = 480 + number * 65
                episode.level = show_data["level"]
                episode.transcript = [
                    # Timed against the shared demo track (~11s) so the
                    # line-by-line highlighting stays in sync out of the box.
                    TranscriptLine(
                        start=index * 2.7,
                        end=index * 2.7 + 2.6,
                        speaker=speaker,
                        text=text,
                        translation=tt(fa_t, en_t, de_t),
                    )
                    for index, (speaker, text, fa_t, en_t, de_t) in enumerate(transcript_bank)
                ]
                episode.vocabulary = [
                    VocabItem(term=term, article=article, meaning=tt(fa_m, en_m, de_m), example=example)
                    for term, article, fa_m, en_m, de_m, example in
                    [(v[0], v[1], v[2], v[3], v[4], v[5]) for v in vocab_bank]
                ]
                episode.plays = 2400 - number * 120
                episode.is_premium = number > 4
                episode.published_at = datetime.utcnow() - timedelta(days=number * 7)
                episode.save()
                episodes.append(episode)
        return episodes

    # -- demo student ---------------------------------------------------------

    def seed_demo_user(self, courses, exams, episodes):
        user = User.objects(email="student@goteh.de").first() or User(email="student@goteh.de")
        user.first_name = "Erfan"
        user.last_name = "Divsalar"
        user.phone = "+989120000000"
        user.city = "Tehran"
        user.country = "Iran"
        user.bio = "Preparing for the Goethe B2 exam this autumn."
        user.birth_date = "1996-04-12"
        user.avatar = "/media/avatars/demo.jpg"
        user.preferred_locale = "fa"
        user.current_level = "B1"
        user.target_level = "C1"
        user.email_verified = True
        user.wallet_balance = 12_500_000
        user.set_password("goteh1234")
        user.save()

        WalletTransaction.objects(user=user).delete()
        for amount, kind, title in (
            (20_000_000, "topup", "شارژ کیف پول از درگاه بانکی"),
            (-13_000_000, "purchase", "خرید دوره آمادگی آزمون B2"),
            (500_000, "bonus", "هدیه معرفی دوست"),
            (5_000_000, "topup", "شارژ کیف پول"),
        ):
            WalletTransaction(
                user=user, amount=amount, balance_after=user.wallet_balance, kind=kind, title=title
            ).save()

        Enrollment.objects(user=user).delete()
        for index, course in enumerate(courses[:4]):
            Enrollment(
                user=user,
                course=course,
                progress=[72, 45, 100, 18][index],
                completed_lessons=[17, 11, 24, 4][index],
                minutes_spent=[840, 520, 1900, 160][index],
                last_activity=datetime.utcnow() - timedelta(days=index),
                certificate_url=f"/media/certificates/{course.slug}.pdf" if index == 2 else "",
            ).save()
            course.students_count += 1
            course.save()

        ExamAttempt.objects(user=user).delete()
        ExamAccess.objects(user=user).delete()
        # The demo student owns every simulator so all of them are explorable.
        for exam in exams:
            ExamAccess(user=user, exam=str(exam.id), order_code="GO-10000001").save()

        for index, exam in enumerate(exams[:3]):
            score = [88, 64, 71][index]
            attempt = ExamAttempt(
                user=user,
                exam=exam,
                status="finished",
                score=score,
                raw_score=score,
                max_score=100,
                correct_count=int(score / 100 * exam.questions_count),
                passed=score >= exam.pass_score,
                cefr_estimate=exam.level,
                started_at=datetime.utcnow() - timedelta(days=index * 9 + 2),
                finished_at=datetime.utcnow() - timedelta(days=index * 9 + 2) + timedelta(minutes=75),
                duration_seconds=4500,
            )
            attempt.save()

        Notification.objects(user=user).delete()
        for title, body, kind, link in (
            ("نتیجه آزمون B1 آماده است", "نمره شما ۷۱٪ — سطح تخمینی B1.", "exam", "/dashboard/exams"),
            ("درس جدید در دوره B2", "بخش «نوشتار پیشرفته» منتشر شد.", "course", "/dashboard/courses"),
            ("شارژ کیف پول موفق", "مبلغ ۵٬۰۰۰٬۰۰۰ ریال به کیف پول شما اضافه شد.", "payment", "/dashboard/wallet"),
            ("قسمت تازه پادکست", "«اخبار آهسته» قسمت ۶ منتشر شد.", "podcast", "/podcasts"),
        ):
            Notification(user=user, title=title, body=body, kind=kind, link=link).save()

        Message.objects(user=user).delete()
        for sender, role, subject, body in (
            ("Dr. Sara Ahmadi", "teacher", "بازخورد تکلیف نوشتاری",
             "متن شما را خواندم. ساختار جملات خیلی بهتر شده؛ فقط روی حروف اضافه با Dativ بیشتر تمرین کنید."),
            ("GOTEH Academy", "staff", "برنامه کلاس زنده هفته آینده",
             "کلاس مکالمه سه‌شنبه ساعت ۱۸:۰۰ برگزار می‌شود. لینک ورود در پنل شما فعال است."),
            ("Markus Weber", "teacher", "Feedback zur Aussprache",
             "Ihre Aussprache der Umlaute ist deutlich klarer geworden. Weiter so!"),
        ):
            Message(user=user, sender_name=sender, sender_role=role, subject=subject, body=body).save()

        ListenProgress.objects(user=user).delete()
        Bookmark.objects(user=user).delete()
        for episode in episodes[:3]:
            ListenProgress(
                user=user, episode=episode, position_seconds=180, completed=False
            ).save()
        for episode in episodes[3:5]:
            Bookmark(user=user, episode=episode).save()
