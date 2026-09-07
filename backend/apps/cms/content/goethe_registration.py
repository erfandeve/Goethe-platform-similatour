"""«نحوه ثبت نام آزمون گوته» — the practical registration guide."""

from apps.core.i18n import tt

from ._helpers import bullets, callout, cta, faq, h2, p, steps, table

SLUG = "sabtenam-azmoun-goethe"

META = {
    "slug": SLUG,
    "order": 3,
    "reading_minutes": 14,
    "cover": "/media/covers/exams/b2-cover-8f00ecf8.png",
    "related": ["similator-zaban-almani", "nahve-khandan-zaban-almani"],
    "title": tt(
        "نحوه ثبت نام آزمون گوته: راهنمای گام‌به‌گام",
        "How to register for a Goethe exam: a step-by-step guide",
        "Anmeldung zur Goethe-Prüfung: eine Schritt-für-Schritt-Anleitung",
    ),
    "meta_title": tt(
        "نحوه ثبت نام آزمون گوته — راهنمای گام‌به‌گام | لکسورا",
        "How to Register for a Goethe Exam — Step by Step | Lexora",
        "Goethe-Prüfung anmelden — Schritt für Schritt | Lexora",
    ),
    "meta_description": tt(
        "نحوه ثبت نام آزمون گوته از انتخاب سطح تا روز آزمون: مدارک لازم، هزینه، انتخاب مرکز، "
        "ثبت‌نام آنلاین، ماژول جداگانه و کارهایی که باید قبل از رزرو انجام دهی.",
        "How to register for a Goethe exam, from choosing the level to exam day: documents, fees, "
        "picking a centre, the online form, single modules, and what to do before you pay.",
        "Anmeldung zur Goethe-Prüfung von der Niveauwahl bis zum Prüfungstag: Unterlagen, Gebühren, "
        "Prüfungszentrum, Online-Formular, Einzelmodule und was vor der Zahlung zu tun ist.",
    ),
    "focus_keyword": tt(
        "نحوه ثبت نام آزمون گوته",
        "how to register for a Goethe exam",
        "Goethe-Prüfung anmelden",
    ),
    "keywords": tt(
        "نحوه ثبت نام آزمون گوته, ثبت نام آزمون گوته, آزمون گوته, هزینه آزمون گوته, مدارک آزمون "
        "گوته, آزمون گوته B1, آزمون گوته B2, مرکز آزمون گوته, لکسورا, Lexora",
        "how to register for a Goethe exam, Goethe exam registration, Goethe-Zertifikat, Goethe "
        "exam fee, Goethe exam documents, Goethe B1, Goethe B2, exam centre, Lexora",
        "Goethe-Prüfung anmelden, Anmeldung Goethe-Zertifikat, Goethe-Prüfungsgebühr, Unterlagen "
        "Goethe-Prüfung, Goethe B1, Goethe B2, Prüfungszentrum, Lexora",
    ),
    "excerpt": tt(
        "نحوه ثبت نام آزمون گوته از انتخاب سطح شروع می‌شود، نه از باز کردن سایت. این راهنما کل مسیر "
        "را باز می‌کند: چه سطحی، کدام مرکز، چه مدارکی، چه هزینه‌ای، و چه کاری را باید قبل از پرداخت "
        "انجام دهی تا پولت هدر نرود.",
        "Registering for a Goethe exam starts with choosing the level, not with opening the website. "
        "This guide covers the whole road: which level, which centre, which documents, what it "
        "costs, and what to do before you pay so the money is not wasted.",
        "Die Anmeldung zur Goethe-Prüfung beginnt mit der Niveauwahl, nicht mit dem Öffnen der "
        "Website. Dieser Leitfaden zeigt den ganzen Weg: welches Niveau, welches Zentrum, welche "
        "Unterlagen, welche Kosten — und was vor der Zahlung zu tun ist.",
    ),
}

