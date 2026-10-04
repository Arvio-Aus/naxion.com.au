"""Generates the isometric placeholder product renders in assets/img/products/.

Run:  python tools/gen_product_images.py
Replace the generated SVGs with real product photography when available
(and update the `image` field in data/products.js).
"""
import math
import os

C, S = math.cos(math.pi / 6), 0.5
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "products")
FONT = "font-family=\"'Space Grotesk','Segoe UI',Arial,sans-serif\""
VB_W, VB_H = 480, 400

AMBER = "#FFB81C"
INK = "#E8EDF5"
MUTED = "#8C9BB4"


def P(u, w, h):
    """Isometric projection: u = width axis, w = depth axis, h = up."""
    return (C * u - C * w, -S * u - S * w - h)


def mat(a, b, c, d, origin):
    return f"matrix({a:.4f} {b:.4f} {c:.4f} {d:.4f} {origin[0]:.3f} {origin[1]:.3f})"


class Box:
    def __init__(self, W, D, H):
        self.W, self.D, self.H = W, D, H
        self.front_tf = mat(C, -S, 0, 1, P(0, 0, H))
        self.side_tf = mat(C, S, 0, 1, P(0, D, H))
        self.top_tf = mat(C, -S, C, S, P(0, D, H))

    def bbox(self):
        W, D, H = self.W, self.D, self.H
        return (-C * D, -(S * W + S * D + H), C * W, 0)


