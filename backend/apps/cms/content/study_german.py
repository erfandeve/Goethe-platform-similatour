"""«نحوه خواندن زبان آلمانی» — the top-of-funnel guide."""

from apps.core.i18n import tt

from ._helpers import bullets, callout, cta, faq, h2, h3, p, quote, steps, table

SLUG = "nahve-khandan-zaban-almani"

META = {
    "slug": SLUG,
    "order": 2,
    "reading_minutes": 14,
    "cover": "/media/covers/courses/einreise-cover-201c4ad9.png",
    "related": ["similator-zaban-almani", "sabtenam-azmoun-goethe"],
    "title": tt(
        "نحوه خواندن زبان آلمانی: راهنمای کامل از صفر تا C1",
        "How to study German: a complete guide from zero to C1",
        "Deutsch lernen: der vollständige Leitfaden von null bis C1",
    ),
    "meta_title": tt(
        "نحوه خواندن زبان آلمانی — راهنمای کامل صفر تا C1 | لکسورا",
        "How to Study German — Complete Guide, Zero to C1 | Lexora",
        "Deutsch lernen — vollständiger Leitfaden von null bis C1 | Lexora",
    ),
    "meta_description": tt(
        "نحوه خواندن زبان آلمانی از صفر تا C1: برنامه هفتگی، روش یادگیری گرامر و واژگان، تقویت "
        "شنیداری و مکالمه، و اشتباهات رایج فارسی‌زبان‌ها.",
        "How to study German from zero to C1: a weekly plan, how to learn grammar and vocabulary, "
        "building listening and speaking, and the mistakes that cost learners most.",
        "Deutsch lernen von null bis C1: Wochenplan, Grammatik und Wortschatz richtig lernen, Hören "
        "und Sprechen aufbauen — und die teuersten Fehler.",
    ),
    "focus_keyword": tt("نحوه خواندن زبان آلمانی", "how to study German", "Deutsch lernen"),
    "keywords": tt(
        "نحوه خواندن زبان آلمانی, یادگیری زبان آلمانی, آموزش زبان آلمانی از صفر, چطور آلمانی یاد "
        "بگیریم, برنامه یادگیری زبان آلمانی, گرامر زبان آلمانی, سطح A1 تا C1, لکسورا, Lexora",
        "how to study German, learn German from scratch, German study plan, German grammar order, "
        "German vocabulary method, A1 to C1, Lexora",
        "Deutsch lernen, Deutsch von null lernen, Deutsch Lernplan, deutsche Grammatik Reihenfolge, "
        "Wortschatz Deutsch, A1 bis C1, Lexora",
    ),
    "excerpt": tt(
        "اگر می‌خواهی بدانی نحوه خواندن زبان آلمانی از کجا شروع می‌شود و تا C1 چه مسیری دارد، این "
        "راهنما همان نقشه‌ای است که کاش روز اول داشتی: برنامه هفتگی، ترتیب درست موضوع‌ها و "
        "دام‌هایی که یادگیرنده‌ها تویشان می‌افتند.",
        "If you want to know where studying German starts and what the road to C1 looks like, this "
        "is the map you wish you had on day one: a weekly plan, the right order for the grammar, "
        "and the traps learners fall into.",
        "Wenn Sie wissen wollen, wo Deutschlernen beginnt und wie der Weg bis C1 aussieht: Das ist "
        "die Karte, die man sich am ersten Tag wünscht — Wochenplan, die richtige Reihenfolge der "
        "Grammatik und die Fallen, in die Lernende geraten.",
    ),
}

