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
  <linearGradient id="gTeal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6FF0E2"/><stop offset="1" stop-color="#1FA7C9"/></linearGradient>
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


def uc_wordmark(x, y, width, color=INK):
    """UltraCap logo (capacitor mark + ULTRACAP wordmark), top-left at x,y in local units."""
    k = width / 268
    return (
        f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f}) translate(0 -14)">'
        '<circle cx="24" cy="24" r="20.4" stroke="url(#gTeal)" stroke-width="3.2" stroke-dasharray="104 24" stroke-linecap="round" fill="none" transform="rotate(-62 24 24)"/>'
        f'<path d="M10.5 24H18.5M29.5 24H37.5" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>'
        '<path d="M19.5 13.5v21" stroke="url(#gTeal)" stroke-width="4.4" stroke-linecap="round"/>'
        f'<path d="M28.5 13.5v21" stroke="{color}" stroke-width="4.4" stroke-linecap="round"/>'
        f'<g stroke="{color}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate(62 14)">'
        '<path d="M0 0v12a8 8 0 0 0 16 0V0"/><path d="M28 0v20h14"/><path d="M52 0h16M60 0v20"/>'
        '<path d="M78 20V0h9a5.5 5.5 0 0 1 0 11h-9M87 11l7 9"/><path d="M104 20 113 0l9 20"/></g>'
        '<g stroke="url(#gTeal)" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate(62 14)">'
        '<path d="M150 4A10 10 0 1 0 150 16"/><path d="M160 20 169 0l9 20"/><path d="M188 20V0h9a5.5 5.5 0 0 1 0 11h-9"/></g></g>'
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


TEAL = "#3DD6C8"


def uc_pack_front(W, H, px, y=0, label=True):
    """Front panel of a liquid-cooled 360 V capacitor pack (local units)."""
    f = [
        f'<rect x="{W * .015}" y="{y + H * .08}" width="{W * .97}" height="{H * .84}" rx="{px(3)}" fill="url(#gFront)" stroke="#ffffff" stroke-opacity=".08" stroke-width="{px(1)}"/>',
        # handles
        f'<rect x="{W * .03}" y="{y + H * .3}" width="{W * .05}" height="{H * .4}" rx="{H * .08}" fill="none" stroke="#9AA6B8" stroke-width="{H * .05}"/>',
        f'<rect x="{W * .92}" y="{y + H * .3}" width="{W * .05}" height="{H * .4}" rx="{H * .08}" fill="none" stroke="#9AA6B8" stroke-width="{H * .05}"/>',
        # coolant quick-connectors
        f'<circle cx="{W * .62}" cy="{y + H * .5}" r="{H * .13}" fill="#0A0F1A" stroke="{TEAL}" stroke-width="{H * .04}"/>',
        f'<circle cx="{W * .7}" cy="{y + H * .5}" r="{H * .13}" fill="#0A0F1A" stroke="#1FA7C9" stroke-width="{H * .04}"/>',
        # HV connectors
        f'<rect x="{W * .77}" y="{y + H * .32}" width="{W * .055}" height="{H * .36}" rx="{px(2)}" fill="#0A0F1A" stroke="{AMBER}" stroke-width="{px(1.2)}"/>',
        f'<rect x="{W * .845}" y="{y + H * .32}" width="{W * .055}" height="{H * .36}" rx="{px(2)}" fill="#0A0F1A" stroke="#9AA6B8" stroke-width="{px(1.2)}"/>',
        # status light
        f'<rect x="{W * .46}" y="{y + H * .44}" width="{W * .1}" height="{H * .12}" rx="{H * .06}" fill="url(#gTeal)" filter="url(#glow)"/>',
    ]
    if label:
        f.append(uc_wordmark(W * .11, y + H * .52, W * .3))
    return "".join(f)


def uc_pack(W, D, H):
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px, front="#0B1220", side="url(#gSide)", top="#26354F")]
        out.append(f'<g transform="{b.front_tf}">{uc_pack_front(W, H, px)}</g>')
        t = []
        cols, rows = 5, 9
        for c in range(cols):
            for r in range(rows):
                t.append(
                    f'<rect x="{W * (.06 + c * .178)}" y="{D * (.05 + r * .1)}" width="{W * .15}" height="{D * .08}" rx="{px(2)}" '
                    f'fill="#ffffff" fill-opacity=".04" stroke="#ffffff" stroke-opacity=".08" stroke-width="{px(1)}"/>'
                )
        t.append(f'<rect x="{W * .03}" y="{D * .02}" width="{W * .94}" height="{D * .96}" rx="{px(4)}" fill="none" stroke="{TEAL}" stroke-opacity=".35" stroke-width="{px(1.2)}"/>')
        out.append(f'<g transform="{b.top_tf}">{"".join(t)}</g>')
        return "".join(out)

    return render(build, b.bbox())


