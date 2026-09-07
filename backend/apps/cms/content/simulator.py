"""«سیمیلیتور زبان آلمانی» — the article carrying the site's head keyword."""

from apps.core.i18n import tt

from ._helpers import bullets, callout, cta, faq, h2, h3, p, quote, steps, table

SLUG = "similator-zaban-almani"

META = {
    "slug": SLUG,
    "order": 1,
    "reading_minutes": 14,
    "cover": "/media/covers/exams/b2-cover-8f00ecf8.png",
    "related": ["nahve-khandan-zaban-almani", "sabtenam-azmoun-goethe"],
    "title": tt(
        "سیمیلیتور زبان آلمانی چیست و چطور نمره‌ات را بالا می‌برد",
        "What a German language simulator is, and how it raises your score",
        "Was ein Deutsch-Simulator ist und wie er Ihre Punktzahl hebt",
    ),
    "meta_title": tt(
        "سیمیلیتور زبان آلمانی — شبیه‌ساز کامل آزمون گوته | لکسورا",
        "German Language Simulator — Full Goethe Exam Practice | Lexora",
        "Deutsch-Simulator — vollständige Goethe-Prüfung üben | Lexora",
    ),
    "meta_description": tt(
        "سیمیلیتور زبان آلمانی یعنی تجربه‌ی دقیق آزمون قبل از آزمون. راهنمای کامل شبیه‌ساز "
        "آزمون گوته A1 تا C1، ماژول‌ها، تایمر، کد آزمون و روش استفاده‌ی درست.",
        "A German language simulator lets you sit the exam before the exam. A full guide to "
        "Goethe simulators A1–C1: the modules, the timer, exam codes and how to use them well.",
        "Ein Deutsch-Simulator lässt Sie die Prüfung vor der Prüfung ablegen. Der vollständige "
        "Leitfaden zu Goethe-Simulatoren A1–C1: Module, Timer, Prüfungscodes und Nutzung.",
    ),
    "focus_keyword": tt(
        "سیمیلیتور زبان آلمانی", "German language simulator", "Deutsch-Simulator"
    ),
    "keywords": tt(
        "سیمیلیتور زبان آلمانی, شبیه ساز آزمون آلمانی, سیمولاتور آزمون گوته, آزمون آزمایشی آلمانی, "
        "شبیه ساز آزمون گوته B2, آزمون آنلاین زبان آلمانی, مدل ساتز گوته, لکسورا, Lexora",
        "German language simulator, Goethe exam simulator, German mock exam, online German exam "
        "practice, Goethe B2 simulator, Modellsatz, Lexora",
        "Deutsch-Simulator, Goethe-Prüfungssimulator, Deutsch Modelltest, Deutschprüfung online "
        "üben, Goethe B2 Simulator, Modellsatz, Lexora",
    ),
    "excerpt": tt(
        "سیمیلیتور زبان آلمانی فقط یک آزمون آزمایشی نیست؛ بازسازی دقیق محیط، تایمر و قوانین آزمون "
        "واقعی است. اینجا می‌خوانی که یک شبیه‌ساز درست چه ویژگی‌هایی دارد، چطور از آن استفاده کنی "
        "و چرا نمره‌ات را چند نمره بالا می‌برد.",
        "A German language simulator is not just a mock test; it rebuilds the environment, the "
        "timer and the rules of the real exam. Here is what a proper simulator does, how to use "
        "it, and why it moves your score.",
        "Ein Deutsch-Simulator ist kein bloßer Modelltest; er baut Umgebung, Timer und Regeln der "
        "echten Prüfung nach. Hier steht, was ein guter Simulator leistet, wie man ihn nutzt und "
        "warum er Punkte bringt.",
    ),
}