BODY = [
    p(
        "سؤال «نحوه خواندن زبان آلمانی چطور است؟» تقریباً همیشه با یک جواب اشتباه روبه‌رو می‌شود: "
        "«یک کتاب بخر و از درس اول شروع کن.» این جواب بد نیست، ناقص است. زبان آلمانی سه گلوگاه دارد "
        "که هیچ‌کدام در درس اول کتاب پیدا نمی‌شوند: جنسیت اسم‌ها، سیستم حالت‌ها (Fälle) و ترتیب "
        "کلمات در جمله. کسی که این سه را از همان هفته‌های اول درست بچیند، در ماه ششم روان صحبت "
        "می‌کند؛ کسی که نچیند، در ماه بیست‌وچهارم هنوز وسط جمله دنبال فعل می‌گردد.",
        "\"How do I study German?\" almost always gets the same incomplete answer: buy a book and "
        "start at lesson one. German has three bottlenecks, and none of them appear in lesson one: "
        "noun gender, the case system, and word order. Get those three right in the first weeks and "
        "you speak fluently by month six; get them wrong and at month twenty-four you are still "
        "hunting for the verb halfway through a sentence.",
        "„Wie lerne ich Deutsch?“ bekommt fast immer dieselbe unvollständige Antwort: Kaufen Sie ein "
        "Buch und beginnen Sie bei Lektion eins. Deutsch hat drei Engstellen, und keine steht in "
        "Lektion eins: Nomengenus, das Kasussystem und die Wortstellung. Wer diese drei in den "
        "ersten Wochen richtig legt, spricht im sechsten Monat flüssig; wer nicht, sucht im "
        "vierundzwanzigsten noch mitten im Satz das Verb.",
    ),
    p(
        "این راهنما مسیر کامل را از صفر تا C1 باز می‌کند: چه چیزی را با چه ترتیبی بخوانی، هر روز "
        "چقدر وقت بگذاری، چطور واژه حفظ کنی که فراموش نشود، و مهم‌تر از همه، از کجا بفهمی واقعاً "
        "پیشرفت کرده‌ای یا فقط احساس پیشرفت داری.",
        "This guide lays out the whole road from zero to C1: what to study in what order, how much "
        "time per day, how to memorise vocabulary so it stays, and above all how to tell real "
        "progress from the feeling of progress.",
        "Dieser Leitfaden zeigt den ganzen Weg von null bis C1: was in welcher Reihenfolge, wie viel "
        "Zeit pro Tag, wie Vokabeln haften bleiben und vor allem, wie Sie echten Fortschritt vom "
        "Gefühl des Fortschritts unterscheiden.",
    ),

    h2("hadaf", "قدم صفر: هدفت را دقیق کن، وگرنه مسیر را اشتباه می‌روی",
       "Step zero: name the goal, or you will take the wrong road",
       "Schritt null: das Ziel benennen, sonst nehmen Sie den falschen Weg"),
    p(
        "قبل از اینکه اولین کلمه را حفظ کنی باید بدانی برای چه می‌خوانی، چون نحوه خواندن زبان آلمانی "
        "برای مهاجرت کاری با خواندن برای تحصیل فرق دارد. سه هدف رایج وجود دارد و هر کدام سطح مقصد "
        "متفاوتی دارند:",
        "Before the first word, know what you are studying for: preparing for a work visa is not "
        "the same as preparing for university. Three goals are common, each with its own target "
        "level:",
        "Vor dem ersten Wort sollten Sie wissen, wofür Sie lernen: Vorbereitung auf ein "
        "Arbeitsvisum ist etwas anderes als auf ein Studium. Drei Ziele sind häufig, jedes mit "
        "eigenem Zielniveau:",
    ),
    bullets(
        ("ویزای همراه یا ازدواج: معمولاً A1 کافی است — تمرکز روی جمله‌های ساده روزمره.",
         "Family or spouse visa: A1 is usually enough — simple everyday sentences.",
         "Familien- oder Ehegattenvisum: A1 genügt meist — einfache Alltagssätze."),
        ("ویزای کار، Ausbildung یا پرستاری: B1 تا B2. اینجا مکالمه و نوشتن رسمی وزن زیادی دارند.",
         "Work visa, Ausbildung or nursing: B1 to B2, where speaking and formal writing carry real "
         "weight.",
         "Arbeitsvisum, Ausbildung oder Pflege: B1 bis B2, wo Sprechen und formelles Schreiben stark "
         "zählen."),
        ("تحصیل در دانشگاه آلمان: C1، و در بعضی رشته‌ها C1 با نمره‌ی بالا.",
         "University in Germany: C1, and in some subjects C1 with a high score.",
         "Studium in Deutschland: C1, in manchen Fächern C1 mit hoher Punktzahl."),
    ),
    p(
        "اگر هدفت B1 است، وقت گذاشتن روی گرامر پیشرفته‌ی C1 در ماه سوم فقط انرژی‌ات را می‌سوزاند. "
        "برعکس، اگر هدفت C1 است، رها کردن نوشتن در سطح A2 یعنی سه ماه بعد باید از اول شروع کنی.",
        "If B1 is the goal, grinding C1 grammar in month three only burns energy. Conversely, if C1 "
        "is the goal, skipping writing at A2 means restarting it three months later.",
        "Ist B1 das Ziel, verbrennt C1-Grammatik im dritten Monat nur Energie. Ist C1 das Ziel, "
        "bedeutet ausgelassenes Schreiben auf A2, dass Sie drei Monate später von vorn anfangen.",
    ),
    table(
        ("زمان تقریبی لازم برای هر سطح، با فرض مطالعه‌ی روزانه",
         "Roughly how long each level takes, studying daily",
         "Ungefährer Zeitbedarf pro Niveau bei täglichem Lernen"),
        [("سطح", "Level", "Niveau"), ("ساعت مطالعه", "Study hours", "Lernstunden"),
         ("با ۱ ساعت در روز", "At 1 h/day", "Bei 1 Std./Tag"),
         ("با ۳ ساعت در روز", "At 3 h/day", "Bei 3 Std./Tag"),
         ("چه کاری می‌توانی بکنی", "What you can do", "Was Sie können")],
        [
            [("A1", "A1", "A1"), ("۸۰ تا ۱۰۰", "80–100", "80–100"), ("۳ ماه", "3 months", "3 Monate"),
             ("۵ هفته", "5 weeks", "5 Wochen"),
             ("معرفی خود، خرید کردن، جمله‌های کوتاه", "Introduce yourself, shop, short sentences",
              "Sich vorstellen, einkaufen, kurze Sätze")],
            [("A2", "A2", "A2"), ("۱۸۰ تا ۲۰۰", "180–200", "180–200"), ("۶ ماه", "6 months", "6 Monate"),
             ("۲ ماه", "2 months", "2 Monate"),
             ("گفتگوی روزمره، توصیف گذشته", "Everyday conversation, describing the past",
              "Alltagsgespräche, Vergangenes beschreiben")],
            [("B1", "B1", "B1"), ("۳۵۰ تا ۴۰۰", "350–400", "350–400"), ("۱۱ ماه", "11 months", "11 Monate"),
             ("۴ ماه", "4 months", "4 Monate"),
             ("بیان نظر، نامه‌ی نیمه‌رسمی", "Give opinions, semi-formal letters",
              "Meinung äußern, halbformelle Briefe")],
            [("B2", "B2", "B2"), ("۶۰۰ تا ۶۵۰", "600–650", "600–650"), ("۱۸ ماه", "18 months", "18 Monate"),
             ("۶ ماه", "6 months", "6 Monate"),
             ("بحث، متن تخصصی، ایمیل کاری", "Debate, specialist texts, work email",
              "Diskutieren, Fachtexte, Arbeits-E-Mails")],
            [("C1", "C1", "C1"), ("۸۵۰ تا ۱۰۰۰", "850–1000", "850–1000"),
             ("۲.۵ سال", "2.5 years", "2,5 Jahre"), ("۱۰ ماه", "10 months", "10 Monate"),
             ("متن آکادمیک، سخنرانی، ظرافت‌های زبانی", "Academic text, presenting, nuance",
              "Akademische Texte, Vorträge, Nuancen")],
        ],
    ),
    callout(
        ("این عددها میانگین‌اند، نه قانون", "These are averages, not rules",
         "Das sind Mittelwerte, keine Regeln"),
        ("کسی که انگلیسی خوبی دارد معمولاً ۲۰ تا ۳۰ درصد سریع‌تر پیش می‌رود، چون ساختار جمله و بخش "
         "بزرگی از واژگان مشترک است. از B1 به بعد این فاصله کم می‌شود.",
         "Solid English usually buys you twenty to thirty per cent, because sentence structure and "
         "a large share of the vocabulary are shared. From B1 onwards the gap narrows.",
         "Gutes Englisch bringt meist zwanzig bis dreißig Prozent, weil Satzbau und ein großer Teil "
         "des Wortschatzes geteilt werden. Ab B1 wird der Abstand kleiner."),
    ),

    h2("se-sotoon", "سه ستون یادگیری: ورودی، ساختار، خروجی",
       "Three pillars: input, structure, output",
       "Drei Säulen: Input, Struktur, Output"),
    p(
        "هر برنامه‌ی موفقی برای یادگیری زبان آلمانی روی سه ستون می‌ایستد و اگر یکی‌شان بلنگد، کل "
        "ساختمان کج می‌شود. بیشتر زبان‌آموزها ستون دوم را بیش از حد و ستون سوم را تقریباً هیچ تمرین "
        "می‌کنند.",
        "Every workable German plan stands on three pillars, and if one is short the whole thing "
        "leans. Most learners over-practise the second and barely touch the third.",
        "Jeder brauchbare Deutschplan steht auf drei Säulen, und fehlt einer die Höhe, neigt sich "
        "das Ganze. Die meisten üben die zweite zu viel und die dritte kaum.",
    ),
    h3("ستون اول — ورودی (Input)", "Pillar one — input", "Säule eins — Input"),
    p(
        "مغز از تکرار الگو زبان می‌سازد، نه از حفظ قاعده. ورودی یعنی حجم زیادی آلمانیِ کمی بالاتر از "
        "سطح فعلی‌ات. قانون ساده این است: باید حدود ۸۰ درصد را بفهمی. اگر کمتر بفهمی، مغز خاموش "
        "می‌شود؛ اگر بیشتر بفهمی، چیزی یاد نمی‌گیری.",
        "The brain builds language from repeated patterns, not memorised rules. Input means a lot "
        "of German slightly above your level. The rule of thumb: you should understand about eighty "
        "per cent. Less and the brain switches off; more and you learn nothing.",
        "Das Gehirn baut Sprache aus wiederholten Mustern, nicht aus auswendig gelernten Regeln. "
        "Input heißt viel Deutsch knapp über Ihrem Niveau. Faustregel: etwa achtzig Prozent sollten "
        "Sie verstehen. Weniger, und das Gehirn schaltet ab; mehr, und Sie lernen nichts.",
    ),
    h3("ستون دوم — ساختار (Grammatik)", "Pillar two — grammar", "Säule zwei — Grammatik"),
    p(
        "گرامر آلمانی ترسناک نیست، فقط بی‌رحم است: یک حرف اشتباه در آرتیکل، معنی جمله را عوض می‌کند. "
        "ولی گرامر ابزار است نه هدف. هفته‌ای دو یا سه ساعت گرامر کافی است، به شرطی که بلافاصله در "
        "نوشتن و گفتن استفاده شود.",
        "German grammar is not frightening, only unforgiving: one wrong letter in an article changes "
        "the sentence. But grammar is a tool, not the goal. Two or three hours a week is plenty, so "
        "long as it is used immediately in writing and speech.",
        "Deutsche Grammatik ist nicht furchteinflößend, nur unnachgiebig: Ein falscher Buchstabe im "
        "Artikel ändert den Satz. Doch Grammatik ist Werkzeug, nicht Ziel. Zwei bis drei Stunden "
        "pro Woche genügen — sofern sie sofort im Schreiben und Sprechen benutzt werden.",
    ),
    h3("ستون سوم — خروجی (Output)", "Pillar three — output", "Säule drei — Output"),
    p(
        "این همان ستونی است که ۹۰ درصد زبان‌آموزها نادیده می‌گیرند و بعد در آزمون شفاهی شوکه می‌شوند. "
        "خروجی یعنی تولید زبان زیر فشار زمان. خواندن ده کتاب گرامر تو را برای دو دقیقه صحبت پیوسته "
        "آماده نمی‌کند؛ فقط خودِ صحبت کردن این کار را می‌کند.",
        "This is the pillar nine learners in ten ignore, then get a shock in the oral exam. Output "
        "means producing language under time pressure. Ten grammar books will not prepare you for "
        "two minutes of continuous speech; only speaking does that.",
        "Das ist die Säule, die neun von zehn Lernenden auslassen — und dann in der mündlichen "
        "Prüfung erschrecken. Output heißt Sprachproduktion unter Zeitdruck. Zehn Grammatikbücher "
        "bereiten nicht auf zwei Minuten zusammenhängendes Sprechen vor; nur Sprechen tut das.",
    ),
    quote(
        "فهمیدن آلمانی و تولید آلمانی دو مهارت جدا هستند. کسی که فقط ورودی تمرین کرده، در آزمون "
        "Sprechen مثل کسی است که ده سال فوتبال تماشا کرده و حالا باید پنالتی بزند.",
        "Understanding German and producing it are two skills. Practising only input leaves you like "
        "someone who has watched football for ten years and is now asked to take the penalty.",
        "Deutsch verstehen und Deutsch produzieren sind zwei Fertigkeiten. Wer nur Input übt, steht "
        "da wie jemand, der zehn Jahre Fußball geschaut hat und nun den Elfmeter schießen soll.",
    ),
]

