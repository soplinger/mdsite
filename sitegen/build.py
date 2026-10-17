"""Build a folder of Markdown files into HTML pages with an index. Standard library only."""

import html
import re
import sys
from pathlib import Path

from sitegen.markdown import convert

TEMPLATE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
{body}
</body>
</html>
"""


def page_title(md: str, fallback: str) -> str:
    """Use the first top-level heading as the title, or the file name if there is none."""
    for line in md.splitlines():
        match = re.match(r"^#\s+(.*)$", line.strip())
        if match:
            # Titles are plain text: drop backticks and emphasis marks.
            return re.sub(r"[`*]", "", match.group(1)).strip()
    return fallback


def build(src: Path, out: Path) -> int:
    """Build every .md file in src into out, plus index.html. Return the page count."""
    if (src / "index.md").exists():
        raise ValueError("index.md is reserved: the index page is generated")
    out.mkdir(parents=True, exist_ok=True)
    pages = []
    for md_file in sorted(src.glob("*.md")):
        # utf-8-sig drops a byte-order mark, which would otherwise hide the first heading.
        text = md_file.read_text(encoding="utf-8-sig")
        title = page_title(text, md_file.stem)
        name = md_file.stem + ".html"
        page = TEMPLATE.format(title=html.escape(title), body=convert(text))
        (out / name).write_text(page, encoding="utf-8")
        pages.append((title, name))
    items = "\n".join(
        f'<li><a href="{html.escape(name, quote=True)}">{html.escape(title)}</a></li>'
        for title, name in pages
    )
    index_body = f"<h1>Index</h1>\n<ul>\n{items}\n</ul>"
    (out / "index.html").write_text(
        TEMPLATE.format(title="Index", body=index_body), encoding="utf-8"
    )
    return len(pages)


def main(argv: list) -> int:
    if len(argv) != 3:
        print("usage: python3 -m sitegen.build <source-dir> <output-dir>", file=sys.stderr)
        return 2
    count = build(Path(argv[1]), Path(argv[2]))
    print(f"built {count} page(s) plus index")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