def defs():
    return f"""<defs>
  <linearGradient id="gFront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1D2B47"/><stop offset="1" stop-color="#0F1829"/></linearGradient>
  <linearGradient id="gSide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111B2E"/><stop offset="1" stop-color="#090F1B"/></linearGradient>
  <linearGradient id="gTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2F4266"/><stop offset="1" stop-color="#22324F"/></linearGradient>
  <linearGradient id="gAmber" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFC93C"/><stop offset="1" stop-color="#FF7A1A"/></linearGradient>
  <linearGradient id="gMetal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E4E9F1"/><stop offset="1" stop-color="#8E9AAE"/></linearGradient>
  <linearGradient id="gCyl" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0A111F"/><stop offset=".35" stop-color="#26385A"/><stop offset=".6" stop-color="#16233B"/><stop offset="1" stop-color="#070C17"/>
  </linearGradient>
  <linearGradient id="gCylAmber" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#B36A00"/><stop offset=".35" stop-color="#FFC93C"/><stop offset=".6" stop-color="#FF9A1A"/><stop offset="1" stop-color="#8A4300"/>
  </linearGradient>
  <radialGradient id="gShadow"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""


def wordmark(x, y, width, color=INK, mark=True):
    """Naxion wordmark (geometric strokes) placed with top-left at x,y in local units."""
    total = 146 + (62 if mark else 0)
    k = width / total
    hexmark = ""
    off = 0
    if mark:
        hexmark = (
            '<g transform="translate(0 -14)">'
            '<path d="M24 3.5 41.8 13.75v20.5L24 44.5 6.2 34.25v-20.5Z" stroke="url(#gAmber)" stroke-width="3.2" fill="none" stroke-linejoin="round"/>'
            f'<path d="M16.5 33V15M31.5 33V15" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M16.5 15 31.5 33" stroke="url(#gAmber)" stroke-width="4" stroke-linecap="round"/></g>'
        )
        off = 62
    return (
        f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f})">{hexmark}'
        f'<g transform="translate({off} 0)" stroke="{color}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M0 20V0l16 20V0"/><path d="M28 20 37 0l9 20"/><path d="M58 0l16 20M74 0 58 20"/>'
        '<path d="M86 0v20"/><circle cx="108" cy="10" r="10"/><path d="M130 20V0l16 20V0"/></g></g>'
    )


def box_faces(b, px, front="url(#gFront)", side="url(#gSide)", top="url(#gTop)"):
    edge = f'stroke="#ffffff" stroke-opacity=".10" stroke-width="{px(1)}"'
    return (
        f'<g transform="{b.side_tf}"><rect width="{b.D}" height="{b.H}" fill="{side}" {edge}/></g>'
        f'<g transform="{b.front_tf}"><rect width="{b.W}" height="{b.H}" fill="{front}" {edge}/></g>'
        f'<g transform="{b.top_tf}"><rect width="{b.W}" height="{b.D}" fill="{top}" {edge}/></g>'
    )


def stud(b, u, w, r, height, metal="url(#gMetal)", ring=None, px=lambda n: n):
    """A cylindrical terminal on the top face, built from stacked discs."""
    out = []
    steps = 6
    for i in range(steps + 1):
        dy = -height * i / steps
        fill = "#5B677C" if i < steps else metal
        out.append(f'<g transform="translate(0 {dy:.2f})"><g transform="{b.top_tf}"><circle cx="{u}" cy="{w}" r="{r}" fill="{fill}"/></g></g>')
    if ring:
        out.append(
            f'<g transform="translate(0 {-height:.2f})"><g transform="{b.top_tf}">'
            f'<circle cx="{u}" cy="{w}" r="{r * 0.78}" fill="none" stroke="{ring}" stroke-width="{r * 0.16}"/>'
            f'<circle cx="{u}" cy="{w}" r="{r * 0.3}" fill="#3A4558"/></g></g>'
        )
    else:
        out.append(f'<g transform="translate(0 {-height:.2f})"><g transform="{b.top_tf}"><circle cx="{u}" cy="{w}" r="{r * 0.3}" fill="#3A4558"/></g></g>')
    return "".join(out)


def frame(content, bbox):
    """Scale and centre content (in mm) into the fixed viewBox, with floor shadow."""
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0
    s = min(380 / w, 310 / h)
    tx = VB_W / 2 - (x0 + w / 2) * s
    ty = 360 - y1 * s
    shadow_w = w * s * 0.62
    return s, (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" fill="none">{defs()}'
        f'<ellipse cx="{VB_W / 2}" cy="362" rx="{shadow_w:.1f}" ry="{max(14, shadow_w * 0.16):.1f}" fill="url(#gShadow)"/>'
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">{content}</g></svg>'
    )


def render(build, bbox):
    # Two-pass: compute scale, then build content with pixel-correct stroke widths.
    x0, y0, x1, y1 = bbox
    s = min(380 / (x1 - x0), 310 / (y1 - y0))
    px = lambda n: n / s
    _, svg = frame(build(px), bbox)
    return svg


# ---------------------------------------------------------------- products

def prismatic(W, D, H, model, rating):
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px)]
        # front label
        f = [
            f'<rect x="{W * .07}" y="{H * .07}" width="{W * .86}" height="{H * .86}" rx="{W * .03}" fill="#ffffff" fill-opacity=".03" stroke="#ffffff" stroke-opacity=".08" stroke-width="{px(1)}"/>',
            wordmark(W * .14, H * .19, W * .72),
            f'<text x="{W * .14}" y="{H * .47}" {FONT} font-size="{W * .062}" letter-spacing="{W * .012}" fill="{MUTED}">SODIUM-ION CELL</text>',
            f'<text x="{W * .14}" y="{H * .62}" {FONT} font-size="{W * .14}" font-weight="700" fill="{INK}">{model}</text>',
            f'<text x="{W * .14}" y="{H * .74}" {FONT} font-size="{W * .075}" font-weight="600" fill="{AMBER}">{rating}</text>',
            f'<rect x="{W * .14}" y="{H * .82}" width="{W * .72}" height="{H * .018}" rx="{H * .009}" fill="url(#gAmber)"/>',
        ]
        out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        # top: vent + QR-ish patch
        r = min(W * .085, D * .30)
        t = [
            f'<ellipse cx="{W / 2}" cy="{D / 2}" rx="{W * .07}" ry="{D * .17}" fill="#0A0F1A" stroke="#ffffff" stroke-opacity=".12" stroke-width="{px(1)}"/>',
            f'<rect x="{W * .36}" y="{D * .2}" width="{W * .05}" height="{D * .6}" rx="{px(2)}" fill="#ffffff" fill-opacity=".06"/>',
        ]
        out.append(f'<g transform="{b.top_tf}">{"".join(t)}</g>')
        out.append(stud(b, W * .2, D / 2, r, H * .035, ring=AMBER))
        out.append(stud(b, W * .8, D / 2, r, H * .035))
        return "".join(out)

    return render(build, (b.bbox()[0], b.bbox()[1] - H * .04, b.bbox()[2], b.bbox()[3]))


def cylindrical(d, h, model, rating):
    r = d / 2
    rx, ry = C * math.sqrt(2) * r, S * math.sqrt(2) * r

    def cell(cx, cy, px):
        body = f'M{cx - rx} {cy - h} L{cx - rx} {cy} A{rx} {ry} 0 0 0 {cx + rx} {cy} L{cx + rx} {cy - h} Z'

        def band(y1, y2, fill):
            return f'<path d="M{cx - rx} {cy - y2} L{cx - rx} {cy - y1} A{rx} {ry} 0 0 0 {cx + rx} {cy - y1} L{cx + rx} {cy - y2} A{rx} {ry} 0 0 1 {cx - rx} {cy - y2} Z" fill="{fill}"/>'

        return "".join([
            f'<path d="{body}" fill="url(#gCyl)"/>',
            band(h * .12, h * .17, "url(#gCylAmber)"),
            band(h * .83, h * .86, "url(#gCylAmber)"),
            f'<text x="{cx}" y="{cy - h * .5}" text-anchor="middle" {FONT} font-size="{d * .17}" font-weight="700" fill="{INK}">{model}</text>',
            f'<text x="{cx}" y="{cy - h * .42}" text-anchor="middle" {FONT} font-size="{d * .11}" font-weight="600" fill="{AMBER}">{rating}</text>',
            f'<text x="{cx}" y="{cy - h * .66}" text-anchor="middle" {FONT} font-size="{d * .09}" letter-spacing="{d * .02}" fill="{MUTED}">NAXION</text>',
            f'<ellipse cx="{cx}" cy="{cy - h}" rx="{rx}" ry="{ry}" fill="url(#gMetal)"/>',
            f'<ellipse cx="{cx}" cy="{cy - h}" rx="{rx * .82}" ry="{ry * .82}" fill="#0E1626"/>',
            f'<ellipse cx="{cx}" cy="{cy - h - d * .03}" rx="{rx * .36}" ry="{ry * .36}" fill="#6E7B90"/>',
            f'<ellipse cx="{cx}" cy="{cy - h - d * .06}" rx="{rx * .36}" ry="{ry * .36}" fill="url(#gMetal)"/>',
        ])

    def build(px):
        return cell(-rx * 1.15, -ry * 0.9, px) + cell(rx * 1.15, 0, px)

    return render(build, (-rx * 2.3, -h - ry * 2.2 - d * .1, rx * 2.3, ry))


def wall(W, D, H, model):
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px, front="#E9EDF3", side="#B9C2D0", top="#F6F8FB")]
        f = [
            f'<rect x="{W * .06}" y="{H * .05}" width="{W * .88}" height="{H * .9}" rx="{W * .04}" fill="#DCE2EB"/>',
            f'<rect x="{W * .06}" y="{H * .05}" width="{W * .88}" height="{H * .22}" rx="{W * .04}" fill="#0F1829"/>',
            wordmark(W * .2, H * .145, W * .6),
            f'<rect x="{W * .25}" y="{H * .34}" width="{W * .5}" height="{H * .012}" rx="{H * .006}" fill="url(#gAmber)" filter="url(#glow)"/>',
        ]
        for i in range(5):
            fill = AMBER if i < 4 else "#9AA6B8"
            f.append(f'<circle cx="{W * (.38 + i * .06)}" cy="{H * .39}" r="{W * .012}" fill="{fill}"/>')
        f.append(f'<text x="{W / 2}" y="{H * .88}" text-anchor="middle" {FONT} font-size="{W * .05}" font-weight="700" letter-spacing="{W * .01}" fill="#5A678C">{model}</text>')
        out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        s = []
        for i in range(10):
            s.append(f'<rect x="{D * .3}" y="{H * (.55 + i * .035)}" width="{D * .4}" height="{H * .012}" rx="{px(2)}" fill="#8995A9"/>')
        out.append(f'<g transform="{b.side_tf}">{"".join(s)}</g>')
        return "".join(out)

    return render(build, b.bbox())


def rack(W, D, H, model):
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px, top="#26354F")]
        f = [
            f'<rect x="0" y="0" width="{W * .05}" height="{H}" fill="#2B3B58"/>',
            f'<rect x="{W * .95}" y="0" width="{W * .05}" height="{H}" fill="#2B3B58"/>',
            f'<rect x="{W * .07}" y="{H * .18}" width="{W * .025}" height="{H * .64}" rx="{W * .012}" fill="none" stroke="#9AA6B8" stroke-width="{W * .008}"/>',
            f'<rect x="{W * .905}" y="{H * .18}" width="{W * .025}" height="{H * .64}" rx="{W * .012}" fill="none" stroke="#9AA6B8" stroke-width="{W * .008}"/>',
            wordmark(W * .13, H * .42, W * .26),
            f'<text x="{W * .13}" y="{H * .78}" {FONT} font-size="{H * .11}" font-weight="700" fill="{MUTED}">{model}</text>',
            # LEDs
            *[f'<circle cx="{W * (.45 + i * .03)}" cy="{H * .5}" r="{H * .035}" fill="{AMBER if i < 3 else "#3DD6C8"}" filter="url(#glow)"/>' for i in range(4)],
            # comms ports
            *[f'<rect x="{W * (.58 + i * .05)}" y="{H * .38}" width="{W * .035}" height="{H * .22}" rx="{px(1.5)}" fill="#0A0F1A" stroke="#4A5A76" stroke-width="{px(1)}"/>' for i in range(2)],
            # breaker
            f'<rect x="{W * .7}" y="{H * .25}" width="{W * .06}" height="{H * .5}" rx="{px(2)}" fill="#0A0F1A"/>',
            f'<rect x="{W * .715}" y="{H * .3}" width="{W * .03}" height="{H * .2}" rx="{px(2)}" fill="url(#gAmber)"/>',
            # terminals
            f'<circle cx="{W * .81}" cy="{H * .5}" r="{H * .13}" fill="#0A0F1A" stroke="{AMBER}" stroke-width="{H * .025}"/>',
            f'<circle cx="{W * .87}" cy="{H * .5}" r="{H * .13}" fill="#0A0F1A" stroke="#9AA6B8" stroke-width="{H * .025}"/>',
        ]
        out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        t = [f'<rect x="{W * .08}" y="{D * .08}" width="{W * .84}" height="{D * .84}" rx="{px(3)}" fill="none" stroke="#ffffff" stroke-opacity=".06" stroke-width="{px(1)}"/>']
        out.append(f'<g transform="{b.top_tf}">{"".join(t)}</g>')
        return "".join(out)

    return render(build, b.bbox())


def stack(W, D, H, n, model):
    """n rack modules stacked in an open frame (shown as one tall rack)."""
    b = Box(W, D, H * n)

    def build(px):
        out = [box_faces(b, px, front="#0B1220", top="#26354F")]
        for i in range(n):
            y = H * i
            f = [
                f'<rect x="{W * .03}" y="{y + H * .06}" width="{W * .94}" height="{H * .88}" rx="{px(3)}" fill="url(#gFront)" stroke="#ffffff" stroke-opacity=".08" stroke-width="{px(1)}"/>',
                wordmark(W * .1, y + H * .45, W * .22),
                *[f'<circle cx="{W * (.45 + k * .03)}" cy="{y + H * .5}" r="{H * .035}" fill="{AMBER if k < 3 else "#3DD6C8"}"/>' for k in range(4)],
                f'<circle cx="{W * .8}" cy="{y + H * .5}" r="{H * .12}" fill="#0A0F1A" stroke="{AMBER}" stroke-width="{H * .025}"/>',
                f'<circle cx="{W * .87}" cy="{y + H * .5}" r="{H * .12}" fill="#0A0F1A" stroke="#9AA6B8" stroke-width="{H * .025}"/>',
            ]
            out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        return "".join(out)

    return render(build, b.bbox())


def lv12(W, D, H, model, rating):
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px)]
        f = [
            f'<rect x="0" y="{H * .1}" width="{W}" height="{H * .02}" fill="#ffffff" fill-opacity=".08"/>',
            wordmark(W * .1, H * .27, W * .5),
            f'<text x="{W * .1}" y="{H * .58}" {FONT} font-size="{W * .12}" font-weight="700" fill="{INK}">{rating}</text>',
            f'<text x="{W * .1}" y="{H * .7}" {FONT} font-size="{W * .042}" letter-spacing="{W * .008}" fill="{MUTED}">SODIUM-ION · {model}</text>',
            f'<rect x="0" y="{H * .86}" width="{W}" height="{H * .06}" fill="url(#gAmber)"/>',
        ]
        out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        t = [
            f'<rect x="{W * .3}" y="{D * .42}" width="{W * .4}" height="{D * .16}" rx="{D * .08}" fill="#0A0F1A"/>',
            f'<rect x="{W * .02}" y="{D * .02}" width="{W * .96}" height="{D * .96}" rx="{px(4)}" fill="none" stroke="#ffffff" stroke-opacity=".08" stroke-width="{px(1)}"/>',
        ]
        out.append(f'<g transform="{b.top_tf}">{"".join(t)}</g>')
        r = D * .1
        out.append(stud(b, W * .1, D * .5, r, H * .06, ring=AMBER))
        out.append(stud(b, W * .9, D * .5, r, H * .06))
        return "".join(out)

    return render(build, (b.bbox()[0], b.bbox()[1] - H * .07, b.bbox()[2], 0))


def cabinet(W, D, H, model):
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px, front="#E9EDF3", side="#B9C2D0", top="#F6F8FB")]
        f = [
            f'<rect x="0" y="{H * .955}" width="{W}" height="{H * .045}" fill="#1A2436"/>',
            f'<rect x="{W * .05}" y="{H * .03}" width="{W * .9}" height="{H * .9}" fill="none" stroke="#AAB4C3" stroke-width="{px(1.2)}"/>',
            f'<line x1="{W / 2}" y1="{H * .03}" x2="{W / 2}" y2="{H * .93}" stroke="#AAB4C3" stroke-width="{px(1.2)}"/>',
            f'<rect x="{W * .46}" y="{H * .42}" width="{W * .015}" height="{H * .12}" rx="{W * .007}" fill="#1A2436"/>',
            f'<rect x="{W * .525}" y="{H * .42}" width="{W * .015}" height="{H * .12}" rx="{W * .007}" fill="#1A2436"/>',
            f'<rect x="{W * .1}" y="{H * .07}" width="{W * .34}" height="{H * .08}" rx="{px(3)}" fill="#0F1829"/>',
            wordmark(W * .13, H * .108, W * .28),
            f'<rect x="{W * .1}" y="{H * .18}" width="{W * .34}" height="{H * .006}" fill="url(#gAmber)" filter="url(#glow)"/>',
            f'<path d="M{W * .75} {H * .1} l{W * .045} {H * .045} h-{W * .09} Z" fill="{AMBER}"/>',
            f'<text x="{W * .1}" y="{H * .25}" {FONT} font-size="{W * .035}" font-weight="700" fill="#5A678C">{model}</text>',
        ]
        for side_x in (W * .1, W * .6):
            for i in range(8):
                f.append(f'<rect x="{side_x}" y="{H * (.7 + i * .025)}" width="{W * .3}" height="{H * .008}" rx="{px(2)}" fill="#AAB4C3"/>')
        out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        s = [f'<rect x="0" y="{H * .955}" width="{D}" height="{H * .045}" fill="#121A29"/>']
        for i in range(12):
            s.append(f'<rect x="{D * .2}" y="{H * (.3 + i * .03)}" width="{D * .6}" height="{H * .009}" rx="{px(2)}" fill="#8995A9"/>')
        out.append(f'<g transform="{b.side_tf}">{"".join(s)}</g>')
        return "".join(out)

    return render(build, b.bbox())


PRODUCTS = {
    "nx-p160": lambda: prismatic(173.7, 71.7, 207.2, "NX-P160", "3.0V · 160Ah"),
    "nx-p210": lambda: prismatic(173.7, 86.0, 207.2, "NX-P210", "3.1V · 210Ah"),
    "nx-p50": lambda: prismatic(148.0, 27.0, 129.0, "NX-P50", "3.0V · 50Ah"),
    "nx-c26": lambda: cylindrical(26.0, 70.0, "NX-C26", "3.0V 3.5Ah"),
    "nx-w7": lambda: wall(600, 170, 880, "NX-W7"),
    "nx-r5": lambda: rack(442, 420, 133, "NX-R5"),
    "nx-m12": lambda: lv12(330, 172, 215, "NX-M12", "12V · 100Ah"),
    "nx-ci115": lambda: cabinet(1100, 1000, 2200, "NX-CI115"),
    "nx-r5-stack": lambda: stack(442, 420, 133, 4, "NX-R5"),
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in PRODUCTS.items():
        path = os.path.join(OUT, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fn())
        print("wrote", os.path.normpath(path))