BODY = [
    p(
        "بیشتر کسانی که در آزمون گوته رد می‌شوند، آلمانی‌شان ضعیف نیست. مشکل جای دیگری است: روز "
        "آزمون، برای اولین بار با محیطی روبه‌رو می‌شوند که نمی‌شناسند. نمی‌دانند فایل صوتی چند بار "
        "پخش می‌شود، نمی‌دانند می‌شود به سؤال قبلی برگشت یا نه، نمی‌دانند تایمر کجای صفحه است و "
        "چقدر مانده. همین چند «نمی‌دانم» کافی است تا تمرکز بشکند و ده نمره از دست برود. سیمیلیتور "
        "زبان آلمانی دقیقاً برای حذف این ناشناخته‌ها ساخته شده است.",
        "Most people who fail a Goethe exam do not have weak German. The problem sits elsewhere: "
        "on exam day they meet an environment they have never seen. They do not know how many "
        "times the audio plays, whether they can return to a previous question, or where the "
        "timer sits and how much is left. Those few unknowns are enough to break concentration "
        "and cost ten marks. A German language simulator exists to remove them.",
        "Die meisten, die eine Goethe-Prüfung nicht bestehen, haben kein schwaches Deutsch. Das "
        "Problem liegt anderswo: Am Prüfungstag treffen sie auf eine Umgebung, die sie nie gesehen "
        "haben. Sie wissen nicht, wie oft das Audio läuft, ob sie zu einer Frage zurückkehren "
        "dürfen, wo der Timer steht und wie viel Zeit bleibt. Diese wenigen Unbekannten genügen, "
        "um die Konzentration zu brechen und zehn Punkte zu kosten. Genau dafür gibt es einen "
        "Deutsch-Simulator.",
    ),
    p(
        "در این راهنما می‌خوانی که یک سیمیلیتور واقعی با یک «آزمون آزمایشی» معمولی چه فرقی دارد، "
        "هر ماژول آزمون گوته چطور شبیه‌سازی می‌شود، کد آزمون به چه کار می‌آید، و مهم‌تر از همه — "
        "چطور از سیمیلیتور استفاده کنی که واقعاً نمره‌ات بالا برود، نه اینکه فقط یک عدد ببینی و رد "
        "شوی.",
        "This guide covers how a real simulator differs from an ordinary mock test, how each "
        "Goethe module is reproduced, what exam codes are for, and above all how to use a "
        "simulator so it actually raises your score instead of just showing you a number.",
        "Dieser Leitfaden zeigt, worin sich ein echter Simulator von einem gewöhnlichen Modelltest "
        "unterscheidet, wie jedes Goethe-Modul nachgebaut wird, wozu Prüfungscodes dienen und vor "
        "allem, wie Sie einen Simulator so nutzen, dass er Ihre Punktzahl wirklich hebt, statt "
        "Ihnen nur eine Zahl zu zeigen.",
    ),

    h2("chist", "سیمیلیتور زبان آلمانی دقیقاً چیست؟",
       "What exactly is a German language simulator?",
       "Was genau ist ein Deutsch-Simulator?"),
    p(
        "سیمیلیتور زبان آلمانی نرم‌افزاری است که آزمون رسمی را نه فقط از نظر سؤال، بلکه از نظر "
        "محیط، زمان‌بندی و قوانین بازسازی می‌کند. تفاوتش با یک «تست آنلاین» ساده در همین جزئیات است:",
        "A German language simulator is software that reproduces the official exam not only in its "
        "questions but in its environment, its timing and its rules. The difference from a plain "
        "online quiz lives in exactly those details:",
        "Ein Deutsch-Simulator ist Software, die die offizielle Prüfung nicht nur inhaltlich, "
        "sondern auch in Umgebung, Zeitrahmen und Regeln nachbaut. Der Unterschied zu einem "
        "einfachen Online-Test liegt genau in diesen Details:",
    ),
    table(
        ("تفاوت آزمون آزمایشی معمولی با سیمیلیتور واقعی",
         "An ordinary mock test versus a real simulator",
         "Gewöhnlicher Modelltest gegenüber echtem Simulator"),
        [("ویژگی", "Feature", "Merkmal"),
         ("آزمون آزمایشی معمولی", "Ordinary mock test", "Gewöhnlicher Modelltest"),
         ("سیمیلیتور واقعی", "Real simulator", "Echter Simulator")],
        [
            [("ظاهر صفحه", "Interface", "Oberfläche"),
             ("قالب دلخواه سایت", "Whatever the site looks like", "Beliebiges Seitenlayout"),
             ("همان رابط، رنگ و چیدمان آزمون دیجیتال",
              "The digital exam's own layout and colours",
              "Layout und Farben der digitalen Prüfung")],
            [("تایمر", "Timer", "Timer"),
             ("معمولاً ندارد یا کلی است", "Usually absent or global", "Meist keiner oder global"),
             ("تایمر جداگانه برای هر ماژول", "A separate timer per module",
              "Ein eigener Timer pro Modul")],
            [("پخش صوت", "Audio replays", "Audiowiederholungen"),
             ("نامحدود", "Unlimited", "Unbegrenzt"),
             ("همان تعداد دفعات مجاز", "Only as often as the exam allows",
              "Nur so oft wie erlaubt")],
            [("حرکت بین سؤال‌ها", "Moving between questions", "Navigation"),
             ("آزاد", "Free", "Frei"),
             ("طبق قانون همان ماژول؛ در Hören برگشت ممنوع",
              "Per module rule; no going back inside Hören",
              "Je Modul geregelt; im Hören kein Zurück")],
            [("نوع تسک‌ها", "Task types", "Aufgabentypen"),
             ("چهارگزینه‌ای ساده", "Plain multiple choice", "Nur Multiple Choice"),
             ("تطبیق، کشیدن و رها کردن، تطبیق عنوان و پاراگراف",
              "Matching, drag-and-drop, heading-to-paragraph",
              "Zuordnen, Drag-and-drop, Überschrift zu Absatz")],
            [("کارنامه", "Report", "Auswertung"),
             ("یک درصد کلی", "A single overall percentage", "Ein Gesamtprozentwert"),
             ("تفکیک مهارتی با پاسخ تشریحی", "Per-skill, with worked explanations",
              "Nach Fertigkeit, mit Erklärungen")],
        ],
    ),
    p(
        "این تفاوت‌ها تزئینی نیستند. وقتی در Hören می‌دانی که فایل فقط یک بار پخش می‌شود، کاملاً "
        "متفاوت گوش می‌دهی: قبل از شروع سؤال‌ها را می‌خوانی، حین پخش یادداشت برمی‌داری و روی "
        "جزئیات گیر نمی‌کنی. کسی که فقط با پخش نامحدود تمرین کرده، این عادت‌ها را ندارد.",
        "None of this is decorative. When you know a Hören track plays once, you listen "
        "differently: you read the questions first, take notes while it runs, and refuse to get "
        "stuck on a detail. Someone who only ever practised with unlimited replays has none of "
        "those habits.",
        "Nichts davon ist Dekoration. Wenn Sie wissen, dass ein Hörtext nur einmal läuft, hören "
        "Sie anders: Sie lesen vorher die Fragen, notieren währenddessen und bleiben an keinem "
        "Detail hängen. Wer nur mit unbegrenzten Wiederholungen geübt hat, hat diese Gewohnheiten "
        "nicht.",
    ),

    h2("chera", "چرا شبیه‌سازی محیط، نمره را جابه‌جا می‌کند",
       "Why reproducing the environment moves the score",
       "Warum die nachgebaute Umgebung Punkte bringt"),
    p(
        "آزمون زبان دو چیز را همزمان می‌سنجد: دانش زبانی، و توانایی استفاده از آن دانش زیر فشار. "
        "دومی مهارت جداگانه‌ای است و فقط با تمرین در شرایط مشابه ساخته می‌شود. سه اثر مشخص وجود دارد:",
        "A language exam measures two things at once: what you know, and whether you can use it "
        "under pressure. The second is a separate skill, built only by practising in matching "
        "conditions. Three effects are measurable:",
        "Eine Sprachprüfung misst zweierlei zugleich: Ihr Wissen und Ihre Fähigkeit, es unter Druck "
        "einzusetzen. Das Zweite ist eine eigene Fertigkeit, die nur unter gleichen Bedingungen "
        "entsteht. Drei Wirkungen sind messbar:",
    ),
    h3("۱. کاهش بار شناختی", "1. Lower cognitive load", "1. Geringere kognitive Last"),
    p(
        "مغز ظرفیت محدودی دارد. اگر بخشی از آن صرف فهمیدن «این دکمه چه کار می‌کند» شود، همان مقدار "
        "از فهم متن کم می‌شود. وقتی محیط آشناست، تمام ظرفیت روی خود زبان می‌رود. این تنها دلیلی است "
        "که برای بالا بردن نمره، هیچ ربطی به یاد گرفتن واژه‌ی جدید ندارد و با یک بار تمرین کامل حل "
        "می‌شود.",
        "The brain has a fixed budget. Whatever it spends working out what a button does comes "
        "straight out of reading comprehension. When the environment is familiar, the whole budget "
        "goes to the language. This is the one way to raise a score that has nothing to do with "
        "learning new words and is solved by a single full rehearsal.",
        "Das Gehirn hat ein festes Budget. Was es dafür aufwendet zu verstehen, was ein Knopf tut, "
        "fehlt direkt beim Leseverstehen. Ist die Umgebung vertraut, fließt das ganze Budget in die "
        "Sprache. Das ist die einzige Punktsteigerung, die nichts mit neuen Vokabeln zu tun hat und "
        "sich mit einem einzigen vollständigen Durchgang erledigt.",
    ),
    h3("۲. ساخته شدن حس زمان", "2. A sense of time", "2. Ein Zeitgefühl"),
    p(
        "در Lesen سطح B2، شصت‌وپنج دقیقه برای پنج بخش داری. تقسیم درست این زمان چیزی است که فقط با "
        "تجربه به دست می‌آید. داوطلبی که سه بار نشست کامل داده، بدون نگاه کردن به ساعت می‌فهمد که "
        "روی تسک دوم زیادی مانده است. داوطلبی که نداده، معمولاً بخش آخر را نیمه‌کاره رها می‌کند.",
        "B2 Lesen gives you sixty-five minutes for five parts. Dividing that time correctly only "
        "comes with experience. A candidate who has sat three full rehearsals senses, without "
        "checking the clock, that they have lingered on part two. One who has not usually leaves "
        "the last part half finished.",
        "B2-Lesen gibt Ihnen fünfundsechzig Minuten für fünf Teile. Diese Zeit richtig aufzuteilen "
        "kommt nur mit Erfahrung. Wer drei vollständige Durchgänge hinter sich hat, spürt ohne Blick "
        "auf die Uhr, dass er bei Teil zwei zu lange verweilt. Wer nicht, lässt meist den letzten "
        "Teil halb fertig liegen.",
    ),
    h3("۳. کم شدن اضطراب", "3. Less anxiety", "3. Weniger Prüfungsangst"),
    p(
        "اضطراب آزمون عمدتاً از ناشناخته می‌آید. وقتی صفحه‌ی شروع، دکمه‌ها، ترتیب ماژول‌ها و حتی حس "
        "دیدن تایمر برایت تکراری شده باشد، بدنت آن را به‌عنوان تهدید ثبت نمی‌کند. این تفاوت در "
        "Sprechen و Schreiben بیشترین اثر را دارد.",
        "Exam anxiety mostly comes from the unknown. Once the start screen, the buttons, the order "
        "of the modules and even the feeling of watching a timer have become repetitive, your body "
        "stops registering them as a threat. The difference shows up most in Sprechen and "
        "Schreiben.",
        "Prüfungsangst entsteht überwiegend aus dem Unbekannten. Sobald Startbildschirm, "
        "Schaltflächen, Modulreihenfolge und selbst das Gefühl, einen Timer zu sehen, zur Routine "
        "geworden sind, wertet Ihr Körper sie nicht mehr als Bedrohung. Am deutlichsten zeigt sich "
        "das in Sprechen und Schreiben.",
    ),
    quote(
        "سیمیلیتور دانش جدیدی به تو اضافه نمی‌کند؛ کاری می‌کند که دانشی که داری، در روز آزمون قابل "
        "استفاده باشد.",
        "A simulator adds no knowledge. It makes the knowledge you already have usable on the day.",
        "Ein Simulator fügt kein Wissen hinzu. Er macht das Wissen, das Sie haben, am Prüfungstag "
        "nutzbar.",
    ),
]

