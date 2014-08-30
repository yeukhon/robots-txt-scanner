import os
import unittest
from robots_scanner import parser

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROBOTS_DIR = os.path.join(TEST_DIR, 'robots')

class TestParserTree(unittest.TestCase):
    def get_text(self, fname):
        with open(os.path.join(ROBOTS_DIR, fname), 'r') as f:
            text = f.read()
        return text

    def setUp(self):
        self.robot = parser.Robotstxt()

    def test_basic(self):
        """Should find * as user-agent and return disallow on /"""
        text = self.get_text("basic.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"*": {"disallow": ["/"]}}
        )

    def test_basic_stacked_ua(self):
        """Should find Google and Yahoo and return disallow on /"""
        text = self.get_text("basic-stacked-ua.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"Google": {"disallow": ["/"]},
             "Yahoo": {"disallow": ["/"]}
            }
        )

    def test_basic_comment_at_top(self):
        """Should see * and disallow on / and comment is not in the tree."""
        text = self.get_text("basic-comment-at-top.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"*": {"disallow": ["/"]}}
        )

    def test_basic_comment_multiple_ua_separated(self):
        """Should see *, Google and Yahoo with its own rule."""
        text = self.get_text("basic-multiple-ua.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"*": {"disallow": ["/all"]},
             "Google": {"disallow": ["/google-only/"]},
             "Yahoo": {"disallow": ["/yahoo-only"]}}
        )

    def test_inline_comment(self):
        """Should still see Google even though inline is applied."""
        text = self.get_text("basic-inline-comment.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"*": {"disallow": ["/all"]},
             "Google": {"disallow": ["/google-only/"]}}
        )

    def test_disallow_and_allow(self):
        """Should be able to read disallow and allow."""
        text = self.get_text("basic-disallow-allow.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"*": {"disallow": ["/all"],
                   "allow": ["/all-allow"]},
             "Google": {"disallow": ["/google-only/"],
                        "allow": ["/google-okay", "/google-okay2"]}}
        )

    def test_comment_between_every_where(self):
        """Should still see * and Google with comments everywhere."""
        text = self.get_text("basic-comments-everywhere.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"*": {"disallow": ["/all"]},
             "Google": {"disallow": ["/google-only"]}}
        )

    # Start testing extensions (built-in)
    def test_sitemap(self):
        """Should see * and Google accepts Sitemap."""
        text = self.get_text("extended-sitemap.txt")
        self.robot.parse(text)
        self.assertEqual(self.robot._tree,
            {"*": {"sitemap": ["http://example.org/sitemap.xml"]},
             "Google": {"sitemap":
                            ["http://example.org/google/sitemap.xml.gz"]}}
        )