BODY += [
    h2("gerammar", "گرامر آلمانی را با چه ترتیبی بخوانیم",
       "The right order for German grammar", "Die richtige Reihenfolge der Grammatik"),
    p(
        "ترتیب اشتباه در گرامر، بزرگ‌ترین اتلاف وقت در یادگیری زبان آلمانی است. این ترتیبی است که در "
        "عمل بهترین نتیجه را می‌دهد:",
        "The wrong grammar order is the single biggest waste of time in learning German. This order "
        "works best in practice:",
        "Die falsche Grammatikreihenfolge ist die größte Zeitverschwendung beim Deutschlernen. Diese "
        "Reihenfolge funktioniert in der Praxis am besten:",
    ),
    steps(
        ("جنسیت اسم و آرتیکل معین/نامعین (der, die, das / ein, eine). از روز اول هر اسم را با "
         "آرتیکلش حفظ کن.",
         "Noun gender and articles (der, die, das / ein, eine). From day one, learn every noun with "
         "its article.",
         "Nomengenus und Artikel (der, die, das / ein, eine). Vom ersten Tag an jedes Nomen mit "
         "Artikel lernen."),
        ("زمان حال و فعل‌های بی‌قاعده‌ی پرکاربرد (sein, haben, werden, gehen, kommen).",
         "The present tense and the common irregular verbs (sein, haben, werden, gehen, kommen).",
         "Präsens und die häufigen unregelmäßigen Verben (sein, haben, werden, gehen, kommen)."),
        ("حالت Akkusativ و تفاوتش با Nominativ — اینجاست که آرتیکل‌ها تغییر می‌کنند.",
         "Accusative and how it differs from nominative — this is where the articles change.",
         "Akkusativ und sein Unterschied zum Nominativ — hier ändern sich die Artikel."),
        ("ترتیب کلمات در جمله‌ی ساده: فعل همیشه جای دوم است، حتی اگر جمله با قید شروع شود.",
         "Word order in a simple sentence: the verb is always second, even after an adverbial start.",
         "Wortstellung im Hauptsatz: Das Verb steht immer an zweiter Stelle, auch nach einer "
         "Angabe."),
        ("حالت Dativ و افعالی که همیشه Dativ می‌گیرند (helfen, danken, gefallen).",
         "Dative, and the verbs that always take it (helfen, danken, gefallen).",
         "Dativ und die Verben, die ihn immer fordern (helfen, danken, gefallen)."),
        ("افعال جدایی‌پذیر (aufstehen, ankommen) و جایگاه پیشوند در انتهای جمله.",
         "Separable verbs (aufstehen, ankommen) and where the prefix lands.",
         "Trennbare Verben (aufstehen, ankommen) und die Stellung des Präfixes."),
        ("زمان گذشته: اول Perfekt که در گفتار استفاده می‌شود، بعد Präteritum که بیشتر نوشتاری است.",
         "The past: Perfekt first because it is spoken, then Präteritum which is mostly written.",
         "Vergangenheit: zuerst Perfekt, weil gesprochen, dann Präteritum, überwiegend schriftlich."),
        ("جمله‌های پیرو با weil، dass، wenn — و قانون رفتن فعل به آخر جمله.",
         "Subordinate clauses with weil, dass, wenn — and the verb going to the end.",
         "Nebensätze mit weil, dass, wenn — und das Verb ans Ende."),
        ("صفت و صرف آن (Adjektivdeklination) — سخت‌ترین بخش A2/B1، حتماً با تمرین نوشتاری.",
         "Adjective declension — the hardest part of A2/B1, and only learned by writing.",
         "Adjektivdeklination — der schwerste Teil von A2/B1, nur durch Schreiben zu lernen."),
        ("حالت Genitiv، مجهول (Passiv) و Konjunktiv II — از B1 به بعد.",
         "Genitive, passive and Konjunktiv II — from B1 onwards.",
         "Genitiv, Passiv und Konjunktiv II — ab B1."),
    ),
    p(
        "یک نکته که کمتر گفته می‌شود: صرف صفت را زودتر از موعد نخوان. اگر قبل از تسلط بر سه حالت اول "
        "سراغش بروی، جدولش را حفظ می‌کنی و دو هفته بعد فراموش می‌کنی. صبر کن تا Nominativ، Akkusativ "
        "و Dativ در ذهنت خودکار شوند.",
        "One thing rarely said: do not take adjective declension early. Reach for it before the "
        "first three cases are automatic and you memorise a table you will forget in a fortnight. "
        "Wait until nominative, accusative and dative are reflexes.",
        "Etwas, das selten gesagt wird: Nehmen Sie die Adjektivdeklination nicht zu früh. Greifen "
        "Sie danach, bevor die ersten drei Kasus sitzen, lernen Sie eine Tabelle, die Sie in zwei "
        "Wochen vergessen. Warten Sie, bis Nominativ, Akkusativ und Dativ Reflexe sind.",
    ),

    h2("vajegan", "واژگان: چند کلمه در روز و با چه روشی",
       "Vocabulary: how many words a day, and how",
       "Wortschatz: wie viele Wörter pro Tag — und wie"),
    p(
        "عدد واقع‌بینانه روزی ۱۰ تا ۱۵ کلمه‌ی جدید است. برای رسیدن به B2 حدود ۴۰۰۰ تا ۵۰۰۰ واژه لازم "
        "است؛ با روزی ۱۲ کلمه، این یعنی حدود یک سال.",
        "Ten to fifteen new words a day is the realistic number. B2 needs roughly four to five "
        "thousand words, so at twelve a day that is about a year.",
        "Zehn bis fünfzehn neue Wörter am Tag ist die realistische Zahl. B2 verlangt etwa vier- bis "
        "fünftausend Wörter — bei zwölf am Tag also rund ein Jahr.",
    ),
    h3("قانون طلایی: اسم را هرگز تنها حفظ نکن",
       "The golden rule: never learn a noun alone",
       "Die goldene Regel: nie ein Nomen allein lernen"),
    p(
        "به‌جای «Tisch = میز» بنویس «der Tisch, die Tische». آرتیکل و جمع، بخشی از خود کلمه‌اند. اگر "
        "اسم را بدون آرتیکل حفظ کنی، در هر جمله‌ای که بسازی باید حدس بزنی — و حدس زدن یعنی خطا در "
        "آزمون.",
        "Instead of \"Tisch = table\", write \"der Tisch, die Tische\". The article and plural are "
        "part of the word. Learn a noun bare and you will guess in every sentence you build — and "
        "guessing means marks lost.",
        "Statt „Tisch = table“ schreiben Sie „der Tisch, die Tische“. Artikel und Plural gehören zum "
        "Wort. Lernen Sie ein Nomen nackt, raten Sie in jedem Satz — und Raten kostet Punkte.",
    ),
    h3("تکرار فاصله‌دار، نه مرور یک‌جا",
       "Spaced repetition, not one long review",
       "Verteiltes Wiederholen statt einer langen Sitzung"),
    p(
        "کلمه‌ای که امروز یاد گرفتی را فردا، سه روز بعد، یک هفته بعد و یک ماه بعد ببین. هر بار که "
        "درست به یاد آوردی، فاصله را بیشتر کن. این روش از مرور طولانی و یک‌باره چند برابر مؤثرتر است.",
        "See today's word again tomorrow, in three days, in a week, in a month. Each time you recall "
        "it, stretch the gap. This beats one long cram by a wide margin.",
        "Sehen Sie das heutige Wort morgen wieder, in drei Tagen, in einer Woche, in einem Monat. "
        "Jedes Mal, wenn Sie es erinnern, verlängern Sie den Abstand. Das schlägt eine lange "
        "Pauksitzung deutlich.",
    ),
    h3("کلمه را در جمله حفظ کن، نه در لیست",
       "Learn words in sentences, not in lists",
       "Wörter in Sätzen lernen, nicht in Listen"),
    p(
        "«sich bewerben» را به‌صورت «Ich bewerbe mich um eine Stelle» حفظ کن. اینطوری هم حرف "
        "اضافه‌اش (um) را یاد می‌گیری، هم ساختار انعکاسی‌اش را، هم یک جمله‌ی آماده برای آزمون شفاهی "
        "داری.",
        "Learn \"sich bewerben\" as \"Ich bewerbe mich um eine Stelle\". That gives you the "
        "preposition, the reflexive structure, and a sentence ready for the oral exam.",
        "Lernen Sie „sich bewerben“ als „Ich bewerbe mich um eine Stelle“. Damit haben Sie die "
        "Präposition, die reflexive Struktur und einen fertigen Satz für die mündliche Prüfung.",
    ),

    h2("shenidari", "تقویت شنیداری", "Building listening", "Hörverstehen aufbauen"),
    p(
        "آلمانی سرعت گفتار بالایی دارد و کلمه‌ها در گفتار روزمره به هم می‌چسبند. اگر متن را می‌فهمی "
        "ولی صوت را نه، مشکل واژگان نیست، مشکل عادت گوش است. راه‌حل، شنیدنِ زیاد با متن است:",
        "German is spoken fast and words run together. If you understand the text but not the audio, "
        "the problem is not vocabulary — it is ear training. The cure is a lot of listening with a "
        "transcript:",
        "Deutsch wird schnell gesprochen und Wörter verschmelzen. Verstehen Sie den Text, aber nicht "
        "das Audio, liegt es nicht am Wortschatz, sondern am Ohr. Das Mittel ist viel Hören mit "
        "Transkript:",
    ),
    steps(
        ("یک‌بار بدون متن گوش کن و ببین چقدر می‌فهمی.",
         "Listen once without the transcript and see how much you get.",
         "Einmal ohne Transkript hören und prüfen, wie viel Sie verstehen."),
        ("بار دوم با متن گوش کن و کلمه‌هایی را که نشنیده بودی علامت بزن.",
         "Listen again with the transcript and mark what you missed.",
         "Erneut mit Transkript hören und markieren, was Sie überhört haben."),
        ("بار سوم دوباره بدون متن — این بار همان کلمه‌ها را می‌شنوی.",
         "Listen a third time without it — now you hear those same words.",
         "Ein drittes Mal ohne Transkript — jetzt hören Sie genau diese Wörter."),
        ("بخشی از فایل را همزمان با گوینده بلند بخوان (Shadowing).",
         "Shadow a stretch of it, reading aloud along with the speaker.",
         "Einen Abschnitt mitlesen und laut mitsprechen (Shadowing)."),
    ),
    cta(
        ("با گوش دادن شروع کن", "Start by listening", "Mit Hören beginnen"),
        ("پادکست‌های سطح‌بندی‌شده با متن دوزبانه و سرعت قابل تنظیم.",
         "Levelled podcasts with a bilingual transcript and adjustable speed.",
         "Podcasts nach Niveau mit zweisprachigem Transkript und einstellbarem Tempo."),
        "/podcasts",
        ("دیدن پادکست‌ها", "Browse the podcasts", "Zu den Podcasts"),
    ),

    h2("neveshtan", "نوشتن: کم‌هزینه‌ترین راه برای تثبیت گرامر",
       "Writing: the cheapest way to fix grammar",
       "Schreiben: der günstigste Weg, Grammatik zu festigen"),
    p(
        "نوشتن تنها مهارتی است که در آن وقت داری فکر کنی، پس بهترین جا برای تبدیل قاعده‌ی گرامری به "
        "عادت است. روزی ۱۰ دقیقه نوشتن، بیشتر از دو ساعت خواندن کتاب گرامر اثر دارد.",
        "Writing is the one skill where you have time to think, which makes it the best place to "
        "turn a rule into a habit. Ten minutes of writing a day beats two hours of grammar reading.",
        "Schreiben ist die einzige Fertigkeit, bei der Sie Zeit zum Nachdenken haben — der beste "
        "Ort, aus einer Regel eine Gewohnheit zu machen. Zehn Minuten Schreiben am Tag schlagen zwei "
        "Stunden Grammatiklektüre.",
    ),
    bullets(
        ("A1/A2: روزی پنج جمله درباره‌ی کاری که کردی. فقط زمان حال و Perfekt.",
         "A1/A2: five sentences a day about what you did. Present and Perfekt only.",
         "A1/A2: fünf Sätze täglich über Ihren Tag. Nur Präsens und Perfekt."),
        ("B1: هفته‌ای یک ایمیل نیمه‌رسمی — درخواست مرخصی، اعتراض به فاکتور، دعوت از دوست.",
         "B1: one semi-formal email a week — leave request, disputed invoice, an invitation.",
         "B1: eine halbformelle E-Mail pro Woche — Urlaubsantrag, Rechnungsreklamation, Einladung."),
        ("B2: هفته‌ای یک متن ۱۸۰ کلمه‌ای که در آن نظر می‌دهی و دلیل می‌آوری.",
         "B2: a 180-word opinion piece a week, with reasons.",
         "B2: wöchentlich ein Meinungstext von 180 Wörtern, mit Begründung."),
        ("C1: خلاصه‌نویسی از یک مقاله‌ی خبری، با کلمات خودت.",
         "C1: summarise a news article in your own words.",
         "C1: einen Zeitungsartikel in eigenen Worten zusammenfassen."),
    ),
    p(
        "نکته‌ی مهم: متنی که کسی تصحیح نکند، فقط اشتباه‌ها را در ذهنت تثبیت می‌کند. اگر معلم نداری، "
        "حداقل متن را یک روز بعد خودت با چشم تازه بخوان.",
        "One caveat: an uncorrected text only cements your mistakes. With no teacher, at least read "
        "it again a day later with fresh eyes.",
        "Ein Vorbehalt: Ein unkorrigierter Text festigt nur Ihre Fehler. Ohne Lehrkraft lesen Sie "
        "ihn wenigstens einen Tag später mit frischem Blick.",
    ),

    h2("sohbat", "صحبت کردن: جایی که بیشترین نمره از دست می‌رود",
       "Speaking: where most marks are lost",
       "Sprechen: wo die meisten Punkte verloren gehen"),
    p(
        "در آزمون‌های گوته، Sprechen معمولاً پایین‌ترین نمره است. دلیلش ساده است: تنها مهارتی است که "
        "نمی‌شود تنهایی و بی‌صدا تمرینش کرد. ولی راه‌هایی هست که واقعاً جواب می‌دهند:",
        "In Goethe exams Sprechen is usually the lowest score, for a simple reason: it is the only "
        "skill you cannot practise alone and in silence. Some approaches genuinely work:",
        "In Goethe-Prüfungen ist Sprechen meist die schwächste Note, aus einem einfachen Grund: Es "
        "ist die einzige Fertigkeit, die man nicht allein und lautlos üben kann. Einiges hilft "
        "wirklich:",
    ),
    steps(
        ("بلند بخوان. روزی ۵ دقیقه بلند خواندن متن آلمانی، عضلات تلفظ را می‌سازد.",
         "Read aloud. Five minutes a day builds the muscles pronunciation needs.",
         "Laut lesen. Fünf Minuten täglich bauen die Muskeln für die Aussprache auf."),
        ("با خودت حرف بزن. کاری که می‌کنی را به آلمانی توصیف کن، حتی با جمله‌های غلط.",
         "Talk to yourself. Narrate what you are doing in German, wrong sentences included.",
         "Sprechen Sie mit sich selbst. Beschreiben Sie auf Deutsch, was Sie tun — auch falsch."),
        ("صدایت را ضبط کن و گوش بده. اولین بار آزاردهنده است، از بار سوم بی‌نهایت مفید.",
         "Record yourself and listen back. Excruciating the first time, invaluable by the third.",
         "Nehmen Sie sich auf und hören Sie zu. Beim ersten Mal unangenehm, ab dem dritten "
         "unbezahlbar."),
        ("جواب‌های آماده بساز. برای سؤال‌های همیشگی یک جواب ۴۰ ثانیه‌ای بنویس و حفظ کن.",
         "Build set answers. Write and memorise a forty-second reply to the perennial questions.",
         "Bauen Sie feste Antworten. Schreiben und lernen Sie eine 40-Sekunden-Antwort auf die "
         "immergleichen Fragen."),
        ("زیر فشار زمان تمرین کن. در آزمون واقعی، ۳۰ ثانیه برای فکر کردن داری، نه ۳ دقیقه.",
         "Practise against the clock. The real exam gives thirty seconds to think, not three "
         "minutes.",
         "Üben Sie gegen die Uhr. Die echte Prüfung gibt dreißig Sekunden zum Nachdenken, nicht "
         "drei Minuten."),
    ),
    cta(
        ("آلمانی در محیط", "German in Context", "Deutsch im Kontext"),
        ("به‌جای تمرین جمله‌های بی‌ربط، وارد یک موقعیت واقعی شو و جواب بده. صدایت ضبط می‌شود و "
         "بازخورد تفکیکی می‌گیری.",
         "Instead of disconnected drills, step into a real situation and answer. Your voice is "
         "recorded and the feedback is broken down by criterion.",
         "Statt zusammenhangloser Übungen treten Sie in eine echte Situation und antworten. Ihre "
         "Stimme wird aufgenommen, die Rückmeldung nach Kriterien aufgeschlüsselt."),
        "/courses/einreise-nach-deutschland",
        ("شروع «آلمانی در محیط»", "Start German in Context", "Deutsch im Kontext starten"),
    ),
]