BODY += [
    h2("modulha", "ماژول‌های آزمون و شبیه‌سازی هرکدام",
       "The exam modules, and how each is reproduced",
       "Die Prüfungsmodule und ihre Nachbildung"),
    p(
        "آزمون گوته از چهار ماژول تشکیل شده و هرکدام قوانین خودش را دارد. یک سیمیلیتور زبان آلمانی "
        "درست، هر چهار را جداگانه بازسازی می‌کند.",
        "A Goethe exam has four modules, each with its own rules. A proper German simulator "
        "rebuilds all four separately.",
        "Eine Goethe-Prüfung besteht aus vier Modulen mit jeweils eigenen Regeln. Ein guter "
        "Deutsch-Simulator bildet alle vier einzeln nach.",
    ),
    h3("Lesen — درک مطلب", "Lesen — reading", "Lesen — Leseverstehen"),
    p(
        "در سطح B2 پنج بخش دارد: تطبیق افراد با متن‌های کوتاه، پر کردن جای خالی با کشیدن گزینه‌ها، "
        "چهارگزینه‌ای روی یک متن بلند، تطبیق عنوان با پاراگراف و تشخیص موافق/مخالف بودن نویسنده. "
        "سیمیلیتور باید همین تنوع را داشته باشد، چون هر نوع تسک استراتژی خواندن متفاوتی می‌خواهد — "
        "در یکی باید کل متن را بخوانی و در دیگری فقط دنبال کلیدواژه بگردی.",
        "At B2 it has five parts: matching people to short texts, filling gaps by dragging options, "
        "multiple choice over a long text, matching headings to paragraphs, and deciding whether "
        "the writer agrees. A simulator needs that same variety, because each task type demands a "
        "different reading strategy — one wants the whole text, another only a keyword hunt.",
        "Auf B2 hat es fünf Teile: Personen kurzen Texten zuordnen, Lücken per Drag-and-drop füllen, "
        "Multiple Choice zu einem langen Text, Überschriften Absätzen zuordnen und entscheiden, ob "
        "die Autorin zustimmt. Ein Simulator braucht dieselbe Vielfalt, denn jeder Aufgabentyp "
        "verlangt eine andere Lesestrategie — einer den ganzen Text, ein anderer nur die Suche nach "
        "Schlüsselwörtern.",
    ),
    h3("Hören — درک شنیداری", "Hören — listening", "Hören — Hörverstehen"),
    p(
        "سخت‌گیرانه‌ترین ماژول از نظر قوانین. بعضی بخش‌ها یک بار و بعضی دو بار پخش می‌شوند، و بعد از "
        "رد شدن از یک سؤال نمی‌توانی برگردی. سیمیلیتوری که اجازه‌ی برگشت و پخش دوباره بدهد، عملاً "
        "ماژول را از سختی می‌اندازد و کارنامه‌اش دروغ می‌گوید.",
        "The strictest module. Some parts play once, some twice, and once you pass a question you "
        "cannot go back. A simulator that allows replays and backtracking removes the difficulty "
        "altogether, and its report lies to you.",
        "Das strengste Modul. Manche Teile laufen einmal, manche zweimal, und eine übersprungene "
        "Frage lässt sich nicht mehr aufrufen. Ein Simulator, der Wiederholungen und Zurückspringen "
        "erlaubt, nimmt dem Modul die Schwierigkeit — und seine Auswertung lügt.",
    ),
    h3("Schreiben — نگارش", "Schreiben — writing", "Schreiben — Schriftlicher Ausdruck"),
    p(
        "دو تسک: یک متن اظهار نظر و یک نامه‌ی نیمه‌رسمی، در مجموع ۷۵ دقیقه در سطح B2. اینجا سیمیلیتور "
        "نمی‌تواند خودکار نمره‌ی دقیق بدهد، ولی می‌تواند دو کار مهم بکند: تایمر واقعی بگذارد و "
        "شمارنده‌ی کلمه نشان دهد. بیشتر داوطلب‌ها در تمرین خانگی زمان را رعایت نمی‌کنند و در آزمون "
        "واقعی نصف متن دومشان نانوشته می‌ماند.",
        "Two tasks: an opinion text and a semi-formal letter, seventy-five minutes in total at B2. "
        "A simulator cannot grade this precisely on its own, but it can do two things that matter: "
        "run the real timer and show a word counter. Most candidates ignore the clock when "
        "practising at home, then leave half of their second text unwritten in the real exam.",
        "Zwei Aufgaben: ein Meinungstext und ein halbformeller Brief, auf B2 insgesamt "
        "fünfundsiebzig Minuten. Ein Simulator kann das nicht allein präzise bewerten, aber zwei "
        "wichtige Dinge tun: den echten Timer laufen lassen und einen Wortzähler zeigen. Die "
        "meisten ignorieren beim Üben zu Hause die Uhr und lassen dann in der echten Prüfung den "
        "halben zweiten Text ungeschrieben.",
    ),
    h3("Sprechen — گفتار", "Sprechen — speaking", "Sprechen — Mündlicher Ausdruck"),
    p(
        "دشوارترین بخش برای شبیه‌سازی، چون به شریک مکالمه نیاز دارد. راه‌حل عملی، مربی مکالمه‌ی هوش "
        "مصنوعی است: صحنه‌ای واقعی می‌بینی، سؤال از تو پرسیده می‌شود، ۳۰ ثانیه فرصت داری و جوابت ضبط، "
        "پیاده‌سازی و تفکیکی نمره‌گذاری می‌شود — تلفظ، گرامر، واژگان و روانی.",
        "The hardest part to simulate, because it needs a partner. The practical answer is an AI "
        "speaking teacher: you watch a real scene, a question is put to you, you get thirty "
        "seconds, and your answer is recorded, transcribed and scored per criterion — "
        "pronunciation, grammar, vocabulary and fluency.",
        "Der am schwersten zu simulierende Teil, weil er eine Partnerin braucht. Die praktische "
        "Lösung ist eine KI-Sprechlehrerin: Sie sehen eine echte Szene, bekommen eine Frage, haben "
        "dreißig Sekunden, und Ihre Antwort wird aufgenommen, transkribiert und nach Kriterien "
        "bewertet — Aussprache, Grammatik, Wortschatz und Redefluss.",
    ),
    cta(
        ("سیمیلیتور کامل A1 تا C1", "Full simulators, A1 to C1", "Vollständige Simulatoren, A1 bis C1"),
        ("همان رابط، همان تایمر، همان قوانین. با کارنامه‌ی تفکیکی و پاسخ تشریحی.",
         "The same interface, timer and rules, with a per-skill report and worked answers.",
         "Dieselbe Oberfläche, derselbe Timer, dieselben Regeln — mit Auswertung nach Fertigkeit "
         "und Musterlösungen."),
        "/exams",
        ("دیدن سیمیلیتورها", "Open the simulators", "Zu den Simulatoren"),
    ),

    h2("code", "کد آزمون: چرا یک نشست کافی نیست",
       "Exam codes: why one sitting is not enough",
       "Prüfungscodes: warum eine Sitzung nicht genügt"),
    p(
        "بزرگ‌ترین ضعف آزمون‌های آزمایشی رایگان این است که فقط یک مجموعه سؤال دارند. بار دوم که همان "
        "آزمون را می‌دهی، بخشی از جواب‌ها را به خاطر داری و نمره‌ات بالاتر می‌آید — بدون اینکه واقعاً "
        "بهتر شده باشی. این «پیشرفت کاذب» خطرناک است، چون با اعتماد به نفس اشتباه سر جلسه‌ی واقعی "
        "می‌روی.",
        "The biggest weakness of free mock tests is that they have one question set. The second "
        "time you sit it you remember some answers and score higher without having improved. That "
        "false progress is dangerous, because you walk into the real exam with misplaced "
        "confidence.",
        "Die größte Schwäche kostenloser Modelltests ist ihr einziger Aufgabensatz. Beim zweiten "
        "Mal erinnern Sie sich an Antworten und schneiden besser ab, ohne besser geworden zu sein. "
        "Dieser falsche Fortschritt ist gefährlich, denn Sie gehen mit trügerischer Sicherheit in "
        "die echte Prüfung.",
    ),
    p(
        "راه‌حل، کد آزمون است: هر کد یک مجموعه سؤال کاملاً مستقل با همان ساختار و همان سطح دشواری. "
        "یعنی می‌توانی سطح B2 را چهار بار بدهی و هر بار سؤال‌ها تازه باشند. آن‌وقت نمودار نمره‌ات "
        "واقعی است و می‌شود روی آن تصمیم گرفت.",
        "The answer is exam codes: each code is an entirely separate question set with the same "
        "structure and the same difficulty. You can sit B2 four times with fresh questions every "
        "time, and your score curve becomes something you can act on.",
        "Die Lösung sind Prüfungscodes: Jeder Code ist ein völlig eigener Aufgabensatz mit gleicher "
        "Struktur und gleichem Schwierigkeitsgrad. Sie können B2 viermal ablegen, jedes Mal mit "
        "frischen Aufgaben — und Ihre Punktekurve wird zu etwas, worauf sich Entscheidungen stützen "
        "lassen.",
    ),
    bullets(
        ("قیمت آزمون، هزینه‌ی اولین کد را پوشش می‌دهد.",
         "The exam price covers the first code.",
         "Der Prüfungspreis deckt den ersten Code ab."),
        ("کدهای بعدی با هزینه‌ی کمتر اضافه می‌شوند و همان لحظه‌ی خرید انتخاب می‌شوند.",
         "Extra codes cost less and are chosen at the moment of purchase.",
         "Weitere Codes kosten weniger und werden beim Kauf ausgewählt."),
        ("اشتراک‌ها همه‌ی کدهای هر آزمونی که باز کرده‌ای را آزاد می‌کنند.",
         "A subscription unlocks every code of any exam you own.",
         "Ein Abo schaltet alle Codes jeder freigeschalteten Prüfung frei."),
    ),
    callout(
        ("دو نشست، دو هفته فاصله", "Two sittings, two weeks apart", "Zwei Sitzungen, zwei Wochen Abstand"),
        ("بهترین الگو این است که دو نشست کامل با حدود دو هفته فاصله بدهی و بینشان روی ضعف‌های "
         "کارنامه کار کنی. اگر نمره‌ی دوم بالاتر بود، پیشرفت واقعی است؛ اگر نبود، برنامه‌ات باید "
         "عوض شود نه تلاشت.",
         "The best pattern is two full sittings about two weeks apart, working on the report's "
         "weak points in between. If the second score is higher, the progress is real; if it is "
         "not, change the plan rather than the effort.",
         "Das beste Muster sind zwei vollständige Sitzungen im Abstand von etwa zwei Wochen, "
         "dazwischen Arbeit an den Schwachstellen der Auswertung. Ist die zweite Punktzahl höher, "
         "ist der Fortschritt echt; wenn nicht, ändern Sie den Plan, nicht die Anstrengung."),
    ),

    h2("ravesh", "روش درست استفاده از سیمیلیتور",
       "How to use a simulator properly",
       "Wie man einen Simulator richtig nutzt"),
    p(
        "بیشترین اشتباه این است که آدم سیمیلیتور را مثل تمرین باز می‌کند: وسطش قهوه می‌خورد، به گوشی "
        "نگاه می‌کند، یک سؤال را دو بار گوش می‌دهد. نتیجه‌اش کارنامه‌ای است که هیچ ربطی به آزمون "
        "واقعی ندارد. برای اینکه سیمیلیتور واقعاً کار کند:",
        "The commonest mistake is opening a simulator the way you open an exercise: coffee halfway "
        "through, a glance at the phone, one question heard twice. The result is a report with no "
        "relation to the real exam. To make a simulator actually work:",
        "Der häufigste Fehler ist, einen Simulator wie eine Übung zu öffnen: zwischendurch Kaffee, "
        "ein Blick aufs Handy, eine Frage zweimal gehört. Das Ergebnis ist eine Auswertung ohne "
        "Bezug zur echten Prüfung. Damit ein Simulator wirklich wirkt:",
    ),
    steps(
        ("زمان را مثل روز آزمون بگذار. صبح، بعد از صبحانه، در همان ساعتی که آزمون واقعی برگزار می‌شود.",
         "Book the time like exam day: morning, after breakfast, at the hour the real exam runs.",
         "Legen Sie die Zeit wie am Prüfungstag: morgens, nach dem Frühstück, zur Uhrzeit der "
         "echten Prüfung."),
        ("گوشی را خاموش کن و در اتاق را ببند. یک نشست کامل یعنی بدون وقفه.",
         "Phone off, door closed. A full sitting means no interruptions.",
         "Handy aus, Tür zu. Eine vollständige Sitzung heißt: keine Unterbrechungen."),
        ("کاغذ و خودکار کنار دستت باشد، چون در آزمون واقعی هم هست.",
         "Keep paper and a pen beside you, because the real exam gives you both.",
         "Papier und Stift bereitlegen — die echte Prüfung gibt Ihnen beides."),
        ("وسط ماژول توقف نکن. اگر سؤالی را نمی‌دانی، ردش کن — دقیقاً کاری که باید در آزمون بکنی.",
         "Do not pause mid-module. Skip what you do not know, exactly as you would on the day.",
         "Nicht mitten im Modul pausieren. Überspringen Sie, was Sie nicht wissen — genau wie in "
         "der Prüfung."),
        ("بعد از پایان، بلافاصله کارنامه را نبند. هر سؤال غلط را با پاسخ تشریحی بخوان و دلیل اشتباه "
         "را بنویس.",
         "Do not close the report when it appears. Read every wrong answer's explanation and write "
         "down why you missed it.",
         "Schließen Sie die Auswertung nicht sofort. Lesen Sie zu jeder falschen Antwort die "
         "Erklärung und notieren Sie den Grund."),
        ("اشتباه‌ها را دسته‌بندی کن: نفهمیدن واژه، نفهمیدن ساختار، کم آوردن وقت، یا بی‌دقتی. هر دسته "
         "درمان متفاوتی دارد.",
         "Sort the mistakes: unknown word, unknown structure, ran out of time, or carelessness. "
         "Each category has a different cure.",
         "Sortieren Sie die Fehler: unbekanntes Wort, unbekannte Struktur, Zeit nicht gereicht oder "
         "Unachtsamkeit. Jede Kategorie hat ein anderes Gegenmittel."),
    ),
    p(
        "قدم ششم مهم‌ترین است. اگر ده غلط داشتی و هشت‌تایش «بی‌دقتی» بود، مشکلت زبانی نیست و باید "
        "روی تمرکز و سرعت کار کنی. اگر هشت‌تایش «نفهمیدن واژه» بود، باید سراغ واژگان بروی. بدون این "
        "دسته‌بندی، آدم معمولاً همه‌چیز را می‌گذارد پای «باید بیشتر بخوانم» که کلی‌ترین و "
        "بی‌فایده‌ترین نتیجه‌گیری ممکن است.",
        "Step six matters most. If eight of ten mistakes were carelessness, your problem is not "
        "language and you should work on focus and pace. If eight were unknown words, go to "
        "vocabulary. Without that sorting, people default to \"I should study more\" — the vaguest "
        "and least useful conclusion available.",
        "Schritt sechs ist der wichtigste. Waren acht von zehn Fehlern Unachtsamkeit, liegt Ihr "
        "Problem nicht an der Sprache, sondern an Konzentration und Tempo. Waren acht unbekannte "
        "Wörter, gehen Sie an den Wortschatz. Ohne diese Sortierung landet man bei „ich muss mehr "
        "lernen“ — der vagesten und nutzlosesten Schlussfolgerung überhaupt.",
    ),
]

