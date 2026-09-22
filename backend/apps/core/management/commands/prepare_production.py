"""Turn a seeded database into one fit for the public site:

    python manage.py prepare_production --admin-email you@example.com --admin-password '…'

The seeders fill the catalogue — courses, exams, podcasts, articles — which a
live site keeps. They also invent things a live site must not show:

- a demo account whose password is printed in the README, with admin rights;
- ratings, review counts, student and play counts, and reviews signed with
  made-up names. The course pages publish ratings to Google as structured
  data, and invented review markup is grounds for a manual penalty.

This command keeps the catalogue, removes the demo account and every trace of
it, resets the invented numbers to what really happened (zero, at launch), and
creates the real admin. It is idempotent and safe to run again.
"""

import secrets

from django.core.management.base import BaseCommand, CommandError

from apps.accounts.models import Message, Notification, User, WalletTransaction

DEMO_EMAILS = ("student@goteh.de",)


class Command(BaseCommand):
    help = "Remove demo accounts and invented numbers; create the real admin."

    def add_arguments(self, parser):
        parser.add_argument("--admin-email", default="", help="The real back-office account.")
        parser.add_argument(
            "--admin-password",
            default="",
            help="At least 12 characters. Omit to keep an existing admin's password.",
        )
        parser.add_argument(
            "--keep-stats",
            action="store_true",
            help="Leave ratings and counters alone (only remove the demo account).",
        )

    def handle(self, *args, **options):
        email = options["admin_email"].strip().lower()
        password = options["admin_password"]
        if email and password and len(password) < 12:
            raise CommandError("Use an admin password of at least 12 characters.")

        self.remove_demo_accounts()
        if not options["keep_stats"]:
            self.reset_invented_numbers()
        if email:
            self.ensure_admin(email, password)
        elif not User.objects(is_staff=True).count():
            self.stdout.write(
                self.style.WARNING(
                    "No admin account exists. Run again with --admin-email and --admin-password."
                )
            )
        self.stdout.write(self.style.SUCCESS("Database is ready for production."))

    # ------------------------------------------------------------------

    def remove_demo_accounts(self):
        from apps.billing.models import CouponRedemption, Subscription
        from apps.courses.models import Cart, Enrollment, Order
        from apps.exams.models import ExamAccess, ExamAttempt
        from apps.learning.models import SpeakingAttempt, VideoProgress

        for email in DEMO_EMAILS:
            user = User.objects(email=email).first()
            if not user:
                continue
            for model in (
                Enrollment, Order, Cart, ExamAccess, ExamAttempt, Subscription,
                SpeakingAttempt, VideoProgress, CouponRedemption,
                WalletTransaction, Notification, Message,
            ):
                model.objects(user=user).delete()
            user.delete()
            self.stdout.write(f"Removed demo account {email} and its activity.")

    def reset_invented_numbers(self):
        from apps.courses.models import Course, Instructor, Review
        from apps.exams.models import Exam, ExamAttempt
        from apps.podcasts.models import Episode, Podcast

        # Seeded reviews carry a name but no account; real ones have a user.
        fake = Review.objects(user=None)
        removed = fake.count()
        fake.delete()

        from apps.courses.models import Enrollment

        for course in Course.objects():
            ratings = [review.rating for review in Review.objects(course=course)]
            course.rating = round(sum(ratings) / len(ratings), 1) if ratings else 0
            course.reviews_count = len(ratings)
            course.students_count = Enrollment.objects(course=course).count()
            course.save()

        for exam in Exam.objects():
            exam.rating = 0
            exam.attempts_count = ExamAttempt.objects(exam=exam).count()
            exam.save()

        for podcast in Podcast.objects():
            podcast.rating = 0
            podcast.plays = 0
            podcast.save()
        Episode.objects().update(set__plays=0)

        for instructor in Instructor.objects():
            instructor.rating = 0
            instructor.students = 0
            instructor.save()

        self.stdout.write(
            f"Removed {removed} seeded reviews; ratings and counters now reflect real activity."
        )

    def ensure_admin(self, email, password):
        user = User.objects(email=email).first()
        created = user is None
        if created:
            if not password:
                raise CommandError("A new admin needs --admin-password.")
            user = User(email=email, first_name="Admin")
        if password:
            user.set_password(password)
        elif created:
            user.set_password(secrets.token_urlsafe(24))
        user.is_staff = True
        user.is_active = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"{'Created' if created else 'Updated'} admin account {email}.")
        )
