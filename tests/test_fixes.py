import tempfile
import unittest
from pathlib import Path

from sitegen.build import build, page_title
from sitegen.markdown import convert


class TestMarkdownFixes(unittest.TestCase):
    def test_lone_asterisks_stay_literal(self):
        self.assertEqual(convert("2 * 3 * 4"), "<p>2 * 3 * 4</p>\n")

    def test_unmatched_backtick_stays_literal(self):
        self.assertEqual(convert("a ` b **c**"), "<p>a ` b <strong>c</strong></p>\n")


class TestBuildFixes(unittest.TestCase):
    def test_index_link_attribute_is_escaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            src.mkdir()
            (src / 'a" onmouseover="alert(1).md').write_text("# Hi\n", encoding="utf-8")
            build(src, Path(tmp) / "out")
            index = (Path(tmp) / "out" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn('" onmouseover="', index)
            self.assertIn("&quot;", index)

    def test_byte_order_mark_does_not_hide_the_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            src.mkdir()
            (src / "bom.md").write_bytes("﻿# Real Title\n".encode("utf-8"))
            build(src, Path(tmp) / "out")
            page = (Path(tmp) / "out" / "bom.html").read_text(encoding="utf-8")
            self.assertIn("<title>Real Title</title>", page)
            self.assertIn("<h1>Real Title</h1>", page)

    def test_title_has_no_markdown_marks(self):
        self.assertEqual(page_title("# Use **bold** and `code`", "x"), "Use bold and code")


if __name__ == "__main__":
    unittest.main()