BODY += [
    h2("kay", "کِی سیمیلیتور بدهیم؟", "When to sit a simulator", "Wann man einen Simulator ablegt"),
    p(
        "زمان‌بندی اهمیت دارد. خیلی زود دادن سیمیلیتور فقط ناامیدکننده است و خیلی دیر دادنش فرصت "
        "اصلاح را می‌گیرد. الگوی پیشنهادی:",
        "Timing matters. Too early is merely discouraging; too late removes the chance to fix "
        "anything. A workable pattern:",
        "Der Zeitpunkt zählt. Zu früh ist nur entmutigend, zu spät nimmt die Möglichkeit, noch "
        "etwas zu ändern. Ein brauchbares Muster:",
    ),
    table(
        ("زمان‌بندی نشست‌های سیمیلیتور نسبت به روز آزمون",
         "Simulator sittings relative to exam day",
         "Simulator-Sitzungen im Verhältnis zum Prüfungstag"),
        [("زمان", "When", "Wann"), ("چه کاری", "What", "Was"), ("هدف", "Purpose", "Zweck")],
        [
            [("۳ ماه مانده", "3 months out", "3 Monate vorher"),
             ("یک ماژول تنها (مثلاً فقط Lesen)", "A single module, say Lesen alone",
              "Ein einzelnes Modul, etwa nur Lesen"),
             ("آشنایی با فرمت، بدون فشار", "Meet the format without pressure",
              "Das Format ohne Druck kennenlernen")],
            [("۸ هفته مانده", "8 weeks out", "8 Wochen vorher"),
             ("نشست کامل، کد اول", "A full sitting on the first code",
              "Vollständige Sitzung, erster Code"),
             ("گرفتن خط پایه‌ی واقعی", "Get a true baseline", "Eine echte Ausgangslage")],
            [("۵ هفته مانده", "5 weeks out", "5 Wochen vorher"),
             ("دو ماژول ضعیف‌تر", "The two weaker modules", "Die zwei schwächeren Module"),
             ("کار روی نقطه‌ضعف مشخص", "Work the named weakness",
              "Gezielt an der Schwachstelle arbeiten")],
            [("۳ هفته مانده", "3 weeks out", "3 Wochen vorher"),
             ("نشست کامل، کد دوم", "A full sitting on the second code",
              "Vollständige Sitzung, zweiter Code"),
             ("سنجش پیشرفت واقعی", "Measure real progress", "Echten Fortschritt messen")],
            [("۱ هفته مانده", "1 week out", "1 Woche vorher"),
             ("یک ماژول سبک", "One light module", "Ein leichtes Modul"),
             ("زنده نگه داشتن حس فرمت", "Keep the format fresh", "Das Formatgefühl frisch halten")],
            [("۲ روز مانده", "2 days out", "2 Tage vorher"),
             ("هیچ", "Nothing", "Nichts"),
             ("استراحت؛ آزمون دادن در این مرحله فقط اضطراب می‌آورد",
              "Rest; a test now only adds anxiety",
              "Ausruhen; ein Test bringt jetzt nur Angst")],
        ],
    ),

    h2("karnameh", "کارنامه را چطور بخوانیم", "How to read the report", "Wie man die Auswertung liest"),
    p(
        "یک درصد کلی تقریباً هیچ اطلاعاتی نمی‌دهد. کارنامه‌ی مفید حداقل سه چیز را نشان می‌دهد: نمره "
        "به تفکیک ماژول، نمره به تفکیک نوع تسک، و زمان صرف‌شده روی هر بخش. با این سه، دقیقاً می‌فهمی "
        "کجا خون‌ریزی داری.",
        "A single percentage tells you almost nothing. A useful report shows at least three things: "
        "the score per module, the score per task type, and the time spent on each part. With those "
        "three you can see exactly where you are losing marks.",
        "Ein einzelner Prozentwert sagt fast nichts. Eine brauchbare Auswertung zeigt mindestens "
        "dreierlei: Punkte je Modul, Punkte je Aufgabentyp und die Zeit pro Teil. Damit sehen Sie "
        "genau, wo Sie Punkte verlieren.",
    ),
    bullets(
        ("اگر Lesen خوب و Hören ضعیف است: مشکل عادت گوش است، نه واژگان. شنیدن روزانه با متن را زیاد کن.",
         "Strong Lesen, weak Hören: the problem is ear training, not vocabulary. Increase daily "
         "listening with a transcript.",
         "Starkes Lesen, schwaches Hören: Das Problem ist das Ohr, nicht der Wortschatz. Mehr "
         "tägliches Hören mit Transkript."),
        ("اگر همه‌ی ماژول‌ها متوسط‌اند ولی بخش آخر هرکدام ضعیف است: مشکل مدیریت زمان است.",
         "Every module average but the last part of each one weak: this is time management.",
         "Alle Module mittelmäßig, aber jeweils der letzte Teil schwach: Das ist Zeitmanagement."),
        ("اگر تسک‌های تطبیقی ضعیف‌اند ولی چهارگزینه‌ای‌ها خوب: مشکل استراتژی خواندن است، نه فهم.",
         "Matching tasks weak, multiple choice fine: this is reading strategy, not comprehension.",
         "Zuordnungsaufgaben schwach, Multiple Choice gut: Das ist Lesestrategie, nicht Verstehen."),
        ("اگر Schreiben ناتمام مانده: باید با تایمر و شمارنده‌ی کلمه تمرین کنی، نه بدون آن‌ها.",
         "Schreiben left unfinished: practise with the timer and word counter, not without them.",
         "Schreiben unfertig: mit Timer und Wortzähler üben, nicht ohne."),
    ),
    p(
        "پاسخ تشریحی هم فقط برای سؤال‌های غلط نیست. سؤال‌هایی که درست جواب دادی ولی مطمئن نبودی را "
        "هم بخوان؛ اینها همان‌هایی هستند که دفعه‌ی بعد ممکن است غلط شوند.",
        "Worked answers are not only for the questions you got wrong. Read the ones you answered "
        "correctly but were unsure about; those are the ones that flip next time.",
        "Musterlösungen sind nicht nur für falsche Antworten da. Lesen Sie auch die, die Sie "
        "richtig, aber unsicher beantwortet haben — genau die kippen beim nächsten Mal.",
    ),

    h2("digital", "آزمون دیجیتال گوته و چرا شبیه‌سازی امروز مهم‌تر از قبل است",
       "The digital Goethe exam, and why simulation matters more now",
       "Die digitale Goethe-Prüfung und warum Simulation heute wichtiger ist"),
    p(
        "گوته در سال‌های اخیر بخش بزرگی از آزمون‌ها را به نسخه‌ی دیجیتال منتقل کرده است. در نسخه‌ی "
        "کاغذی، داوطلب می‌توانست کل دفترچه را ورق بزند، روی متن خط بکشد و آزادانه بین سؤال‌ها برگردد. "
        "در نسخه‌ی دیجیتال هیچ‌کدام از این‌ها به همان شکل ممکن نیست و همین، مهارت تازه‌ای می‌طلبد.",
        "Goethe has moved a large share of its exams to a digital version. On paper you could leaf "
        "through the whole booklet, underline the text and move freely between questions. None of "
        "that works the same way digitally, and that demands a new skill.",
        "Goethe hat einen großen Teil seiner Prüfungen auf die digitale Fassung umgestellt. Auf "
        "Papier konnte man das ganze Heft durchblättern, im Text unterstreichen und frei zwischen "
        "Fragen wechseln. Digital funktioniert nichts davon gleich — und das verlangt eine neue "
        "Fertigkeit.",
    ),
    bullets(
        ("خط کشیدن روی متن جایش را به یادداشت روی کاغذ باطله می‌دهد، پس باید تمرین کنی سریع و خوانا "
         "یادداشت برداری.",
         "Underlining gives way to notes on scrap paper, so practise taking fast, legible notes.",
         "Unterstreichen weicht Notizen auf Schmierpapier — üben Sie schnelles, lesbares Notieren."),
        ("متن‌های بلند در یک پنجره‌ی اسکرول‌شونده نمایش داده می‌شوند؛ پیدا کردن دوباره‌ی یک پاراگراف "
         "کندتر از ورق زدن است.",
         "Long texts sit in a scrolling pane; finding a paragraph again is slower than turning a page.",
         "Lange Texte stehen in einem Scrollfenster; einen Absatz wiederzufinden ist langsamer als "
         "Blättern."),
        ("تسک‌های کشیدن و رها کردن با ماوس انجام می‌شوند و اگر با آن‌ها آشنا نباشی، فقط برای فهمیدن "
         "نحوه‌ی کار چند دقیقه از دست می‌دهی.",
         "Drag-and-drop tasks are done with the mouse; unfamiliar, they cost minutes just to work out.",
         "Drag-and-drop-Aufgaben laufen mit der Maus; unvertraut kosten sie Minuten, nur um sie zu "
         "verstehen."),
        ("تایمر همیشه روی صفحه است. این هم کمک است هم فشار، و باید به دیدنش عادت کنی.",
         "The timer is always on screen. That is both help and pressure, and you must get used to it.",
         "Der Timer ist immer sichtbar. Das hilft und setzt zugleich unter Druck — daran muss man "
         "sich gewöhnen."),
    ),
    p(
        "به همین دلیل، یک سیمیلیتور زبان آلمانی که فقط سؤال‌های کاغذی را آنلاین کرده باشد، دیگر کافی "
        "نیست. شبیه‌سازی باید همان تعامل‌های نسخه‌ی دیجیتال را داشته باشد: کشیدن و رها کردن واقعی، "
        "پنجره‌ی اسکرول‌شونده، پخش‌کننده‌ی صوتی با شمارنده‌ی دفعات، و تایمری که همان‌جایی باشد که در "
        "آزمون واقعی هست.",
        "So a German simulator that merely puts paper questions online is no longer enough. It has "
        "to reproduce the digital interactions: real drag-and-drop, a scrolling pane, an audio "
        "player that counts plays, and a timer where the real one sits.",
        "Ein Deutsch-Simulator, der Papieraufgaben nur ins Netz stellt, genügt daher nicht mehr. Er "
        "muss die digitalen Interaktionen nachbilden: echtes Drag-and-drop, ein Scrollfenster, "
        "einen Audioplayer mit Wiedergabezähler und einen Timer an derselben Stelle wie im Original.",
    ),

    h2("sotoohe", "سیمیلیتور در هر سطح چه شکلی است",
       "What a simulator looks like at each level",
       "Wie ein Simulator auf jedem Niveau aussieht"),
    p(
        "ساختار آزمون از A1 تا C1 یکسان نیست و سیمیلیتور هم باید همین تفاوت‌ها را منعکس کند. آنچه در "
        "هر سطح تغییر می‌کند فقط سختی واژگان نیست؛ نوع تسک‌ها، طول متن‌ها و مدت زمان هم عوض می‌شوند.",
        "The exam is not the same shape from A1 to C1, and a simulator has to mirror the "
        "differences. What changes is not only vocabulary difficulty but the task types, the text "
        "lengths and the durations.",
        "Die Prüfung hat von A1 bis C1 nicht dieselbe Form, und ein Simulator muss die Unterschiede "
        "abbilden. Es ändert sich nicht nur die Wortschatzschwierigkeit, sondern auch Aufgabentypen, "
        "Textlängen und Dauer.",
    ),
    table(
        ("تفاوت ماژول‌ها در سطوح مختلف", "How the modules differ by level",
         "Wie sich die Module je Niveau unterscheiden"),
        [("سطح", "Level", "Niveau"), ("Lesen", "Lesen", "Lesen"), ("Hören", "Hören", "Hören"),
         ("Schreiben", "Schreiben", "Schreiben"), ("ویژگی خاص", "Distinctive", "Besonderheit")],
        [
            [("A1", "A1", "A1"), ("۲۵ دقیقه", "25 min", "25 Min."), ("۲۰ دقیقه", "20 min", "20 Min."),
             ("۲۰ دقیقه", "20 min", "20 Min."),
             ("متن‌های خیلی کوتاه، آگهی و پیام", "Very short texts, adverts and messages",
              "Sehr kurze Texte, Anzeigen und Nachrichten")],
            [("A2", "A2", "A2"), ("۳۰ دقیقه", "30 min", "30 Min."), ("۳۰ دقیقه", "30 min", "30 Min."),
             ("۳۰ دقیقه", "30 min", "30 Min."),
             ("ورود تسک‌های تطبیقی", "Matching tasks appear", "Zuordnungsaufgaben kommen dazu")],
            [("B1", "B1", "B1"), ("۶۵ دقیقه", "65 min", "65 Min."), ("۴۰ دقیقه", "40 min", "40 Min."),
             ("۶۰ دقیقه", "60 min", "60 Min."),
             ("ماژول‌ها جداگانه قابل قبول‌اند", "Modules can be passed separately",
              "Module einzeln bestehbar")],
            [("B2", "B2", "B2"), ("۶۵ دقیقه", "65 min", "65 Min."), ("۴۰ دقیقه", "40 min", "40 Min."),
             ("۷۵ دقیقه", "75 min", "75 Min."),
             ("پنج بخش در Lesen، متن‌های استدلالی", "Five Lesen parts, argumentative texts",
              "Fünf Lesen-Teile, argumentative Texte")],
            [("C1", "C1", "C1"), ("۷۰ دقیقه", "70 min", "70 Min."), ("۴۰ دقیقه", "40 min", "40 Min."),
             ("۷۵ دقیقه", "75 min", "75 Min."),
             ("متن آکادمیک، واژگان انتزاعی", "Academic text, abstract vocabulary",
              "Akademische Texte, abstrakter Wortschatz")],
        ],
    ),
    p(
        "نکته‌ای که خیلی‌ها نمی‌دانند: از سطح B1 به بعد، ماژول‌ها جداگانه قابل قبول شدن هستند. یعنی "
        "اگر سه ماژول را قبول شوی و یکی را رد، فقط همان یکی را دوباره می‌دهی. این موضوع استراتژی "
        "آماده‌سازی را کاملاً عوض می‌کند و سیمیلیتور بهترین جا برای فهمیدن این است که کدام ماژول را "
        "باید جدی‌تر بگیری.",
        "Something many people miss: from B1 upwards the modules can be passed separately. Pass "
        "three and fail one, and you resit only that one. That changes preparation strategy "
        "entirely, and a simulator is the best place to learn which module needs the attention.",
        "Was viele übersehen: Ab B1 lassen sich die Module einzeln bestehen. Bestehen Sie drei und "
        "fallen bei einem durch, wiederholen Sie nur dieses. Das ändert die Vorbereitungsstrategie "
        "vollständig, und ein Simulator ist der beste Ort, um zu erkennen, welches Modul die "
        "Aufmerksamkeit braucht.",
    ),

    h2("portekrar", "سؤالات پرتکرار: مکمل سیمیلیتور، نه جایگزین آن",
       "High-frequency sets: a complement, not a replacement",
       "Häufige Aufgaben: Ergänzung, kein Ersatz"),
    p(
        "در کنار شبیه‌ساز کامل، مجموعه‌های «پرتکرار» وجود دارند: سؤال‌ها و الگوهایی که در آزمون‌های "
        "اخیر بارها تکرار شده‌اند. این مجموعه‌ها برای سطوح B2 و C1 معنا دارند، چون در سطوح پایین‌تر "
        "تنوع سؤال آنقدر زیاد نیست که الگویابی ارزش داشته باشد.",
        "Alongside the full simulator sit high-frequency sets: the questions and patterns that keep "
        "coming back in recent exams. They make sense at B2 and C1; below that the variety is small "
        "enough that pattern-hunting earns little.",
        "Neben dem vollständigen Simulator stehen Sammlungen häufiger Aufgaben: Fragen und Muster, "
        "die in jüngeren Prüfungen immer wieder auftauchen. Sinnvoll sind sie auf B2 und C1; darunter "
        "ist die Vielfalt so gering, dass Mustersuche wenig bringt.",
    ),
    p(
        "کاربرد درست پرتکرارها این است: بعد از اینکه یک نشست کامل دادی و فهمیدی کجا ضعیف هستی، سراغ "
        "پرتکرارهای همان بخش برو. مثلاً اگر تسک تطبیق عنوان و پاراگراف را از دست می‌دهی، بیست نمونه "
        "از همان تسک را پشت سر هم کار کن تا الگو در ذهنت بنشیند. این کار از دادن پنج نشست کامل "
        "مؤثرتر و سریع‌تر است.",
        "Use them like this: sit a full simulator, learn where you are weak, then go to the "
        "high-frequency set for that part. If you keep losing heading-to-paragraph tasks, work "
        "twenty of them back to back until the pattern settles. That beats five more full sittings, "
        "and it is faster.",
        "Nutzen Sie sie so: eine vollständige Sitzung ablegen, die Schwäche erkennen, dann zur "
        "Sammlung häufiger Aufgaben genau dieses Teils gehen. Verlieren Sie ständig Punkte bei "
        "Überschrift-zu-Absatz, arbeiten Sie zwanzig davon hintereinander, bis sich das Muster "
        "setzt. Das schlägt fünf weitere Sitzungen — und geht schneller.",
    ),
    p(
        "ولی پرتکرار به‌تنهایی خطرناک است. کسی که فقط پرتکرار کار می‌کند، در حل همان الگوها ماهر "
        "می‌شود اما وقتی سر جلسه با ترکیب کامل ماژول‌ها و فشار زمان روبه‌رو می‌شود، آمادگی ندارد. "
        "ترتیب درست همیشه این است: نشست کامل، بعد پرتکرارِ هدفمند، بعد دوباره نشست کامل.",
        "But high-frequency work alone is dangerous. It makes you good at those patterns and leaves "
        "you unprepared for the full combination of modules under time pressure. The right order is "
        "always: full sitting, targeted high-frequency work, full sitting again.",
        "Allein ist die Arbeit mit häufigen Aufgaben jedoch gefährlich. Sie macht Sie in diesen "
        "Mustern stark und lässt Sie auf die volle Modulkombination unter Zeitdruck unvorbereitet. "
        "Die richtige Reihenfolge ist immer: vollständige Sitzung, gezielte Häufig-Aufgaben, wieder "
        "vollständige Sitzung.",
    ),

    h2("sprechen", "بخش گفتار: جایی که سیمیلیتور معمولی کم می‌آورد",
       "Speaking: where an ordinary simulator falls short",
       "Sprechen: wo ein gewöhnlicher Simulator versagt"),
    p(
        "تقریباً هیچ سیمیلیتور رایگانی Sprechen ندارد، چون به شریک مکالمه نیاز دارد. ولی همین ماژول "
        "است که پایین‌ترین نمره‌ی داوطلب‌های فارسی‌زبان را می‌سازد. راه‌حل عملی، تمرین با یک مربی هوش "
        "مصنوعی است که سه شرط را رعایت کند:",
        "Almost no free simulator covers Sprechen, because it needs a partner — and yet it is the "
        "module that produces the lowest scores. The practical answer is an AI teacher that meets "
        "three conditions:",
        "Kaum ein kostenloser Simulator deckt Sprechen ab, weil es eine Partnerin braucht — und "
        "gerade dieses Modul liefert die schwächsten Noten. Die praktische Lösung ist eine "
        "KI-Lehrerin, die drei Bedingungen erfüllt:",
    ),
    steps(
        ("موقعیت واقعی بدهد، نه سؤال انتزاعی. «در کنترل مرزی فرودگاه فرانکفورت هستی» خیلی مؤثرتر از "
         "«درباره‌ی سفر صحبت کن» است.",
         "Give a real situation, not an abstract prompt. \"You are at border control in Frankfurt\" "
         "beats \"talk about travel\" by a wide margin.",
         "Eine echte Situation geben, keine abstrakte Aufgabe. „Sie stehen an der Grenzkontrolle in "
         "Frankfurt“ wirkt weit besser als „Sprechen Sie über Reisen“."),
        ("زمان محدود بگذارد، چون در آزمون واقعی هم فرصت فکر کردن محدود است.",
         "Limit the time, because thinking time is limited in the real exam too.",
         "Die Zeit begrenzen, denn auch in der echten Prüfung ist Denkzeit knapp."),
        ("بازخورد تفکیکی بدهد — تلفظ، گرامر، واژگان و روانی جدا — و توضیحش به زبان خودت باشد تا "
         "واقعاً بفهمی چه چیزی را باید عوض کنی.",
         "Score per criterion — pronunciation, grammar, vocabulary, fluency — and explain in your "
         "own language, so you actually know what to change.",
         "Nach Kriterien bewerten — Aussprache, Grammatik, Wortschatz, Redefluss — und in Ihrer "
         "Sprache erklären, damit Sie wissen, was zu ändern ist."),
    ),
    cta(
        ("آلمانی در محیط", "German in Context", "Deutsch im Kontext"),
        ("وارد یک صحنه‌ی واقعی شو، سؤال بشنو، جواب بده و بازخورد تفکیکی با توضیح به زبان خودت بگیر.",
         "Step into a real scene, hear the question, answer aloud, and get feedback broken down by "
         "criterion in your own language.",
         "Treten Sie in eine echte Szene, hören Sie die Frage, antworten Sie laut und erhalten Sie "
         "eine nach Kriterien aufgeschlüsselte Rückmeldung in Ihrer Sprache."),
        "/courses/einreise-nach-deutschland",
        ("شروع «آلمانی در محیط»", "Start German in Context", "Deutsch im Kontext starten"),
    ),

    h2("eshtebah", "پنج اشتباه رایج در استفاده از سیمیلیتور",
       "Five common mistakes with simulators",
       "Fünf häufige Fehler beim Simulator"),
    steps(
        ("دادن سیمیلیتور بدون تایمر. بدون فشار زمان، آزمون به یک تمرین درک مطلب تبدیل می‌شود و "
         "کارنامه‌اش بی‌معنی است.",
         "Sitting it without a timer. Without time pressure it becomes a reading exercise and the "
         "report means nothing.",
         "Ohne Timer ablegen. Ohne Zeitdruck wird daraus eine Leseübung, und die Auswertung ist "
         "bedeutungslos."),
        ("نگاه کردن به جواب وسط آزمون. حتی یک بار، کل نشست را بی‌اعتبار می‌کند. جواب‌ها بعد از پایان.",
         "Peeking at an answer mid-exam. Once is enough to invalidate the whole sitting. Answers "
         "come after.",
         "Mitten in der Prüfung eine Lösung ansehen. Einmal genügt, um die Sitzung zu entwerten. "
         "Lösungen danach."),
        ("دادن دوباره‌ی همان کد. نمره بالا می‌رود ولی به‌خاطر حفظ بودن، نه پیشرفت. همیشه کد تازه.",
         "Repeating the same code. The score rises from memory, not progress. Always a fresh code.",
         "Denselben Code wiederholen. Die Punktzahl steigt durch Erinnerung, nicht durch "
         "Fortschritt. Immer ein neuer Code."),
        ("نبستن کارنامه با تحلیل. عددی که تحلیل نشود، فقط اضطراب می‌سازد و هیچ چیزی را اصلاح نمی‌کند.",
         "Leaving the report unanalysed. An unexamined number only produces anxiety and fixes "
         "nothing.",
         "Die Auswertung nicht analysieren. Eine ungeprüfte Zahl erzeugt nur Angst und verbessert "
         "nichts."),
        ("دادن نشست کامل در هفته‌ی آخر. در این مرحله، نتیجه‌ی بد فقط اعتماد به نفس را می‌شکند و "
         "فرصتی هم برای اصلاح نمانده.",
         "A full sitting in the final week. A bad result now only breaks confidence, with no time "
         "left to act on it.",
         "Eine vollständige Sitzung in der letzten Woche. Ein schlechtes Ergebnis bricht jetzt nur "
         "das Selbstvertrauen, ohne Zeit zum Handeln."),
    ),
    p(
        "اشتباه ششمی هم هست که کمتر گفته می‌شود: مقایسه‌ی نمره با دیگران. نمره‌ی سیمیلیتور فقط با "
        "نمره‌ی قبلی خودت معنا دارد. دو نفر با نمره‌ی یکسان می‌توانند دو نقطه‌ضعف کاملاً متفاوت داشته "
        "باشند و برنامه‌ی یکی برای دیگری بی‌فایده باشد.",
        "There is a sixth, less often said: comparing your score with other people's. A simulator "
        "score only means something against your own previous one. Two people with the same score "
        "can have entirely different weaknesses, and one's plan is useless to the other.",
        "Es gibt einen sechsten, seltener genannten: den Vergleich mit anderen. Eine "
        "Simulator-Punktzahl bedeutet nur etwas im Vergleich zur eigenen vorherigen. Zwei Personen "
        "mit gleicher Punktzahl können völlig verschiedene Schwächen haben, und der Plan der einen "
        "nützt der anderen nichts.",
    ),

    h2("jamebandi", "جمع‌بندی", "In short", "Kurz gefasst"),
    p(
        "سیمیلیتور زبان آلمانی جایگزین مطالعه نیست؛ ابزار سنجش و تنظیم آن است. مطالعه به تو دانش "
        "می‌دهد و سیمیلیتور به تو می‌گوید آن دانش در شرایط واقعی چقدر قابل استفاده است. این دو با هم "
        "کار می‌کنند و هیچ‌کدام به‌تنهایی کافی نیست.",
        "A German language simulator does not replace study; it measures and tunes it. Study gives "
        "you knowledge; the simulator tells you how much of it survives real conditions. They work "
        "together, and neither is enough alone.",
        "Ein Deutsch-Simulator ersetzt das Lernen nicht; er misst und justiert es. Lernen gibt Ihnen "
        "Wissen, der Simulator zeigt, wie viel davon reale Bedingungen übersteht. Beide gehören "
        "zusammen, keines genügt allein.",
    ),
    p(
        "یک نکته‌ی عملی هم برای انتخاب سیمیلیتور: قبل از خرید، ببین آیا کارنامه‌اش تفکیکی است و پاسخ "
        "تشریحی دارد یا نه. سرویسی که فقط یک درصد کلی نشان می‌دهد، عملاً به تو می‌گوید «خوب بودی» یا "
        "«بد بودی» و همین. سرویسی که می‌گوید در کدام نوع تسک، در کدام دقیقه و به چه دلیل نمره از دست "
        "داده‌ای، برنامه‌ی هفته‌ی بعدت را می‌نویسد.",
        "One practical test when choosing: check whether the report is broken down and whether it "
        "explains answers. A service that shows one percentage is telling you \"good\" or \"bad\" and "
        "nothing else. One that names the task type, the minute and the reason writes next week's "
        "study plan for you.",
        "Ein praktischer Prüfstein bei der Auswahl: Sehen Sie nach, ob die Auswertung aufgeschlüsselt "
        "ist und Antworten erklärt. Ein Dienst, der einen Prozentwert zeigt, sagt Ihnen „gut“ oder "
        "„schlecht“ — mehr nicht. Einer, der Aufgabentyp, Minute und Grund benennt, schreibt Ihren "
        "Lernplan für die nächste Woche.",
    ),
    p(
        "اگر فقط یک چیز از این مقاله برمی‌داری، این باشد: قبل از اینکه پول یک آزمون گران را بدهی، "
        "حداقل دو نشست کامل در شرایط واقعی بده. هزینه‌اش کسری از هزینه‌ی آزمون است و به تو می‌گوید "
        "آماده‌ای یا نه — قبل از اینکه دیر شده باشد.",
        "If you take one thing from this: before paying for an expensive exam, sit at least two full "
        "rehearsals under real conditions. It costs a fraction of the exam fee and tells you whether "
        "you are ready — while that still helps.",
        "Wenn Sie eines mitnehmen: Bevor Sie eine teure Prüfung bezahlen, legen Sie mindestens zwei "
        "vollständige Durchgänge unter echten Bedingungen ab. Das kostet einen Bruchteil der "
        "Prüfungsgebühr und sagt Ihnen, ob Sie bereit sind — solange es noch hilft.",
    ),
]

