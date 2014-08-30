import itertools
from collections import namedtuple

import lexer
import tokens

ErrorRecord = namedtuple("ErrorRecord",
                ["lineno", "columno", "reason"])

UA_NOT_DEFINED = "User-agent must be defined before any rule can be applied."

def sort_tokens(tks):
    return sorted(tks, key=lambda x: x.lineno)

def group_tokens(tks):
    return [ list(line_tokens) 
        for _, line_tokens in itertools.groupby(
                tks, lambda x: x.lineno) ]

def parse(text):
    """Returns a dictionary containing AST of the robots.txt
    and a list of (possibily empty) errors found during
    parsing.

    .. code-block:: python

        {
            records: [
                [
                    {
                        'agent': ['Google', 'Yahoo'],
                        'rules': {
                            'disallow': [],
                            'allow': []
                        }
                    }
                ]
            ],
            errors: [
                ErrorRecord(lineno=, columnno=, reason=,),
            ]
        }
    """
    outputs = {"records": [], "errors": []}
    tks = [token for token in lexer.get_tokens(text, tokens.TK_DEFINITIONS)]

    # Group tokens on the same lines together
    # by first sort them by lineno.
    sorted_tokens = sort_tokens(tks)
    grouped_tokens = group_tokens(sorted_tokens)

    seen_ua = False
    last_start_line = 0

    """
    for line in grouped_tokens:
        for tk in line:
            if tk.type == tokens.COMMENT:
                continue
            # User-agent is not defined yet
            elif not seen_ua and tk.type !== tokens.UA_ID:
                outputs = add_error(outputs, tk, UA_UNDEFINED)
            elif tk.type == tokens.UA_ID:
                pass
    """
    return grouped_tokens

text = """
# COMMENT GOES HERE
User-agent: Google
User-agent: Yahoo
Disallow: /admin
Disallow: /tmp/
Allow: /index.html

User-agent: Yahoo
# Some comments here
Disallow: /yahoo/
"""
import pprint
pprint.pprint(parse(text), indent=2)
