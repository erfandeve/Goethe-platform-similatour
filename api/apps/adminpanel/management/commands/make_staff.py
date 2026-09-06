"""Grant or revoke back-office access:

    python manage.py make_staff erfan@example.com
    python manage.py make_staff erfan@example.com --revoke
"""

from django.core.management.base import BaseCommand

from apps.accounts.models import User


class Command(BaseCommand):
    help = "Grant (or revoke) staff access for a user."

    def add_arguments(self, parser):
        parser.add_argument("email")
        parser.add_argument("--revoke", action="store_true")

    def handle(self, *args, **options):
        user = User.objects(email=options["email"].lower().strip()).first()
        if not user:
            self.stdout.write(self.style.ERROR(f"No user with email {options['email']}."))
            return
        user.is_staff = not options["revoke"]
        user.save()
        state = "revoked" if options["revoke"] else "granted"
        self.stdout.write(self.style.SUCCESS(f"Staff access {state} for {user.email}."))
