"""Build the Goethe-format B2 simulator: python manage.py seed_b2"""

from django.core.management.base import BaseCommand

from apps.core.i18n import tt
from apps.exams.content import b2_hoeren as H
from apps.exams.content import b2_lesen as L
from apps.exams.content import b2_schreiben as S
from apps.exams.models import (
    AudioTrack,
    Exam,
    ExamItem,
    ExamModule,
    ExamOption,
    ExamPart,
    StimulusBlock,
)


def options(pairs):
    """`[("a", "text"), …]` → option documents whose label is the letter."""
    return [ExamOption(key=key, label=key, text=text) for key, text in pairs]


def mcq_items(rows):
    """Rows of `(number, prompt, [(key, text)…], answer)`."""
    return [
        ExamItem(
            number=number,
            prompt=prompt,
            options=[ExamOption(key=key, label=key, text=text) for key, text in choices],
            answer=answer,
        )
        for number, prompt, choices, answer in rows
    ]


class Command(BaseCommand):
    help = "Seed the Goethe-Zertifikat B2 model set (Lesen, Hören, Schreiben)."

    def handle(self, *args, **options_):
        exam = Exam.objects(slug="simulator-b2").first()
        if not exam:
            self.stdout.write(self.style.ERROR("Run `manage.py seed` first."))
            return

        exam.modules = [self.lesen(), self.hoeren(), self.schreiben()]
        exam.sections = []  # the Goethe modules replace the placeholder sections
        exam.duration_minutes = sum(m.duration_minutes for m in exam.modules)
        exam.exam_board = "Goethe-Zertifikat B2"
        exam.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"B2 rebuilt: {len(exam.modules)} modules, {exam.questions_count} items, "
                f"{exam.max_score} auto-scored points."
            )
        )

    # -- Lesen ---------------------------------------------------------------

    def lesen(self):
        teil1 = ExamPart(
            number=1,
            part_type="match_person",
            title=tt("لزن ۱", "Lesen 1", "Lesen 1"),
            instructions=tt(
                "در یک انجمن اینترنتی می‌خوانید که مردم درباره مینیمالیسم در زندگی روزمره چه فکر می‌کنند. "
                "هر جمله به کدام‌یک از این چهار نفر مربوط است؟ هر شخص می‌تواند چند بار انتخاب شود.",
                "You read in a forum how people think about minimalism in everyday life. "
                "Which of the four people does each statement apply to? People can be chosen more than once.",
                "Sie lesen in einem Forum, wie Menschen über Minimalismus im täglichen Leben denken. "
                "Auf welche der vier Personen treffen die einzelnen Aussagen zu? Die Personen können "
                "mehrmals gewählt werden.",
            ),
            work_minutes=18,
            stimulus_title="Moderne Lebensformen",
            blocks=[
                StimulusBlock(kind="person", label=key, title=name, text=text)
                for key, name, text in L.PERSONS
            ],
            options=[
                ExamOption(key=key, label=name) for key, name, _ in L.PERSONS
            ],
            example_prompt="Wer will nur die wirklich notwendigen Dinge haben?",
            example_answer="a",
            items=[
                ExamItem(number=number, prompt=prompt, answer=answer)
                for number, prompt, answer in L.TEIL1_ITEMS
            ],
        )

        teil2 = ExamPart(
            number=2,
            part_type="gap_drag",
            title=tt("لزن ۲", "Lesen 2", "Lesen 2"),
            instructions=tt(
                "در یک مجله مقاله‌ای درباره تاریخ سفر می‌خوانید. کدام جمله در کدام جای خالی می‌نشیند؟ "
                "دو جمله اضافه است.",
                "You read a magazine article about the history of travel. Which sentences fit the "
                "gaps? Two sentences do not fit.",
                "Sie lesen in einer Zeitschrift einen Artikel über die Geschichte des Reisens. "
                "Welche Sätze passen in die Lücken? Zwei Sätze passen nicht.",
            ),
            work_minutes=12,
            stimulus_title="Reisefieber",
            stimulus_subtitle="Heute verreist fast jeder, früher aber kaum jemand.",
            stimulus_image="/media/exams/b2/lesen/reisefieber.jpg",
            blocks=[
                StimulusBlock(kind="paragraph", text=text) for text in L.TEIL2_PARAGRAPHS
            ],
            options=options(L.TEIL2_OPTIONS),
            example_prompt="0",
            example_answer="Denn immer mehr Menschen können es sich leisten zu verreisen.",
            items=[
                ExamItem(number=number, prompt=f"Lücke {number}", answer=answer)
                for number, answer in L.TEIL2_ITEMS
            ],
        )

        teil3 = ExamPart(
            number=3,
            part_type="mcq",
            title=tt("لزن ۳", "Lesen 3", "Lesen 3"),
            instructions=tt(
                "در یک روزنامه مقاله‌ای درباره رفتار بیماران در عصر اینترنت می‌خوانید. "
                "برای هر سؤال گزینه درست را انتخاب کنید.",
                "You read a newspaper article about how sick people behave in the age of the "
                "internet. Choose the correct answer for each task.",
                "Sie lesen in einer Zeitung einen Artikel über das Verhalten von Kranken in Zeiten "
                "des Internets. Wählen Sie bei jeder Aufgabe die richtige Lösung.",
            ),
            work_minutes=12,
            stimulus_title="Doktor Google",
            blocks=[
                StimulusBlock(kind="paragraph", text=text) for text in L.TEIL3_PARAGRAPHS
            ],
            example_prompt="Immer mehr Kranke in Deutschland …",
            example_answer="b – vertrauen auf Hilfe im Internet.",
            items=mcq_items(L.TEIL3_ITEMS),
        )

        teil4 = ExamPart(
            number=4,
            part_type="match_heading",
            title=tt("لزن ۴", "Lesen 4", "Lesen 4"),
            instructions=tt(
                "در یک مجله نظرهایی درباره سبک زندگی «کوچ‌نشین دیجیتال» می‌خوانید. هر نظر به کدام "
                "عنوان می‌خورد؟ یک نظر اضافه است. نظر a نمونه است و دوباره استفاده نمی‌شود.",
                "You read opinions in a magazine about the “digital nomad” way of life. Which "
                "opinion matches which heading? One opinion does not fit; opinion a is the example.",
                "Sie lesen in einer Zeitschrift Meinungsäußerungen zu dem Lebensmodell „digitale "
                "Nomaden“. Welche Äußerung passt zu welcher Überschrift? Eine Äußerung passt nicht. "
                "Die Äußerung a ist das Beispiel und kann nicht noch einmal verwendet werden.",
            ),
            work_minutes=12,
            blocks=[
                StimulusBlock(kind="statement", label=key, author=author, text=text)
                for key, author, text in L.TEIL4_STATEMENTS
            ],
            options=[
                ExamOption(key=key, label=key, author=author, text=text)
                for key, author, text in L.TEIL4_STATEMENTS
            ],
            example_prompt="Familie und Beruf kann man vereinbaren",
            example_answer="a",
            items=[
                ExamItem(number=number, prompt=prompt, answer=answer)
                for number, prompt, answer in L.TEIL4_ITEMS
            ],
        )

        teil5 = ExamPart(
            number=5,
            part_type="match_paragraph",
            title=tt("لزن ۵", "Lesen 5", "Lesen 5"),
            instructions=tt(
                "می‌خواهید در دانشگاه برمن تحصیل کنید و آیین‌نامه آموزشی را می‌خوانید. کدام عنوان "
                "از فهرست مطالب به کدام بند می‌خورد؟ چهار عنوان لازم نمی‌شود.",
                "You want to study at the University of Bremen and read the study regulations. "
                "Which headings from the table of contents match the paragraphs? Four headings are "
                "not needed.",
                "Sie möchten an der Universität Bremen studieren und lesen die Studienordnung. "
                "Welche der Überschriften aus dem Inhaltsverzeichnis passen zu den Paragrafen? "
                "Vier Überschriften werden nicht gebraucht.",
            ),
            work_minutes=6,
            stimulus_title="Studienordnung",
            stimulus_subtitle="für den Bachelorstudiengang Theaterwissenschaft",
            blocks=[
                StimulusBlock(kind="section", label=label, text=text)
                for number, label, text, _ in L.TEIL5_PARAGRAPHS
                if number
            ],
            options=[ExamOption(key=key, label=key, text=text) for key, text in L.TEIL5_HEADINGS],
            example_prompt="§ 0 — Das Studium kann nur zum Wintersemester aufgenommen werden.",
            example_answer="c",
            items=[
                ExamItem(number=number, prompt=label, answer=answer)
                for number, label, _, answer in L.TEIL5_PARAGRAPHS
                if number
            ],
        )

        return ExamModule(
            skill="lesen",
            title=tt("درک مطلب", "Reading", "Lesen"),
            intro=tt(
                "ماژول لزن پنج بخش دارد. متن‌ها را می‌خوانید و به سؤال‌ها پاسخ می‌دهید.",
                "The Lesen module has five parts. You read several texts and solve the tasks.",
                "Das Modul Lesen hat fünf Teile. Sie lesen mehrere Texte und lösen dazu Aufgaben.",
            ),
            duration_minutes=65,
            max_points=30,
            parts=[teil1, teil2, teil3, teil4, teil5],
        )

    # -- Hören ---------------------------------------------------------------

    def hoeren(self):
        teil1_items = []
        for number, prompt, choices, answer, track in H.TEIL1_ITEMS:
            teil1_items.append(
                ExamItem(
                    number=number,
                    prompt=prompt,
                    options=[ExamOption(key=key, label=label) for key, label in choices],
                    answer=answer,
                    audio_index=track,
                )
            )

        teil1 = ExamPart(
            number=1,
            part_type="listening_mixed",
            title=tt("هؤرن ۱", "Hören 1", "Hören 1"),
            instructions=tt(
                "پنج گفت‌وگو و اظهارنظر می‌شنوید. هر متن را یک بار می‌شنوید و برای هر متن دو سؤال "
                "پاسخ می‌دهید.",
                "You hear five conversations and statements. You hear each text once and solve two "
                "tasks per text.",
                "Sie hören fünf Gespräche und Äußerungen. Sie hören jeden Text einmal. Zu jedem "
                "Text lösen Sie zwei Aufgaben. Wählen Sie bei jeder Aufgabe die richtige Lösung.",
            ),
            work_minutes=10,
            audio=[
                AudioTrack(url=url, label=label, plays=1, pre_read_seconds=15, covers=covers)
                for url, label, covers in H.TEIL1_TRACKS
            ],
            items=teil1_items,
        )

        teil2 = ExamPart(
            number=2,
            part_type="mcq",
            title=tt("هؤرن ۲", "Hören 2", "Hören 2"),
            instructions=tt(
                "در رادیو مصاحبه‌ای با یک شخصیت علمی می‌شنوید. متن را دو بار می‌شنوید.",
                "You hear a radio interview with a scientist. You hear the text twice.",
                "Sie hören im Radio ein Interview mit einer Persönlichkeit aus der Wissenschaft. "
                "Sie hören den Text zweimal. Wählen Sie bei jeder Aufgabe die richtige Lösung.",
            ),
            work_minutes=10,
            audio=[
                AudioTrack(
                    url=f"{H.AUDIO_BASE}/teil2.m4a",
                    label="Aufgaben 11 bis 16",
                    plays=2,
                    pre_read_seconds=90,
                    covers=list(range(11, 17)),
                )
            ],
            items=mcq_items(H.TEIL2_ITEMS),
        )

        teil3 = ExamPart(
            number=3,
            part_type="mcq",
            title=tt("هؤرن ۳", "Hören 3", "Hören 3"),
            instructions=tt(
                "در رادیو گفت‌وگویی با چند نفر درباره شکل‌های جایگزین سکونت می‌شنوید. متن را یک بار "
                "می‌شنوید. در هر سؤال انتخاب کنید: چه کسی این را می‌گوید؟",
                "You hear a radio discussion with several people about alternative ways of living. "
                "You hear the text once. For each task decide: who says this?",
                "Sie hören im Radio ein Gespräch mit mehreren Personen. Die Personen sprechen über "
                "alternative Wohnformen. Sie hören den Text einmal. Wählen Sie bei jeder Aufgabe: "
                "Wer sagt das?",
            ),
            work_minutes=8,
            audio=[
                AudioTrack(
                    url=f"{H.AUDIO_BASE}/teil3.m4a",
                    label="Aufgaben 17 bis 22",
                    plays=1,
                    pre_read_seconds=60,
                    covers=list(range(17, 23)),
                )
            ],
            options=[
                ExamOption(key=key, label=name, author=role)
                for key, name, role in H.TEIL3_SPEAKERS
            ],
            example_prompt="In deutschen Großstädten spielen alternative Wohnformen eine Rolle.",
            example_answer="a",
            items=[
                ExamItem(number=number, prompt=prompt, answer=answer)
                for number, prompt, answer in H.TEIL3_ITEMS
            ],
        )

        teil4 = ExamPart(
            number=4,
            part_type="mcq",
            title=tt("هؤرن ۴", "Hören 4", "Hören 4"),
            instructions=tt(
                "یک سخنرانی کوتاه درباره «روش‌های بهتر کار کردن» می‌شنوید. متن را دو بار می‌شنوید.",
                "You hear a short lecture on “better working techniques”. You hear the text twice.",
                "Sie hören einen kurzen Vortrag. Der Redner spricht über das Thema „Bessere "
                "Arbeitstechniken“. Sie hören den Text zweimal. Wählen Sie bei jeder Aufgabe die "
                "richtige Lösung.",
            ),
            work_minutes=12,
            audio=[
                AudioTrack(
                    url=f"{H.AUDIO_BASE}/teil4.m4a",
                    label="Aufgaben 23 bis 30",
                    plays=2,
                    pre_read_seconds=90,
                    covers=list(range(23, 31)),
                )
            ],
            items=mcq_items(H.TEIL4_ITEMS),
        )

        return ExamModule(
            skill="hoeren",
            title=tt("درک شنیداری", "Listening", "Hören"),
            intro=tt(
                "ماژول هؤرن چهار بخش دارد. اول سؤال‌ها را بخوانید، بعد متن را بشنوید.",
                "The Hören module has four parts. Read the tasks first, then listen to the text.",
                "Das Modul Hören hat vier Teile. Lesen Sie jeweils zuerst die Aufgaben und hören "
                "Sie dann den Text dazu.",
            ),
            duration_minutes=40,
            max_points=30,
            parts=[teil1, teil2, teil3, teil4],
        )

    # -- Schreiben -----------------------------------------------------------

    def schreiben(self):
        parts = []
        for index, (data, number, kind) in enumerate(
            ((S.TEIL1, 1, "Forumsbeitrag"), (S.TEIL2, 2, "Nachricht")), start=0
        ):
            parts.append(
                ExamPart(
                    number=number,
                    part_type="writing",
                    title=tt(f"شرایبن {number}", f"Schreiben {number}", f"Schreiben {number}"),
                    instructions=tt(data["instructions"], data["instructions"], data["instructions"]),
                    work_minutes=data["work_minutes"],
                    stimulus_image=data["image"],
                    stimulus_intro=data["note"],
                    blocks=[
                        StimulusBlock(kind="bullet", text=bullet) for bullet in data["bullets"]
                    ],
                    min_words=data["min_words"],
                    items=[
                        ExamItem(
                            number=number,
                            prompt="Schreiben Sie Ihren Text in dieses Feld.",
                            points=0,
                        )
                    ],
                )
            )

        return ExamModule(
            skill="schreiben",
            title=tt("نگارش", "Writing", "Schreiben"),
            intro=tt(
                "ماژول شرایبن دو بخش دارد: یک پست انجمن و یک پیام. می‌توانید با هر بخشی شروع کنید.",
                "The Schreiben module has two parts: a forum post and a message. You may start "
                "with either task.",
                "Das Modul Schreiben hat zwei Teile. In Teil 1 schreiben Sie einen Forumsbeitrag, "
                "in Teil 2 eine Nachricht. Sie können mit jeder Aufgabe beginnen.",
            ),
            duration_minutes=75,
            max_points=0,
            parts=parts,
        )