BODY += [
    h2("barnameh", "یک برنامه‌ی هفتگی که واقعاً اجرا می‌شود",
       "A weekly plan you will actually follow",
       "Ein Wochenplan, den Sie wirklich durchhalten"),
    p(
        "برنامه‌ی خوب برنامه‌ای است که در هفته‌ی چهارم هم اجرا شود. این نمونه برای کسی است که روزی "
        "یک ساعت و نیم وقت دارد و هدفش B1 تا B2 است:",
        "A good plan is one still running in week four. This one assumes ninety minutes a day and a "
        "B1–B2 target:",
        "Ein guter Plan läuft auch in Woche vier noch. Dieser rechnet mit neunzig Minuten täglich "
        "und einem Ziel von B1 bis B2:",
    ),
    table(
        ("برنامه‌ی نمونه، حدود ۹۰ دقیقه در روز", "A sample day of about 90 minutes",
         "Ein Beispieltag von etwa 90 Minuten"),
        [("روز", "Day", "Tag"), ("۳۰ دقیقه‌ی اول", "First 30 min", "Erste 30 Min."),
         ("۳۰ دقیقه‌ی دوم", "Second 30 min", "Zweite 30 Min."),
         ("۳۰ دقیقه‌ی سوم", "Third 30 min", "Dritte 30 Min.")],
        [
            [("شنبه", "Monday", "Montag"), ("گرامر جدید", "New grammar", "Neue Grammatik"),
             ("تمرین کتبی همان گرامر", "Written drill on it", "Schriftliche Übung dazu"),
             ("مرور فلش‌کارت", "Flashcard review", "Karteikarten")],
            [("یکشنبه", "Tuesday", "Dienstag"),
             ("پادکست با متن", "Podcast with transcript", "Podcast mit Transkript"),
             ("۱۵ واژه‌ی جدید", "15 new words", "15 neue Wörter"),
             ("بلندخوانی", "Reading aloud", "Lautes Lesen")],
            [("دوشنبه", "Wednesday", "Mittwoch"),
             ("درک مطلب", "Reading comprehension", "Leseverstehen"),
             ("نوشتن ۱۰۰ کلمه", "Write 100 words", "100 Wörter schreiben"),
             ("مرور فلش‌کارت", "Flashcard review", "Karteikarten")],
            [("سه‌شنبه", "Thursday", "Donnerstag"),
             ("پادکست بدون متن", "Podcast without transcript", "Podcast ohne Transkript"),
             ("تمرین گرامر هفته", "This week's grammar drill", "Grammatikübung der Woche"),
             ("مکالمه / ضبط صدا", "Speaking / recording", "Sprechen / Aufnahme")],
            [("چهارشنبه", "Friday", "Freitag"), ("گرامر جدید", "New grammar", "Neue Grammatik"),
             ("۱۵ واژه‌ی جدید", "15 new words", "15 neue Wörter"),
             ("مرور فلش‌کارت", "Flashcard review", "Karteikarten")],
            [("پنجشنبه", "Saturday", "Samstag"),
             ("یک بخش از سیمیلیتور آزمون", "One simulator module", "Ein Simulator-Modul"),
             ("بررسی اشتباه‌ها", "Review the mistakes", "Fehler durchgehen"),
             ("مکالمه / ضبط صدا", "Speaking / recording", "Sprechen / Aufnahme")],
            [("جمعه", "Sunday", "Sonntag"),
             ("استراحت یا فیلم آلمانی", "Rest, or a German film", "Pause oder ein deutscher Film"),
             ("—", "—", "—"), ("—", "—", "—")],
        ],
    ),
    callout(
        ("یک روز را خالی بگذار", "Leave one day empty", "Lassen Sie einen Tag frei"),
        ("برنامه‌ای که هفت روز پر باشد، در هفته‌ی سوم شکسته می‌شود. یک روز خالی، برنامه را ماه‌ها "
         "زنده نگه می‌دارد.",
         "A plan filling all seven days breaks in week three. One empty day keeps it alive for "
         "months.",
         "Ein Plan, der alle sieben Tage füllt, bricht in Woche drei. Ein freier Tag hält ihn "
         "monatelang am Leben."),
    ),

    h2("manabe", "از چه منابعی استفاده کنیم", "Which resources to use", "Welche Materialien"),
    p(
        "منبع خوب منبعی است که سطحش با تو جور باشد و تمرین کافی داشته باشد. تعداد منبع را کم نگه "
        "دار: دو منبع که تا آخر بروی، بی‌نهایت بهتر از ده منبعی است که هرکدام را تا درس سوم بخوانی.",
        "A good resource matches your level and has enough exercises. Keep the count low: two you "
        "finish beat ten you abandon at lesson three.",
        "Gutes Material passt zu Ihrem Niveau und hat genug Übungen. Halten Sie die Zahl klein: Zwei, "
        "die Sie beenden, schlagen zehn, die Sie bei Lektion drei liegen lassen.",
    ),
    bullets(
        ("یک کتاب اصلی سطح‌بندی‌شده که ساختار درس‌ها را بدهد و تا آخر با آن پیش بروی.",
         "One levelled core book to give the course its structure, worked to the end.",
         "Ein Hauptlehrwerk nach Niveau, das die Struktur vorgibt — bis zum Ende durchgearbeitet."),
        ("یک مرجع گرامری برای وقتی که سؤالی پیش می‌آید — نه برای خواندن از اول تا آخر.",
         "One grammar reference for when a question arises — not to be read cover to cover.",
         "Eine Grammatik zum Nachschlagen — nicht von vorn bis hinten zu lesen."),
        ("یک اپلیکیشن فلش‌کارت با تکرار فاصله‌دار، فقط برای واژه‌هایی که خودت از متن‌ها بیرون کشیده‌ای.",
         "One spaced-repetition app, only for words you pulled out of real texts yourself.",
         "Eine App mit verteiltem Wiederholen, nur für Wörter, die Sie selbst aus Texten gezogen "
         "haben."),
        ("یک منبع صوتی سطح‌بندی‌شده با متن همزمان، برای ساختن عادت گوش.",
         "One levelled audio source with a synchronised transcript, to train the ear.",
         "Eine Audioquelle nach Niveau mit synchronem Transkript, um das Ohr zu schulen."),
        ("یک سیمیلیتور آزمون، برای سنجش ماهانه در شرایط واقعی.",
         "One exam simulator, for a monthly check under real conditions.",
         "Ein Prüfungssimulator für die monatliche Kontrolle unter echten Bedingungen."),
    ),
    p(
        "فیلم و سریال آلمانی از سطح B1 به بعد مفید می‌شوند. اگر خیلی مشتاقی، با زیرنویس آلمانی ببین "
        "نه زبان مادری — زیرنویس زبان مادری مغز را از پردازش آلمانی معاف می‌کند.",
        "German film and television start paying off from B1. If you cannot wait, watch with German "
        "subtitles, not your own language — native-language subtitles excuse the brain from "
        "processing German at all.",
        "Deutsche Filme und Serien lohnen sich ab B1. Wenn Sie nicht warten wollen, schauen Sie mit "
        "deutschen Untertiteln, nicht in Ihrer Sprache — muttersprachliche Untertitel entbinden das "
        "Gehirn davon, überhaupt Deutsch zu verarbeiten.",
    ),

    h2("eshtebahat", "شش اشتباه رایج", "Six common mistakes", "Sechs häufige Fehler"),
    steps(
        ("حفظ اسم بدون آرتیکل. بعداً اصلاحش چند برابر سخت‌تر از یاد گرفتن درستش است.",
         "Learning nouns without articles. Fixing it later costs many times what learning it right "
         "would have.",
         "Nomen ohne Artikel lernen. Die spätere Korrektur kostet ein Vielfaches."),
        ("ترجمه‌ی جمله‌به‌جمله از زبان مادری. باید الگوی آلمانی را مستقیم یاد بگیری.",
         "Translating sentence by sentence from your own language. Learn the German pattern "
         "directly.",
         "Satz für Satz aus der eigenen Sprache übersetzen. Lernen Sie das deutsche Muster direkt."),
        ("تمرکز بیش از حد روی گرامر و فرار از مکالمه. گرامر امن است چون کسی قضاوتت نمی‌کند — و "
         "دقیقاً به همین دلیل دام است.",
         "Over-studying grammar to avoid speaking. Grammar is safe because nobody judges you — which "
         "is exactly why it is a trap.",
         "Zu viel Grammatik, um dem Sprechen auszuweichen. Grammatik ist sicher, weil niemand "
         "urteilt — genau deshalb ist sie eine Falle."),
        ("خواندن متن‌های خیلی سخت. متنی که نصفش را نمی‌فهمی، انگیزه را می‌کشد.",
         "Reading texts far above your level. A text you half understand kills motivation.",
         "Zu schwere Texte lesen. Ein Text, den Sie halb verstehen, tötet die Motivation."),
        ("نادیده گرفتن تلفظ در ماه‌های اول. تلفظ غلطِ جاافتاده در سطح B2 دیگر به‌سختی اصلاح می‌شود؛ "
         "مخصوصاً ü، ö و r.",
         "Ignoring pronunciation early. A settled wrong sound is very hard to fix at B2 — especially "
         "ü, ö and r.",
         "Aussprache am Anfang ignorieren. Ein gefestigter falscher Laut ist auf B2 kaum noch zu "
         "korrigieren — besonders ü, ö und r."),
        ("ندادن آزمون آزمایشی. تا وقتی در شرایط واقعی امتحان ندهی، نمی‌دانی مدیریت زمانت چقدر ضعیف "
         "است.",
         "Never sitting a mock exam. Until you test under real conditions you have no idea how weak "
         "your time management is.",
         "Nie einen Modelltest ablegen. Ohne echte Bedingungen wissen Sie nicht, wie schwach Ihr "
         "Zeitmanagement ist."),
    ),

    h2("sanjesh", "از کجا بفهمی واقعاً پیشرفت کرده‌ای",
       "How to tell you are really improving",
       "Woran Sie echten Fortschritt erkennen"),
    p(
        "حس پیشرفت، سنجه‌ی بدی است. آدم بعد از یک هفته‌ی پرکار احساس می‌کند خیلی جلو رفته و بعد از یک "
        "هفته‌ی خسته احساس می‌کند همه‌چیز را فراموش کرده — در حالی که هیچ‌کدام درست نیست. سه سنجه‌ی "
        "واقعی وجود دارد:",
        "The feeling of progress is a poor gauge. After a busy week you feel far ahead; after a "
        "tired one you feel you have forgotten everything. Neither is true. Three real measures "
        "exist:",
        "Das Gefühl von Fortschritt ist ein schlechter Maßstab. Nach einer fleißigen Woche fühlen "
        "Sie sich weit voraus, nach einer müden, Sie hätten alles vergessen. Beides stimmt nicht. "
        "Es gibt drei echte Maße:",
    ),
    bullets(
        ("درصد فهم یک فایل صوتی که قبلاً گوش نکرده‌ای، در همان سطح.",
         "How much of an unheard audio file at your level you understand.",
         "Wie viel Sie von einer ungehörten Audiodatei auf Ihrem Niveau verstehen."),
        ("تعداد کلمه‌ای که در ۱۰ دقیقه می‌توانی بدون توقف بنویسی.",
         "How many words you can write in ten minutes without stopping.",
         "Wie viele Wörter Sie in zehn Minuten ohne Pause schreiben."),
        ("نمره‌ی یک نشست کامل سیمیلیتور، با تایمر و بدون توقف.",
         "Your score in a full simulator sitting, timed and uninterrupted.",
         "Ihre Punktzahl in einer vollständigen Simulator-Sitzung, mit Timer und ohne "
         "Unterbrechung."),
    ),
    p(
        "سومی از همه گویاتر است. آزمون واقعی فقط دانش زبانی را نمی‌سنجد؛ مدیریت زمان، تمرکز در "
        "دقیقه‌ی چهلم و توانایی رد شدن از سؤال سخت را هم می‌سنجد. اینها فقط در شرایط واقعی خودشان را "
        "نشان می‌دهند، و دقیقاً به همین دلیل سیمیلیتور بخش جدانشدنی برنامه است، نه یک تمرین اضافه.",
        "The third says the most. A real exam measures more than language: time management, focus at "
        "minute forty, and the willingness to skip a hard question. Those only show under real "
        "conditions, which is why a simulator is part of the plan rather than an extra.",
        "Das dritte sagt am meisten. Eine echte Prüfung misst mehr als Sprache: Zeitmanagement, "
        "Konzentration in Minute vierzig und die Bereitschaft, eine schwere Frage zu überspringen. "
        "Das zeigt sich nur unter echten Bedingungen — deshalb gehört ein Simulator zum Plan und ist "
        "keine Zugabe.",
    ),
    cta(
        ("خودت را در شرایط واقعی بسنج", "Measure yourself under real conditions",
         "Messen Sie sich unter echten Bedingungen"),
        ("سیمیلیتور کامل A1 تا C1 با همان رابط، همان تایمر و همان قوانین آزمون گوته.",
         "Full A1–C1 simulators with the Goethe exam's own interface, timer and rules.",
         "Vollständige Simulatoren von A1 bis C1 mit Oberfläche, Timer und Regeln der "
         "Goethe-Prüfung."),
        "/exams",
        ("دیدن سیمیلیتورها", "Open the simulators", "Zu den Simulatoren"),
    ),

    h2("nazm", "نظم مهم‌تر از استعداد است",
       "Consistency beats talent", "Beständigkeit schlägt Talent"),
    p(
        "بین دو نفر که یکی روزی سه ساعت اما هفته‌ای دو روز می‌خواند و دیگری روزی چهل دقیقه اما هر "
        "روز، نفر دوم همیشه جلوتر می‌افتد. مغز برای تثبیت زبان به تکرار در فواصل کوتاه نیاز دارد، نه "
        "به حجم زیاد در یک نشست.",
        "Between someone studying three hours twice a week and someone doing forty minutes daily, "
        "the second always pulls ahead. Language settles through short, frequent repetition, not "
        "volume in one sitting.",
        "Zwischen jemandem, der zweimal die Woche drei Stunden lernt, und jemandem mit täglich "
        "vierzig Minuten zieht immer der Zweite davon. Sprache setzt sich durch kurze, häufige "
        "Wiederholung, nicht durch Masse in einer Sitzung.",
    ),
    p(
        "یک ترفند ساده که خیلی جواب می‌دهد: مطالعه را به یک عادت موجود بچسبان. بعد از صبحانه، یا "
        "بلافاصله بعد از رسیدن به خانه. تصمیم‌گیری روزانه درباره‌ی «کی بخوانم» انرژی می‌برد.",
        "One trick that works: attach studying to an existing habit — after breakfast, or the moment "
        "you get home. Deciding daily when to study costs energy you could spend studying.",
        "Ein Trick, der wirkt: Hängen Sie das Lernen an eine bestehende Gewohnheit — nach dem "
        "Frühstück oder direkt nach dem Heimkommen. Täglich zu entscheiden, wann Sie lernen, kostet "
        "Energie.",
    ),
    p(
        "و آخرین نکته: افت‌های موقت طبیعی‌اند. تقریباً همه در جایی بین A2 و B1 به دیواری می‌خورند که "
        "حس می‌کنند دیگر پیشرفت نمی‌کنند. دلیلش این است که در این سطح، پیشرفت از «یاد گرفتن چیزهای "
        "جدید» به «روان‌تر شدن در چیزهای بلد» تغییر می‌کند — که کندتر حس می‌شود ولی همان‌قدر واقعی "
        "است. راهش ادامه دادن است، نه عوض کردن روش.",
        "A last note: plateaus are normal. Almost everyone hits a wall somewhere between A2 and B1 "
        "and feels stuck. It happens because progress shifts from learning new things to becoming "
        "fluent in known ones — slower to feel, just as real. The answer is to continue, not to "
        "change method.",
        "Zuletzt: Plateaus sind normal. Fast alle stoßen irgendwo zwischen A2 und B1 an eine Wand "
        "und fühlen sich festgefahren. Das liegt daran, dass Fortschritt vom Neulernen zum "
        "Flüssigerwerden im Bekannten wechselt — langsamer spürbar, genauso echt. Die Antwort ist "
        "weitermachen, nicht die Methode wechseln.",
    ),

    h2("jamebandi", "جمع‌بندی", "In short", "Kurz gefasst"),
    p(
        "نحوه خواندن زبان آلمانی پیچیده نیست، ولی بی‌رحم است نسبت به بی‌نظمی. اگر هدفت را مشخص کنی، "
        "سه ستون ورودی و ساختار و خروجی را متوازن نگه داری، اسم‌ها را با آرتیکل حفظ کنی و ماهی "
        "یک‌بار خودت را در شرایط واقعی آزمون بسنجی، مسیر A1 تا B2 در حدود یک سال و نیم با روزی یک "
        "ساعت و نیم کاملاً شدنی است.",
        "Studying German is not complicated, but it is unforgiving of disorder. Name the goal, keep "
        "input, structure and output balanced, learn nouns with their articles, and test yourself "
        "monthly under exam conditions: A1 to B2 in about eighteen months at ninety minutes a day is "
        "entirely doable.",
        "Deutsch zu lernen ist nicht kompliziert, verzeiht aber keine Unordnung. Benennen Sie das "
        "Ziel, halten Sie Input, Struktur und Output im Gleichgewicht, lernen Sie Nomen mit Artikel "
        "und prüfen Sie sich monatlich unter Prüfungsbedingungen: A1 bis B2 in etwa achtzehn Monaten "
        "bei neunzig Minuten täglich ist gut machbar.",
    ),
    p(
        "مهم‌ترین جمله‌ی این راهنما همین است: زبان را با تولید یاد می‌گیری، نه با مصرف. هر روز چیزی "
        "بنویس و چیزی بگو، حتی اگر غلط باشد. غلطِ گفته‌شده قابل اصلاح است؛ جمله‌ای که هرگز گفته نشد، "
        "هیچ‌وقت درست نمی‌شود.",
        "The most important line here: you learn a language by producing it, not by consuming it. "
        "Write something and say something every day, wrong or not. A spoken mistake can be "
        "corrected; a sentence never said never gets right.",
        "Der wichtigste Satz hier: Man lernt eine Sprache durch Produzieren, nicht durch "
        "Konsumieren. Schreiben und sagen Sie täglich etwas, ob richtig oder falsch. Ein "
        "ausgesprochener Fehler lässt sich korrigieren; ein nie gesagter Satz wird nie richtig.",
    ),
]