BODY = [
    p(
        "نحوه ثبت نام آزمون گوته در ظاهر ساده است: وارد سایت مرکز آزمون می‌شوی، سطح را انتخاب "
        "می‌کنی، پرداخت می‌کنی و تمام. ولی هر سال هزاران داوطلب دقیقاً در همین مسیر ساده پولشان را از "
        "دست می‌دهند — یا سطح اشتباه انتخاب می‌کنند، یا ظرفیت را از دست می‌دهند، یا مدرکی که سر جلسه "
        "لازم است را نمی‌آورند و راهشان نمی‌دهند.",
        "Registering for a Goethe exam looks simple: open the centre's site, pick a level, pay, "
        "done. Yet every year thousands of candidates lose their money on exactly this simple path — "
        "wrong level, missed capacity, or a document they needed at the door and did not bring.",
        "Die Anmeldung zur Goethe-Prüfung wirkt einfach: Website des Zentrums öffnen, Niveau wählen, "
        "bezahlen, fertig. Doch jedes Jahr verlieren Tausende genau auf diesem einfachen Weg ihr "
        "Geld — falsches Niveau, verpasste Plätze oder ein Dokument, das am Eingang nötig war und "
        "fehlte.",
    ),
    p(
        "این راهنما کل مسیر را از تصمیم‌گیری تا روز آزمون باز می‌کند: چطور سطح درست را انتخاب کنی، چه "
        "زمانی ثبت‌نام کنی، چه مدارکی لازم است، هزینه‌ها چطور محاسبه می‌شوند، تفاوت آزمون کامل و "
        "ماژول جداگانه چیست، و چه کارهایی را باید قبل از پرداخت انجام دهی.",
        "This guide covers the whole road from decision to exam day: choosing the right level, when "
        "to register, which documents are required, how fees work, full exam versus single module, "
        "and what to settle before you pay.",
        "Dieser Leitfaden deckt den ganzen Weg von der Entscheidung bis zum Prüfungstag ab: das "
        "richtige Niveau wählen, der Anmeldezeitpunkt, nötige Unterlagen, wie Gebühren funktionieren, "
        "Gesamtprüfung gegen Einzelmodul und was vor der Zahlung zu klären ist.",
    ),

    h2("sath", "قدم اول: کدام سطح؟", "Step one: which level?", "Schritt eins: welches Niveau?"),
    p(
        "این تصمیم قبل از هر چیز دیگری است و بیشترین اثر را روی نتیجه دارد. انتخاب سطح باید بر اساس "
        "دو چیز باشد: هدفی که مدرک برایش لازم است، و سطح واقعی فعلی‌ات — نه سطحی که فکر می‌کنی داری.",
        "This decision comes before everything else and shapes the result most. Base it on two "
        "things: what the certificate is for, and your actual current level — not the level you "
        "think you have.",
        "Diese Entscheidung steht vor allem anderen und prägt das Ergebnis am stärksten. Stützen Sie "
        "sie auf zweierlei: wofür das Zertifikat gebraucht wird und Ihr tatsächliches Niveau — nicht "
        "das, das Sie zu haben glauben.",
    ),
    table(
        ("کدام سطح برای کدام هدف", "Which level for which goal", "Welches Niveau für welches Ziel"),
        [("هدف", "Goal", "Ziel"), ("سطح لازم", "Level needed", "Nötiges Niveau"),
         ("توضیح", "Note", "Hinweis")],
        [
            [("ویزای همراه / ازدواج", "Family or spouse visa", "Familien- oder Ehegattenvisum"),
             ("A1", "A1", "A1"),
             ("معمولاً Start Deutsch 1 کافی است", "Start Deutsch 1 is usually enough",
              "Start Deutsch 1 genügt meist")],
            [("اقامت دائم", "Permanent residence", "Niederlassungserlaubnis"),
             ("B1", "B1", "B1"),
             ("همراه با آزمون Leben in Deutschland", "Alongside the Leben in Deutschland test",
              "Zusammen mit dem Test Leben in Deutschland")],
            [("Ausbildung و کار فنی", "Ausbildung and skilled work", "Ausbildung und Fachkräfte"),
             ("B1 تا B2", "B1 to B2", "B1 bis B2"),
             ("بسته به رشته؛ پرستاری معمولاً B2", "Depends on the field; nursing usually B2",
              "Je nach Bereich; Pflege meist B2")],
            [("ویزای تحصیلی (دوره زبان)", "Student visa for a language course",
              "Visum für einen Sprachkurs"),
             ("A2 تا B1", "A2 to B1", "A2 bis B1"),
             ("بسته به نامه‌ی پذیرش", "Depends on the acceptance letter",
              "Je nach Zulassungsschreiben")],
            [("تحصیل دانشگاهی", "University study", "Hochschulstudium"),
             ("C1", "C1", "C1"),
             ("بعضی رشته‌ها C1 با نمره‌ی بالا می‌خواهند", "Some subjects want C1 with a high score",
              "Manche Fächer verlangen C1 mit hoher Punktzahl")],
            [("پزشکی و پرستاری", "Medicine and nursing", "Medizin und Pflege"),
             ("B2 تا C1", "B2 to C1", "B2 bis C1"),
             ("غالباً به‌همراه آزمون تخصصی زبان", "Often with a specialist language exam",
              "Oft mit einer Fachsprachprüfung")],
        ],
    ),
    callout(
        ("قبل از انتخاب سطح، یک نشست کامل سیمیلیتور بده",
         "Sit a full simulator before choosing the level",
         "Vor der Niveauwahl eine vollständige Simulator-Sitzung"),
        ("اگر بالای ۷۰ درصد گرفتی، سطح درست است. اگر زیر ۵۰ درصد گرفتی، یک سطح پایین‌تر ثبت‌نام کن یا "
         "آزمون را عقب بینداز. هزینه‌ی سیمیلیتور کسری از هزینه‌ی آزمون است.",
         "Above seventy per cent and the level is right. Below fifty, register a level lower or push "
         "the date back. A simulator costs a fraction of the exam fee.",
         "Über siebzig Prozent, und das Niveau stimmt. Unter fünfzig: ein Niveau tiefer anmelden "
         "oder den Termin verschieben. Ein Simulator kostet einen Bruchteil der Prüfungsgebühr."),
    ),
    cta(
        ("قبل از ثبت‌نام، سطحت را بسنج", "Measure your level before you register",
         "Messen Sie Ihr Niveau vor der Anmeldung"),
        ("سیمیلیتور کامل A1 تا C1 با کارنامه‌ی تفکیکی؛ دقیقاً بفهم کجای کار ایستاده‌ای.",
         "Full A1–C1 simulators with a per-skill report, so you know exactly where you stand.",
         "Vollständige Simulatoren von A1 bis C1 mit Auswertung nach Fertigkeit — Sie wissen genau, "
         "wo Sie stehen."),
        "/exams",
        ("دیدن سیمیلیتورها", "Open the simulators", "Zu den Simulatoren"),
    ),

    h2("markaz", "قدم دوم: انتخاب مرکز آزمون",
       "Step two: choosing an exam centre", "Schritt zwei: das Prüfungszentrum"),
    p(
        "آزمون گوته را می‌شود در مؤسسه‌ی گوته یا در مراکز همکار مجاز داد. مدرک هر دو یکسان و معتبر "
        "است، ولی تفاوت‌هایی هست که روی تجربه‌ات اثر می‌گذارد:",
        "You can sit a Goethe exam at a Goethe-Institut or at an authorised partner centre. The "
        "certificate is identical and equally valid, but some differences shape the experience:",
        "Sie können die Goethe-Prüfung am Goethe-Institut oder bei einem autorisierten Partnerzentrum "
        "ablegen. Das Zertifikat ist identisch und gleich gültig, doch einige Unterschiede prägen den "
        "Ablauf:",
    ),
    bullets(
        ("تاریخ‌های آزمون: مؤسسه معمولاً تاریخ‌های ثابت دارد؛ مراکز همکار گاهی انعطاف بیشتری دارند.",
         "Dates: the institute usually has fixed dates; partner centres are sometimes more flexible.",
         "Termine: Das Institut hat meist feste Termine; Partnerzentren sind teils flexibler."),
        ("ظرفیت: در شهرهای پرتقاضا، ظرفیت سطح B1 و B2 گاهی ظرف چند ساعت پر می‌شود.",
         "Capacity: in busy cities B1 and B2 places can fill within hours.",
         "Kapazität: In nachgefragten Städten sind B1- und B2-Plätze binnen Stunden belegt."),
        ("هزینه: بین مراکز مختلف تفاوت دارد، گاهی قابل توجه.",
         "Fees vary between centres, sometimes substantially.",
         "Die Gebühren unterscheiden sich zwischen Zentren, teils deutlich."),
        ("زمان اعلام نتیجه: معمولاً بین دو تا شش هفته.",
         "Results usually take between two and six weeks.",
         "Ergebnisse dauern meist zwei bis sechs Wochen."),
        ("نسخه‌ی دیجیتال یا کاغذی: همه‌ی مراکز هر دو را ارائه نمی‌دهند و فرمت روی آماده‌سازی اثر دارد.",
         "Digital or paper: not every centre offers both, and the format changes how you prepare.",
         "Digital oder Papier: Nicht jedes Zentrum bietet beides, und das Format ändert die "
         "Vorbereitung."),
    ),
    p(
        "قبل از ثبت‌نام حتماً از مرکز بپرس آزمون به کدام صورت برگزار می‌شود. اگر دیجیتال است، تمرینت "
        "باید روی محیط دیجیتال باشد نه روی کاغذ. این نکته‌ای است که خیلی‌ها نادیده می‌گیرند و روز "
        "آزمون غافلگیر می‌شوند.",
        "Always ask the centre which format they run. If it is digital, practise digitally rather "
        "than on paper. Many people skip this question and get caught out on the day.",
        "Fragen Sie das Zentrum unbedingt nach dem Format. Ist es digital, üben Sie digital statt auf "
        "Papier. Viele überspringen diese Frage und werden am Prüfungstag überrascht.",
    ),

    h2("zaman", "قدم سوم: چه زمانی ثبت‌نام کنیم",
       "Step three: when to register", "Schritt drei: wann anmelden"),
    p(
        "ثبت‌نام معمولاً چهار تا هشت هفته قبل از تاریخ آزمون باز می‌شود و در سطوح پرتقاضا سریع پر "
        "می‌شود. قانون عملی این است که وقتی ثبت‌نام کنی که حدود شش تا هشت هفته تا آزمون مانده باشد و "
        "در سیمیلیتور بالای ۶۰ درصد بگیری.",
        "Registration usually opens four to eight weeks before the date and fills fast at popular "
        "levels. The practical rule: register when the exam is six to eight weeks away and you are "
        "scoring above sixty per cent in a simulator.",
        "Die Anmeldung öffnet meist vier bis acht Wochen vor dem Termin und ist bei gefragten Niveaus "
        "schnell voll. Praktische Regel: Melden Sie sich an, wenn die Prüfung sechs bis acht Wochen "
        "entfernt ist und Sie im Simulator über sechzig Prozent erreichen.",
    ),
    table(
        ("برنامه‌ی زمانی پیشنهادی", "A suggested timeline", "Ein empfohlener Zeitplan"),
        [("زمان", "When", "Wann"), ("کار", "What to do", "Was zu tun ist")],
        [
            [("۱۲ هفته مانده", "12 weeks out", "12 Wochen vorher"),
             ("تعیین سطح با یک نشست کامل سیمیلیتور", "Set your level with a full simulator sitting",
              "Niveau mit einer vollständigen Simulator-Sitzung bestimmen")],
            [("۸ هفته مانده", "8 weeks out", "8 Wochen vorher"),
             ("ثبت‌نام و رزرو تاریخ", "Register and book the date", "Anmelden und Termin buchen")],
            [("۶ هفته مانده", "6 weeks out", "6 Wochen vorher"),
             ("تمرکز روی ضعف‌های کارنامه", "Work on the report's weak points",
              "An den Schwachstellen der Auswertung arbeiten")],
            [("۳ هفته مانده", "3 weeks out", "3 Wochen vorher"),
             ("نشست کامل دوم با کد جدید", "Second full sitting on a new code",
              "Zweite vollständige Sitzung mit neuem Code")],
            [("۱ هفته مانده", "1 week out", "1 Woche vorher"),
             ("مرور سبک، آماده کردن مدارک", "Light review, get the documents ready",
              "Leichte Wiederholung, Unterlagen bereitlegen")],
            [("۱ روز مانده", "1 day out", "1 Tag vorher"),
             ("بررسی آدرس مرکز، خواب کافی", "Check the address, sleep properly",
              "Adresse prüfen, ausreichend schlafen")],
        ],
    ),

    h2("madarek", "قدم چهارم: مدارک لازم",
       "Step four: the documents", "Schritt vier: die Unterlagen"),
    p(
        "مدارک هم برای ثبت‌نام لازم است هم برای روز آزمون، و این دو یکی نیستند. برای ثبت‌نام آنلاین "
        "معمولاً این‌ها کافی است:",
        "Documents are needed both to register and on the day, and the two lists differ. For the "
        "online registration you usually need:",
        "Unterlagen brauchen Sie sowohl zur Anmeldung als auch am Prüfungstag — und die Listen "
        "unterscheiden sich. Für die Online-Anmeldung genügen meist:",
    ),
    steps(
        ("مشخصات هویتی دقیقاً مطابق پاسپورت یا کارت ملی — نام و نام خانوادگی به لاتین.",
         "Identity details exactly as on your passport or ID — the Latin spelling of your name.",
         "Personendaten genau wie im Pass oder Ausweis — die lateinische Schreibweise Ihres Namens."),
        ("تاریخ تولد کامل؛ اشتباه در این مورد بعداً اصلاحش دردسر دارد و گاهی هزینه.",
         "Your full date of birth; a mistake here is troublesome and sometimes costly to fix.",
         "Das vollständige Geburtsdatum; ein Fehler hier ist mühsam und mitunter teuer zu "
         "korrigieren."),
        ("ایمیل معتبر و در دسترس، چون کارت ورود به جلسه و اعلام نتیجه از همین مسیر می‌آید.",
         "A working email — the entry card and the result arrive there.",
         "Eine funktionierende E-Mail-Adresse — Zulassung und Ergebnis kommen dorthin."),
        ("شماره تماس فعال برای اطلاع‌رسانی تغییرات احتمالی.",
         "An active phone number, for notice of any changes.",
         "Eine aktive Telefonnummer für Mitteilungen über Änderungen."),
        ("روش پرداخت معتبر برای ثبت نهایی.",
         "A valid payment method to complete the booking.",
         "Eine gültige Zahlungsmethode für den Abschluss."),
    ),
    p(
        "برای روز آزمون، مدرک شناسایی عکس‌دار معتبر و اصل — نه کپی — الزامی است، و نام روی آن باید "
        "دقیقاً با نام ثبت‌نام یکی باشد. کارت ورود به جلسه هم لازم است. اگر زیر ۱۸ سال داری، معمولاً "
        "رضایت‌نامه‌ی کتبی ولی هم خواسته می‌شود.",
        "On the day you need an original photo ID — not a copy — with a name matching your "
        "registration exactly, plus the entry card. Under eighteen, written parental consent is "
        "usually required too.",
        "Am Prüfungstag brauchen Sie einen amtlichen Lichtbildausweis im Original — keine Kopie — mit "
        "einem Namen, der exakt der Anmeldung entspricht, dazu die Zulassung. Unter achtzehn ist "
        "meist auch eine schriftliche Einverständniserklärung der Eltern nötig.",
    ),
    callout(
        ("املای نام را دو بار چک کن", "Check the spelling of your name twice",
         "Prüfen Sie die Schreibweise Ihres Namens zweimal"),
        ("بیشترین مشکل روز آزمون از اختلاف املای نام بین فرم ثبت‌نام و مدرک شناسایی می‌آید. حتی یک "
         "حرف اختلاف می‌تواند به معنی راه ندادن به جلسه باشد.",
         "The commonest problem on the day is a name that does not match between the form and the "
         "ID. A single letter can mean being turned away.",
         "Das häufigste Problem am Prüfungstag ist ein Name, der zwischen Formular und Ausweis nicht "
         "übereinstimmt. Ein einziger Buchstabe kann Abweisung bedeuten."),
    ),

    h2("sabtenam", "قدم پنجم: مراحل ثبت‌نام آنلاین",
       "Step five: the online form", "Schritt fünf: das Online-Formular"),
    steps(
        ("ساخت حساب کاربری در سایت مرکز آزمون با ایمیل معتبر.",
         "Create an account on the centre's site with a working email.",
         "Konto auf der Website des Zentrums mit gültiger E-Mail anlegen."),
        ("انتخاب سطح (A1 تا C2) و نوع آزمون: کامل یا ماژول جداگانه.",
         "Choose the level (A1–C2) and the type: full exam or single module.",
         "Niveau (A1–C2) und Art wählen: Gesamtprüfung oder Einzelmodul."),
        ("انتخاب تاریخ و شهر از میان تاریخ‌های موجود.",
         "Pick the date and city from what is available.",
         "Termin und Stadt aus dem Angebot wählen."),
        ("پر کردن مشخصات هویتی دقیقاً مطابق مدرک شناسایی.",
         "Fill in your identity details exactly as on your ID.",
         "Personendaten genau wie im Ausweis eintragen."),
        ("بررسی صفحه‌ی خلاصه — این آخرین جایی است که می‌شود اشتباه را رایگان اصلاح کرد.",
         "Read the summary page — the last place a mistake is free to fix.",
         "Die Übersicht prüfen — die letzte Stelle, an der ein Fehler kostenlos korrigierbar ist."),
        ("پرداخت هزینه و دریافت کد رهگیری.",
         "Pay the fee and keep the reference number.",
         "Gebühr zahlen und die Vorgangsnummer aufbewahren."),
        ("دریافت ایمیل تأیید؛ اگر ظرف ۲۴ ساعت نیامد، اسپم را ببین و بعد با مرکز تماس بگیر.",
         "Wait for the confirmation email; if none arrives in 24 hours, check spam, then call the "
         "centre.",
         "Auf die Bestätigungs-E-Mail warten; kommt binnen 24 Stunden keine, Spam prüfen und dann "
         "das Zentrum anrufen."),
        ("چند روز قبل از آزمون، دریافت کارت ورود به جلسه با آدرس دقیق و ساعت حضور.",
         "A few days before, the entry card arrives with the exact address and arrival time.",
         "Wenige Tage vorher kommt die Zulassung mit genauer Adresse und Ankunftszeit."),
    ),
    p(
        "دو نکته‌ی عملی: اول اینکه ثبت‌نام را روی کامپیوتر انجام بده نه گوشی، چون فرم‌ها طولانی‌اند و "
        "قطع شدن وسط کار گاهی رزرو را باطل می‌کند. دوم اینکه از صفحه‌ی تأیید و کد رهگیری اسکرین‌شات "
        "بگیر و نگه دار.",
        "Two practical notes: register on a computer rather than a phone, because the forms are long "
        "and a dropped session can void the booking; and screenshot the confirmation page and "
        "reference number.",
        "Zwei praktische Hinweise: Melden Sie sich am Computer an, nicht am Handy — die Formulare "
        "sind lang, und ein Abbruch kann die Buchung ungültig machen. Und machen Sie einen "
        "Screenshot der Bestätigung samt Vorgangsnummer.",
    ),

    h2("hazineh", "هزینه‌ها", "Fees", "Gebühren"),
    p(
        "هزینه‌ی آزمون گوته به سطح، شهر و مرکز بستگی دارد و هر سال تغییر می‌کند، پس عدد دقیق را همیشه "
        "از خود مرکز بگیر. ولی چند اصل ثابت وجود دارد که در برنامه‌ریزی مالی کمک می‌کند:",
        "The fee depends on level, city and centre, and changes yearly, so always get the exact "
        "figure from the centre. A few constants help you plan:",
        "Die Gebühr hängt von Niveau, Stadt und Zentrum ab und ändert sich jährlich — holen Sie die "
        "genaue Zahl immer beim Zentrum ein. Einige Konstanten helfen bei der Planung:",
    ),
    bullets(
        ("هرچه سطح بالاتر، هزینه بیشتر. اختلاف A1 تا C1 معمولاً قابل توجه است.",
         "Higher levels cost more; the gap between A1 and C1 is usually considerable.",
         "Höhere Niveaus kosten mehr; der Abstand zwischen A1 und C1 ist meist erheblich."),
        ("ماژول جداگانه ارزان‌تر از آزمون کامل است، ولی مجموع چهار ماژول جدا معمولاً گران‌تر درمی‌آید.",
         "A single module is cheaper than the full exam, but four separate modules usually cost more "
         "than one sitting.",
         "Ein Einzelmodul ist günstiger als die Gesamtprüfung, doch vier einzelne Module kosten meist "
         "mehr als eine Sitzung."),
        ("هزینه‌ی آزمون معمولاً مسترد نمی‌شود؛ در بهترین حالت با شرایط مشخص و جریمه منتقل می‌شود.",
         "Fees are usually non-refundable; at best they transfer to another date under set "
         "conditions and a penalty.",
         "Gebühren sind meist nicht erstattungsfähig; bestenfalls werden sie unter Bedingungen und "
         "mit Gebühr auf einen anderen Termin übertragen."),
        ("درخواست بازبینی نتیجه معمولاً هزینه‌ی جداگانه دارد.",
         "Asking for a result review usually costs extra.",
         "Eine Ergebnisüberprüfung kostet meist zusätzlich."),
        ("صدور المثنی مدرک هم هزینه دارد، پس اصل مدرک را جای امن نگه دار.",
         "A replacement certificate costs money too, so keep the original safe.",
         "Auch eine Zweitschrift kostet, bewahren Sie das Original also sicher auf."),
    ),
    p(
        "همین بند سوم است که سیمیلیتور را از هزینه به سرمایه‌گذاری تبدیل می‌کند: وقتی پول آزمون "
        "برنمی‌گردد، مطمئن شدن از آمادگی قبل از پرداخت، منطقی‌ترین کار ممکن است.",
        "That third point is what turns a simulator from a cost into an investment: when the fee does "
        "not come back, confirming readiness before paying is simply the rational move.",
        "Genau dieser dritte Punkt macht aus einem Simulator statt einer Ausgabe eine Investition: "
        "Wenn die Gebühr nicht zurückkommt, ist es schlicht vernünftig, die Bereitschaft vor der "
        "Zahlung zu prüfen.",
    ),

    h2("module", "آزمون کامل یا ماژول جداگانه؟",
       "Full exam or single modules?", "Gesamtprüfung oder Einzelmodule?"),
    p(
        "از سطح B1 به بعد می‌توانی به‌جای آزمون کامل، فقط یک یا چند ماژول را ثبت‌نام کنی. این امکان "
        "خیلی مفید است ولی باید درست ازش استفاده کرد.",
        "From B1 you can register one or more modules instead of the whole exam. It is a useful "
        "option, used correctly.",
        "Ab B1 können Sie statt der Gesamtprüfung ein oder mehrere Module anmelden. Richtig genutzt "
        "ist das sehr nützlich.",
    ),
    steps(
        ("بار اول، آزمون کامل بده. اگر همه را قبول شوی، ارزان‌تر و سریع‌تر تمام شده است.",
         "First time, sit the full exam. Passing everything at once is cheaper and faster.",
         "Beim ersten Mal die Gesamtprüfung ablegen. Alles auf einmal zu bestehen ist günstiger und "
         "schneller."),
        ("اگر یک یا دو ماژول را رد شدی، فقط همان‌ها را دوباره ثبت‌نام کن.",
         "If one or two modules fail, resit only those.",
         "Fallen ein oder zwei Module durch, melden Sie nur diese erneut an."),
        ("مدرک نهایی وقتی صادر می‌شود که هر چهار ماژول قبول شده باشند.",
         "The certificate issues once all four modules are passed.",
         "Das Zertifikat wird ausgestellt, sobald alle vier Module bestanden sind."),
        ("معمولاً محدودیت زمانی وجود دارد؛ ماژول‌های قبول‌شده تا مدت مشخصی معتبر می‌مانند.",
         "There is usually a time limit; passed modules stay valid only for a set period.",
         "Meist gilt eine Frist; bestandene Module bleiben nur eine bestimmte Zeit gültig."),
    ),
    p(
        "استثنا وقتی است که از قبل مطمئنی یک مهارت خیلی ضعیف‌تر از بقیه است. مثلاً کسی که Lesen و "
        "Hören قوی دارد ولی Sprechen را تازه شروع کرده، منطقی است که سه ماژول را حالا و Sprechen را "
        "دو ماه بعد بدهد.",
        "The exception is when you already know one skill lags badly. Someone strong in Lesen and "
        "Hören but new to Sprechen sensibly sits three modules now and Sprechen two months later.",
        "Die Ausnahme: Sie wissen bereits, dass eine Fertigkeit deutlich zurückliegt. Wer in Lesen "
        "und Hören stark, im Sprechen aber Anfänger ist, legt sinnvoll drei Module jetzt und Sprechen "
        "zwei Monate später ab.",
    ),
]

