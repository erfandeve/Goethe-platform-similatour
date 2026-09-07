"""Create the AI speaking course from the recorded scenes.

    python manage.py seed_speaking_course [--enroll student@goteh.de]

Scenes 1–3 set the situation and are watch-only; the border-control interview
from scene 4 onwards carries the speaking prompts.
"""

from datetime import datetime

from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.core.i18n import tt
from apps.courses.models import Category, Course, Enrollment, Instructor
from apps.learning.models import LessonVideo, Part, Question

VIDEO_BASE = "/media/courses/einreise-nach-deutschland/videos"

# (scene, de title, fa title, en title, question or None)
SCENES = [
    (1, "Vorbereitung auf die Reise", "آماده شدن برای سفر", "Getting ready to travel", None),
    (2, "Am Flughafen", "در فرودگاه", "At the airport", None),
    (3, "Der Flug", "پرواز", "The flight", None),
    (4, "ANKUNFT IN FRANKFURT", "ورود به فرانکفورت", "Arrival in Frankfurt",
     "Guten Tag. Ihren Reisepass, bitte."),
    (5, "GRENZKONTROLLE – EINREISEGRUND", "کنترل مرزی — دلیل سفر", "Border control – reason for entry",
     "Was ist der Grund für Ihre Einreise nach Deutschland?"),
    (6, "GRENZKONTROLLE – VISUM", "کنترل مرزی — ویزا", "Border control – visa",
     "Haben Sie ein Visum für Deutschland?"),
    (7, "GRENZKONTROLLE – AUFENTHALTSDAUER", "کنترل مرزی — مدت اقامت", "Border control – length of stay",
     "Wie lange werden Sie in Deutschland bleiben?"),
    (8, "GRENZKONTROLLE – UNTERKUNFT", "کنترل مرزی — محل اقامت", "Border control – accommodation",
     "Wo werden Sie während Ihres Aufenthalts wohnen?"),
    (9, "GRENZKONTROLLE – FINANZIELLE MITTEL", "کنترل مرزی — تمکن مالی", "Border control – funds",
     "Wie viel Geld haben Sie für Ihren Aufenthalt zur Verfügung?"),
    (10, "GRENZKONTROLLE – KRANKENVERSICHERUNG", "کنترل مرزی — بیمه درمانی", "Border control – health insurance",
     "Haben Sie eine Krankenversicherung?"),
    (11, "GRENZKONTROLLE – ERSTER AUFENTHALT", "کنترل مرزی — اولین سفر", "Border control – first stay",
     "Ist das Ihr erster Aufenthalt in Deutschland?"),
    (12, "GRENZKONTROLLE – ABSCHLUSS", "کنترل مرزی — پایان", "Border control – closing",
     "Gut. Vielen Dank. Willkommen in Deutschland."),
]

# Per-scene coaching material handed to the teacher model.
QUESTION_META = {
    4: (["Höflich grüßen", "Den Pass übergeben"],
        ["Höfliche Anrede", "Imperativ (Sie-Form)"],
        ["der Reisepass", "bitte schön", "hier ist"]),
    5: (["Den Reisegrund nennen", "Kurz begründen"],
        ["Nebensatz mit 'weil'", "Präpositionen: zu, für"],
        ["der Urlaub", "das Studium", "die Arbeit", "der Besuch"]),
    6: (["Bestätigen oder verneinen", "Die Visumsart nennen"],
        ["Ja/Nein-Antwort", "Perfekt"],
        ["das Visum", "das Sprachvisum", "beantragen", "gültig"]),
    7: (["Eine Zeitangabe machen"],
        ["Zeitangaben im Akkusativ", "Futur mit 'werden'"],
        ["drei Monate", "ein Jahr", "bis", "voraussichtlich"]),
    8: (["Die Adresse oder Unterkunft nennen"],
        ["Wechselpräpositionen: bei, in", "Dativ"],
        ["das Hotel", "das Studentenwohnheim", "bei Verwandten", "die Adresse"]),
    9: (["Einen Betrag nennen", "Die Finanzierung erklären"],
        ["Zahlen", "Genitiv/Dativ nach Präpositionen"],
        ["das Sperrkonto", "der Euro", "zur Verfügung", "das Stipendium"]),
    10: (["Bestätigen", "Die Versicherung benennen"],
         ["Ja/Nein-Antwort", "Artikelgebrauch"],
         ["die Krankenversicherung", "die Reiseversicherung", "abgeschlossen"]),
    11: (["Bestätigen oder verneinen", "Frühere Aufenthalte erwähnen"],
         ["Perfekt", "Temporale Angaben"],
         ["zum ersten Mal", "schon einmal", "vor zwei Jahren"]),
    12: (["Sich höflich bedanken", "Sich verabschieden"],
         ["Höflichkeitsformeln"],
         ["vielen Dank", "auf Wiedersehen", "danke schön"]),
}

PART_SPLIT = {"ankunft": range(1, 4), "grenzkontrolle": range(4, 13)}


