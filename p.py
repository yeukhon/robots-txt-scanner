import re

def user_agent(scanner, token):
    return "\USER_AGENT/", token

def user_agent_value(scanner, token):
    return "\USER_AGENT_VALUE/", token

def comment(scanner, token):
    return "\COMMENT/", token

def newline(scanner, token):
    return "\NEWLINE/", token

def disallow(scanner, token):
    return "\DISALLOW/", token

def disallow_value(scanner, token):
    return "\DISALLOW_VALUE/", token

scanner = re.Scanner([
    #("User-agent: |User-agent:", user_agent),
    ("User-agent: \*|User-agent:\*|User-agent: [a-zA-Z_0-9]+|User-agent:[a-zA-Z_0-9]+", user_agent_value),
    #("\*|[a-zA-Z_]+", user_agent_value),
    ("#\w+", comment),
    #("Disallow: | Disallow:", disallow),
    ("Disallow: [a-zA-Z_/\-0-9\s\.~]*|Disallow:[a-zA-Z_/\-0-9\s\.~]*", disallow_value)])

#    ("\\n+", newline)])
test_cases = [
        "User-agent: hello",
        "User-agent: *",
        "User-agent: hello\nUser-agent: *",
        "User-agent: hello\nUser-agent: *\n",
        "User-agent: *\nUser-agent: hello",
        "User-agent: *\nUser-agent: hello\n",
        "#This is a comment\nUser-agent: *",
        "#This is a comment\nUser-agent: hello",
        "#This is a comment\nUser-agent: hello\n",
        "#This is a comment\nUser-agent: hello\nUser-agent: *",
        "#This is a comment\nUser-agent: hello\nUser-agent: *\n",
        "#This is a comment\nUser-agent: *\n",
        "#This is a comment\nUser-agent: *\nUser-agent: hello",
        "#This is a comment\nUser-agent: *\nUser-agent: hello\n",
        "#This is a comment\nUser-agent: * #Inline",
        "#This is a comment\nUser-agent: *#Inline-closer",
        "#This is a comment\n#Second comment\nUser-agent: *\n",
        "User-agent: hello\nDisallow: /"]

with open('robots.txt', 'r') as f:
    test_cases.append(f.read())

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

#def test_scan():
#    tokens = []
#    for tc in test_cases:
#        print "===== beginning ", tc
#        tokens.append(scan(tc))
#        print "===== ending "
#    return tokens
#tokens = test_scan()
#print tokens


