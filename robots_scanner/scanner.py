import re

def user_agent_value(scanner, token):
    return "\USER_AGENT_VALUE/", token

def comment(scanner, token):
    return "\COMMENT/", token

def disallow_value(scanner, token):
    return "\DISALLOW_VALUE/", token

def sitemap(scaner, token):
    return "\SITEMAP_VALUE/", token

UA_REGEX = "User-agent: \*|User-agent:\*|User-agent: [a-zA-Z_0-9]+|User-agent:[a-zA-Z_0-9]+"
CM_REGEX = "^#.*"
DIS_REGEX = "Disallow: [a-zA-Z_/\-0-9\s\.~]*|Disallow:[a-zA-Z_/\-0-9\s\.~]*"
URL_REGEX = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
SM_REGEX = "Sitemap: %s|Sitemap:%s" %(URL_REGEX, URL_REGEX)

scanner = re.Scanner([
    (UA_REGEX, user_agent_value),
    (CM_REGEX, comment),
    (DIS_REGEX, disallow_value),
    (SM_REGEX, sitemap)])

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
    DISALLOW_VALUE. """

    tokens = []
    first_ua_found = False
    first_cm_found = False
    lines = body.split("\n")
    for line in lines:
        # the last item is usually empty if it has a newline character
        if line:
            print "working on ", line
            token, rem = scanner.scan(line)
            token_name = token[0][0]
            if token_name != "\\COMMENT/":
                if not first_ua_found and token_name == "\\USER_AGENT_VALUE/":
                    first_ua_found = True
                elif token_name == "\\DISALLOW_VALUE/" and not first_ua_found:
                    raise Exception("robots.txt is invalid because Disallow is found before User-agent at the beginning of the document.")
                # tokeb is a list of lists
                # but we only need the first element in this list collection
                tokens.append(tuple(token)[0])
            print token
    return tuple(tokens)

