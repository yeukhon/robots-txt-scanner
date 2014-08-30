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

SITEMAP = "TK_SITEMAP"

_EXTENDED_DEFINITIONS = [
    (r"\s*sitemap:\s*", SITEMAP, verify_SITEMAP)
]
