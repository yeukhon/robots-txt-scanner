UA_ID = "TK_UA_ID"
ALLOW_ID = "TK_ALLOW_ID"
DISALLOW_ID = "TK_DISALLOW_ID"
COMMENT = "TK_COMMENT"
VALUE = "TK_VALUE"
IGNORES = "TK_IGNORES"

TK_DEFINITIONS = [
    (r"[\s\n\t"]+, IGNORES),
    (r"#.+", COMMENT),
    (r"\s*user-agent:\s*", UA_ID),
    (r"\s*allow:\s", ALLOW_ID),
    (r"\sdisallow:\s*", DISALLOW_ID),
    (r".+", VALUE)
]
