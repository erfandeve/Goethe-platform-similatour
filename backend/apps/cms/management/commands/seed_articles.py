"""Load the shipped articles: python manage.py seed_articles [--reset]

Each article exists in Persian, English and German. They are seeded rather than
hard-coded so the back office can edit them, and re-running leaves edited ones
alone unless --reset is passed.
"""

from django.core.management.base import BaseCommand

from apps.cms.content import goethe_registration, simulator, study_german
from apps.cms.models import Article

MODULES = (simulator, study_german, goethe_registration)


class Command(BaseCommand):
    help = "Create or refresh the shipped articles in all three languages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Overwrite articles that already exist instead of leaving edits alone.",
        )

    def handle(self, *args, **options):
        created = updated = skipped = 0

        for module in MODULES:
            article = Article.objects(slug=module.SLUG).first()
            if article and not options["reset"]:
                skipped += 1
                continue

            if not article:
                article = Article(slug=module.SLUG)
                created += 1
            else:
                updated += 1

            for field, value in module.META.items():
                if field != "slug":
                    setattr(article, field, value)
            article.body = module.BODY
            article.faq = module.FAQ
            article.is_published = True
            article.save()

            counts = " / ".join(
                f"{code}: {article.word_count(code)}" for code in ("fa", "en", "de")
            )
            self.stdout.write(f"  {article.slug} — {counts} words")

        self.stdout.write(
            self.style.SUCCESS(
                f"Articles — created {created}, updated {updated}, left alone {skipped}."
            )
        )
