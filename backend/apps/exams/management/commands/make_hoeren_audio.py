"""Render the Hören tracks from their transcripts:

    python manage.py make_hoeren_audio [--only a1,b1] [--force]

Uses the system's German voices, so a fresh checkout can produce playable
listening modules without a recording session. Existing files are kept unless
--force is passed.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.exams.content.levels._audio import SCRIPTS

# The scripts name speakers briefly; `say` needs the exact German voice. Bare
# names are dangerous: "Sandy" exists in fifteen languages and "Markus" not at
# all, and `say` silently falls back to another voice instead of failing —
# German read with an English accent.
VOICES = {
    "Anna": "Anna",
    "Sandy": "Sandy (German (Germany))",
    "Markus": "Eddy (German (Germany))",
    "Reed": "Reed (German (Germany))",
    "Flo": "Flo (German (Germany))",
    "Shelley": "Shelley (German (Germany))",
}

# A short pause between turns, so items stay tellable apart.
GAP_SECONDS = 0.7
RATE = 165  # words per minute; the exam recordings are deliberately unhurried


class Command(BaseCommand):
    help = "Render the Hören audio for the in-house levels from their transcripts."

    def add_arguments(self, parser):
        parser.add_argument("--only", default="", help="Comma-separated levels, e.g. a1,b1.")
        parser.add_argument("--force", action="store_true", help="Overwrite existing files.")

    def handle(self, *args, **options):
        if not shutil.which("say") or not shutil.which("afconvert"):
            self.stdout.write(
                self.style.ERROR(
                    "`say` and `afconvert` are required (macOS). Provide the audio files "
                    "manually on other platforms."
                )
            )
            return

        wanted = [key.strip() for key in options["only"].split(",") if key.strip()]
        made = kept = 0

        for level, tracks in SCRIPTS.items():
            if wanted and level not in wanted:
                continue

            out_dir = Path(settings.MEDIA_ROOT) / "exams" / level / "hoeren"
            out_dir.mkdir(parents=True, exist_ok=True)

            for stem, lines in tracks.items():
                target = out_dir / f"{stem}.m4a"
                if target.exists() and not options["force"]:
                    kept += 1
                    continue

                self.stdout.write(f"  rendering {level}/{stem} …")
                self._check_voices(lines)
                self._render(lines, target)
                made += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {level}/{stem}.m4a — {target.stat().st_size // 1024} KB"
                    )
                )

        self.stdout.write(self.style.SUCCESS(f"Audio: {made} rendered, {kept} already present."))

    @staticmethod
    def _check_voices(lines):
        unknown = sorted({voice for voice, _ in lines if voice not in VOICES})
        if unknown:
            raise CommandError(f"No German voice mapped for: {', '.join(unknown)}")

    def _render(self, lines, target):
        """One WAV per turn, concatenated, then converted to m4a.

        WAV rather than AIFF because Python 3.13 dropped the `aifc` module, and
        `wave` is the one audio container still in the standard library.
        """
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            pieces = []

            for index, (voice, text) in enumerate(lines):
                piece = tmp / f"{index:03d}.wav"
                # A trailing silence keeps consecutive turns from running together.
                spoken = f"{text} [[slnc {int(GAP_SECONDS * 1000)}]]"
                subprocess.run(
                    [
                        "say", "-v", VOICES.get(voice, voice), "-r", str(RATE),
                        "--data-format=LEI16@22050", "-o", str(piece), spoken,
                    ],
                    check=True,
                )
                pieces.append(piece)

            joined = tmp / "joined.wav"
            self._concat(pieces, joined)

            subprocess.run(
                ["/usr/bin/afconvert", "-f", "m4af", "-d", "aac", "-b", "64000",
                 str(joined), str(target)],
                check=True,
            )

    @staticmethod
    def _concat(pieces, out_path):
        import wave

        with wave.open(str(pieces[0]), "rb") as first:
            params = first.getparams()

        with wave.open(str(out_path), "wb") as out:
            out.setparams(params)
            for piece in pieces:
                with wave.open(str(piece), "rb") as src:
                    out.writeframes(src.readframes(src.getnframes()))