class Command(BaseCommand):
    help = "Seed the 'Einreise nach Deutschland' speaking course."

    def add_arguments(self, parser):
        parser.add_argument("--enroll", default="student@goteh.de")

    def handle(self, *args, **options):
        course = self.build_course()
        parts = self.build_parts(course)
        videos = self.build_videos(course, parts)

        email = options["enroll"]
        user = User.objects(email=email).first()
        if user and not Enrollment.objects(user=user, course=course).first():
            Enrollment(user=user, course=course).save()
            course.students_count += 1
            course.save()
            self.stdout.write(f"Enrolled {email}.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Course '{course.slug}': {len(parts)} parts, {len(videos)} videos, "
                f"{sum(1 for v in videos if v.has_speaking_task)} speaking tasks."
            )
        )

    def build_course(self):
        course = Course.objects(slug="einreise-nach-deutschland").first() or Course(
            slug="einreise-nach-deutschland"
        )
        course.title = tt(
            "آلمانی در محیط",
            "German in Context — Speaking with an AI Teacher",
            "Deutsch im Kontext — Sprechen mit KI-Lehrerin",
        )
        course.subtitle = tt(
            "مکالمه با هوش مصنوعی در موقعیت واقعی؛ بعد از هر صحنه خودت جواب می‌دهی",
            "A real border-control scenario: after every scene you answer out loud",
            "Ein echtes Grenzkontroll-Szenario: Nach jeder Szene antworten Sie selbst",
        )
        course.description = tt(
            "«آلمانی در محیط» تمرین مکالمه در موقعیت واقعی است: صحنه‌به‌صحنه ورود به آلمان را "
            "می‌بینید و بعد از هر صحنه، پاسخ خود را "
            "با صدای خودتان می‌گویید. معلم هوش مصنوعی گفتار شما را متن می‌کند، آن را با معیار "
            "سطح زبانی‌تان بررسی می‌کند و نمره، تصحیح، توضیح گرامری و بازخورد می‌دهد.",
            "Watch the arrival in Germany scene by scene and answer each officer's question out "
            "loud. The AI teacher transcribes what you said, checks it against your CEFR level and "
            "returns a score, a corrected version, grammar notes and feedback.",
            "Sie sehen die Einreise nach Deutschland Szene für Szene und antworten nach jeder "
            "Szene laut. Die KI-Lehrerin transkribiert Ihre Antwort, prüft sie auf Ihrem "
            "GER-Niveau und gibt Punkte, eine korrigierte Fassung, Grammatikhinweise und Feedback.",
        )
        course.category = Category.objects(slug="conversation", kind="course").first()
        course.instructor = Instructor.objects(slug="markus-weber").first()
        course.level = "A2"
        course.language = "de"
        course.format = "self_paced"
        course.accent = "#22d3ee"
        course.cover = "/media/courses/einreise-nach-deutschland/cover.jpg"
        course.price = 4_900_000
        course.discount_price = 2_900_000
        course.duration_minutes = 45
        course.sessions_count = len(SCENES)
        course.tags = ["A2", "conversation", "speaking", "ai"]
        course.outcomes = [
            tt("پاسخ دادن به سؤال‌های افسر مرزی", "Answer border-control questions",
               "Fragen der Grenzkontrolle beantworten"),
            tt("تلفظ و روانی گفتار", "Pronunciation and fluency", "Aussprache und Redefluss"),
            tt("بازخورد فوری روی گرامر", "Instant grammar feedback", "Sofortiges Grammatik-Feedback"),
        ]
        course.requirements = [
            tt("میکروفون و مرورگر به‌روز", "A microphone and a modern browser",
               "Ein Mikrofon und ein aktueller Browser"),
        ]
        course.is_published = True
        course.is_featured = True
        course.starts_at = datetime.utcnow()
        course.save()
        return course

    def build_parts(self, course):
        blueprint = [
            ("ankunft", 1,
             tt("بخش ۱: سفر و ورود", "Part 1: Journey and arrival", "Teil 1: Reise und Ankunft"),
             "Teil 1 – Reise und Ankunft",
             tt("سه صحنه اول برای تماشا؛ هنوز نوبت صحبت نیست.",
                "Three scenes to watch; no speaking yet.",
                "Drei Szenen zum Ansehen; noch ohne Sprechaufgabe.")),
            ("grenzkontrolle", 2,
             tt("بخش ۲: کنترل مرزی", "Part 2: Border control", "Teil 2: Grenzkontrolle"),
             "Teil 2 – Grenzkontrolle",
             tt("بعد از هر صحنه به سؤال افسر جواب می‌دهید.",
                "After each scene you answer the officer's question.",
                "Nach jeder Szene beantworten Sie die Frage des Beamten.")),
        ]
        parts = {}
        for slug, order, title, title_de, description in blueprint:
            part = Part.objects(course=course, slug=slug).first() or Part(
                course=course, slug=slug
            )
            part.order = order
            part.title = title
            part.title_de = title_de
            part.description = description
            part.is_published = True
            part.save()
            parts[slug] = part
        return parts

    def build_videos(self, course, parts):
        videos = []
        for scene, de, fa, en, prompt in SCENES:
            part_slug = next(
                key for key, scenes in PART_SPLIT.items() if scene in scenes
            )
            slug = f"einreise-szene-{scene:02d}"
            video = LessonVideo.objects(slug=slug).first() or LessonVideo(slug=slug)
            video.course = course
            video.part = parts[part_slug]
            video.order = scene
            video.title = tt(fa, en, de.title() if de.isupper() else de)
            video.title_de = de
            video.scene_label = f"SZENE {scene} – {de}" if scene >= 4 else f"SZENE {scene}"
            video.video_url = f"{VIDEO_BASE}/szene-{scene:02d}.mp4"
            video.cefr_level = "A2"
            video.is_published = True

            if prompt:
                points, grammar, vocabulary = QUESTION_META.get(scene, ([], [], []))
                video.question = Question(
                    prompt_de=prompt,
                    prompt=tt(fa, en, prompt),
                    hint=tt(
                        "با جمله کامل و مؤدبانه جواب بده.",
                        "Answer politely in full sentences.",
                        "Antworten Sie höflich in ganzen Sätzen.",
                    ),
                    expected_points=points,
                    grammar_topics=grammar,
                    vocabulary=vocabulary,
                    min_words=2,
                )
            else:
                video.question = None

            video.save()
            videos.append(video)
        return videos
