# mdsite

A small static site generator. Turns a folder of Markdown files into HTML pages and an index page.
Standard library only, no install step.

Supported Markdown: `#` headings, paragraphs, `- ` lists, `` `code` ``, `**bold**`, `*italic*`.
Links and images are not supported yet.

Build a site: `python3 -m sitegen.build <source-dir> <output-dir>`

Run the tests: `python3 -m unittest -q tests.test_build tests.test_fixes tests.test_markdown`
