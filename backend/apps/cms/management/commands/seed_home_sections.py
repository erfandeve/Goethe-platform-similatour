"""Fill the home page with its editable sections: python manage.py seed_home_sections

These are the blocks a search engine actually reads on the landing page. They
are seeded rather than hard-coded so the back office can rewrite, reorder or
remove any of them without a deploy.
"""

from django.core.management.base import BaseCommand

from apps.cms.models import HomeSection, SectionItem
from apps.core.i18n import tt

EXAM_COVER = "/media/covers/exams/b2-cover-8f00ecf8.png"
COURSE_COVER = "/media/covers/courses/einreise-cover-201c4ad9.png"


def item(fa_t, en_t, de_t, fa_b, en_b, de_b, icon=""):
    return SectionItem(title=tt(fa_t, en_t, de_t), body=tt(fa_b, en_b, de_b), icon=icon)


SECTIONS = [
    {
        "key": "about-lexora",
        "kind": "text_image",
        "order": 10,
        "image": COURSE_COVER,
        "image_side": "end",
        "accent": "#8b7dff",
        "eyebrow": tt("درباره لکسورا", "About Lexora", "Über Lexora"),
        "title": tt(
            "لکسورا چیست و چه فرقی با یک آموزشگاه معمولی دارد",
            "What Lexora is, and why it is not another language school",
            "Was Lexora ist — und warum es keine gewöhnliche Sprachschule ist",
        ),
        "body": tt(
            "لکسورا (Lexora) یک آکادمی سه‌زبانه‌ی زبان آلمانی است که دور یک ایده ساخته شده: "
            "روز آزمون نباید اولین باری باشد که محیط آزمون را می‌بینی. به همین دلیل قلب لکسورا "
            "یک سیمیلیتور زبان آلمانی است که آزمون گوته را صفحه‌به‌صفحه، تایمر‌به‌تایمر و "
            "قانون‌به‌قانون بازسازی می‌کند.\n\n"
            "بیشتر داوطلب‌ها به‌خاطر ضعف زبانی رد نمی‌شوند؛ به این خاطر رد می‌شوند که فرمت "
            "غافلگیرشان می‌کند: نمی‌دانند فایل صوتی چند بار پخش می‌شود، نمی‌دانند می‌شود به "
            "سؤال قبلی برگشت یا نه، و وقتی تایمر را می‌بینند تمرکزشان می‌شکند. لکسورا دقیقاً "
            "همین ناشناخته‌ها را حذف می‌کند.\n\n"
            "کنار سیمیلیتور، دوره‌های ساختاریافته‌ی A1 تا C1، سؤالات پرتکرار B2 و C1، "
            "پادکست‌های دوزبانه با متن همزمان و «آلمانی در محیط» — مربی مکالمه‌ی هوش مصنوعی — "
            "قرار دارند. همه‌چیز به فارسی، آلمانی و انگلیسی.",
            "Lexora is a trilingual German academy built around a single idea: exam day should "
            "not be the first time you see the exam. That is why the heart of Lexora is a German "
            "language simulator that rebuilds the Goethe exam screen for screen, timer for timer "
            "and rule for rule.\n\n"
            "Most candidates do not fail because their German is weak. They fail because the "
            "format surprises them: they do not know how often the audio plays, whether they can "
            "go back a question, or how the timer will feel. Lexora removes exactly those "
            "unknowns.\n\n"
            "Around the simulator sit structured A1–C1 courses, high-frequency B2 and C1 question "
            "banks, bilingual podcasts with synchronised transcripts, and German in Context — an "
            "AI speaking teacher. All of it in Persian, German and English.",
            "Lexora ist eine dreisprachige Deutsch-Akademie mit einer einzigen Idee im Zentrum: "
            "Der Prüfungstag sollte nicht der erste Tag sein, an dem Sie die Prüfung sehen. "
            "Deshalb steht im Kern von Lexora ein Deutsch-Simulator, der die Goethe-Prüfung "
            "Bildschirm für Bildschirm, Timer für Timer und Regel für Regel nachbaut.\n\n"
            "Die meisten Kandidatinnen und Kandidaten scheitern nicht an ihrem Deutsch, sondern "
            "am Format: Sie wissen nicht, wie oft das Audio läuft, ob sie zurückspringen dürfen "
            "oder wie sich der Timer anfühlt. Genau diese Unbekannten nimmt Lexora heraus.\n\n"
            "Um den Simulator herum liegen strukturierte Kurse von A1 bis C1, Aufgabenbänke mit "
            "häufigen B2- und C1-Fragen, zweisprachige Podcasts mit synchronem Transkript und "
            "„Deutsch im Kontext“ — eine KI-Sprechlehrerin. Alles auf Persisch, Deutsch und "
            "Englisch.",
        ),
        "cta_label": tt("بیشتر درباره لکسورا", "More about Lexora", "Mehr über Lexora"),
        "cta_href": "/about",
    },
    {
        "key": "why-simulator",
        "kind": "text_image",
        "order": 20,
        "image": EXAM_COVER,
        "image_side": "start",
        "accent": "#22d3ee",
        "eyebrow": tt(
            "سیمیلیتور زبان آلمانی", "German language simulator", "Deutsch-Simulator"
        ),
        "title": tt(
            "چرا یک سیمیلیتور زبان آلمانی نمره‌ات را بالا می‌برد",
            "Why a German language simulator raises your score",
            "Warum ein Deutsch-Simulator Ihre Punktzahl hebt",
        ),
        "body": tt(
            "آزمون زبان دو چیز را همزمان می‌سنجد: دانش زبانی، و توانایی استفاده از آن دانش زیر "
            "فشار زمان. دومی مهارت جداگانه‌ای است و فقط با تمرین در شرایط مشابه ساخته می‌شود.\n\n"
            "سیمیلیتور زبان آلمانی لکسورا با یک «آزمون آزمایشی» معمولی فرق دارد: تایمر جداگانه "
            "برای هر ماژول، همان تعداد دفعات مجاز پخش صوت، ممنوعیت برگشت در Hören، و همان "
            "تسک‌های واقعی — تطبیق افراد با متن، کشیدن و رها کردن، تطبیق عنوان با پاراگراف.\n\n"
            "هر نشست با یک کد آزمون مستقل انجام می‌شود، پس دفعه‌ی دوم سؤال‌ها تازه‌اند و نمره‌ات "
            "واقعاً پیشرفت را نشان می‌دهد، نه حفظ بودن جواب‌ها را. کارنامه هم تفکیکی است: نمره به "
            "ازای هر ماژول، هر نوع تسک، و پاسخ تشریحی برای هر سؤال.",
            "A language exam measures two things at once: what you know, and whether you can use "
            "it under time pressure. The second is a separate skill, and it is only built by "
            "practising in the same conditions.\n\n"
            "The Lexora German simulator is not a generic mock test: a separate timer per module, "
            "the same number of audio replays the real exam allows, no going back inside Hören, "
            "and the real task types — matching people to texts, drag-and-drop gaps, matching "
            "headings to paragraphs.\n\n"
            "Every sitting uses its own exam code, so the second attempt brings fresh questions "
            "and your score reflects real progress rather than remembered answers. The report is "
            "broken down per module, per task type, with a worked explanation for every question.",
            "Eine Sprachprüfung misst zweierlei zugleich: Ihr Wissen und Ihre Fähigkeit, es unter "
            "Zeitdruck einzusetzen. Das Zweite ist eine eigene Fertigkeit und entsteht nur durch "
            "Üben unter denselben Bedingungen.\n\n"
            "Der Lexora-Simulator ist kein beliebiger Modelltest: ein eigener Timer pro Modul, "
            "genauso viele Audiowiederholungen wie in der echten Prüfung, kein Zurückspringen im "
            "Hören und die echten Aufgabentypen — Personen zu Texten zuordnen, Lücken per "
            "Drag-and-drop füllen, Überschriften Absätzen zuordnen.\n\n"
            "Jede Sitzung nutzt einen eigenen Prüfungscode, der zweite Versuch bringt also frische "
            "Aufgaben und Ihre Punktzahl zeigt echten Fortschritt statt erinnerter Antworten. Die "
            "Auswertung ist nach Modul und Aufgabentyp aufgeschlüsselt, mit einer Erklärung zu "
            "jeder Frage.",
        ),
        "cta_label": tt("دیدن سیمیلیتورها", "Open the simulators", "Zu den Simulatoren"),
        "cta_href": "/exams",
    },
    {
        "key": "how-it-works",
        "kind": "features",
        "order": 30,
        "accent": "#8b7dff",
        "eyebrow": tt("مسیر یادگیری", "The path", "Der Weg"),
        "title": tt(
            "چهار قدم از جایی که هستی تا مدرک گوته",
            "Four steps from where you are to a Goethe certificate",
            "Vier Schritte von hier bis zum Goethe-Zertifikat",
        ),
        "subtitle": tt(
            "هر قدم یک ابزار مشخص دارد و خروجی‌اش ورودی قدم بعد است.",
            "Each step has one tool, and its output feeds the next.",
            "Jeder Schritt hat ein Werkzeug, dessen Ergebnis den nächsten speist.",
        ),
        "items": [
            item(
                "۱. سطحت را بسنج", "1. Measure your level", "1. Niveau messen",
                "یک نشست کامل سیمیلیتور با تایمر واقعی. کارنامه‌ی تفکیکی می‌گوید کدام ماژول ضعیف است.",
                "One full simulator sitting with a real timer. The per-skill report says which module is weak.",
                "Eine vollständige Simulator-Sitzung mit echtem Timer. Die Auswertung zeigt das schwache Modul.",
            ),
            item(
                "۲. همان ضعف را درست کن", "2. Fix that one weakness", "2. Genau diese Schwäche beheben",
                "دوره‌های A1 تا C1 و سؤالات پرتکرار B2 و C1، هدفمند روی همان نقطه.",
                "A1–C1 courses and the high-frequency B2 and C1 banks, aimed at that exact gap.",
                "Kurse von A1 bis C1 und die häufigen B2- und C1-Aufgaben, gezielt auf diese Lücke.",
            ),
            item(
                "۳. مکالمه را تمرین کن", "3. Practise speaking", "3. Sprechen üben",
                "«آلمانی در محیط»: صحنه‌ی واقعی، ضبط صدا، بازخورد تفکیکی روی تلفظ و گرامر.",
                "German in Context: a real scene, your recorded answer, feedback on pronunciation and grammar.",
                "Deutsch im Kontext: echte Szene, aufgenommene Antwort, Rückmeldung zu Aussprache und Grammatik.",
            ),
            item(
                "۴. دوباره بسنج", "4. Measure again", "4. Erneut messen",
                "کد آزمون تازه، سؤال‌های تازه. اختلاف دو کارنامه، پیشرفت واقعی توست.",
                "A fresh exam code, fresh questions. The gap between two reports is your real progress.",
                "Neuer Prüfungscode, neue Fragen. Der Abstand zwischen zwei Auswertungen ist Ihr Fortschritt.",
            ),
        ],
    },
    {
        "key": "ai-speaking",
        "kind": "text_image",
        "order": 40,
        "image": COURSE_COVER,
        "image_side": "end",
        "accent": "#f472b6",
        "eyebrow": tt("آلمانی در محیط", "German in Context", "Deutsch im Kontext"),
        "title": tt(
            "مکالمه با هوش مصنوعی، داخل یک موقعیت واقعی",
            "Speak with an AI teacher inside a real situation",
            "Sprechen mit einer KI-Lehrerin in einer echten Situation",
        ),
        "body": tt(
            "بخش Sprechen معمولاً پایین‌ترین نمره‌ی داوطلب‌های فارسی‌زبان است، چون تنها مهارتی "
            "است که نمی‌شود تنهایی و بی‌صدا تمرینش کرد. «آلمانی در محیط» دقیقاً همین شکاف را پر "
            "می‌کند.\n\n"
            "تو وارد یک صحنه‌ی واقعی می‌شوی — مثلاً کنترل مرزی فرودگاه فرانکفورت — ویدیو کامل "
            "پخش می‌شود، بعد میکروفون خودکار باز می‌شود و باید به سؤال افسر جواب بدهی. صدایت "
            "ضبط و پیاده‌سازی می‌شود، و بازخورد تفکیکی می‌گیری: تلفظ، گرامر، واژگان و روانی — "
            "با توضیح فارسی و نسخه‌ی تصحیح‌شده‌ی جمله‌ات به آلمانی.\n\n"
            "هیچ چیزی نصب نمی‌شود؛ میکروفون هر لپ‌تاپ یا گوشی کافی است.",
            "Sprechen is usually the lowest score for Persian-speaking candidates, because it is "
            "the one skill you cannot practise alone and in silence. German in Context fills "
            "exactly that gap.\n\n"
            "You step into a real scene — border control at Frankfurt airport, say — the video "
            "plays through, then the microphone opens on its own and you answer the officer. Your "
            "answer is recorded and transcribed, and you get feedback broken down by "
            "pronunciation, grammar, vocabulary and fluency — explained in your own language, with "
            "a corrected German version of what you said.\n\n"
            "Nothing to install; any laptop or phone microphone works.",
            "Sprechen ist bei persischsprachigen Kandidatinnen und Kandidaten meist die "
            "schwächste Note, weil es die einzige Fertigkeit ist, die man nicht allein und "
            "lautlos üben kann. Genau diese Lücke schließt „Deutsch im Kontext“.\n\n"
            "Sie treten in eine echte Szene — etwa die Grenzkontrolle am Frankfurter Flughafen — "
            "das Video läuft vollständig, dann öffnet sich das Mikrofon von selbst und Sie "
            "antworten dem Beamten. Ihre Antwort wird aufgenommen und transkribiert, und Sie "
            "erhalten eine Rückmeldung nach Aussprache, Grammatik, Wortschatz und Redefluss — "
            "erklärt in Ihrer Sprache, mit einer korrigierten deutschen Fassung.\n\n"
            "Nichts zu installieren; jedes Laptop- oder Handymikrofon genügt.",
        ),
        "cta_label": tt("شروع آلمانی در محیط", "Start German in Context", "Deutsch im Kontext starten"),
        "cta_href": "/courses/einreise-nach-deutschland",
    },
    {
        "key": "home-faq",
        "kind": "faq",
        "order": 50,
        "accent": "#22d3ee",
        "eyebrow": tt("پرسش‌های پرتکرار", "Frequently asked", "Häufige Fragen"),
        "title": tt(
            "سؤال‌هایی که قبل از شروع می‌پرسند",
            "What people ask before they start",
            "Was man vor dem Start fragt",
        ),
        "items": [
            item(
                "سیمیلیتور زبان آلمانی دقیقاً چیست؟",
                "What exactly is a German language simulator?",
                "Was genau ist ein Deutsch-Simulator?",
                "نرم‌افزاری که آزمون گوته را نه فقط از نظر سؤال، بلکه از نظر محیط، تایمر و قوانین بازسازی می‌کند: همان رابط کاربری، همان تعداد دفعات مجاز پخش صوت و همان محدودیت حرکت بین سؤال‌ها.",
                "Software that rebuilds the Goethe exam not only question by question but environment, timer and rules too: the same interface, the same number of audio replays, the same limits on moving between questions.",
                "Software, die die Goethe-Prüfung nicht nur inhaltlich, sondern auch als Umgebung, Timer und Regelwerk nachbaut: dieselbe Oberfläche, dieselbe Zahl an Audiowiederholungen, dieselben Navigationsgrenzen.",
            ),
            item(
                "برای کدام سطوح سیمیلیتور دارید؟",
                "Which levels do you cover?",
                "Welche Niveaus decken Sie ab?",
                "شبیه‌ساز کامل برای A1، A2، B1، B2 و C1. برای B2 و C1 علاوه بر شبیه‌ساز کامل، مجموعه‌های سؤالات پرتکرار هم موجود است.",
                "Full simulators for A1, A2, B1, B2 and C1. For B2 and C1 there are also high-frequency question sets alongside the full simulator.",
                "Vollständige Simulatoren für A1, A2, B1, B2 und C1. Für B2 und C1 gibt es zusätzlich Sammlungen häufiger Prüfungsaufgaben.",
            ),
            item(
                "می‌توانم یک آزمون را چند بار بدهم؟",
                "Can I sit the same exam more than once?",
                "Kann ich dieselbe Prüfung mehrfach ablegen?",
                "بله. هر کد آزمون یک مجموعه سؤال کاملاً مستقل است، پس می‌توانی یک سطح را چند بار بدهی بدون اینکه سؤال‌ها تکرار شوند. قیمت آزمون هزینه‌ی اولین کد را پوشش می‌دهد و کدهای بعدی ارزان‌تر اضافه می‌شوند.",
                "Yes. Each exam code is a completely separate question set, so you can sit the same level several times without repeating questions. The exam price covers the first code; extra codes cost less.",
                "Ja. Jeder Prüfungscode ist ein eigener Aufgabensatz, Sie können dieselbe Stufe also mehrfach ablegen, ohne Aufgaben zu wiederholen. Der Prüfungspreis deckt den ersten Code ab, weitere Codes kosten weniger.",
            ),
            item(
                "بخش گفتار هم تمرین می‌شود؟",
                "Is speaking covered too?",
                "Wird auch das Sprechen geübt?",
                "بله، از طریق «آلمانی در محیط». صحنه‌ی واقعی می‌بینی، جواب می‌دهی، صدایت ضبط و پیاده‌سازی می‌شود و بازخورد تفکیکی روی تلفظ، گرامر، واژگان و روانی می‌گیری.",
                "Yes, through German in Context. You watch a real scene, answer out loud, and your recorded answer comes back transcribed with feedback on pronunciation, grammar, vocabulary and fluency.",
                "Ja, über „Deutsch im Kontext“. Sie sehen eine echte Szene, antworten laut, und Ihre Aufnahme kommt transkribiert zurück — mit Rückmeldung zu Aussprache, Grammatik, Wortschatz und Redefluss.",
            ),
            item(
                "سایت به چند زبان است؟",
                "How many languages is the site in?",
                "In wie vielen Sprachen gibt es die Seite?",
                "سه زبان: فارسی، آلمانی و انگلیسی. رابط کاربری، متن پادکست‌ها، پاسخ‌های تشریحی و بازخورد هوش مصنوعی همگی سه‌زبانه‌اند.",
                "Three: Persian, German and English. The interface, the podcast transcripts, the worked answers and the AI feedback are all trilingual.",
                "Drei: Persisch, Deutsch und Englisch. Oberfläche, Podcast-Transkripte, Musterlösungen und KI-Feedback sind durchgehend dreisprachig.",
            ),
            item(
                "اشتراک بگیرم یا تکی بخرم؟",
                "Subscription or single purchase?",
                "Abo oder Einzelkauf?",
                "اگر فقط یک آزمون می‌خواهی، خرید تکی منطقی است. اگر چند سطح یا چند نشست لازم داری، اشتراک‌ها همه‌ی کدهای آزمون، همه‌ی آزمون‌ها یا کل کاتالوگ به‌همراه مکالمه با هوش مصنوعی را باز می‌کنند.",
                "For a single exam, buy it on its own. If you need several levels or several sittings, the plans open every exam code, every exam, or the whole catalogue including the AI speaking course.",
                "Für eine einzelne Prüfung lohnt der Einzelkauf. Brauchen Sie mehrere Stufen oder Sitzungen, öffnen die Abos alle Prüfungscodes, alle Prüfungen oder den ganzen Katalog inklusive KI-Sprechkurs.",
            ),
        ],
    },
]


class Command(BaseCommand):
    help = "Create or refresh the editable home page sections."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Overwrite sections that already exist instead of leaving edits alone.",
        )

    def handle(self, *args, **options):
        created = updated = skipped = 0

        for spec in SECTIONS:
            section = HomeSection.objects(key=spec["key"]).first()
            if section and not options["reset"]:
                skipped += 1
                continue

            if not section:
                section = HomeSection(key=spec["key"])
                created += 1
            else:
                updated += 1

            for field, value in spec.items():
                if field != "key":
                    setattr(section, field, value)
            section.is_published = True
            section.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Home sections — created {created}, updated {updated}, left alone {skipped}."
            )
        )
