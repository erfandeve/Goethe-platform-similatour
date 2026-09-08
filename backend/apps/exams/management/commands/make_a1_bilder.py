"""Draw the picture options for A1 Hören Teil 1:

    python manage.py make_a1_bilder [--force]

Start Deutsch 1 answers Teil 1 with three pictures per question. These are
drawn here as plain SVG rather than shipped as assets: they are ours, they
scale to any screen, and a fresh checkout gets them without a download.
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

W, H = 240, 220
INK = "#3d4142"       # the exam's own dark grey
SOFT = "#9a9a96"
ACCENT = "#a4c63f"    # the Goethe-style green the player already uses


def svg(body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img">'
        f'<rect width="{W}" height="{H}" fill="#fff"/>'
        f'<g fill="none" stroke="{INK}" stroke-width="3.2" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>'
    )


def clock(hour, minute):
    """An analogue face; the hands are what the learner actually compares."""
    import math

    cx, cy, r = 120, 105, 62
    ticks = ""
    for i in range(12):
        a = math.radians(i * 30 - 90)
        x1, y1 = cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a)
        x2, y2 = cx + (r - 5) * math.cos(a), cy + (r - 5) * math.sin(a)
        ticks += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="2"/>'

    ha = math.radians((hour % 12) * 30 + minute * 0.5 - 90)
    ma = math.radians(minute * 6 - 90)
    hx, hy = cx + 32 * math.cos(ha), cy + 32 * math.sin(ha)
    mx, my = cx + 48 * math.cos(ma), cy + 48 * math.sin(ma)
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}"/>{ticks}'
        f'<line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" stroke-width="4.5"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INK}"/>'
    )


def price(amount):
    """A tag with the figure on it."""
    return (
        '<path d="M52 66h108a14 14 0 0 1 14 14v60a14 14 0 0 1-14 14H52l-26-44z"/>'
        '<circle cx="60" cy="110" r="7"/>'
        f'<text x="118" y="122" font-family="Helvetica,Arial" font-size="34" '
        f'font-weight="700" fill="{INK}" stroke="none" text-anchor="middle">{amount}</text>'
    )


def drink(kind):
    if kind == "tea":
        return (
            '<path d="M62 88h86v44a30 30 0 0 1-30 30H92a30 30 0 0 1-30-30z"/>'
            '<path d="M148 98h18a16 16 0 0 1 0 32h-18"/>'
            '<path d="M92 70c0-10 10-10 10-20M120 70c0-10 10-10 10-20"/>'
            '<line x1="52" y1="178" x2="170" y2="178"/>'
        )
    if kind == "coffee":
        return (
            '<path d="M66 78h84v52a26 26 0 0 1-26 26H92a26 26 0 0 1-26-26z"/>'
            '<path d="M150 92h14a14 14 0 0 1 0 28h-14"/>'
            f'<rect x="66" y="78" width="84" height="14" fill="{INK}" stroke="none"/>'
            '<line x1="56" y1="176" x2="176" y2="176"/>'
        )
    return (  # water
        '<path d="M78 62h64l-8 106a16 16 0 0 1-16 14h-16a16 16 0 0 1-16-14z"/>'
        f'<path d="M83 112h54l-5 56a10 10 0 0 1-10 9h-24a10 10 0 0 1-10-9z" '
        f'fill="{ACCENT}" fill-opacity="0.35" stroke="none"/>'
        '<line x1="83" y1="112" x2="137" y2="112" stroke-width="2.4"/>'
    )


def weather(kind):
    cloud = '<path d="M76 116a26 26 0 0 1 5-51 34 34 0 0 1 64-6 24 24 0 0 1 3 57z"/>'
    if kind == "sun":
        import math

        rays = ""
        for i in range(8):
            a = math.radians(i * 45)
            x1, y1 = 120 + 52 * math.cos(a), 105 + 52 * math.sin(a)
            x2, y2 = 120 + 70 * math.cos(a), 105 + 70 * math.sin(a)
            rays += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'
        return f'<circle cx="120" cy="105" r="38"/>{rays}'
    if kind == "rain":
        drops = "".join(
            f'<line x1="{x}" y1="132" x2="{x - 8}" y2="{164}"/>' for x in (88, 112, 136, 160)
        )
        return cloud + drops
    flakes = ""
    for x in (88, 120, 152):
        flakes += (
            f'<line x1="{x}" y1="134" x2="{x}" y2="166"/>'
            f'<line x1="{x - 13}" y1="142" x2="{x + 13}" y2="158"/>'
            f'<line x1="{x - 13}" y1="158" x2="{x + 13}" y2="142"/>'
        )
    return cloud + flakes


def people(count):
    """Simple figures, spaced so the number is countable at a glance."""
    xs = {3: (68, 120, 172), 4: (56, 100, 144, 188), 6: (44, 76, 108, 140, 172, 204)}[count]
    scale = 1.0 if count < 5 else 0.82
    out = ""
    for x in xs:
        head_r = 13 * scale
        cy = 78
        out += (
            f'<circle cx="{x}" cy="{cy}" r="{head_r:.1f}"/>'
            f'<path d="M{x - 20 * scale:.0f} {cy + 66 * scale:.0f}'
            f'v-{30 * scale:.0f}a{20 * scale:.0f} {20 * scale:.0f} 0 0 1 {40 * scale:.0f} 0'
            f'v{30 * scale:.0f}"/>'
        )
    return out


def signpost(where):
    """A tiny street plan: the cross is the landmark, the pin the pharmacy."""
    roads = (
        '<line x1="20" y1="120" x2="220" y2="120" stroke-width="8" stroke="#e2e2de"/>'
        '<line x1="120" y1="24" x2="120" y2="200" stroke-width="8" stroke="#e2e2de"/>'
    )
    boxes = {
        "bank": ('<rect x="40" y="52" width="58" height="46"/>'
                 '<text x="69" y="82" font-family="Helvetica,Arial" font-size="19" '
                 f'fill="{INK}" stroke="none" text-anchor="middle">Bank</text>'),
        "bahnhof": ('<rect x="142" y="52" width="70" height="46"/>'
                    '<text x="177" y="82" font-family="Helvetica,Arial" font-size="16" '
                    f'fill="{INK}" stroke="none" text-anchor="middle">Bahnhof</text>'),
        "post": ('<rect x="40" y="52" width="58" height="46"/>'
                 '<text x="69" y="82" font-family="Helvetica,Arial" font-size="19" '
                 f'fill="{INK}" stroke="none" text-anchor="middle">Post</text>'),
    }
    pins = {"bank": (150, 74), "bahnhof": (72, 74), "post": (69, 158)}
    px, py = pins[where]
    pin = (
        f'<path d="M{px} {py + 22}c0 0 18-18 18-30a18 18 0 0 0-36 0c0 12 18 30 18 30z" '
        f'fill="{ACCENT}" fill-opacity="0.5"/>'
        f'<text x="{px}" y="{py - 2}" font-family="Helvetica,Arial" font-size="17" '
        f'font-weight="700" fill="{INK}" stroke="none" text-anchor="middle">+</text>'
    )
    return roads + boxes[where] + pin


# item number → (option key, filename stem, drawing)
PICTURES = {
    1: [("a", "zug-0915", clock(9, 15)), ("b", "zug-0950", clock(9, 50)),
        ("c", "zug-1015", clock(10, 15))],
    2: [("a", "preis-12", price("12 €")), ("b", "preis-20", price("20 €")),
        ("c", "preis-22", price("22 €"))],
    3: [("a", "apo-bank", signpost("bank")), ("b", "apo-bahnhof", signpost("bahnhof")),
        ("c", "apo-post", signpost("post"))],
    4: [("a", "trinken-tee", drink("tea")), ("b", "trinken-kaffee", drink("coffee")),
        ("c", "trinken-wasser", drink("water"))],
    5: [("a", "wetter-regen", weather("rain")), ("b", "wetter-schnee", weather("snow")),
        ("c", "wetter-sonne", weather("sun"))],
    6: [("a", "leute-3", people(3)), ("b", "leute-4", people(4)),
        ("c", "leute-6", people(6))],
}


class Command(BaseCommand):
    help = "Draw the A1 Hören Teil 1 picture options as SVG."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Redraw existing files.")

    def handle(self, *args, **options):
        out_dir = Path(settings.MEDIA_ROOT) / "exams" / "a1" / "bilder"
        out_dir.mkdir(parents=True, exist_ok=True)

        made = kept = 0
        for number, entries in PICTURES.items():
            for _key, stem, body in entries:
                target = out_dir / f"{stem}.svg"
                if target.exists() and not options["force"]:
                    kept += 1
                    continue
                target.write_text(svg(body), encoding="utf-8")
                made += 1

        self.stdout.write(
            self.style.SUCCESS(f"A1 pictures: {made} drawn, {kept} already present → {out_dir}")
        )
