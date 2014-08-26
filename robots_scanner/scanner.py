import re

def user_agent_value(scanner, token):
    return "\USER_AGENT_VALUE/", token

def comment(scanner, token):
    return "\COMMENT/", token

def disallow_value(scanner, token):
    return "\DISALLOW_VALUE/", token

def sitemap(scaner, token):
    return "\SITEMAP_VALUE/", token

def allow_value(scanner, token):
    return "\ALLOW_VALUE/", token

def crawl_delay_value(scanner, token):
    return "\CRAWL_DELAY_VALUE/", token

def request_rate_value(scanner, token):
    return "\REQUEST_RATE_VALUE/", token

def visit_time_value(scanner, token):
    return "\VISIT_TIME_VALUE/", token

UA_REGEX = "User-agent: \*|User-agent:\*|User-agent: [a-zA-Z_0-9]+|User-agent:[a-zA-Z_0-9]+"
CM_REGEX = "^#.*"
DIS_REGEX = "Disallow: [a-zA-Z_/\-0-9\s\.~]*|Disallow:[a-zA-Z_/\-0-9\s\.~]*"
ALLOW_REGEX = "Allow: [a-zA-Z_/\-0-9\s\.~]*|Allow:[a-zA-Z_/\-0-9\s\.~]*"
URL_REGEX = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
SM_REGEX = "Sitemap: %s|Sitemap:%s" %(URL_REGEX, URL_REGEX)
CRAWL_REGEX = "Crawl-delay:(\s)?\d+([\/.]\d+)?"
REQRATE_REGEX = "Request-rate:(\s)?\d+\/\d+"
VISIT_TIME_REGEX = "Visit-time:(\s)?\d+\-\d+"

scanner = re.Scanner([
    (UA_REGEX, user_agent_value),
    (CM_REGEX, comment),
    (DIS_REGEX, disallow_value),
    (ALLOW_REGEX, allow_value),
    (SM_REGEX, sitemap),
    (CRAWL_REGEX, crawl_delay_value),
    (REQRATE_REGEX, request_rate_value),
    (VISIT_TIME_REGEX, visit_time_value)])

def scan(body):
    """ Return token tuples after scanning through each line
    in robots.txt. Raise Exception if the first non-comment value
    is not User-agent. 

    Our basic validation is so simple and the validation is inspired
    by the rule specify here: http://www.robotstxt.org/orig.html.

    As soon as the first non-comment value is not "\\USER_AGENT_VALUE/"
    we should abort. 
    1. All comments are ignored in the output tuple of tokens
    2. The first entry in a valid robots.txt should be a USER_AGENT_VALUE.
    3. There is one or more USER_AGENT_VALUE follows by one or more 
    DISALLOW_VALUE and/or ALLOW_VALUE. """

    options = ('\\DISALLOW_VALUE/', '\\ALLOW_VALUE/')
    tokens = []
    first_ua_found = False
    first_cm_found = False
    lines = body.split("\n")
    for line in lines:
        # the last item is usually empty if it has a newline character
        if line:
            token, rem = scanner.scan(line)
            token_name = token[0][0]
            tokens.append(tuple(token)[0])

    return tokens

def validate(tokens):
    token_dict = {}
    ua_found = False
    ua_name = None
    for token in tokens:
        lexeme, token = token[0], token[1]
        if lexeme == "\\COMMENT/":
            continue
        elif lexeme != "\\USER_AGENT_VALUE/" and ua_found:
            if token_dict[ua_name].get(lexeme):
                token_dict[ua_name][lexeme].append(token)
            else:
                token_dict[ua_name][lexeme] = [token]
        elif lexeme != "\\USER_AGENT_VALUE/" and not ua_found:
            raise Exception(
                "There must be a user-agent preceeding {}".format(lexeme))
        elif lexeme == "\\USER_AGENT_VALUE/" and not ua_found:
            ua_found, ua_name = True, token
        elif lexeme == "\\USER_AGENT_VALUE/" and ua_found:
            ua_found, ua_name = False, None
    return token_dict

def _name(name):
    if 'DISALLOW' in name:
        return 'Disallow'
    elif 'ALLOW' in name:
        return 'Allow'