BODY += [
    h2("bavarha", "پنج باور غلط که وقتت را می‌گیرند",
       "Five myths that cost you time", "Fünf Mythen, die Zeit kosten"),
    p(
        "بخش بزرگی از کندی در یادگیری زبان آلمانی از تلاش کم نمی‌آید، از باورهای غلط می‌آید. اینها "
        "پنج موردی هستند که بیشترین ساعت را از زبان‌آموزها می‌گیرند:",
        "A large share of slow progress in German comes not from lack of effort but from wrong "
        "beliefs. These five cost learners the most hours:",
        "Ein großer Teil des langsamen Fortschritts im Deutschen kommt nicht von zu wenig Fleiß, "
        "sondern von falschen Annahmen. Diese fünf kosten Lernende die meisten Stunden:",
    ),
    steps(
        ("«اول باید گرامر را کامل کنم، بعد حرف بزنم.» هیچ‌وقت کامل نمی‌شود. از هفته‌ی دوم شروع کن به "
         "حرف زدن، حتی با ده کلمه.",
         "\u201cI will finish the grammar first, then speak.\u201d It never finishes. Start speaking in "
         "week two, even with ten words.",
         "\u201eErst die Grammatik fertig, dann sprechen.\u201c Sie wird nie fertig. Beginnen Sie in Woche "
         "zwei zu sprechen, notfalls mit zehn Wörtern."),
        ("«آلمانی سخت‌ترین زبان دنیاست.» آلمانی قاعده‌مند است و استثناهایش کمتر از انگلیسی است؛ فقط "
         "قاعده‌هایش را باید از اول درست یاد بگیری.",
         "\u201cGerman is the hardest language.\u201d German is regular and has fewer exceptions than "
         "English; the rules simply have to be learned properly from the start.",
         "\u201eDeutsch ist die schwerste Sprache.\u201c Deutsch ist regelmäßig und hat weniger Ausnahmen "
         "als Englisch; die Regeln müssen nur von Anfang an richtig gelernt werden."),
        ("«با اپلیکیشن به B2 می‌رسم.» اپلیکیشن‌ها برای واژگان عالی‌اند و برای تولید زبان تقریباً "
         "بی‌فایده. تا A2 کمک می‌کنند، بعد از آن باید بنویسی و بگویی.",
         "\u201cAn app will get me to B2.\u201d Apps are excellent for vocabulary and nearly useless for "
         "production. They help to A2; after that you must write and speak.",
         "\u201eEine App bringt mich auf B2.\u201c Apps sind hervorragend für Wortschatz und fast nutzlos "
         "für Produktion. Bis A2 helfen sie; danach müssen Sie schreiben und sprechen."),
        ("«باید در آلمان زندگی کنم تا یاد بگیرم.» زندگی در آلمان ورودی می‌دهد، نه ساختار. کسانی که "
         "بدون برنامه به آلمان می‌روند، معمولاً در سطح A2 گیر می‌کنند.",
         "\u201cI have to live in Germany to learn.\u201d Living there supplies input, not structure. "
         "People who move without a plan usually stall at A2.",
         "\u201eIch muss in Deutschland leben, um zu lernen.\u201c Dort zu leben liefert Input, keine "
         "Struktur. Wer ohne Plan umzieht, bleibt meist auf A2 stecken."),
        ("«اشتباه کردن بد است.» اشتباهی که گفته و اصلاح شود، بهترین معلم است. سکوت هیچ چیزی یاد "
         "نمی‌دهد.",
         "\u201cMistakes are bad.\u201d A mistake made aloud and corrected is the best teacher. Silence "
         "teaches nothing.",
         "\u201eFehler sind schlecht.\u201c Ein laut gemachter und korrigierter Fehler ist die beste "
         "Lehrerin. Schweigen lehrt nichts."),
    ),
    p(
        "پشت هر پنج باور یک چیز مشترک هست: همه‌شان بهانه‌ای می‌سازند برای به تعویق انداختن تولید زبان. "
        "خواندن، تماشا کردن و حفظ کردن راحت‌اند چون در آن‌ها شکست دیده نمی‌شود. نوشتن و گفتن سخت‌اند "
        "چون خطا بلافاصله معلوم می‌شود — و دقیقاً به همین دلیل مؤثرند.",
        "All five share one thing: each supplies an excuse to postpone producing language. Reading, "
        "watching and memorising are comfortable because failure stays invisible. Writing and "
        "speaking are hard because the error shows at once — which is exactly why they work.",
        "Alle fünf teilen eines: Jede liefert einen Vorwand, die Sprachproduktion aufzuschieben. "
        "Lesen, Schauen und Auswendiglernen sind bequem, weil Scheitern unsichtbar bleibt. Schreiben "
        "und Sprechen sind hart, weil der Fehler sofort sichtbar wird — und genau deshalb wirken "
        "sie.",
    ),
]

