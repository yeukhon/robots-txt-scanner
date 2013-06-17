import os
import unittest
from robots_scanner.scanner import scan, _name

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROBOTS_DIR = os.path.join(TEST_DIR, 'robots')

class TestRobotScanner(unittest.TestCase):
    def do_scan(self, fname):
        with open(os.path.join(ROBOTS_DIR, fname), 'r') as f:
            body = f.read()
        return scan(body)

    def test_disallow_first_raise_exception(self):
        with open(os.path.join(ROBOTS_DIR, 'disallow-first.txt'), 'r') as f:
            body = f.read()
        self.assertRaises(Exception, scan, body)

    def test_allow_first_raise_exception(self):
        with open(os.path.join(ROBOTS_DIR, 'allow-first.txt'), 'r') as f:
            body = f.read()
        self.assertRaises(Exception, scan, body)

    def test_sitemap(self):
        tokens = self.do_scan('robots-with-sitemap.txt')
        self.assertEqual(
                (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\SITEMAP_VALUE/', 'Sitemap: https://example.org/sitemaps/sitemap.xml.gz')),
                tokens)
    def test_basic_robots(self):
        tokens = self.do_scan('robots-basic.txt')
        self.assertEqual(
                (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\DISALLOW_VALUE/', 'Disallow: /json/')),
                tokens)
    def test_user_agents_two_disallows(self):
        tokens = self.do_scan('robots-with-two-ua-two-dis.txt')
        self.assertEqual(
                (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\USER_AGENT_VALUE/', 'User-agent: cheeseBurgerCat'), ('\\DISALLOW_VALUE/', 'Disallow: /ceiling-cat-place/')),
                tokens)

    def test_robots_with_newline_comments(self):
        """ We reuse robots-with-two-ua-two-dis.txt but with more comments. """
        tokens = self.do_scan('robots-with-newline-comments.txt')
        self.assertEqual(
               (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\USER_AGENT_VALUE/', 'User-agent: cheeseBurgerCat'), ('\\DISALLOW_VALUE/', 'Disallow: /ceiling-cat-place/')),
                tokens)
    def test_robots_with_allow_value(self):
        """ This robots.txt comes from marketplace.mozilla.com. """
        tokens = self.do_scan("robots-with-allow-value.txt")
        self.assertEqual(
                (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\ALLOW_VALUE/', 'Allow: /'), \
                    ('\\DISALLOW_VALUE/', 'Disallow: /downloads/'), ('\\DISALLOW_VALUE/', 'Disallow: /telefonica/')),
                tokens)
    def test_disabllow_name(self):
        name = '\\DISALLOW_VALUE/'
        resp = _name(name)
        self.assertEqual(resp, 'Disallow')
    def test_allow_name(self):
        name = '\\ALLOW_NAME/'
        resp = _name(name)
        self.assertEqual(resp, 'Allow')
