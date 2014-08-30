from tokens import SyntacticError, _verify

def verify_SITEMAP(value):
    m = _verify(
        r"http[s]?://"+
        r"(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"+
        r"\.xml(?:\.gz)?$",
        value)
    if not m:
        raise SyntacticError(
            "Sitemap must be a full URL and ends with .xml or .xml.gz")

def verify_CRAWL_DELAY(value):
    m = _verify(r"[0-9]+(?:\.[0-9]+)?", value)
    if not m:
        raise SyntacticError(
            "Crawl-delay value must be an integer, a float or a fraction."
        )

SITEMAP = "TK_SITEMAP"
CRAWL_DELAY = "TK_CRAWL_DELAY"

_EXTENDED_DEFINITIONS = [
    (r"\s*sitemap:\s*", SITEMAP, verify_SITEMAP),
    (r"\s*crawl-delay:\s*", CRAWL_DELAY, verify_CRAWL_DELAY)
]
