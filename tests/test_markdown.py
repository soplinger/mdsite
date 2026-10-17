import unittest

from sitegen.markdown import convert


class TestConvert(unittest.TestCase):
    def test_heading_and_paragraph(self):
        self.assertEqual(convert("# Title\n\nHello there."), "<h1>Title</h1>\n<p>Hello there.</p>\n")

    def test_paragraph_lines_join_with_a_space(self):
        self.assertEqual(convert("one\ntwo"), "<p>one two</p>\n")

    def test_list_items(self):
        self.assertEqual(convert("- a\n- b"), "<ul>\n<li>a</li>\n<li>b</li>\n</ul>\n")

    def test_html_is_escaped(self):
        self.assertEqual(convert("<script>x</script>"), "<p>&lt;script&gt;x&lt;/script&gt;</p>\n")

    def test_bold_and_italic(self):
        self.assertEqual(convert("**b** and *i*"), "<p><strong>b</strong> and <em>i</em></p>\n")

    def test_code_span_is_not_formatted(self):
        self.assertEqual(convert("`**not bold**`"), "<p><code>**not bold**</code></p>\n")


if __name__ == "__main__":
    unittest.main()