BODY += [
    h2("rooz", "روز آزمون: چه چیزی در انتظارت است",
       "Exam day: what to expect", "Der Prüfungstag: was Sie erwartet"),
    p(
        "معمولاً باید حدود ۳۰ دقیقه قبل از شروع در محل باشی. مراحل روز آزمون تقریباً همیشه یکسان است:",
        "You are usually asked to arrive about thirty minutes early. The day almost always runs the "
        "same way:",
        "Meist sollen Sie etwa dreißig Minuten früher da sein. Der Tag läuft fast immer gleich ab:",
    ),
    steps(
        ("ثبت حضور و بررسی مدرک شناسایی.", "Check-in and ID inspection.",
         "Anmeldung vor Ort und Ausweiskontrolle."),
        ("تحویل وسایل شخصی؛ گوشی، ساعت هوشمند و کیف معمولاً اجازه‌ی ورود ندارند.",
         "Handing in belongings; phones, smartwatches and bags are usually not allowed in.",
         "Abgabe persönlicher Gegenstände; Handy, Smartwatch und Tasche sind meist nicht erlaubt."),
        ("نشستن سر جای تعیین‌شده و دریافت کاغذ باطله.",
         "Taking your assigned seat and receiving scrap paper.",
         "Den zugewiesenen Platz einnehmen und Schmierpapier erhalten."),
        ("ماژول‌های کتبی به ترتیب Lesen، Hören و Schreiben، با استراحت کوتاه بین بعضی‌شان.",
         "The written modules in order — Lesen, Hören, Schreiben — with short breaks between some.",
         "Die schriftlichen Module der Reihe nach — Lesen, Hören, Schreiben — mit kurzen Pausen "
         "dazwischen."),
        ("ماژول Sprechen که ممکن است همان روز یا روز دیگری و معمولاً دو نفره برگزار شود.",
         "Sprechen, which may be the same day or another, and is usually taken in pairs.",
         "Sprechen, entweder am selben oder an einem anderen Tag, meist zu zweit."),
    ),
    p(
        "چند نکته‌ی کوچک که تفاوت ایجاد می‌کنند: آب همراه داشته باش اگر مرکز اجازه می‌دهد، لباس "
        "لایه‌لایه بپوش چون دمای سالن قابل پیش‌بینی نیست، و شب قبل به‌جای مرور، بخواب. هیچ چیزی که شب "
        "قبل یاد بگیری به اندازه‌ی چهار ساعت خواب بیشتر به نمره‌ات کمک نمی‌کند.",
        "Small things that matter: bring water if the centre allows it, dress in layers because hall "
        "temperature is unpredictable, and the night before, sleep instead of revising. Nothing you "
        "learn that night helps your score as much as four more hours of sleep.",
        "Kleinigkeiten, die zählen: Wasser mitnehmen, wenn erlaubt; sich in Schichten kleiden, weil "
        "die Saaltemperatur unvorhersehbar ist; und in der Nacht davor schlafen statt wiederholen. "
        "Nichts, was Sie in dieser Nacht lernen, hilft so viel wie vier Stunden mehr Schlaf.",
    ),

    h2("natije", "بعد از آزمون: نتیجه و مدرک",
       "After the exam: result and certificate", "Nach der Prüfung: Ergebnis und Zertifikat"),
    p(
        "نتیجه معمولاً بین دو تا شش هفته اعلام می‌شود. برای قبولی باید در هر ماژول حداقل ۶۰ درصد "
        "بگیری؛ میانگین گرفتن بین ماژول‌ها پذیرفته نیست، یعنی نمره‌ی ۹۰ در Lesen، نمره‌ی ۵۰ در Hören "
        "را جبران نمی‌کند.",
        "Results usually arrive in two to six weeks. You need at least sixty per cent in each "
        "module; there is no averaging, so ninety in Lesen does not rescue fifty in Hören.",
        "Ergebnisse kommen meist in zwei bis sechs Wochen. Sie brauchen in jedem Modul mindestens "
        "sechzig Prozent; es wird nicht gemittelt, neunzig im Lesen rettet also keine fünfzig im "
        "Hören.",
    ),
    bullets(
        ("مدرک Goethe-Zertifikat تاریخ انقضا ندارد، ولی بعضی سازمان‌ها مدرک قدیمی‌تر از دو سال را "
         "نمی‌پذیرند.",
         "A Goethe-Zertifikat does not expire, but some organisations refuse one older than two "
         "years.",
         "Ein Goethe-Zertifikat verfällt nicht, doch manche Stellen akzeptieren keines, das älter "
         "als zwei Jahre ist."),
        ("اگر به نتیجه اعتراض داری، معمولاً مهلت مشخصی برای درخواست بازبینی وجود دارد.",
         "If you dispute the result, there is usually a fixed window to request a review.",
         "Bei Zweifeln am Ergebnis gibt es meist eine feste Frist für eine Überprüfung."),
        ("برای دفعه‌ی بعد معمولاً فاصله‌ی زمانی مشخصی لازم است؛ از مرکز بپرس.",
         "A minimum gap before resitting usually applies; ask the centre.",
         "Vor einer Wiederholung gilt meist eine Mindestfrist; fragen Sie das Zentrum."),
        ("اصل مدرک را اسکن کن و نسخه‌ی دیجیتال را جای امن نگه دار.",
         "Scan the original and keep the digital copy somewhere safe.",
         "Scannen Sie das Original und bewahren Sie die digitale Kopie sicher auf."),
    ),

    h2("tafavot", "گوته، TestDaF یا telc؟",
       "Goethe, TestDaF or telc?", "Goethe, TestDaF oder telc?"),
    p(
        "قبل از اینکه پول آزمون گوته را بدهی، مطمئن شو که سازمان مقصد همین مدرک را می‌خواهد. سه مدرک "
        "رایج وجود دارد و هر کدام جای خودش را دارد:",
        "Before paying for a Goethe exam, make sure the organisation you are applying to wants that "
        "certificate. Three are common, each with its own place:",
        "Bevor Sie eine Goethe-Prüfung bezahlen, vergewissern Sie sich, dass die Zielstelle genau "
        "dieses Zertifikat will. Drei sind verbreitet, jedes mit eigenem Platz:",
    ),
    table(
        ("مقایسه‌ی مدارک رایج زبان آلمانی", "Common German certificates compared",
         "Gängige Deutschzertifikate im Vergleich"),
        [("مدرک", "Certificate", "Zertifikat"), ("بیشتر برای", "Mostly for", "Vor allem für"),
         ("سطوح", "Levels", "Niveaus"), ("نکته", "Note", "Hinweis")],
        [
            [("Goethe-Zertifikat", "Goethe-Zertifikat", "Goethe-Zertifikat"),
             ("ویزا، کار، اقامت، دانشگاه", "Visa, work, residence, university",
              "Visum, Arbeit, Aufenthalt, Studium"),
             ("A1 تا C2", "A1–C2", "A1–C2"),
             ("شناخته‌شده‌ترین و مورد قبول‌ترین", "The most widely recognised",
              "Das am breitesten anerkannte")],
            [("telc", "telc", "telc"),
             ("ویزا، کار، اقامت", "Visa, work, residence", "Visum, Arbeit, Aufenthalt"),
             ("A1 تا C2", "A1–C2", "A1–C2"),
             ("معمولاً ارزان‌تر و در دسترس‌تر", "Usually cheaper and easier to book",
              "Meist günstiger und leichter buchbar")],
            [("TestDaF", "TestDaF", "TestDaF"),
             ("فقط تحصیل دانشگاهی", "University study only", "Nur Hochschulstudium"),
             ("B2 تا C1", "B2–C1", "B2–C1"),
             ("نمره‌محور، بدون قبول/رد ساده", "Score-based, no simple pass/fail",
              "Punktebasiert, kein einfaches Bestehen/Durchfallen")],
            [("ÖSD", "ÖSD", "ÖSD"),
             ("ویزا و اقامت", "Visa and residence", "Visum und Aufenthalt"),
             ("A1 تا C2", "A1–C2", "A1–C2"),
             ("اتریشی، در بعضی موارد پذیرفته می‌شود", "Austrian, accepted in some cases",
              "Österreichisch, in manchen Fällen anerkannt")],
        ],
    ),
    p(
        "قاعده‌ی ساده این است: اگر مقصدت سفارت یا اداره‌ی مهاجرت است، Goethe مطمئن‌ترین انتخاب است چون "
        "همه‌جا شناخته می‌شود. ولی هرگز بر اساس شنیده‌ها تصمیم نگیر؛ شرط زبانی را مستقیم از خود سازمان "
        "مقصد بپرس و به‌صورت مکتوب بگیر.",
        "The simple rule: if an embassy or immigration office is the destination, Goethe is the "
        "safest choice because it is recognised everywhere. But never decide on hearsay — ask the "
        "receiving organisation directly and get the requirement in writing.",
        "Die einfache Regel: Geht es an eine Botschaft oder Ausländerbehörde, ist Goethe die "
        "sicherste Wahl, weil es überall anerkannt wird. Entscheiden Sie aber nie nach Hörensagen — "
        "fragen Sie die Zielstelle direkt und lassen Sie sich die Anforderung schriftlich geben.",
    ),

    h2("amadegi", "بین ثبت‌نام تا آزمون: هشت هفته را چطور بگذرانیم",
       "Between registering and sitting: how to spend eight weeks",
       "Zwischen Anmeldung und Prüfung: acht Wochen sinnvoll nutzen"),
    p(
        "بعد از پرداخت، بیشتر داوطلب‌ها دچار یکی از دو حالت می‌شوند: یا آنقدر مضطرب می‌شوند که هر روز "
        "همه‌چیز را می‌خوانند و در هفته‌ی چهارم می‌سوزند، یا آنقدر خیالشان راحت می‌شود که تا دو هفته "
        "مانده کاری نمی‌کنند. هیچ‌کدام جواب نمی‌دهد.",
        "After paying, most candidates fall into one of two states: anxious enough to study "
        "everything daily and burn out by week four, or relaxed enough to do nothing until two weeks "
        "remain. Neither works.",
        "Nach der Zahlung geraten die meisten in einen von zwei Zuständen: so nervös, dass sie täglich "
        "alles lernen und in Woche vier ausbrennen — oder so entspannt, dass sie bis zwei Wochen "
        "vorher nichts tun. Keines funktioniert.",
    ),
    steps(
        ("هفته‌ی اول و دوم: کارنامه‌ی سیمیلیتور را باز کن و دو ضعف اصلی را مشخص کن.",
         "Weeks one and two: open the simulator report and name the two main weaknesses.",
         "Woche eins und zwei: die Simulator-Auswertung öffnen und die zwei Hauptschwächen benennen."),
        ("هفته‌ی سوم و چهارم: تسک‌های پرتکرارِ همان دو ضعف را پشت سر هم تمرین کن.",
         "Weeks three and four: drill the high-frequency tasks for exactly those two.",
         "Woche drei und vier: die häufigen Aufgaben genau dieser beiden Punkte am Stück üben."),
        ("هفته‌ی پنجم: نشست کامل دوم با کد جدید. مقایسه‌ی نمره، تنها سنجه‌ی واقعی است.",
         "Week five: a second full sitting on a new code. Comparing scores is the only real measure.",
         "Woche fünf: eine zweite vollständige Sitzung mit neuem Code. Der Punktvergleich ist das "
         "einzige echte Maß."),
        ("هفته‌ی ششم: Schreiben و Sprechen، که همیشه کمترین تمرین را می‌گیرند و بیشترین نمره را می‌برند.",
         "Week six: Schreiben and Sprechen — always the least practised and the biggest point loss.",
         "Woche sechs: Schreiben und Sprechen — stets am wenigsten geübt und am teuersten."),
        ("هفته‌ی هفتم: مرور واژگان پرتکرار و تمرین مدیریت زمان روی ماژول‌های کتبی.",
         "Week seven: review high-frequency vocabulary and rehearse timing on the written modules.",
         "Woche sieben: häufigen Wortschatz wiederholen und das Timing der schriftlichen Module üben."),
        ("هفته‌ی هشتم: سبک بخوان، مدارک را آماده کن، مسیر مرکز را یک بار برو و ببین.",
         "Week eight: study lightly, prepare the documents, and travel to the centre once to see it.",
         "Woche acht: leicht lernen, Unterlagen vorbereiten und den Weg zum Zentrum einmal abfahren."),
    ),
    p(
        "نکته‌ی مهم درباره‌ی Sprechen: این ماژول را نمی‌شود در هفته‌ی آخر جبران کرد. اگر تا حالا با کسی "
        "آلمانی صحبت نکرده‌ای، از همان هفته‌ی اول شروع کن — حتی اگر فقط ضبط کردن صدای خودت باشد.",
        "One point about Sprechen: it cannot be rescued in the final week. If you have never spoken "
        "German with anyone, start in week one — even if it is only recording yourself.",
        "Ein Hinweis zum Sprechen: In der letzten Woche ist es nicht mehr zu retten. Haben Sie noch "
        "nie mit jemandem Deutsch gesprochen, beginnen Sie in Woche eins — und sei es nur mit "
        "Aufnahmen von sich selbst.",
    ),
    cta(
        ("بخش گفتار را جدی بگیر", "Take speaking seriously", "Nehmen Sie das Sprechen ernst"),
        ("«آلمانی در محیط»: وارد یک صحنه‌ی واقعی شو، جواب بده و بازخورد تفکیکی بگیر.",
         "German in Context: step into a real scene, answer, and get feedback per criterion.",
         "Deutsch im Kontext: in eine echte Szene treten, antworten und Rückmeldung nach Kriterien "
         "erhalten."),
        "/courses/einreise-nach-deutschland",
        ("شروع «آلمانی در محیط»", "Start German in Context", "Deutsch im Kontext starten"),
    ),

    h2("eshtebahat", "شش اشتباه رایج در ثبت‌نام",
       "Six common registration mistakes", "Sechs häufige Anmeldefehler"),
    steps(
        ("انتخاب سطح بر اساس حدس. همیشه با یک نشست کامل سیمیلیتور بسنج.",
         "Choosing a level by guesswork. Always measure with a full simulator sitting.",
         "Das Niveau raten. Messen Sie immer mit einer vollständigen Simulator-Sitzung."),
        ("اختلاف املای نام بین فرم و پاسپورت. حرف‌به‌حرف چک کن.",
         "A name that differs between form and passport. Check it letter by letter.",
         "Ein Name, der zwischen Formular und Pass abweicht. Buchstabe für Buchstabe prüfen."),
        ("ثبت‌نام خیلی زودهنگام برای سطحی که هنوز نزدیکش نیستی. پول برنمی‌گردد.",
         "Registering far too early for a level you are nowhere near. The money does not come back.",
         "Viel zu früh für ein fernes Niveau anmelden. Das Geld kommt nicht zurück."),
        ("نخواندن قوانین انصراف و انتقال قبل از پرداخت.",
         "Not reading the cancellation and transfer rules before paying.",
         "Die Storno- und Umbuchungsregeln vor der Zahlung nicht lesen."),
        ("ندانستن اینکه آزمون دیجیتال است یا کاغذی، و تمرین کردن روی فرمت اشتباه.",
         "Not knowing whether the exam is digital or on paper, and practising the wrong format.",
         "Nicht zu wissen, ob die Prüfung digital oder auf Papier ist — und im falschen Format "
         "üben."),
        ("نگه نداشتن کد رهگیری و ایمیل تأیید.",
         "Not keeping the reference number and confirmation email.",
         "Vorgangsnummer und Bestätigungs-E-Mail nicht aufbewahren."),
    ),

    h2("jamebandi", "جمع‌بندی", "In short", "Kurz gefasst"),
    p(
        "نحوه ثبت نام آزمون گوته از نظر فنی پیچیده نیست؛ چیزی که پیچیده است، تصمیم‌های قبل از آن است. "
        "سطح درست، زمان درست و اطمینان از آمادگی — این سه چیز تعیین می‌کنند که پولی که می‌دهی به مدرک "
        "تبدیل شود یا نه.",
        "Registering for a Goethe exam is not technically complicated; the decisions before it are. "
        "The right level, the right date and real confidence in your readiness decide whether the "
        "money becomes a certificate.",
        "Die Anmeldung zur Goethe-Prüfung ist technisch nicht kompliziert; kompliziert sind die "
        "Entscheidungen davor. Das richtige Niveau, der richtige Termin und echte Sicherheit über "
        "Ihre Bereitschaft entscheiden, ob aus dem Geld ein Zertifikat wird.",
    ),
    p(
        "خلاصه‌ی کل مسیر در یک جمله: سطحت را با یک نشست کامل بسنج، شش تا هشت هفته قبل ثبت‌نام کن، نام "
        "را حرف‌به‌حرف با پاسپورت چک کن، بین ثبت‌نام تا آزمون روی دو ضعف اصلی کارنامه‌ات کار کن و "
        "مدارک را یک هفته قبل آماده بگذار.",
        "The whole road in one line: measure your level with a full sitting, register six to eight "
        "weeks out, check your name against your passport letter by letter, work the two main "
        "weaknesses in between, and have the documents ready a week before.",
        "Der ganze Weg in einem Satz: Niveau mit einer vollständigen Sitzung messen, sechs bis acht "
        "Wochen vorher anmelden, den Namen buchstabengenau mit dem Pass abgleichen, dazwischen an den "
        "zwei Hauptschwächen arbeiten und die Unterlagen eine Woche vorher bereitlegen.",
    ),
    p(
        "ترتیب درست همیشه همین است: اول بسنج، بعد ثبت‌نام کن، بعد آماده شو. برعکسش — ثبت‌نام کردن و "
        "بعد امیدوار بودن — همان کاری است که بیشترین تعداد داوطلب را هر سال ناامید می‌کند.",
        "The order is always: measure, register, prepare. The reverse — register and then hope — is "
        "what disappoints the most candidates every year.",
        "Die Reihenfolge lautet immer: messen, anmelden, vorbereiten. Umgekehrt — anmelden und dann "
        "hoffen — enttäuscht jedes Jahr die meisten.",
    ),
]