def uc_cluster(W, D, pack_h, n, box_h):
    H = pack_h * n + box_h
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px, front="#070B14", side="#0B1220", top="#26354F")]
        f = [
            # high-voltage box on top
            f'<rect x="{W * .03}" y="{H * .01}" width="{W * .94}" height="{box_h * .92}" rx="{px(3)}" fill="#1A2232" stroke="#ffffff" stroke-opacity=".08" stroke-width="{px(1)}"/>',
            uc_wordmark(W * .07, box_h * .5, W * .34),
            f'<rect x="{W * .5}" y="{box_h * .3}" width="{W * .12}" height="{box_h * .38}" rx="{px(3)}" fill="#0A0F1A"/>',
            f'<circle cx="{W * .56}" cy="{box_h * .49}" r="{box_h * .12}" fill="none" stroke="{AMBER}" stroke-width="{box_h * .04}"/>',
            f'<circle cx="{W * .72}" cy="{box_h * .49}" r="{box_h * .07}" fill="{TEAL}" filter="url(#glow)"/>',
            f'<rect x="{W * .8}" y="{box_h * .3}" width="{W * .12}" height="{box_h * .38}" rx="{px(2)}" fill="#0A0F1A" stroke="#4A5A76" stroke-width="{px(1)}"/>',
        ]
        for i in range(n):
            f.append(uc_pack_front(W, pack_h, px, y=box_h + pack_h * i, label=False))
        out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        return "".join(out)

    return render(build, b.bbox())


def uc_container(W, D, H):
    b = Box(W, D, H)

    def build(px):
        out = [box_faces(b, px, front="#E9EDF3", side="#B9C2D0", top="#F6F8FB")]
        f = []
        # corrugation
        for i in range(60):
            x = W * (i + .5) / 60
            f.append(f'<rect x="{x}" y="0" width="{W * .006}" height="{H}" fill="#C9D1DC"/>')
        # door pairs
        for d in range(4):
            x0 = W * (.08 + d * .225)
            f.append(f'<rect x="{x0}" y="{H * .1}" width="{W * .19}" height="{H * .8}" fill="#E1E6EE" stroke="#9AA6B8" stroke-width="{px(1.2)}"/>')
            f.append(f'<line x1="{x0 + W * .095}" y1="{H * .1}" x2="{x0 + W * .095}" y2="{H * .9}" stroke="#9AA6B8" stroke-width="{px(1.2)}"/>')
            for k in (.03, .07, .12, .16):
                f.append(f'<rect x="{x0 + W * k}" y="{H * .12}" width="{W * .004}" height="{H * .76}" fill="#8995A9"/>')
        # brand band
        f += [
            f'<rect x="0" y="{H * .02}" width="{W}" height="{H * .06}" fill="#0B1220"/>',
            f'<rect x="0" y="{H * .08}" width="{W}" height="{H * .012}" fill="url(#gTeal)"/>',
            uc_wordmark(W * .03, H * .05, W * .18),
            f'<path d="M{W * .93} {H * .03} l{W * .012} {H * .04} h-{W * .024} Z" fill="{AMBER}"/>',
            f'<rect x="0" y="{H * .955}" width="{W}" height="{H * .045}" fill="#1A2436"/>',
        ]
        out.append(f'<g transform="{b.front_tf}">{"".join(f)}</g>')
        s = [f'<rect x="0" y="{H * .955}" width="{D}" height="{H * .045}" fill="#121A29"/>',
             f'<rect x="0" y="{H * .02}" width="{D}" height="{H * .06}" fill="#0B1220"/>']
        for i in range(2):
            s.append(f'<rect x="{D * (.12 + i * .45)}" y="{H * .2}" width="{D * .3}" height="{H * .3}" rx="{px(3)}" fill="#8995A9"/>')
            s.append(f'<circle cx="{D * (.27 + i * .45)}" cy="{H * .35}" r="{H * .11}" fill="#5A6578"/>')
        s.append(f'<rect x="{D * .3}" y="{H * .62}" width="{D * .4}" height="{H * .22}" rx="{px(3)}" fill="#AAB4C3"/>')
        out.append(f'<g transform="{b.side_tf}">{"".join(s)}</g>')
        t = [f'<rect x="{W * .02}" y="{D * .05}" width="{W * .96}" height="{D * .9}" fill="none" stroke="#C9D1DC" stroke-width="{px(1)}"/>']
        out.append(f'<g transform="{b.top_tf}">{"".join(t)}</g>')
        return "".join(out)

    return render(build, b.bbox())


PRODUCTS = {
    "ultracap-pack": lambda: uc_pack(710, 1000, 200),
    "ultracap-cluster": lambda: uc_cluster(710, 1000, 200, 4, 240),
    "ultracap-container": lambda: uc_container(6058, 2438, 2896),
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
