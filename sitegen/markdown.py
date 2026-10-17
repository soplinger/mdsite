"""Convert a small, fixed subset of Markdown to HTML. Standard library only.

Supported: # headings, paragraphs, "- " lists, `code`, **bold**, *italic*.
Everything is HTML-escaped first, so page text cannot inject markup.
"""

import html
import re


def _inline(text: str) -> str:
    """Render inline markup. Code spans are split out first so their text is left alone."""
    # An unmatched backtick means no code spans at all, so the text stays literal.
    parts = text.split("`") if text.count("`") % 2 == 0 else [text]
    out = []
    for i, part in enumerate(parts):
        escaped = html.escape(part, quote=False)
        if i % 2 == 1:
            out.append(f"<code>{escaped}</code>")
        else:
            escaped = re.sub(r"\*\*(?!\s)(.+?)(?<!\s)\*\*", r"<strong>\1</strong>", escaped)
            # A lone * followed or preceded by a space is literal, so "2 * 3 * 4" stays as written.
            escaped = re.sub(r"\*(?!\s)(.+?)(?<!\s)\*", r"<em>\1</em>", escaped)
            out.append(escaped)
    return "".join(out)


def convert(md: str) -> str:
    """Return the HTML body for a Markdown document."""
    blocks = []
    para = []
    items = []

    def flush_para():
        if para:
            blocks.append("<p>" + _inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_list():
        if items:
            rendered = "\n".join(f"<li>{_inline(item)}</li>" for item in items)
            blocks.append("<ul>\n" + rendered + "\n</ul>")
            items.clear()

    for line in md.splitlines():
        stripped = line.strip()
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if not stripped:
            flush_para()
            flush_list()
        elif heading:
            flush_para()
            flush_list()
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
        elif stripped.startswith("- "):
            flush_para()
            items.append(stripped[2:])
        else:
            flush_list()
            para.append(stripped)

    flush_para()
    flush_list()
    return "\n".join(blocks) + "\n"
