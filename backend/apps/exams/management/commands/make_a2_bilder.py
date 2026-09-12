"""Draw the pictures for A2 Hören Teil 2 and Teil 3:

    python manage.py make_a2_bilder [--force]

Teil 2 matches days to nine activity pictures (a–i); Teil 3 answers each
question with three pictures. Like A1's, they are plain SVG line drawings of
our own, so they scale to any screen and a fresh checkout can make them.
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from .make_a1_bilder import ACCENT, INK, SOFT, clock, svg

WATER = f'fill="{ACCENT}" fill-opacity="0.28" stroke="none"'


def label(x, y, text, size=16):
    return (
        f'<text x="{x}" y="{y}" font-family="Helvetica,Arial" font-size="{size}" '
        f'font-weight="700" fill="{INK}" stroke="none" text-anchor="middle">{text}</text>'
    )


def waves(y, x0=36, x1=204, step=24):
    path = f"M{x0} {y}"
    for _ in range((x1 - x0) // step):
        path += f"q{step // 4} -8 {step // 2} 0t{step // 2} 0"
    return f'<path d="{path}" stroke-width="2.6"/>'


def bike(dx=0, dy=0, scale=1.0):
    """Wheels, diamond frame, saddle and bars."""
    def p(x, y):
        return f"{dx + x * scale:.1f} {dy + y * scale:.1f}"

    r = 34 * scale
    return (
        f'<circle cx="{dx + 62 * scale:.1f}" cy="{dy + 140 * scale:.1f}" r="{r:.1f}"/>'
        f'<circle cx="{dx + 178 * scale:.1f}" cy="{dy + 140 * scale:.1f}" r="{r:.1f}"/>'
        f'<path d="M{p(62, 140)}L{p(116, 140)}L{p(96, 84)}L{p(156, 84)}L{p(116, 140)}'
        f'M{p(62, 140)}L{p(96, 84)}M{p(156, 84)}L{p(178, 140)}"/>'
        f'<path d="M{p(96, 84)}L{p(92, 72)}M{p(82, 72)}L{p(104, 72)}'
        f'M{p(156, 84)}L{p(150, 66)}L{p(166, 62)}"/>'
    )


# ------------------------------------------------------ Teil 2: activities


def schwimmbad():
    return (
        '<rect x="30" y="96" width="180" height="86" rx="6"/>'
        f'<rect x="32" y="112" width="176" height="68" rx="4" {WATER}/>'
        + waves(126) + waves(150)
        # the ladder rising out of the water
        + '<path d="M156 146V78a12 12 0 0 1 24 0M172 146V78a12 12 0 0 1 24 0"/>'
        '<path d="M156 96h16M156 114h16M156 132h16"/>'
        # a swimmer's head and arm
        '<circle cx="84" cy="138" r="9"/><path d="M96 134q14-16 28-4"/>'
    )


def museum():
    columns = "".join(
        f'<rect x="{x}" y="96" width="14" height="62"/>' for x in (52, 84, 116, 148, 180)
    )
    return (
        '<path d="M36 88L120 46l84 42z"/><line x1="36" y1="88" x2="204" y2="88"/>'
        '<circle cx="120" cy="72" r="7"/>'
        + columns
        + '<rect x="38" y="160" width="164" height="10"/><line x1="26" y1="182" x2="214" y2="182"/>'
        '<line x1="32" y1="170" x2="208" y2="170"/>'
    )


def radtour():
    return (
        bike(12, 8, 0.82)
        + f'<path d="M16 196q52-16 104-6t104-4" stroke="{SOFT}" stroke-width="2.4"/>'
        # the lake behind
        + f'<ellipse cx="170" cy="46" rx="48" ry="14" {WATER}/>'
        + f'<path d="M126 46q10-6 20 0t20 0t20 0" stroke="{SOFT}" stroke-width="2"/>'
        + '<circle cx="54" cy="44" r="16"/>'
    )


def konzert():
    lights = "".join(
        f'<path d="M{x} 30l{d} 50" stroke="{SOFT}" stroke-width="2.4"/>'
        for x, d in ((40, 24), (120, 0), (200, -24))
    )
    return (
        lights
        + '<path d="M22 160h196v22H22z"/>'
        # a singer at a microphone
        + '<circle cx="120" cy="96" r="12"/><path d="M104 158v-30a16 16 0 0 1 32 0v30"/>'
        '<path d="M150 158v-44M144 110h12"/><circle cx="150" cy="106" r="5"/>'
        # notes
        + f'<circle cx="60" cy="118" r="8" fill="{INK}"/><path d="M68 118V82l18-6v36"/>'
        f'<circle cx="78" cy="112" r="8" fill="{INK}"/>'
        f'<circle cx="184" cy="120" r="8" fill="{INK}"/><path d="M192 120V86l10 8"/>'
    )


def kochen():
    return (
        '<path d="M64 96h112v52a18 18 0 0 1-18 18H82a18 18 0 0 1-18-18z"/>'
        '<path d="M64 108H48M176 108h16"/>'
        '<path d="M58 96h124"/><path d="M110 96v-8h20v8"/>'
        '<path d="M92 76c0-12 10-12 10-24M120 76c0-12 10-12 10-24M148 76c0-12 10-12 10-24"/>'
        '<line x1="40" y1="182" x2="200" y2="182" stroke-width="5"/>'
        f'<path d="M92 176q6-10 12 0M116 176q6-10 12 0M140 176q6-10 12 0" stroke="{ACCENT}"/>'
    )


def kino():
    seats = "".join(
        f'<path d="M{x} 186v-20a14 14 0 0 1 28 0v20"/>' for x in (34, 70, 106, 142, 178)
    )
    heads = "".join(f'<circle cx="{x}" cy="150" r="10"/>' for x in (84, 156))
    return (
        '<rect x="34" y="26" width="172" height="92" rx="4"/>'
        f'<path d="M108 52v40l34-20z" fill="{ACCENT}" fill-opacity="0.45"/>'
        + heads + seats
    )


def wandern():
    return (
        '<path d="M14 182L82 70l38 56 28-40 78 96z"/>'
        '<path d="M68 94l14-24 14 22-8-4-6 8-6-6z" fill="#fff"/>'
        f'<path d="M92 182q18-24 44-30t30-32" stroke="{SOFT}" stroke-dasharray="6 7"/>'
        '<circle cx="190" cy="44" r="16"/>'
        # a hiker with a stick
        '<circle cx="54" cy="136" r="8"/><path d="M54 144v22l-8 16M54 166l10 16M54 150l14 8"/>'
        '<path d="M70 146l-6 36"/>'
    )


def markt():
    scallops = "".join(f'<path d="M{x} 76a12 12 0 0 0 24 0"/>' for x in range(36, 204, 24))
    fruit = "".join(
        f'<circle cx="{x}" cy="{y}" r="11" {extra}/>'
        for x, y, extra in (
            (68, 128, f'fill="{ACCENT}" fill-opacity="0.45"'),
            (92, 128, f'fill="{ACCENT}" fill-opacity="0.45"'),
            (80, 110, f'fill="{ACCENT}" fill-opacity="0.45"'),
            (150, 128, 'fill="#e5a33a" fill-opacity="0.5"'),
            (174, 128, 'fill="#e5a33a" fill-opacity="0.5"'),
            (162, 110, 'fill="#e5a33a" fill-opacity="0.5"'),
        )
    )
    return (
        '<path d="M30 76l14-40h152l14 40z"/>' + scallops
        + '<path d="M44 88v94M196 88v94"/><rect x="36" y="140" width="168" height="18"/>'
        + fruit
    )


def fussball():
    net = "".join(f'<line x1="{x}" y1="64" x2="{x}" y2="150" stroke="{SOFT}" stroke-width="1.6"/>'
                  for x in range(58, 200, 18))
    net += "".join(f'<line x1="40" y1="{y}" x2="200" y2="{y}" stroke="{SOFT}" stroke-width="1.6"/>'
                   for y in range(82, 150, 18))
    return (
        net
        + '<path d="M40 150V60h160v90"/><line x1="20" y1="150" x2="220" y2="150"/>'
        '<circle cx="120" cy="176" r="20"/>'
        f'<path d="M120 166l9 7-4 10h-10l-4-10z" fill="{INK}"/>'
        '<path d="M120 166v-10M129 173l10-4M125 183l6 9M115 183l-6 9M111 173l-10-4" '
        'stroke-width="2"/>'
    )


# -------------------------------------------------- Teil 3: answer pictures


def plate():
    return '<ellipse cx="120" cy="150" rx="92" ry="26"/>'


def pizza():
    return (
        '<circle cx="120" cy="108" r="70"/><circle cx="120" cy="108" r="58" stroke-width="2"/>'
        '<path d="M120 50v116M70 79l100 58M70 137l100-58" stroke-width="2"/>'
        + "".join(
            f'<circle cx="{x}" cy="{y}" r="8" fill="#d9573f" fill-opacity="0.55" stroke="none"/>'
            for x, y in ((98, 82), (146, 90), (92, 130), (140, 136), (120, 108))
        )
    )


def bowl():
    return '<path d="M42 104h156c0 44-34 70-78 70s-78-26-78-70z"/><path d="M92 174h56"/>'


def salat():
    leaves = (
        f'<path d="M58 104c4-30 28-40 44-38-4 20-18 34-44 38z" fill="{ACCENT}" '
        f'fill-opacity="0.45"/>'
        f'<path d="M100 104c6-34 30-46 50-44-6 24-22 38-50 44z" fill="{ACCENT}" '
        f'fill-opacity="0.45"/>'
        f'<path d="M142 104c2-24 20-34 38-32-4 18-16 28-38 32z" fill="{ACCENT}" '
        f'fill-opacity="0.45"/>'
        '<circle cx="128" cy="92" r="9" fill="#d9573f" fill-opacity="0.55"/>'
    )
    return leaves + bowl()


def suppe():
    return (
        bowl()
        + '<path d="M50 104q70 14 140 0" stroke-width="2"/>'
        '<path d="M150 112l44-66" stroke-width="5"/>'
        '<path d="M92 84c0-12 10-12 10-24M120 84c0-12 10-12 10-24"/>'
    )


def handtasche():
    return (
        '<path d="M58 96h124l16 84H42z"/>'
        '<path d="M88 96V82a32 32 0 0 1 64 0v14"/>'
        '<rect x="108" y="112" width="24" height="12" rx="3"/>'
    )


def rucksack():
    return (
        '<path d="M100 44a20 20 0 0 1 40 0"/>'
        '<rect x="66" y="50" width="108" height="140" rx="34"/>'
        '<rect x="88" y="120" width="64" height="48" rx="10"/>'
        '<path d="M88 138h64"/><path d="M78 84h84" stroke-width="2"/>'
    )


def koffer():
    return (
        '<rect x="62" y="64" width="116" height="116" rx="12"/>'
        '<path d="M100 64V48h40v16"/>'
        '<path d="M94 72v100M146 72v100" stroke-width="2.4"/>'
        '<circle cx="82" cy="192" r="8"/><circle cx="158" cy="192" r="8"/>'
    )


def schluessel():
    return (
        '<circle cx="72" cy="110" r="30"/><circle cx="62" cy="110" r="8"/>'
        '<path d="M102 110h104M178 110v20M194 110v14M162 110v12"/>'
    )


def brille():
    return (
        '<circle cx="80" cy="116" r="32"/><circle cx="160" cy="116" r="32"/>'
        '<path d="M112 110q8-12 16 0"/><path d="M48 108l-20-20M192 108l20-20"/>'
    )


def regenschirm():
    scallop = "".join(f"q-10-12 -20 0" for _ in range(8))
    return (
        f'<path d="M40 112a80 72 0 0 1 160 0{scallop}z"/>'
        '<path d="M120 40v-8M120 112v62a12 12 0 0 1-24 0"/>'
        '<path d="M120 40q-30 20-40 72M120 40q30 20 40 72" stroke-width="2"/>'
    )


def auto():
    return (
        '<path d="M28 150v-28l24-8 26-34h82l30 34 26 8v28z"/>'
        '<path d="M86 88h32v26H64zM126 88h30l22 26h-52z" stroke-width="2.4"/>'
        '<circle cx="76" cy="152" r="18" fill="#fff"/><circle cx="170" cy="152" r="18" fill="#fff"/>'
        '<line x1="14" y1="172" x2="226" y2="172" stroke="' + SOFT + '"/>'
    )


def fahrrad():
    return bike(0, 4, 1.0)


def bus():
    windows = "".join(
        f'<rect x="{x}" y="72" width="28" height="30" rx="3" stroke-width="2.4"/>'
        for x in (48, 84, 120)
    )
    return (
        '<rect x="34" y="54" width="176" height="104" rx="14"/>'
        + windows
        + '<rect x="160" y="72" width="36" height="60" rx="3" stroke-width="2.4"/>'
        '<path d="M34 118h120" stroke-width="2.4"/>'
        + label(94, 140, "BUS", 16)
        + '<circle cx="74" cy="162" r="16" fill="#fff"/><circle cx="174" cy="162" r="16" fill="#fff"/>'
    )


# file stem → drawing
PICTURES = {
    "schwimmbad": schwimmbad(),
    "museum": museum(),
    "radtour": radtour(),
    "konzert": konzert(),
    "kochen": kochen(),
    "kino": kino(),
    "wandern": wandern(),
    "markt": markt(),
    "fussball": fussball(),
    "pizza": pizza(),
    "salat": salat(),
    "suppe": suppe(),
    "handtasche": handtasche(),
    "rucksack": rucksack(),
    "koffer": koffer(),
    "schluessel": schluessel(),
    "brille": brille(),
    "regenschirm": regenschirm(),
    "uhr-1830": clock(6, 30),
    "uhr-1900": clock(7, 0),
    "uhr-1930": clock(7, 30),
    "auto": auto(),
    "fahrrad": fahrrad(),
    "bus": bus(),
}


class Command(BaseCommand):
    help = "Draw the A2 Hören Teil 2 and Teil 3 pictures as SVG."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Redraw existing files.")

    def handle(self, *args, **options):
        out_dir = Path(settings.MEDIA_ROOT) / "exams" / "a2" / "bilder"
        out_dir.mkdir(parents=True, exist_ok=True)

        made = kept = 0
        for stem, body in PICTURES.items():
            target = out_dir / f"{stem}.svg"
            if target.exists() and not options["force"]:
                kept += 1
                continue
            target.write_text(svg(body), encoding="utf-8")
            made += 1

        self.stdout.write(
            self.style.SUCCESS(f"A2 pictures: {made} drawn, {kept} already present → {out_dir}")
        )