BODY += [
    h2("khareji", "ثبت‌نام از خارج از آلمان و نکات ویژه",
       "Registering from outside Germany", "Anmeldung aus dem Ausland"),
    p(
        "اگر در کشوری غیر از آلمان ثبت‌نام می‌کنی، چند نکته‌ی اضافه وجود دارد که در راهنماهای عمومی "
        "گفته نمی‌شود و می‌تواند برنامه‌ات را به هم بریزد. اولین و مهم‌ترینشان ظرفیت است: مراکز خارج "
        "از آلمان معمولاً تعداد صندلی کمتری دارند و تاریخ‌های کمتری در سال برگزار می‌کنند، پس از دست "
        "دادن یک تاریخ می‌تواند به معنی سه ماه تأخیر باشد.",
        "Registering from outside Germany brings extra considerations that general guides skip and "
        "that can wreck a timeline. The first and biggest is capacity: centres abroad usually have "
        "fewer seats and fewer dates per year, so missing one date can mean a three-month delay.",
        "Die Anmeldung aus dem Ausland bringt zusätzliche Punkte mit sich, die allgemeine Leitfäden "
        "auslassen und die einen Zeitplan zerstören können. Der erste und wichtigste ist die "
        "Kapazität: Zentren im Ausland haben meist weniger Plätze und weniger Termine pro Jahr — ein "
        "verpasster Termin kann drei Monate Verzögerung bedeuten.",
    ),
    bullets(
        ("روز باز شدن ثبت‌نام را در تقویمت علامت بزن و همان روز اقدام کن.",
         "Mark the day registration opens in your calendar and act that same day.",
         "Markieren Sie den Öffnungstag der Anmeldung im Kalender und handeln Sie am selben Tag."),
        ("روش پرداخت ممکن است با آنچه انتظار داری فرق کند. قبل از رسیدن به مرحله‌ی پرداخت بپرس چه "
         "روش‌هایی پذیرفته می‌شود تا وسط کار رزروت باطل نشود.",
         "Payment methods may not be what you expect. Ask which are accepted before you reach the "
         "payment step, so a booking is not voided halfway through.",
         "Zahlungsmethoden sind womöglich nicht die erwarteten. Fragen Sie vor dem Zahlungsschritt "
         "nach, welche akzeptiert werden, damit keine Buchung mittendrin verfällt."),
        ("اگر برای ارائه به سفارت مدرک می‌خواهی، زمان صدور و ارسال فیزیکی مدرک را هم در برنامه‌ات "
         "حساب کن؛ این مرحله گاهی چند هفته اضافه می‌کند.",
         "If the certificate is for an embassy, budget for issuing and physical delivery as well; "
         "that stage can add weeks.",
         "Ist das Zertifikat für eine Botschaft, rechnen Sie Ausstellung und Postversand ein; diese "
         "Phase kann Wochen kosten."),
        ("اگر برای آزمون به شهر دیگری سفر می‌کنی، طوری برنامه‌ریزی کن که شب قبل آنجا باشی؛ رسیدن در "
         "صبح روز آزمون ریسک غیرضروری است.",
         "If you travel to another city, arrange to be there the night before; arriving on the "
         "morning is an unnecessary risk.",
         "Reisen Sie in eine andere Stadt, seien Sie am Vorabend dort; die Anreise am Prüfungsmorgen "
         "ist ein unnötiges Risiko."),
        ("ایمیل‌های مرکز را جدی بگیر. تغییر ساعت و محل معمولاً فقط از همین راه اطلاع داده می‌شود.",
         "Take the centre's emails seriously. Changes of time and venue are usually announced only "
         "that way.",
         "Nehmen Sie die E-Mails des Zentrums ernst. Zeit- und Ortsänderungen werden meist nur so "
         "mitgeteilt."),
    ),
    p(
        "یک توصیه‌ی عملی هم درباره‌ی مدرک شناسایی: اگر پاسپورتت نزدیک به انقضاست یا در فرآیند تمدید "
        "است، قبل از ثبت‌نام تکلیفش را روشن کن. مدرکی که سر جلسه ارائه می‌دهی باید همان مدرکی باشد که "
        "با آن ثبت‌نام کرده‌ای؛ عوض شدن شماره‌ی پاسپورت بین ثبت‌نام و روز آزمون دردسر درست می‌کند و "
        "حل کردنش در آخرین هفته تقریباً غیرممکن است.",
        "One practical note on ID: if your passport is close to expiry or being renewed, settle that "
        "before you register. The document you present must be the one you registered with; a "
        "passport number changing between registration and exam day causes trouble that is almost "
        "impossible to resolve in the final week.",
        "Ein praktischer Hinweis zum Ausweis: Läuft Ihr Pass bald ab oder wird er erneuert, klären "
        "Sie das vor der Anmeldung. Das vorgelegte Dokument muss dasselbe sein wie bei der Anmeldung; "
        "eine geänderte Passnummer zwischen Anmeldung und Prüfungstag verursacht Probleme, die sich "
        "in der letzten Woche kaum noch lösen lassen.",
    ),
    p(
        "و آخرین نکته که ساده به نظر می‌رسد ولی هر سال عده‌ای را زمین می‌زند: صندوق ایمیلی که برای "
        "ثبت‌نام دادی را تا روز آزمون مرتب چک کن و آدرس فرستنده را به فهرست مخاطبان امن اضافه کن تا "
        "پیام‌ها در پوشه‌ی اسپم نیفتند. کارت ورود به جلسه، تغییر ساعت و حتی لغو احتمالی آزمون، همگی "
        "از همین یک مسیر می‌آیند.",
        "A last point that sounds trivial and still catches people out every year: check the inbox "
        "you registered with regularly until exam day, and add the sender to your safe list so "
        "messages do not land in spam. The entry card, a change of time and even a cancellation all "
        "arrive by that single route.",
        "Ein letzter Punkt, der banal klingt und dennoch jedes Jahr Leute erwischt: Prüfen Sie das "
        "Postfach, mit dem Sie sich angemeldet haben, bis zum Prüfungstag regelmäßig, und setzen Sie "
        "den Absender auf die Positivliste, damit nichts im Spam landet. Zulassung, Zeitänderung und "
        "sogar eine Absage kommen alle über diesen einen Weg.",
    ),
]

