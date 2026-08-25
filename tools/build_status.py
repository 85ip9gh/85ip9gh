"""Regenerates the profile's live service-status card.

The card checks each self-hosted site over HTTP and records whether it
answered and how quickly. Everything on the list is public and served
through a Cloudflare Tunnel, so a plain GET from the Actions runner is the
same request any visitor makes.

Two design points match build_stats.py on purpose.

**Repository-owned SVG, not a third-party badge service.** Shields' endpoint
badges rate limit at view time and render as a broken image when the service
is busy. Writing the file here keeps the read path a plain static asset.

**One file per theme.** GitHub serves README images through its camo proxy,
where a prefers-color-scheme query inside the SVG follows the reader's OS
rather than their GitHub theme, so the README switches with a <picture> and
each card is written twice. There are no animations: GitHub renders an
img-embedded SVG in secure static mode, which freezes them at their first
frame, so the card is drawn in its final visible state.
"""
from __future__ import annotations

import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "assets"
TIMEOUT = 12

# label shown on the card, url that gets the request.
SITES = [
    ("pesanth.com", "https://pesanth.com"),
    ("carsale.pesanth.com", "https://carsale.pesanth.com"),
    ("cubestore.pesanth.com", "https://cubestore.pesanth.com"),
    ("papers.pesanth.com", "https://papers.pesanth.com"),
    ("sentinel.pesanth.com", "https://sentinel.pesanth.com"),
]

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "card": "#161b22",
        "title": "#f0f6fc", "value": "#f0f6fc", "sub": "#8b949e",
        "up": "#3fb950", "down": "#f85149",
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "card": "#f6f8fa",
        "title": "#1f2328", "value": "#1f2328", "sub": "#59636e",
        "up": "#1a7f37", "down": "#cf222e",
    },
}

FONT = "Segoe UI, Ubuntu, Helvetica, Arial, sans-serif"


def check(url: str) -> tuple[bool, int | None]:
    request = urllib.request.Request(
        url, method="GET", headers={"User-Agent": "85ip9gh-profile-status"}
    )
    start = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            response.read(1)
            ms = int((time.monotonic() - start) * 1000)
            return 200 <= response.status < 400, ms
    except urllib.error.HTTPError as exc:
        ms = int((time.monotonic() - start) * 1000)
        return 300 <= exc.code < 400, ms
    except (urllib.error.URLError, TimeoutError, OSError):
        return False, None


def _e(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def card(results: list[tuple[str, bool, int | None]], theme: str, verified: str) -> str:
    c = THEMES[theme]
    up = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    desc = "; ".join(
        f"{label} {'up' if ok else 'down'}" + (f" {ms} ms" if ok and ms is not None else "")
        for label, ok, ms in results
    )
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195"'
        ' role="img" aria-labelledby="title desc">',
        '<title id="title">Self-hosted service status</title>',
        f'<desc id="desc">{_e(desc)}. Checked {_e(verified)}.</desc>',
        '<defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#7c3aed"/><stop offset="0.5" stop-color="#ec4899"/>'
        '<stop offset="1" stop-color="#06b6d4"/></linearGradient></defs>',
        f'<rect x="0.5" y="0.5" width="494" height="194" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        '<rect x="22" y="22" width="451" height="4" rx="2" fill="url(#accent)"/>',
        f'<g font-family="{FONT}">',
        f'<text x="22" y="53" fill="{c["title"]}" font-size="18" font-weight="700">Service status</text>',
        f'<text x="473" y="53" fill="{c["sub"]}" font-size="12" text-anchor="end">{up}/{total} up</text>',
        f'<text x="22" y="72" fill="{c["sub"]}" font-size="11">Self-hosted sites, checked {_e(verified)}</text>',
        "</g>",
        f'<g font-family="{FONT}" font-size="12.5">',
    ]
    for i, (label, ok, ms) in enumerate(results):
        y = 98 + i * 20
        dot = c["up"] if ok else c["down"]
        right = f"{ms} ms" if ok and ms is not None else "unreachable"
        right_fill = c["sub"] if ok else c["down"]
        parts += [
            f'<circle cx="30" cy="{y - 4}" r="4" fill="{dot}"/>',
            f'<text x="44" y="{y}" fill="{c["value"]}">{_e(label)}</text>',
            f'<text x="473" y="{y}" fill="{right_fill}" text-anchor="end">{_e(right)}</text>',
        ]
    parts += ["</g>", "</svg>"]
    return "\n".join(parts) + "\n"


def main() -> int:
    results = [(label, *check(url)) for label, url in SITES]
    verified = date.today().isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = []
    for theme in THEMES:
        svg = card(results, theme, verified)
        path = OUT_DIR / f"status-{theme}.svg"
        if not path.exists() or path.read_text(encoding="utf-8") != svg:
            path.write_text(svg, encoding="utf-8")
            written.append(path.name)

    for label, ok, ms in results:
        state = f"up {ms} ms" if ok else "DOWN"
        print(f"  {label}: {state}")
    print(f"changed: {', '.join(written) if written else 'nothing'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
