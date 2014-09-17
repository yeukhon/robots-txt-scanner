import re

UNIQUE = True
NOT_UNIQUE = False

class SyntacticError(Exception):
    def __init__(self, message):
        super(SyntacticError, self).__init__(message)
        self.message = message

def _verify(pattern, value):
    r = re.compile(pattern, re.I)
    m = r.match(value)
    return m

def verify_UA(value):
    m = _verify(r"[a-zA-Z]+(?:-?[a-zA-Z0-9]+)*", value)
    if not m:
        raise SyntacticError(
            "User-agent can only contain letters, numbers and -")
    return True

def verify_ALLOW(value):
    m = _verify(r"(?:\/[a-zA-Z0-9|\:|\@|\&|\=\.]*)+", value)
    if not m:
        raise SyntacticError(
            "Allow rule accepts only relative path")
    return True

def verify_DISALLOW(value):
    m = _verify(r"(?:\/[a-zA-Z0-9|\:|\@|\&|\=\.\*]*)+", value)
    if not m:
        raise SyntacticError(
            "Disallow rule accepts only relative path")
    return True

UA_ID = "TK_UA_ID"
ALLOW_ID = "TK_ALLOW_ID"
DISALLOW_ID = "TK_DISALLOW_ID"
COMMENT = "TK_COMMENT"
VALUE = "TK_VALUE"
BLANKCOMMENTS = "TK_BLANKCOMMENTS"

TK_DEFINITIONS = [
    (r"(?:[\s\n\t]+|#.+)+", BLANKCOMMENTS, None, NOT_UNIQUE),
    (r"\s*user-agent:\s*", UA_ID, verify_UA, NOT_UNIQUE),
    (r"\s*allow:\s", ALLOW_ID, verify_ALLOW, NOT_UNIQUE),
    (r"\s*disallow:\s*", DISALLOW_ID, verify_DISALLOW, NOT_UNIQUE),
    (r"[^#\s\n\t]+", VALUE, None, NOT_UNIQUE)
]
