#!/usr/bin/env -S uv run --script
"""Generate the repository's game catalog from top-level game.json files."""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "index.html"
GITHUB_URL = "https://github.com/rdslw/gry"
REQUIRED_FIELDS = {
    "title": str,
    "description": str,
    "age": str,
    "status": str,
    "created": str,
    "updated": str,
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_games() -> list[dict[str, object]]:
    games: list[dict[str, object]] = []
    for metadata_path in sorted(ROOT.glob("*/game.json")):
        game_dir = metadata_path.parent
        if not (game_dir / "index.html").is_file():
            fail(f"{game_dir.name}: game.json requires a sibling index.html")

        try:
            data = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            fail(f"{metadata_path.relative_to(ROOT)}: invalid JSON: {error}")

        if not isinstance(data, dict):
            fail(f"{metadata_path.relative_to(ROOT)}: expected a JSON object")

        for field, expected_type in REQUIRED_FIELDS.items():
            value = data.get(field)
            if not isinstance(value, expected_type) or not value.strip():
                fail(f"{metadata_path.relative_to(ROOT)}: {field!r} must be a non-empty string")

        if data["status"] not in {"draft", "published"}:
            fail(f"{metadata_path.relative_to(ROOT)}: status must be 'draft' or 'published'")

        for field in ("created", "updated"):
            try:
                date.fromisoformat(data[field])
            except ValueError:
                fail(f"{metadata_path.relative_to(ROOT)}: {field!r} must use YYYY-MM-DD")

        featured = data.get("featured", False)
        if not isinstance(featured, bool):
            fail(f"{metadata_path.relative_to(ROOT)}: 'featured' must be a boolean")

        thread = data.get("thread")
        if thread is not None and (not isinstance(thread, str) or not thread.startswith("https://ampcode.com/threads/")):
            fail(f"{metadata_path.relative_to(ROOT)}: 'thread' must be an Amp thread URL")

        if data["status"] == "published":
            games.append({**data, "slug": game_dir.name, "featured": featured})

    games.sort(key=lambda game: str(game["title"]).casefold())
    games.sort(key=lambda game: (bool(game["featured"]), str(game["updated"])), reverse=True)
    return games


def render_card(game: dict[str, object]) -> str:
    slug = html.escape(str(game["slug"]), quote=True)
    title = html.escape(str(game["title"]))
    description = html.escape(str(game["description"]))
    age = html.escape(str(game["age"]))
    created = html.escape(str(game["created"]))
    updated = html.escape(str(game["updated"]))
    thread = game.get("thread")
    thread_link = (
        f'<a href="{html.escape(str(thread), quote=True)}">Wątek Amp</a>' if thread else ""
    )
    separator = " · " if thread_link else ""
    return f"""      <article class="game-card">
        <div class="game-meta"><span>{age}</span><span>Aktualizacja: {updated}</span></div>
        <h2>{title}</h2>
        <p>{description}</p>
        <div class="game-actions">
          <a class="play" href="./{slug}/">Graj</a>
          <span><a href="{GITHUB_URL}/tree/main/{slug}">Kod</a> · <a href="{GITHUB_URL}/commits/main/{slug}">Historia</a>{separator}{thread_link}</span>
        </div>
        <small>Dodano: {created}</small>
      </article>"""


def render(games: list[dict[str, object]]) -> str:
    cards = "\n".join(render_card(game) for game in games)
    if not cards:
        cards = '      <p class="empty">Pierwsze gry pojawią się wkrótce.</p>'
    return f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Proste gry przeglądarkowe tworzone z pomocą Amp.">
  <title>Gry</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, sans-serif; background: #f4f7fb; color: #172033; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; }}
    header, main, footer {{ width: min(68rem, calc(100% - 2rem)); margin-inline: auto; }}
    header {{ padding: 3rem 0 1.5rem; }}
    h1 {{ margin: 0 0 .5rem; font-size: clamp(2rem, 8vw, 3.5rem); }}
    header p {{ margin: 0; color: #526079; }}
    .games {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr)); gap: 1rem; padding: 1rem 0 3rem; }}
    .game-card {{ display: flex; flex-direction: column; gap: .8rem; min-height: 16rem; padding: 1.25rem; border: 1px solid #dce3ee; border-radius: 1rem; background: white; box-shadow: 0 .3rem 1.2rem #1d2b4a12; }}
    .game-card h2, .game-card p {{ margin: 0; }}
    .game-card p {{ line-height: 1.55; color: #42506a; }}
    .game-meta, .game-actions {{ display: flex; justify-content: space-between; align-items: center; gap: .75rem; flex-wrap: wrap; }}
    .game-meta, small {{ color: #68758c; font-size: .85rem; }}
    .game-actions {{ margin-top: auto; }}
    a {{ color: #2457c5; }}
    .play {{ display: inline-block; padding: .65rem 1rem; border-radius: .7rem; background: #2457c5; color: white; font-weight: 700; text-decoration: none; }}
    .play:focus-visible, .play:hover {{ background: #173e94; }}
    .empty {{ padding: 2rem; border-radius: 1rem; background: white; text-align: center; color: #526079; }}
    footer {{ padding: 0 0 2rem; color: #68758c; }}
  </style>
</head>
<body>
  <header>
    <h1>Gry</h1>
    <p>Proste gry przeglądarkowe tworzone z pomocą Amp.</p>
  </header>
  <main class="games">
{cards}
  </main>
  <footer><a href="{GITHUB_URL}">Kod źródłowy na GitHubie</a></footer>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if index.html is stale")
    args = parser.parse_args()

    try:
        generated = render(load_games())
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            print("index.html is stale; run: uv run python scripts/build-index.py", file=sys.stderr)
            return 1
        print("index.html is up to date")
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