BODY += [
    h2("agar-rad", "اگر رد شدی چه کار کنی",
       "What to do if you fail", "Was tun, wenn Sie durchfallen"),
    p(
        "رد شدن در آزمون گوته پایان راه نیست و آمار نشان می‌دهد بخش قابل توجهی از داوطلب‌ها بار اول "
        "حداقل یک ماژول را از دست می‌دهند. کاری که در دو هفته‌ی بعد از دیدن نتیجه می‌کنی، تعیین می‌کند "
        "که دفعه‌ی بعد قبول می‌شوی یا دوباره همان‌جا می‌مانی.",
        "Failing a Goethe exam is not the end of the road, and a sizeable share of candidates lose at "
        "least one module on the first attempt. What you do in the fortnight after seeing the result "
        "decides whether the next attempt passes or lands in the same place.",
        "Eine nicht bestandene Goethe-Prüfung ist kein Endpunkt, und ein erheblicher Teil der "
        "Kandidatinnen und Kandidaten verliert beim ersten Versuch mindestens ein Modul. Was Sie in "
        "den zwei Wochen nach dem Ergebnis tun, entscheidet, ob der nächste Versuch besteht oder "
        "wieder dort landet.",
    ),
    steps(
        ("کارنامه را دقیق بخوان و ببین در کدام ماژول و چند نمره کم آورده‌ای. گاهی فاصله دو یا سه "
         "نمره است و با یک اصلاح کوچک پر می‌شود.",
         "Read the report closely: which module, and by how many marks. Sometimes the gap is two or "
         "three points and one small fix closes it.",
         "Lesen Sie die Auswertung genau: welches Modul und wie viele Punkte. Manchmal sind es zwei "
         "oder drei Punkte, die eine kleine Korrektur schließt."),
        ("فقط ماژول‌های رد‌شده را دوباره ثبت‌نام کن، نه کل آزمون را — اگر سطحت B1 یا بالاتر است.",
         "Register only the failed modules, not the whole exam, if you are at B1 or above.",
         "Melden Sie nur die nicht bestandenen Module erneut an, nicht die ganze Prüfung — ab B1."),
        ("قبل از ثبت‌نام دوباره، یک نشست کامل سیمیلیتور با کد تازه بده تا ببینی واقعاً کجا ایستاده‌ای.",
         "Before registering again, sit a full simulator on a fresh code to see where you actually "
         "stand.",
         "Vor der erneuten Anmeldung eine vollständige Simulator-Sitzung mit neuem Code ablegen, um "
         "den tatsächlichen Stand zu sehen."),
        ("مهلت اعتبار ماژول‌های قبول‌شده را از مرکز بپرس و تاریخ بعدی را داخل همان بازه انتخاب کن.",
         "Ask the centre how long your passed modules stay valid and pick a date inside that window.",
         "Fragen Sie das Zentrum, wie lange bestandene Module gültig bleiben, und wählen Sie einen "
         "Termin in diesem Fenster."),
    ),
    p(
        "و یک نکته‌ی روانی که کم گفته می‌شود: بیشتر کسانی که بار دوم رد می‌شوند، دقیقاً همان کاری را "
        "کرده‌اند که بار اول کرده بودند، فقط بیشتر. اگر روشت جواب نداده، تکرار آن با شدت بیشتر هم "
        "جواب نمی‌دهد. کارنامه را ملاک بگذار و برنامه را عوض کن، نه ساعت مطالعه را.",
        "One psychological point that is rarely said: most people who fail a second time did exactly "
        "what they did the first time, only more of it. If the method did not work, more of it will "
        "not either. Let the report set the plan, and change the plan rather than the hours.",
        "Ein psychologischer Punkt, der selten gesagt wird: Die meisten, die ein zweites Mal "
        "durchfallen, haben genau dasselbe getan wie beim ersten Mal, nur mehr davon. Hat die Methode "
        "nicht gewirkt, wirkt auch mehr davon nicht. Lassen Sie die Auswertung den Plan bestimmen und "
        "ändern Sie den Plan, nicht die Stundenzahl.",
    ),
]