BODY += [
    h2("chahar-maharat", "توازن چهار مهارت: چرا یکی‌شان همیشه عقب می‌ماند",
       "Balancing the four skills: why one always lags",
       "Vier Fertigkeiten im Gleichgewicht: warum eine immer zurückbleibt"),
    p(
        "خواندن، شنیدن، نوشتن و گفتن با هم رشد نمی‌کنند و این طبیعی است. تقریباً همیشه خواندن جلوتر "
        "از همه و گفتن عقب‌تر از همه است، چون خواندن را می‌شود تنها و بی‌صدا و بدون قضاوت انجام داد و "
        "گفتن را نه. مشکل وقتی شروع می‌شود که این فاصله آنقدر زیاد شود که مهارت عقب‌مانده جلوی بقیه "
        "را بگیرد.",
        "Reading, listening, writing and speaking do not grow together, and that is normal. Reading "
        "is almost always ahead and speaking almost always behind, because reading can be done alone, "
        "silently and unjudged, and speaking cannot. The trouble starts when the gap grows wide "
        "enough that the lagging skill holds the others back.",
        "Lesen, Hören, Schreiben und Sprechen wachsen nicht gleichmäßig, und das ist normal. Lesen "
        "liegt fast immer vorn, Sprechen fast immer hinten, weil Lesen allein, still und ohne "
        "Bewertung möglich ist und Sprechen nicht. Problematisch wird es, wenn der Abstand so groß "
        "wird, dass die zurückgebliebene Fertigkeit die anderen bremst.",
    ),
    p(
        "یک آزمون ساده برای فهمیدن اینکه توازنت به هم خورده: یک متن در سطح خودت بخوان و بعد بدون "
        "نگاه کردن، خلاصه‌اش را بلند بگو. اگر می‌توانی متن را کامل بفهمی ولی نمی‌توانی سه جمله درباره‌اش "
        "بسازی، فاصله‌ی ورودی و خروجی‌ات خیلی زیاد شده و باید چند هفته تمرکز را کامل روی تولید بگذاری.",
        "A quick test for imbalance: read a text at your level, then summarise it aloud without "
        "looking. If you understand it fully but cannot build three sentences about it, the gap "
        "between input and output has grown too wide and a few weeks focused entirely on production "
        "are due.",
        "Ein schneller Test auf Ungleichgewicht: Lesen Sie einen Text auf Ihrem Niveau und fassen Sie "
        "ihn dann ohne Hinsehen laut zusammen. Verstehen Sie ihn vollständig, bringen aber keine drei "
        "Sätze darüber zustande, ist der Abstand zwischen Input und Output zu groß — dann sind einige "
        "Wochen ganz auf Produktion fällig.",
    ),
    p(
        "قاعده‌ی عملی این است: هر هفته حداقل یک بار هر چهار مهارت را لمس کن، حتی اگر برای بعضی‌شان "
        "فقط ده دقیقه وقت داشته باشی. مهارتی که یک ماه دست نخورد، نه فقط پیشرفت نمی‌کند، بلکه عقب "
        "می‌رود — و برگرداندنش سه برابر زمانی می‌برد که نگه داشتنش می‌برد.",
        "The practical rule: touch all four skills at least once a week, even if some get only ten "
        "minutes. A skill left alone for a month does not merely stall, it slides back — and "
        "recovering it takes three times the effort of maintaining it.",
        "Die praktische Regel: Berühren Sie alle vier Fertigkeiten mindestens einmal pro Woche, auch "
        "wenn manche nur zehn Minuten bekommen. Eine Fertigkeit, die einen Monat ruht, stagniert "
        "nicht nur, sie fällt zurück — und sie zurückzuholen kostet dreimal so viel wie sie zu "
        "halten.",
    ),
]

