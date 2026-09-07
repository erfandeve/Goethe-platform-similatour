"""Rebuild every simulator in the Goethe digital format:

    python manage.py seed_levels [--only a1,b1]

B2 keeps its own command because its material is transcribed from the
published Modellsatz; everything else is written in-house against the same
task shapes, so one builder covers all of them.
"""

from django.core.management.base import BaseCommand

from apps.exams.content.levels import a1, a2, b1, c1, frequent
from apps.exams.content.levels._build import build_modules
from apps.exams.content.levels._build import build_module
from apps.exams.models import Exam

LEVELS = {
    "a1": (a1, "simulator-a1", "Goethe-Zertifikat A1: Start Deutsch 1"),
    "a2": (a2, "simulator-a2", "Goethe-Zertifikat A2"),
    "b1": (b1, "simulator-b1", "Goethe-Zertifikat B1"),
    "c1": (c1, "simulator-c1", "Goethe-Zertifikat C1"),
}

# The high-frequency sets are two modules, not a full sitting.
FREQUENT = {
    "frequent-b2": (
        (frequent.B2_LESEN, frequent.B2_HOEREN),
        "B2 · häufige Aufgaben",
        ("پرتکرارهای B2", "B2 High-Frequency Set", "B2 · Häufige Aufgaben"),
        ("سؤال‌ها و الگوهایی که در آزمون‌های اخیر B2 بارها تکرار شده‌اند.",
         "The questions and patterns that keep coming back in recent B2 exams.",
         "Aufgaben und Muster, die in jüngeren B2-Prüfungen immer wieder auftauchen."),
    ),
    "frequent-c1": (
        (frequent.C1_LESEN, frequent.C1_HOEREN),
        "C1 · häufige Aufgaben",
        ("پرتکرارهای C1", "C1 High-Frequency Set", "C1 · Häufige Aufgaben"),
        ("سخت‌ترین الگوهای C1، پشت سر هم، برای وقتی که کارنامه ضعف را نشان داده.",
         "The hardest C1 patterns back to back, for when the report has named the gap.",
         "Die schwersten C1-Muster am Stück, wenn die Auswertung die Lücke benannt hat."),
    ),
}


class Command(BaseCommand):
    help = "Rebuild the A1, A2, B1 and C1 simulators in the Goethe module format."

    def add_arguments(self, parser):
        parser.add_argument(
            "--only",
            default="",
            help="Comma-separated level keys to rebuild, e.g. a1,b1. Default: all.",
        )

    def handle(self, *args, **options):
        wanted = [key.strip() for key in options["only"].split(",") if key.strip()]
        keys = wanted or list(LEVELS)

        for key in keys:
            if key not in LEVELS:
                self.stdout.write(self.style.WARNING(f"Unknown level '{key}', skipped."))
                continue

            module, slug, board = LEVELS[key]
            exam = Exam.objects(slug=slug).first()
            if not exam:
                self.stdout.write(self.style.ERROR(f"{slug} missing — run `manage.py seed` first."))
                continue

            exam.modules = build_modules(module)
            exam.sections = []  # the modules replace the flat placeholder sections
            exam.duration_minutes = sum(m.duration_minutes for m in exam.modules)
            exam.exam_board = board
            exam.save()

            self._report(exam)

        for slug, (specs, board, title, description) in FREQUENT.items():
            if wanted and slug not in wanted and slug.split("-")[-1] not in wanted:
                continue
            self._build_frequent(slug, specs, board, title, description)

    def _build_frequent(self, slug, specs, board, title, description):
        from apps.core.i18n import tt

        exam = Exam.objects(slug=slug).first()
        created = exam is None
        if created:
            # Mirror the pricing and level of the simulator it belongs to.
            level = slug.split("-")[-1].upper()
            sibling = Exam.objects(slug=f"simulator-{level.lower()}").first()
            exam = Exam(
                slug=slug,
                kind="frequent",
                level=level,
                language="de",
                price=sibling.price if sibling else 4_000_000,
                accent=sibling.accent if sibling else "#f472b6",
                is_published=True,
            )

        exam.title = tt(*title)
        exam.subtitle = tt(*description)
        exam.description = tt(*description)
        exam.exam_board = board
        exam.modules = [build_module(spec) for spec in specs]
        exam.sections = []
        exam.duration_minutes = sum(m.duration_minutes for m in exam.modules)
        exam.save()
        self._report(exam, created=created)

    def _report(self, exam, created=False):
        shape = " · ".join(f"{m.skill} {len(m.parts)}×{m.items_count}" for m in exam.modules)
        mark = "new " if created else "    "
        self.stdout.write(
            self.style.SUCCESS(
                f"{mark}{exam.slug:14} {exam.questions_count:3} items, "
                f"{exam.max_score:3} auto-scored, {exam.duration_minutes:3} min — {shape}"
            )
        )
