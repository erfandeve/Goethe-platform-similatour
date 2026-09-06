"""Fill a fresh database in one step: python manage.py bootstrap

Runs every seeder in dependency order and hands the demo student the keys to
the back office, so a newly deployed instance is browsable immediately.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.accounts.models import User

STEPS = [
    ("seed", {"flush": True}),          # courses, podcasts, users, wallet
    ("seed_b2", {}),                    # the Goethe B2 simulator
    ("seed_speaking_course", {}),       # the AI speaking scenes
    ("seed_plans", {}),                 # the three subscription tiers
]


class Command(BaseCommand):
    help = "Seed a fresh deployment with the full demo dataset."

    def add_arguments(self, parser):
        parser.add_argument(
            "--staff",
            default="student@goteh.de",
            help="Email to grant back-office access to.",
        )

    def handle(self, *args, **options):
        for name, kwargs in STEPS:
            self.stdout.write(self.style.MIGRATE_HEADING(f"→ {name}"))
            call_command(name, **kwargs)

        email = options["staff"].lower().strip()
        user = User.objects(email=email).first()
        if user:
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Staff access granted to {email}."))
        else:
            self.stdout.write(self.style.WARNING(f"No user {email}; skipped staff grant."))

        self.stdout.write(self.style.SUCCESS("Bootstrap complete."))