BODY += [
    h2("baraye-ki", "این روش برای چه کسی جواب می‌دهد و برای چه کسی نه",
       "Who this works for, and who it does not",
       "Für wen das funktioniert — und für wen nicht"),
    p(
        "سیمیلیتور برای همه در همه‌ی مراحل مفید نیست و صادقانه بهتر است این را بدانی. اگر تازه در "
        "سطح A1 هستی و هدفت آزمون نیست، وقت گذاشتن روی شبیه‌ساز فقط دلسردت می‌کند؛ در آن مرحله "
        "ورودی و واژگان اولویت دارند. سیمیلیتور از جایی معنا پیدا می‌کند که تاریخ آزمونی در افق "
        "باشد یا بخواهی بدانی برای کدام سطح ثبت‌نام کنی.",
        "A simulator is not useful to everyone at every stage, and it is fairer to say so. If you "
        "are at A1 with no exam in view, time on a simulator only discourages you; input and "
        "vocabulary matter more there. A simulator starts to pay once an exam date is on the "
        "horizon, or when you need to know which level to register for.",
        "Ein Simulator nützt nicht jedem in jeder Phase, und das sollte man ehrlich sagen. Sind Sie "
        "auf A1 ohne Prüfung in Sicht, entmutigt Zeit im Simulator nur; dort zählen Input und "
        "Wortschatz mehr. Ein Simulator lohnt sich, sobald ein Prüfungstermin am Horizont steht oder "
        "Sie wissen müssen, für welches Niveau Sie sich anmelden.",
    ),
    bullets(
        ("بیشترین سود: کسی که تاریخ آزمون دارد و می‌خواهد بداند کدام ماژول را باید جدی‌تر بگیرد.",
         "Most value: someone with a booked date who needs to know which module to prioritise.",
         "Größter Nutzen: wer einen Termin hat und wissen muss, welches Modul Vorrang braucht."),
        ("سود زیاد: کسی که مردد است بین دو سطح و نمی‌خواهد پول آزمون را اشتباه خرج کند.",
         "High value: someone torn between two levels who does not want to spend the fee wrongly.",
         "Hoher Nutzen: wer zwischen zwei Niveaus schwankt und die Gebühr nicht falsch ausgeben "
         "will."),
        ("سود متوسط: کسی که یک بار رد شده و باید بفهمد دقیقاً کجا نمره را از دست داده است.",
         "Moderate value: someone who has failed once and must find where the marks went.",
         "Mittlerer Nutzen: wer einmal durchgefallen ist und herausfinden muss, wo die Punkte "
         "blieben."),
        ("سود کم: مبتدی بدون هدف آزمون. برای او دوره و پادکست مفیدتر است.",
         "Low value: a beginner with no exam goal, better served by a course and podcasts.",
         "Geringer Nutzen: Anfänger ohne Prüfungsziel — Kurs und Podcasts helfen mehr."),
    ),
    p(
        "همین‌طور، سیمیلیتور جای معلم را نمی‌گیرد. کارنامه به تو می‌گوید کجا اشتباه کرده‌ای و چرا، ولی "
        "برای Schreiben و Sprechen، بازخورد انسانی یا هوش مصنوعی روی متن و گفتار خودت هنوز لازم "
        "است. بهترین ترکیب این است: سیمیلیتور برای سنجش و فرمت، دوره برای ساختار، و بازخورد برای "
        "تولید زبان.",
        "Nor does a simulator replace a teacher. The report tells you where you went wrong and why, "
        "but Schreiben and Sprechen still need human or AI feedback on your own text and speech. The "
        "best combination is a simulator for measurement and format, a course for structure, and "
        "feedback for production.",
        "Ein Simulator ersetzt auch keine Lehrkraft. Die Auswertung sagt, wo und warum Sie falsch "
        "lagen, doch Schreiben und Sprechen brauchen weiterhin menschliche oder KI-Rückmeldung zu "
        "Ihrem eigenen Text und Ihrer Stimme. Die beste Kombination: Simulator zum Messen und für "
        "das Format, Kurs für die Struktur, Rückmeldung für die Produktion.",
    ),
]

