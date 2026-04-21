"""Render OG image, favicon, and demo graphic for endpulse.

Produces:
  docs/og-image.png          1200x630  social share card
  docs/demo.png              1600x900  README hero graphic
  docs/favicon-32.png        32x32     tab icon
  docs/favicon-16.png        16x16     tab icon
  docs/favicon.ico           multi     legacy ICO
  docs/apple-touch-icon.png  180x180   iOS bookmark
  docs/icon-192.png          192x192   PWA / Android
  docs/icon-512.png          512x512   PWA / high-DPI

Run from repo root:
  python scripts/render_og.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------- palette (GitHub dark) ----------
BG = (13, 17, 23)           # #0d1117
SURFACE = (22, 27, 34)      # #161b22
BORDER = (48, 54, 61)       # #30363d
TEXT = (230, 237, 243)      # #e6edf3
DIM = (139, 148, 158)       # #8b949e
ACCENT = (88, 166, 255)     # #58a6ff (brand blue)
GREEN = (63, 185, 80)       # #3fb950
YELLOW = (210, 153, 34)     # #d29922
RED = (248, 81, 73)         # #f85149
CYAN = (121, 192, 255)      # #79c0ff

FONT_SANS = "C:/Windows/Fonts/arial.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"
FONT_MONO_BOLD = "C:/Windows/Fonts/consolab.ttf"


def f(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill=None,
    outline=None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def pulse_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color) -> None:
    """Stylized heartbeat / pulse line — square viewBox centered on (cx, cy).

    Avoids any alphabet characters per design constraint.
    """
    s = size
    x0 = cx - s // 2
    y0 = cy
    # heartbeat polyline: flat -> up spike -> down spike -> flat
    pts = [
        (x0,           y0),
        (x0 + s * 0.25, y0),
        (x0 + s * 0.38, y0 - s * 0.35),
        (x0 + s * 0.50, y0 + s * 0.35),
        (x0 + s * 0.62, y0 - s * 0.45),
        (x0 + s * 0.75, y0),
        (x0 + s,        y0),
    ]
    draw.line(pts, fill=color, width=max(3, s // 18), joint="curve")
    # accent dot at peak
    peak_x = int(x0 + s * 0.62)
    peak_y = int(y0 - s * 0.45)
    r = max(3, s // 22)
    draw.ellipse((peak_x - r, peak_y - r, peak_x + r, peak_y + r), fill=color)


def traffic_lights(draw: ImageDraw.ImageDraw, x: int, y: int, r: int = 7) -> None:
    for i, c in enumerate((RED, YELLOW, GREEN)):
        cx = x + i * (r * 2 + 6)
        draw.ellipse((cx, y, cx + r * 2, y + r * 2), fill=c)


# ---------- OG image (1200 x 630) ----------

def render_og() -> Image.Image:
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    # soft brand strip top
    d.rectangle((0, 0, W, 6), fill=ACCENT)

    pad = 56
    term_w, term_h = 460, 320
    term_x = W - term_w - pad
    term_y = (H - term_h) // 2 + 10
    # text column width (kept strictly < term_x - pad to avoid overlap)
    text_right = term_x - 32

    # wordmark row
    pulse_icon(d, cx=pad + 24, cy=pad + 22, size=48, color=ACCENT)
    wm_font = f(FONT_SANS_BOLD, 26)
    d.text((pad + 60, pad + 6), "endpulse", fill=TEXT, font=wm_font)

    # headline — sized to fit inside text_right
    hl_font = f(FONT_SANS_BOLD, 52)

    def fits(s: str, font) -> int:
        b = d.textbbox((0, 0), s, font=font)
        return b[2] - b[0]

    hl_lines = [
        ("Multi-endpoint",        TEXT),
        ("API health checks",     TEXT),
        ("in one CLI command.",   ACCENT),
    ]
    # shrink until every line fits
    size = 52
    while size >= 36:
        hl_font = f(FONT_SANS_BOLD, size)
        if all(pad + fits(s, hl_font) <= text_right for s, _ in hl_lines):
            break
        size -= 2

    hl_y = pad + 88
    line_h = int(size * 1.18)
    for i, (text, color) in enumerate(hl_lines):
        d.text((pad, hl_y + i * line_h), text, fill=color, font=hl_font)

    # sub line — short enough to fit left column
    sub_font = f(FONT_SANS, 22)
    sub_text = "SSL monitoring · assertions · CI exit codes"
    sub_y = hl_y + len(hl_lines) * line_h + 20
    if pad + fits(sub_text, sub_font) > text_right:
        sub_text = "SSL · assertions · CI exit codes"
    d.text((pad, sub_y), sub_text, fill=DIM, font=sub_font)

    # CTA pill — "$ pip install endpulse"
    cta_font = f(FONT_MONO_BOLD, 26)
    cta_text = "$  pip install endpulse"
    bbox = d.textbbox((0, 0), cta_text, font=cta_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cta_px, cta_py = 24, 14
    cta_w, cta_h = tw + cta_px * 2, th + cta_py * 2
    cta_x, cta_y = pad, sub_y + 48
    rounded_rect(d, (cta_x, cta_y, cta_x + cta_w, cta_y + cta_h),
                 radius=10, fill=SURFACE, outline=BORDER, width=2)
    d.text((cta_x + cta_px, cta_y + cta_py - 2), cta_text, fill=GREEN, font=cta_font)

    # --- right column: mini terminal preview ---
    rounded_rect(d, (term_x, term_y, term_x + term_w, term_y + term_h),
                 radius=14, fill=SURFACE, outline=BORDER, width=2)
    # header bar
    hdr_h = 34
    rounded_rect(d, (term_x, term_y, term_x + term_w, term_y + hdr_h),
                 radius=14, fill=BORDER)
    # flatten bottom of header
    d.rectangle((term_x, term_y + hdr_h - 14, term_x + term_w, term_y + hdr_h), fill=BORDER)
    traffic_lights(d, term_x + 14, term_y + 10, r=6)

    mono_sm = f(FONT_MONO, 17)
    mono_sm_b = f(FONT_MONO_BOLD, 17)
    mono_title = f(FONT_MONO, 13)
    d.text((term_x + 64, term_y + 9), "endpulse --ssl", fill=DIM, font=mono_title)

    # body — mini output
    bx = term_x + 22
    by = term_y + hdr_h + 18
    line = 26

    d.text((bx, by), "$ endpulse api1 api2 api3 --ssl", fill=TEXT, font=mono_sm)
    by += line + 10
    d.text((bx, by), "Endpoint Health Report", fill=TEXT, font=mono_sm_b)
    by += line + 6

    # mini rows
    def row(url: str, status_color, status: str, code: str, ms: str, ssl: str) -> None:
        nonlocal by
        d.text((bx, by), url, fill=CYAN, font=mono_sm)
        d.text((bx + 200, by), status, fill=status_color, font=mono_sm_b)
        d.text((bx + 270, by), code, fill=TEXT, font=mono_sm)
        d.text((bx + 320, by), ms, fill=TEXT, font=mono_sm)
        d.text((bx + 400, by), ssl, fill=DIM, font=mono_sm)
        by += line

    row("api.ex.com/health", GREEN,  " UP  ", "200", " 42ms", "89d")
    row("api.ex.com/v2    ", GREEN,  " UP  ", "200", "118ms", "89d")
    row("api.ex.com/slow  ", YELLOW, "SLOW ", "200", "1.8s ", "89d")

    by += 10
    d.text((bx, by), "2/3 up  ·  avg 667ms  ·  1 slow", fill=DIM, font=mono_sm)

    # footer right
    foot_font = f(FONT_SANS, 18)
    d.text((pad, H - pad - 18),
           "pypi · github.com/kimhinton/endpulse · MIT",
           fill=DIM, font=foot_font)

    return im


# ---------- README demo (1600 x 900) ----------

def render_demo() -> Image.Image:
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    pad = 80

    # terminal frame
    tx, ty = pad, pad
    tw, th = W - pad * 2, H - pad * 2
    rounded_rect(d, (tx, ty, tx + tw, ty + th),
                 radius=18, fill=SURFACE, outline=BORDER, width=2)
    hdr_h = 46
    rounded_rect(d, (tx, ty, tx + tw, ty + hdr_h),
                 radius=18, fill=BORDER)
    d.rectangle((tx, ty + hdr_h - 18, tx + tw, ty + hdr_h), fill=BORDER)
    traffic_lights(d, tx + 20, ty + 14, r=9)
    title_font = f(FONT_MONO, 18)
    d.text((tx + 96, ty + 13), "endpulse --ssl  ·  watch mode", fill=DIM, font=title_font)

    mono = f(FONT_MONO, 22)
    mono_b = f(FONT_MONO_BOLD, 22)
    big = f(FONT_MONO_BOLD, 26)

    bx = tx + 44
    by = ty + hdr_h + 34
    line = 34

    d.text((bx, by), "$ endpulse \\", fill=TEXT, font=mono); by += line
    d.text((bx + 40, by), "https://api.example.com/health \\", fill=CYAN, font=mono); by += line
    d.text((bx + 40, by), "https://api.example.com/v2/status \\", fill=CYAN, font=mono); by += line
    d.text((bx + 40, by), "https://api.example.com/slow \\", fill=CYAN, font=mono); by += line
    d.text((bx + 40, by), "--ssl --fail -a \"body_contains:ok\"", fill=TEXT, font=mono); by += line * 2

    d.text((bx, by), "Endpoint Health Report", fill=TEXT, font=big); by += line + 6

    # nicer box-drawn table
    sep = "─" * 84
    d.text((bx, by), sep, fill=BORDER, font=mono); by += line
    hdr = "URL                                   Status   Code   Time(ms)   SSL"
    d.text((bx, by), hdr, fill=DIM, font=mono); by += line
    d.text((bx, by), sep, fill=BORDER, font=mono); by += line

    def row(url: str, status_color, status: str, code: str, ms: str, ssl: str) -> None:
        nonlocal by
        d.text((bx, by), f"{url:<38}", fill=CYAN, font=mono)
        d.text((bx + 540, by), f"{status:^7}", fill=status_color, font=mono_b)
        d.text((bx + 640, by), f"{code:^5}", fill=TEXT, font=mono)
        d.text((bx + 740, by), f"{ms:>8}", fill=TEXT, font=mono)
        d.text((bx + 890, by), f"{ssl:>5}", fill=DIM, font=mono)
        by += line

    row("api.example.com/health",  GREEN,  " UP  ", "200", "   42.5", "89d")
    row("api.example.com/v2/status", GREEN, " UP  ", "200", "  118.3", "89d")
    row("api.example.com/slow",    YELLOW, "SLOW ", "200", " 1842.1", "89d")
    d.text((bx, by), sep, fill=BORDER, font=mono); by += line + 20

    summary = "2/3 endpoints up   ·   avg response: 667.6ms   ·   1 slow"
    d.text((bx, by), summary, fill=TEXT, font=mono_b); by += line
    d.text((bx, by), "assertion passed: body_contains:ok   ·   exit 0",
           fill=GREEN, font=mono)

    return im


# ---------- favicon / app icons ----------

def render_icon(size: int) -> Image.Image:
    im = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(im)
    # accent ring
    pad = max(2, size // 12)
    d.rounded_rectangle((pad, pad, size - pad, size - pad),
                        radius=size // 5, fill=SURFACE,
                        outline=ACCENT, width=max(2, size // 24))
    # centered pulse mark
    pulse_icon(d, cx=size // 2, cy=size // 2, size=int(size * 0.58), color=ACCENT)
    return im


# ---------- main ----------

def main() -> None:
    root = Path(__file__).resolve().parent.parent
    docs = root / "docs"
    docs.mkdir(exist_ok=True)

    og = render_og()
    og.save(docs / "og-image.png", optimize=True)
    print(f"wrote {docs / 'og-image.png'}  {og.size}")

    demo = render_demo()
    demo.save(docs / "demo.png", optimize=True)
    print(f"wrote {docs / 'demo.png'}  {demo.size}")

    for size, name in [
        (16,  "favicon-16.png"),
        (32,  "favicon-32.png"),
        (180, "apple-touch-icon.png"),
        (192, "icon-192.png"),
        (512, "icon-512.png"),
    ]:
        img = render_icon(size)
        img.save(docs / name, optimize=True)
        print(f"wrote {docs / name}  {img.size}")

    # multi-res ICO (16, 32, 48)
    ico_base = render_icon(256)
    ico_base.save(docs / "favicon.ico",
                  format="ICO",
                  sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"wrote {docs / 'favicon.ico'}")


if __name__ == "__main__":
    main()
