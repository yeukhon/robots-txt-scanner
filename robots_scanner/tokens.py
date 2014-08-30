def SyntacticError(Exception):
    def __init__(self, token, message):
        super(SyntacticError, self).__init__(message)
        self.message = message
        self.token = token

def _verify(pattern, value):
    r = re.compile(pattern, re.I)
    m = r.match(value)
    return m

def verify_UA(token):
    m = _verify(r"[a-zA-Z]+(?:-?[a-zA-Z0-9]+)*", token.value)
    if not m:
        raise SyntacticError(token,
            "User-agent can only contain letters, numbers and -")
    return True

def verify_ALLOW(token):
    m = _verify(r"(?:\/[a-zA-Z0-9|\:|\@|\&|\=\.]*)+", token.value)
    if not m:
        raise SyntacticError(token,
            "Allow rule accepts only relative path")
    return True

def verify_DISALLOW(token):
    m = _verify(r"(?:\/[a-zA-Z0-9|\:|\@|\&|\=\.]*)+", token.value)
    if not m:
        raise SyntacticError(token,
            "Disallow rule accepts only relative path")
    return True

UA_ID = "TK_UA_ID"
ALLOW_ID = "TK_ALLOW_ID"
DISALLOW_ID = "TK_DISALLOW_ID"
COMMENT = "TK_COMMENT"
VALUE = "TK_VALUE"
IGNORES = "TK_IGNORES"

TK_DEFINITIONS = [
    (r"[\s\n\t]+", IGNORES, None),
    (r"#.+", COMMENT, None),
    (r"\s*user-agent:\s*", UA_ID, verify_UA),
    (r"\s*allow:\s", ALLOW_ID, verify_ALLOW),
    (r"\s*disallow:\s*", DISALLOW_ID, verify_DISALLOW),
    (r".+", VALUE, None)
]