FAQ = faq(
    (("یادگیری زبان آلمانی از صفر چقدر طول می‌کشد؟",
      "How long does it take to learn German from scratch?",
      "Wie lange dauert Deutschlernen von null?"),
     ("با روزی یک ساعت مطالعه‌ی منظم، رسیدن به A1 حدود سه ماه، به B1 حدود یازده ماه و به B2 حدود یک "
      "سال و نیم طول می‌کشد. با روزی سه ساعت این زمان‌ها تقریباً به یک‌سوم کاهش پیدا می‌کند.",
      "With an hour a day, A1 takes about three months, B1 about eleven, and B2 about eighteen. At "
      "three hours a day those figures drop to roughly a third.",
      "Bei einer Stunde täglich dauert A1 etwa drei Monate, B1 etwa elf und B2 etwa achtzehn. Bei "
      "drei Stunden täglich sinken diese Werte auf rund ein Drittel.")),
    (("از کدام مهارت شروع کنم؟", "Which skill should I start with?",
      "Mit welcher Fertigkeit beginne ich?"),
     ("از تلفظ و آرتیکل اسم‌ها. تلفظ در ماه‌های اول به‌راحتی اصلاح می‌شود ولی بعداً تقریباً ثابت "
      "می‌ماند، و آرتیکل اگر از روز اول همراه اسم حفظ نشود، بعداً اصلاحش چند برابر سخت‌تر است.",
      "Pronunciation and noun articles. Pronunciation is easy to correct in the first months and "
      "nearly fixed afterwards, and an article not learned with its noun costs many times more to "
      "fix later.",
      "Aussprache und Nomenartikel. Aussprache lässt sich in den ersten Monaten leicht korrigieren "
      "und ist danach fast festgelegt; ein nicht mit dem Nomen gelernter Artikel kostet später ein "
      "Vielfaches.")),
    (("روزی چند کلمه حفظ کنم؟", "How many words a day should I learn?",
      "Wie viele Wörter täglich?"),
     ("ده تا پانزده کلمه در روز عدد واقع‌بینانه‌ای است. مهم‌تر از تعداد، روش است: هر اسم را با "
      "آرتیکل و جمعش، و ترجیحاً داخل یک جمله‌ی کامل حفظ کن.",
      "Ten to fifteen is realistic. Method matters more than count: every noun with its article and "
      "plural, and preferably inside a full sentence.",
      "Zehn bis fünfzehn ist realistisch. Die Methode zählt mehr als die Zahl: jedes Nomen mit "
      "Artikel und Plural, am besten in einem vollständigen Satz.")),
    (("بدون کلاس رفتن می‌شود آلمانی یاد گرفت؟", "Can I learn German without classes?",
      "Kann ich Deutsch ohne Kurs lernen?"),
     ("بله، تا سطح B1 کاملاً شدنی است، به شرطی که نوشتن‌هایت تصحیح شود و مکالمه را جدی بگیری. از B2 "
      "به بعد نبودِ بازخورد روی مکالمه و نوشتار، پیشرفت را به‌شدت کند می‌کند.",
      "Yes, comfortably to B1, provided your writing gets corrected and you take speaking seriously. "
      "From B2 onwards, no feedback on speech and writing slows progress badly.",
      "Ja, bis B1 gut, sofern Ihr Schreiben korrigiert wird und Sie das Sprechen ernst nehmen. Ab B2 "
      "bremst fehlende Rückmeldung zu Sprechen und Schreiben den Fortschritt stark.")),
    (("چطور بفهمم برای آزمون گوته آماده‌ام؟", "How do I know I am ready for the Goethe exam?",
      "Woher weiß ich, dass ich prüfungsbereit bin?"),
     ("یک نشست کامل سیمیلیتور را با تایمر و بدون توقف بده. اگر در دو نشست متوالی بالای ۷۰ درصد "
      "بگیری و در Schreiben متن را در زمان مقرر تمام کنی، آماده‌ای.",
      "Sit a full simulator, timed and uninterrupted. If you clear seventy per cent in two "
      "consecutive sittings and finish Schreiben inside the time, you are ready.",
      "Legen Sie eine vollständige Simulator-Sitzung ab, mit Timer und ohne Unterbrechung. Schaffen "
      "Sie in zwei aufeinanderfolgenden Sitzungen über siebzig Prozent und beenden Schreiben "
      "fristgerecht, sind Sie bereit.")),
)
