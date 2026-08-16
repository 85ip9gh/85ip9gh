"""Regenerates the profile's GitHub activity cards from live API data.

The cards used to be hand-made snapshots, which froze on the day they were
written: by 2026-08-15 the committed figures were 24 days old and the pull
request count read 3 against an actual 22. They are now rebuilt on a schedule
and committed only when a number actually moves.

Two design points are deliberate.

**Repository-owned SVG, not a third-party card service.** An external stats
image is rate limited at view time and renders as a broken image when the
service is busy, which is why those were dropped on 2026-07-23. Generating the
file here keeps the read path a plain static asset.

**One file per theme.** GitHub serves README images through its camo proxy,
where a `prefers-color-scheme` media query inside the SVG follows the reader's
operating system rather than their GitHub theme. The `<picture>` element in the
README is the documented way to switch, so each card is written twice.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

API = "https://api.github.com/graphql"
LOGIN = os.environ.get("STATS_LOGIN", "85ip9gh")
OUT_DIR = Path(__file__).resolve().parent.parent / "assets"
LANGUAGE_COUNT = 6

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { totalContributions }
      totalCommitContributions
      totalPullRequestContributions
    }
    repositories(privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    languageRepos: repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        languages(first: 20) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "card": "#161b22",
        "title": "#f0f6fc", "value": "#f0f6fc", "label": "#8b949e", "sub": "#8b949e",
        "track": "#21262d", "other": "#484f58",
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "card": "#f6f8fa",
        "title": "#1f2328", "value": "#1f2328", "label": "#59636e", "sub": "#59636e",
        "track": "#eaeef2", "other": "#afb8c1",
    },
}

FONT = "Segoe UI, Ubuntu, Helvetica, Arial, sans-serif"

# Motion is a fade and a short rise, once, on load. Anything looping would sit
# on the page moving forever, which is the failure mode of animated profile
# cards. Readers who ask for less motion get none.
MOTION = """
    @keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
    @keyframes sweep { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    .rise { animation: rise .5s cubic-bezier(.2,.7,.3,1) both; }
    .sweep { transform-origin: left center; animation: sweep .7s cubic-bezier(.2,.7,.3,1) both; }
    .grow { transform-origin: left center; animation: grow .8s cubic-bezier(.2,.7,.3,1) both; }
    @media (prefers-reduced-motion: reduce) {
      .rise, .sweep, .grow { animation: none; }
    }
"""


def fetch(token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    request = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{LOGIN}-profile-stats",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read())
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def languages(user: dict) -> list[dict]:
    totals: dict[str, dict] = {}
    for repo in user["languageRepos"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            entry = totals.setdefault(
                name, {"name": name, "color": edge["node"]["color"] or "#8b949e", "bytes": 0}
            )
            entry["bytes"] += edge["size"]
    ranked = sorted(totals.values(), key=lambda e: -e["bytes"])
    total = sum(e["bytes"] for e in totals.values()) or 1
    top = ranked[:LANGUAGE_COUNT]
    for entry in top:
        entry["share"] = entry["bytes"] / total * 100
    return top


def _e(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def stats_card(user: dict, theme: str, verified: str) -> str:
    c = THEMES[theme]
    contributions = user["contributionsCollection"]
    tiles = [
        ("Contributions", f"{contributions['contributionCalendar']['totalContributions']:,}", "#7c3aed"),
        ("Public repositories", f"{user['repositories']['totalCount']:,}", "#06b6d4"),
        ("Public commits", f"{contributions['totalCommitContributions']:,}", "#ec4899"),
        ("Pull requests", f"{contributions['totalPullRequestContributions']:,}", "#22c55e"),
    ]
    desc = (
        f"{tiles[0][1]} contributions, {tiles[1][1]} public repositories, "
        f"{tiles[2][1]} public commits, and {tiles[3][1]} pull requests "
        f"in the twelve months ending {verified}."
    )

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195"'
        ' role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">Pesanth's GitHub snapshot</title>",
        f'<desc id="desc">{_e(desc)}</desc>',
        f"<style>{MOTION}</style>",
        '<defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#7c3aed"/><stop offset="0.5" stop-color="#ec4899"/>'
        '<stop offset="1" stop-color="#06b6d4"/></linearGradient></defs>',
        f'<rect x="0.5" y="0.5" width="494" height="194" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        '<rect class="sweep" x="22" y="22" width="451" height="4" rx="2" fill="url(#accent)"/>',
        f'<g font-family="{FONT}">',
        f'<text class="rise" x="22" y="53" fill="{c["title"]}" font-size="18" font-weight="700">GitHub snapshot</text>',
        f'<text class="rise" style="animation-delay:.05s" x="22" y="72" fill="{c["sub"]}" font-size="11">'
        f"12 months ending {_e(verified)}</text>",
        "</g>",
    ]

    for i, (label, value, dot) in enumerate(tiles):
        col, row = i % 2, i // 2
        x = 22 + col * 231
        y = 88 + row * 48
        delay = 0.1 + i * 0.06
        parts += [
            f'<g class="rise" style="animation-delay:{delay:.2f}s" font-family="{FONT}">',
            f'<rect x="{x}" y="{y}" width="220" height="40" rx="8" fill="{c["card"]}" stroke="{c["border"]}"/>',
            f'<circle cx="{x + 16}" cy="{y + 20}" r="4" fill="{dot}"/>',
            f'<text x="{x + 30}" y="{y + 16}" fill="{c["label"]}" font-size="9" letter-spacing="0.8"'
            f'>{_e(label.upper())}</text>',
            f'<text x="{x + 30}" y="{y + 31}" fill="{c["value"]}" font-size="15" font-weight="700"'
            f' font-family="{FONT}">{_e(value)}</text>',
            "</g>",
        ]
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def languages_card(top: list[dict], theme: str, verified: str) -> str:
    c = THEMES[theme]
    shown = sum(e["share"] for e in top)
    desc = ", ".join(f"{e['name']} {e['share']:.1f} percent" for e in top)
    if 100 - shown > 0.5:
        desc += f", and {100 - shown:.1f} percent across other languages"
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195"'
        ' role="img" aria-labelledby="title desc">',
        "<title id=\"title\">Top public-repository languages</title>",
        f'<desc id="desc">{_e(desc)}. Measured by GitHub-reported bytes.</desc>',
        f"<style>{MOTION}</style>",
        f'<rect x="0.5" y="0.5" width="494" height="194" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        f'<g font-family="{FONT}">',
        f'<text class="rise" x="22" y="45" fill="{c["title"]}" font-size="16" font-weight="700">'
        "Top public-repository languages</text>",
        f'<text class="rise" style="animation-delay:.05s" x="22" y="63" fill="{c["sub"]}" font-size="11">'
        f"GitHub-reported language bytes, verified {_e(verified)}</text>",
        "</g>",
        f'<rect x="22" y="76" width="451" height="10" rx="5" fill="{c["track"]}"/>',
        '<g class="grow" style="transform-origin:22px 81px">',
    ]

    # One rounded track with flat segments laid over it. Rounding each segment
    # would leave visible notches between them at these widths.
    #
    # The bar is scaled by true share, not normalized across the six shown, and
    # everything outside the top six gets a neutral tail. Normalizing would draw
    # a full bar under labels that sum to 83 percent.
    offset = 22.0
    for entry in top:
        width = 451 * entry["share"] / 100
        parts.append(
            f'<rect x="{offset:.1f}" y="76" width="{width:.1f}" height="10" fill="{entry["color"]}"/>'
        )
        offset += width
    remainder = 473 - offset
    if remainder > 0.5:
        parts.append(
            f'<rect x="{offset:.1f}" y="76" width="{remainder:.1f}" height="10" fill="{c["other"]}"/>'
        )
    parts += [
        "</g>",
        f'<rect x="22" y="76" width="451" height="10" rx="5" fill="none" stroke="{c["bg"]}"'
        ' stroke-width="0" />',
        f'<g font-family="{FONT}">',
    ]

    for i, entry in enumerate(top):
        col, row = i % 2, i // 2
        x = 22 + col * 231
        y = 112 + row * 26
        delay = 0.15 + i * 0.05
        parts += [
            f'<g class="rise" style="animation-delay:{delay:.2f}s">',
            f'<circle cx="{x + 6}" cy="{y - 4}" r="5" fill="{entry["color"]}"/>',
            f'<text x="{x + 20}" y="{y}" fill="{c["value"]}" font-size="12">{_e(entry["name"])}</text>',
            f'<text x="{x + 210}" y="{y}" fill="{c["label"]}" font-size="12" text-anchor="end">'
            f'{entry["share"]:.1f}%</text>',
            "</g>",
        ]
    parts += ["</g>", "</svg>"]
    return "\n".join(parts) + "\n"


def main() -> int:
    token = os.environ.get("STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("set STATS_TOKEN or GITHUB_TOKEN", file=sys.stderr)
        return 2

    try:
        user = fetch(token)
    except urllib.error.HTTPError as exc:
        print(f"GitHub API returned {exc.code}: {exc.read()[:200]!r}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"GitHub API unreachable: {exc.reason}", file=sys.stderr)
        return 1

    verified = date.today().isoformat()
    top = languages(user)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = []
    for theme in THEMES:
        for name, svg in (
            (f"github-stats-{theme}.svg", stats_card(user, theme, verified)),
            (f"top-languages-{theme}.svg", languages_card(top, theme, verified)),
        ):
            path = OUT_DIR / name
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                path.write_text(svg, encoding="utf-8")
                written.append(name)

    contributions = user["contributionsCollection"]
    print(
        f"contributions {contributions['contributionCalendar']['totalContributions']:,}, "
        f"repositories {user['repositories']['totalCount']}, "
        f"commits {contributions['totalCommitContributions']}, "
        f"pull requests {contributions['totalPullRequestContributions']}"
    )
    print(f"languages: {', '.join(f'{e['name']} {e['share']:.1f}%' for e in top)}")
    print(f"changed: {', '.join(written) if written else 'nothing'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
