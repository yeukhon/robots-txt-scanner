from tokens import SyntacticError, _verify, UNIQUE, NOT_UNIQUE

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
    m = _verify(r"\d+(?:\.\d+)?", value)
    if not m:
        raise SyntacticError(
            "Crawl-delay value must be an integer, a float or a fraction."
        )

def verify_VISIT_TIME(value):
    m = _verify(r"\d{4,4}\-\d{4,4}$", value)
    if not m:
        raise SyntacticError(
            "Visit-time must be between 0000-2459"
        )

def verify_REQUEST_RATE(value):
    m = _verify("\d+/\d+", value)
    if not m:
        raise SyntacticError(
            "Request-rate must be a faction."
        )

SITEMAP = "TK_SITEMAP"
CRAWL_DELAY = "TK_CRAWL_DELAY"
VISIT_TIME = "TK_VISIT_TIME"
REQUEST_RATE = "TK_REQUEST_RATE"

_EXTENDED_DEFINITIONS = [
    (r"\s*sitemap:\s*", SITEMAP, verify_SITEMAP, NOT_UNIQUE),
    (r"\s*crawl-delay:\s*", CRAWL_DELAY, verify_CRAWL_DELAY, UNIQUE),
    (r"\s*visit-time:\s*", VISIT_TIME, verify_VISIT_TIME, UNIQUE),
    (r"\s*request-rate:\s*", REQUEST_RATE, verify_REQUEST_RATE, UNIQUE)
]
