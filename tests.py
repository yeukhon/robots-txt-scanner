import unittest
from scanner import scan

class TestRobotScanner(unittest.TestCase):
    def test_disallow_first_raise_exception(self):
        with open('robots/disallow-first.txt', 'r') as f:
            body = f.read()
        self.assertRaises(Exception, scan, body)

    def test_sitemap(self):
        with open('robots/robots-with-sitemap.txt', 'r') as f:
            body = f.read()
        tokens = scan(body)
        self.assertEqual(
                (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\SITEMAP_VALUE/', 'Sitemap: https://example.org/sitemaps/sitemap.xml.gz')),
                tokens)
    def test_basic_robots(self):
        with open('robots/robots-basic.txt', 'r') as f:
            body = f.read()
        tokens = scan(body)
        self.assertEqual(
                (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\DISALLOW_VALUE/', 'Disallow: /json/')),
                tokens)
    def test_user_agents_two_disallows(self):
        with open('robots/robots-with-two-ua-two-dis.txt', 'r') as f:
            body = f.read()
        tokens = scan(body)
        self.assertEqual(
                (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\USER_AGENT_VALUE/', 'User-agent: cheeseBurgerCat'), ('\\DISALLOW_VALUE/', 'Disallow: /ceiling-cat-place/')),
                tokens)

    def test_robots_with_newline_comments(self):
        """ We reuse robots-with-two-ua-two-dis.txt but with more comments. """
        with open('robots/robots-with-newline-comments.txt', 'r') as f:
            body = f.read()
        tokens = scan(body)
        self.assertEqual(
               (('\\USER_AGENT_VALUE/', 'User-agent: *'), ('\\DISALLOW_VALUE/', 'Disallow: /john'),
                 ('\\USER_AGENT_VALUE/', 'User-agent: cheeseBurgerCat'), ('\\DISALLOW_VALUE/', 'Disallow: /ceiling-cat-place/')),
                tokens)