BODY += [
    h2("checklist", "فهرست نهایی: قبل از کلیک روی «پرداخت»",
       "Final checklist before you click pay",
       "Letzte Checkliste vor dem Klick auf „Bezahlen“"),
    p(
        "این هشت مورد را یک‌بار مرور کن. هر کدام را که رد کنی، ریسکی اضافه کرده‌ای که لازم نبود، و "
        "بیشترشان بعد از پرداخت دیگر قابل اصلاح رایگان نیستند.",
        "Run through these eight once. Skipping any adds a risk you did not need, and most of them "
        "stop being free to fix the moment you pay.",
        "Gehen Sie diese acht Punkte einmal durch. Jeden übersprungenen Punkt bezahlen Sie mit einem "
        "unnötigen Risiko, und die meisten lassen sich nach der Zahlung nicht mehr kostenlos "
        "korrigieren.",
    ),
    bullets(
        ("سطح را با یک نشست کامل سیمیلیتور سنجیده‌ام و بالای ۶۰ درصد گرفته‌ام.",
         "I measured the level with a full simulator sitting and scored above sixty per cent.",
         "Ich habe das Niveau mit einer vollständigen Simulator-Sitzung gemessen und über sechzig "
         "Prozent erreicht."),
        ("سازمان مقصد را پرسیده‌ام که دقیقاً همین مدرک و همین سطح را قبول دارد.",
         "I confirmed with the receiving organisation that this exact certificate and level is "
         "accepted.",
         "Ich habe bei der Zielstelle bestätigt, dass genau dieses Zertifikat und Niveau anerkannt "
         "wird."),
        ("نام و نام خانوادگی را حرف‌به‌حرف با پاسپورت مقایسه کرده‌ام.",
         "I compared my name letter by letter with my passport.",
         "Ich habe meinen Namen Buchstabe für Buchstabe mit dem Pass verglichen."),
        ("تاریخ تولد و شماره‌ی مدرک شناسایی را دوباره چک کرده‌ام.",
         "I re-checked my date of birth and ID number.",
         "Ich habe Geburtsdatum und Ausweisnummer erneut geprüft."),
        ("پرسیده‌ام آزمون دیجیتال است یا کاغذی، و تمرینم را با همان فرمت تنظیم کرده‌ام.",
         "I asked whether the exam is digital or on paper and matched my practice to it.",
         "Ich habe gefragt, ob die Prüfung digital oder auf Papier ist, und meine Übung angepasst."),
        ("قوانین انصراف، انتقال تاریخ و بازبینی نتیجه را خوانده‌ام.",
         "I read the rules on cancellation, date transfer and result review.",
         "Ich habe die Regeln zu Storno, Terminverlegung und Ergebnisüberprüfung gelesen."),
        ("مطمئن شده‌ام تا روز آزمون پاسپورتم معتبر است و در فرآیند تمدید نیست.",
         "I made sure my passport stays valid until exam day and is not being renewed.",
         "Ich habe sichergestellt, dass mein Pass bis zum Prüfungstag gültig und nicht in Erneuerung "
         "ist."),
        ("ایمیل و شماره‌ی تماسی که وارد می‌کنم تا روز آزمون در دسترسم هستند.",
         "The email and phone number I am entering will reach me until exam day.",
         "Die eingetragene E-Mail-Adresse und Telefonnummer erreichen mich bis zum Prüfungstag."),
    ),
]