FAQ = faq(
    (("سیمیلیتور زبان آلمانی با آزمون آزمایشی چه فرقی دارد؟",
      "How is a German language simulator different from a mock test?",
      "Worin unterscheidet sich ein Deutsch-Simulator von einem Modelltest?"),
     ("آزمون آزمایشی فقط سؤال می‌دهد، ولی سیمیلیتور محیط، تایمر و قوانین آزمون واقعی را هم بازسازی "
      "می‌کند: همان رابط کاربری، همان تعداد دفعات مجاز پخش صوت و همان محدودیت حرکت بین سؤال‌ها.",
      "A mock test only supplies questions. A simulator also rebuilds the environment, the timer "
      "and the rules: the same interface, the same number of audio replays, the same limits on "
      "moving between questions.",
      "Ein Modelltest liefert nur Aufgaben. Ein Simulator baut zusätzlich Umgebung, Timer und "
      "Regeln nach: dieselbe Oberfläche, dieselbe Zahl an Audiowiederholungen, dieselben "
      "Navigationsgrenzen.")),
    (("سیمیلیتور برای چه سطوحی وجود دارد؟", "Which levels are covered?",
      "Welche Niveaus werden abgedeckt?"),
     ("برای همه‌ی سطوح A1، A2، B1، B2 و C1 شبیه‌ساز کامل موجود است. برای سطوح B2 و C1 علاوه بر "
      "شبیه‌ساز کامل، مجموعه‌های سؤالات پرتکرار هم وجود دارد.",
      "Full simulators exist for A1, A2, B1, B2 and C1. B2 and C1 also have high-frequency question "
      "sets alongside the full simulator.",
      "Vollständige Simulatoren gibt es für A1, A2, B1, B2 und C1. Für B2 und C1 kommen Sammlungen "
      "häufiger Prüfungsaufgaben hinzu.")),
    (("چند بار باید سیمیلیتور بدهم؟", "How many times should I sit one?",
      "Wie oft sollte ich ihn ablegen?"),
     ("حداقل دو نشست کامل با حدود دو هفته فاصله. چون هر کد آزمون مجموعه سؤال جداگانه‌ای دارد، "
      "نمره‌ی نشست دوم واقعاً پیشرفت را نشان می‌دهد و از حفظ بودن سؤال‌ها نمی‌آید.",
      "At least two full sittings about two weeks apart. Because each exam code is a separate "
      "question set, the second score reflects real progress rather than remembered answers.",
      "Mindestens zwei vollständige Sitzungen im Abstand von etwa zwei Wochen. Da jeder "
      "Prüfungscode ein eigener Aufgabensatz ist, zeigt die zweite Punktzahl echten Fortschritt "
      "statt erinnerter Antworten.")),
    (("آیا بخش Sprechen هم شبیه‌سازی می‌شود؟", "Is Sprechen simulated as well?",
      "Wird auch Sprechen simuliert?"),
     ("بله، از طریق مربی مکالمه‌ی هوش مصنوعی «آلمانی در محیط». صحنه‌ی واقعی می‌بینی، سؤال از تو "
      "پرسیده می‌شود، صدایت ضبط و پیاده‌سازی می‌شود و بازخورد تفکیکی می‌گیری.",
      "Yes, through the German in Context AI speaking teacher. You watch a real scene, a question "
      "is put to you, your answer is recorded and transcribed, and the feedback is broken down by "
      "criterion.",
      "Ja, über die KI-Sprechlehrerin „Deutsch im Kontext“. Sie sehen eine echte Szene, bekommen "
      "eine Frage, Ihre Antwort wird aufgenommen und transkribiert, und die Rückmeldung ist nach "
      "Kriterien aufgeschlüsselt.")),
    (("نتیجه‌ی سیمیلیتور چقدر به نمره‌ی آزمون واقعی نزدیک است؟",
      "How close is a simulator score to the real one?",
      "Wie nah liegt das Simulator-Ergebnis am echten?"),
     ("اگر نشست را در شرایط واقعی بدهی — بدون وقفه، با تایمر و بدون پخش اضافه — نتیجه معمولاً نزدیک "
      "است. هر تخفیفی که به خودت بدهی، فاصله‌ی کارنامه از واقعیت را بیشتر می‌کند.",
      "If you sit it under real conditions — uninterrupted, timed, with no extra replays — it is "
      "usually close. Every allowance you make for yourself widens the gap between the report and "
      "reality.",
      "Unter echten Bedingungen abgelegt — ohne Unterbrechung, mit Timer, ohne zusätzliche "
      "Wiederholungen — liegt es meist nah. Jede Ausnahme, die Sie sich gestatten, vergrößert den "
      "Abstand zwischen Auswertung und Wirklichkeit.")),
)
