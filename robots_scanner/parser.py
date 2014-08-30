import itertools

import lexer
import tokens
UA_NOT_DEFINED = "User-agent must be defined before any rule can be applied."

def sort_tokens(tks):
    return sorted(tks, key=lambda x: x.lineno)

def group_tokens(tks):
    return [ list(line_tokens) 
        for _, line_tokens in itertools.groupby(
                tks, lambda x: x.lineno) ]

def add_error(out, lineno, message):
    return out.append({lineno: message})

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
                {lineno: error message},
            ]
        }
    """
    outputs = {"records": [], "errors": []}
    tks = [token for token in lexer.get_tokens(text, tokens.TK_DEFINITIONS)]

    # Group tokens on the same lines together
    # by first sort them by lineno.
    sorted_tokens = sort_tokens(tks)
    grouped_tokens = group_tokens(sorted_tokens)

    seen_ua = rule_begin = False
    for line in grouped_tokens:
        field, values = line[0], line[1:]
        if field.type == tokens.COMMENT:
            continue
        # User-agent is not defined yet
        elif not seen_ua and not rule_begin and field.type != tokens.UA_ID:
            outputs = add_error(outputs, field.lineno, UA_UNDEFINED)
        else:
            # Join all the value tokens into a single string and pass to
            # predicate to check the syntax (e.g. joining NUMBER / NUMBER)
            full_value = "".join([_.value for _ in values])
            try:
                field.predicate(full_value)
            except tokens.SyntacticError:
                outputs = add_error(outputs, field.lineno, e.message)
            # If we finally see a UA, memorize it
            if field.type == tokens.UA_ID:
                if not seen_ua:
                    outputs["records"].append({"agents": [], "rules": {}})
                seen_ua = True
                rule_begin = False
            # If we finally see a non-comment and non-UA, it must be a rule
            else:
                rule_begin = True
                seen_ua = False
            curr_record = outputs["records"][-1]
            # We are seeing another user agent line
            if not rule_begin and seen_ua:
                curr_record["agents"].append(full_value)
            else:
                # Slice the field name until : (e.g user-agent: -> user-agent)
                field_name = field.value[:field.value.find(":")].lower()
                rules = curr_record["rules"]
                if not rules.get(field_name):
                    rules[field_name] = [full_value]
                else:
                    rules[field_name].append(full_value)
    return outputs

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
