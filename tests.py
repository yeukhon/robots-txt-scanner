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
