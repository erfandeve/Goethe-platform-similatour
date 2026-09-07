"""Create the three subscription tiers: python manage.py seed_plans"""

from django.core.management.base import BaseCommand

from apps.billing.models import Plan
from apps.core.i18n import tt

T = 10  # prices are quoted in Toman; stored in Rial

PLANS = [
    (
        "exam-codes",
        1,
        ("اشتراک کدهای آزمون", "Exam Codes Pass", "Prüfungscodes-Abo"),
        ("دسترسی به تمام کدهای آزمون", "Access to every exam code", "Zugang zu allen Prüfungscodes"),
        2_000_000 * T,
        ["exam_codes"],
        [
            ("همه کدهای هر آزمونی که باز کرده‌ای", "Every code of any exam you own",
             "Alle Codes jeder freigeschalteten Prüfung"),
            ("کارنامه تفکیکی و پاسخ تشریحی", "Per-skill report and explanations",
             "Auswertung pro Fertigkeit mit Erklärungen"),
        ],
        "#22d3ee",
        "",
    ),
    (
        "all-exams",
        2,
        ("اشتراک کامل آزمون‌ها", "All Exams Pass", "Alle-Prüfungen-Abo"),
        ("دسترسی به تمام آزمون‌ها و همه کدهایشان",
         "Access to every exam and all of its codes",
         "Zugang zu allen Prüfungen und deren Codes"),
        4_000_000 * T,
        ["exam_codes", "exams"],
        [
            ("همه شبیه‌سازها از A1 تا C1", "Every simulator from A1 to C1",
             "Alle Simulatoren von A1 bis C1"),
            ("سؤالات پرتکرار B2 و C1", "High-frequency sets for B2 and C1",
             "Häufigkeitssets für B2 und C1"),
            ("همه کدهای آزمون", "Every exam code", "Alle Prüfungscodes"),
        ],
        "#f59e0b",
        "",
    ),
    (
        "full-access",
        3,
        ("اشتراک کامل آکادمی", "Full Academy Pass", "Komplett-Abo"),
        ("همه آزمون‌ها و کدها، مکالمه با هوش مصنوعی و تمام دوره‌ها",
         "Every exam and code, the AI speaking course and all courses",
         "Alle Prüfungen und Codes, KI-Sprechen und alle Kurse"),
        5_900_000 * T,
        ["exam_codes", "exams", "courses", "speaking", "podcasts"],
        [
            ("تمام دوره‌های آموزشی", "Every course", "Alle Kurse"),
            ("مکالمه با معلم هوش مصنوعی", "AI speaking teacher", "KI-Sprechlehrerin"),
            ("همه آزمون‌ها و کدها", "All exams and codes", "Alle Prüfungen und Codes"),
            ("قسمت‌های ویژه پادکست", "Premium podcast episodes", "Premium-Podcastfolgen"),
        ],
        "#a855f7",
        "پرفروش",
    ),
]


class Command(BaseCommand):
    help = "Seed the subscription plans."

    def handle(self, *args, **options):
        for slug, order, title, description, price, perks, highlights, accent, badge in PLANS:
            plan = Plan.objects(slug=slug).first() or Plan(slug=slug)
            plan.order = order
            plan.title = tt(*title)
            plan.description = tt(*description)
            plan.price = price
            plan.perks = perks
            plan.highlights = [tt(*item) for item in highlights]
            plan.accent = accent
            plan.badge = badge
            plan.duration_days = 365
            plan.is_published = True
            plan.is_featured = slug == "full-access"
            plan.save()
            self.stdout.write(f"  {slug}: {price:,} Rial · {', '.join(perks)}")

        self.stdout.write(self.style.SUCCESS(f"{len(PLANS)} plans ready."))
