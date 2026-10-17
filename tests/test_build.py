import tempfile
import unittest
from pathlib import Path

from sitegen.build import build, page_title


class TestPageTitle(unittest.TestCase):
    def test_uses_first_heading(self):
        self.assertEqual(page_title("text\n# Real Title\n# Second", "fallback"), "Real Title")

    def test_falls_back_to_file_name(self):
        self.assertEqual(page_title("no heading here", "about"), "about")


class TestBuild(unittest.TestCase):
    def test_builds_pages_and_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            out = Path(tmp) / "out"
            src.mkdir()
            (src / "about.md").write_text("# About Me\n\nHi.\n", encoding="utf-8")
            (src / "notes.md").write_text("plain notes\n", encoding="utf-8")
            count = build(src, out)
            self.assertEqual(count, 2)
            about = (out / "about.html").read_text(encoding="utf-8")
            self.assertIn("<title>About Me</title>", about)
            self.assertIn("<p>Hi.</p>", about)
            index = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn('<a href="about.html">About Me</a>', index)
            self.assertIn('<a href="notes.html">notes</a>', index)

    def test_reserved_index_md_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            (src / "index.md").write_text("# Nope\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                build(src, Path(tmp) / "out")


if __name__ == "__main__":
    unittest.main()