FAQ = faq(
    (("نحوه ثبت نام آزمون گوته چگونه است؟", "How do I register for a Goethe exam?",
      "Wie melde ich mich zur Goethe-Prüfung an?"),
     ("در سایت مرکز آزمون حساب می‌سازی، سطح و تاریخ را انتخاب می‌کنی، مشخصات هویتی را دقیقاً مطابق "
      "مدرک شناسایی وارد می‌کنی و هزینه را پرداخت می‌کنی. بعد ایمیل تأیید و چند روز قبل از آزمون، "
      "کارت ورود به جلسه دریافت می‌کنی.",
      "Create an account on the exam centre's site, choose the level and date, enter your identity "
      "details exactly as on your ID, and pay. A confirmation email follows, and the entry card "
      "arrives a few days before the exam.",
      "Legen Sie ein Konto auf der Website des Prüfungszentrums an, wählen Sie Niveau und Termin, "
      "tragen Sie Ihre Daten genau wie im Ausweis ein und zahlen Sie. Danach folgt eine Bestätigung, "
      "und wenige Tage vor der Prüfung kommt die Zulassung.")),
    (("چه مدارکی لازم است؟", "Which documents do I need?", "Welche Unterlagen brauche ich?"),
     ("برای ثبت‌نام آنلاین، مشخصات هویتی مطابق پاسپورت یا کارت ملی، ایمیل و شماره تماس معتبر و روش "
      "پرداخت. برای روز آزمون، اصل مدرک شناسایی عکس‌دار و کارت ورود به جلسه الزامی است.",
      "To register: identity details matching your passport or ID, a working email and phone number, "
      "and a payment method. On the day: an original photo ID and the entry card.",
      "Zur Anmeldung: Personendaten wie im Pass oder Ausweis, eine funktionierende E-Mail-Adresse und "
      "Telefonnummer sowie eine Zahlungsmethode. Am Prüfungstag: Lichtbildausweis im Original und die "
      "Zulassung.")),
    (("چند وقت قبل از آزمون باید ثبت‌نام کنم؟", "How far ahead should I register?",
      "Wie lange im Voraus sollte ich mich anmelden?"),
     ("معمولاً شش تا هشت هفته قبل. در سطوح پرتقاضا مثل B1 و B2 ظرفیت سریع پر می‌شود، پس به محض باز "
      "شدن ثبت‌نام اقدام کن — به شرطی که در سیمیلیتور بالای ۶۰ درصد گرفته باشی.",
      "Usually six to eight weeks. Popular levels like B1 and B2 fill quickly, so act as soon as "
      "registration opens — provided you are already above sixty per cent in a simulator.",
      "Meist sechs bis acht Wochen. Gefragte Niveaus wie B1 und B2 sind schnell voll, handeln Sie "
      "also, sobald die Anmeldung öffnet — sofern Sie im Simulator bereits über sechzig Prozent "
      "liegen.")),
    (("می‌توانم فقط یک ماژول را ثبت‌نام کنم؟", "Can I register for a single module?",
      "Kann ich ein einzelnes Modul anmelden?"),
     ("بله، از سطح B1 به بعد ماژول‌ها جداگانه قابل ثبت‌نام و قبولی هستند. مدرک نهایی وقتی صادر می‌شود "
      "که هر چهار ماژول قبول شده باشند، و ماژول‌های قبول‌شده معمولاً محدودیت زمانی اعتبار دارند.",
      "Yes, from B1 upwards modules can be registered and passed separately. The certificate issues "
      "once all four are passed, and passed modules usually stay valid only for a limited period.",
      "Ja, ab B1 lassen sich Module einzeln anmelden und bestehen. Das Zertifikat wird ausgestellt, "
      "sobald alle vier bestanden sind; bestandene Module bleiben meist nur begrenzt gültig.")),
    (("اگر قبول نشوم پول برمی‌گردد؟", "Do I get a refund if I fail?",
      "Bekomme ich Geld zurück, wenn ich durchfalle?"),
     ("خیر. هزینه‌ی آزمون در صورت رد شدن مسترد نمی‌شود و باید برای دفعه‌ی بعد دوباره ثبت‌نام کنی. به "
      "همین دلیل سنجیدن آمادگی با سیمیلیتور قبل از ثبت‌نام، منطقی‌ترین کار است.",
      "No. The fee is not refunded if you fail and you must register again. That is why measuring "
      "your readiness with a simulator before registering is the rational move.",
      "Nein. Die Gebühr wird bei Nichtbestehen nicht erstattet, Sie müssen sich erneut anmelden. "
      "Deshalb ist es vernünftig, die Bereitschaft vor der Anmeldung mit einem Simulator zu "
      "prüfen.")),
    (("نمره‌ی قبولی چند است؟", "What is the pass mark?", "Wie hoch ist die Bestehensgrenze?"),
     ("در هر ماژول حداقل ۶۰ درصد لازم است. میانگین‌گیری بین ماژول‌ها پذیرفته نمی‌شود، یعنی نمره‌ی بالا "
      "در یک ماژول، نمره‌ی پایین در ماژول دیگر را جبران نمی‌کند.",
      "At least sixty per cent in each module. There is no averaging, so a high score in one module "
      "does not compensate for a low one in another.",
      "Mindestens sechzig Prozent in jedem Modul. Es wird nicht gemittelt, eine hohe Punktzahl in "
      "einem Modul gleicht eine niedrige in einem anderen also nicht aus.")),
)
