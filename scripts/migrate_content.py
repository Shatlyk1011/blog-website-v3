#!/usr/bin/env python3
"""Convert the source Next.js MDX posts into Taiga/Hugo page bundles."""

from __future__ import annotations

import ast
import json
import math
import re
import shutil
import sys
from pathlib import Path


DESCRIPTION_OVERRIDES = {
    "javascript-fundamentals-for-frontend-development": (
        "A practical introduction to the JavaScript fundamentals every frontend developer should understand."
    ),
    "system-design-interview-part-1": (
        "A practical introduction to system design interviews, including architecture, scaling, reliability, latency, and common trade-offs."
    ),
    "system-design-interview-part-2": (
        "A practical guide to networking for system design interviews, covering TCP, UDP, DNS, HTTP, and SSL/TLS."
    ),
    "web-storage": (
        "A comparison of cookies, Local Storage, Session Storage, and IndexedDB, with guidance on when to use each browser storage option."
    ),
}


TAG_OVERRIDES = {
    "debounce-and-throttle": ["javascript", "performance", "frontend-development"],
    "fundamental-introduction-to-web-development": ["web-development", "browser"],
    "gradient-transitions": ["css", "frontend-development"],
    "image-optimization": ["performance", "images", "frontend-development"],
    "javascript-fundamentals-for-frontend-development": ["javascript", "frontend-development"],
    "my-best-resources": ["resources", "frontend-development", "artificial-intelligence"],
    "reusable-jsx-button": ["react", "javascript", "frontend-development"],
    "tips-for-better-performance": ["performance", "frontend-development"],
    "video-optimization": ["performance", "video", "frontend-development"],
    "web-design-rules-and-guidelines": ["web-design", "ui-ux"],
    "web-storage": ["browser", "web-development"],
}


def frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", frontmatter)
    if not match:
        raise ValueError(f"Missing front matter field: {key}")
    return match.group(1).strip().strip("'").strip('"')


def image_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*['\"]([^'\"]+)['\"]", frontmatter)
    return match.group(1) if match else None


def reading_minutes(body: str) -> int:
    without_code = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    without_html = re.sub(r"<[^>]+>", " ", without_code)
    words = re.findall(r"\b[\w’'-]+\b", without_html)
    return max(1, math.ceil(len(words) / 200))


def migrate(source: Path, destination: Path) -> None:
    posts_root = source / "posts"
    output_root = destination / "content" / "articles"
    output_root.mkdir(parents=True, exist_ok=True)

    for post_path in sorted(posts_root.glob("*/*.mdx")):
        text = post_path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"Invalid MDX front matter: {post_path}")

        frontmatter, body = match.groups()
        slug = post_path.stem
        original_section = post_path.parent.name
        title = frontmatter_value(frontmatter, "title")
        date = frontmatter_value(frontmatter, "publishedTime")
        description = DESCRIPTION_OVERRIDES.get(
            slug, frontmatter_value(frontmatter, "description")
        )
        tags = TAG_OVERRIDES.get(
            slug, ast.literal_eval(frontmatter_value(frontmatter, "tags"))
        )
        source_image = image_value(frontmatter, "src")
        placeholder_image = image_value(frontmatter, "placeholder")

        body = re.sub(
            r"/(?:blog|dev|thoughts?)/([a-z0-9-]+)/?",
            r"/articles/\1/",
            body,
        )

        bundle = output_root / slug
        bundle.mkdir(parents=True, exist_ok=True)

        cover_name = None
        if source_image:
            selected_image = (
                placeholder_image
                if Path(source_image).suffix.lower() == ".avif" and placeholder_image
                else source_image
            )
            image_path = source / "public" / "static" / "images" / Path(selected_image).name
            if image_path.exists():
                cover_name = f"cover{image_path.suffix.lower()}"
                shutil.copy2(image_path, bundle / cover_name)

        aliases = sorted({
            f"/blog/{slug}/",
            f"/dev/{slug}/",
            f"/thoughts/{slug}/",
            f"/{original_section}/{slug}/",
        })

        migrated_frontmatter = [
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"slug: {slug}",
            f"date: {json.dumps(date)}",
            f"description: {json.dumps(description, ensure_ascii=False)}",
            f"tags: {json.dumps(tags, ensure_ascii=False)}",
            f"mins: {reading_minutes(body)}",
            "aliases:",
            *[f"  - {alias}" for alias in aliases],
        ]
        if cover_name:
            migrated_frontmatter.append(f"cover: {cover_name}")
        migrated_frontmatter.extend(["---", ""])

        (bundle / "index.md").write_text(
            "\n".join(migrated_frontmatter) + body.lstrip(),
            encoding="utf-8",
        )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: migrate_content.py SOURCE_PROJECT DESTINATION_PROJECT")
    migrate(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
