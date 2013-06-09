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
    return "\DISALLOW_VALUE", token

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

def scan():
    tokens = []
    for tc in test_cases:
        print "===== beginning ", tc

        lines = tc.split("\n")
        for line in lines:
            if line:
                print "working on ", line
                token, rem = scanner.scan(line)
                if token[0][0] != "\\COMMENT/":
                    # token is a list of lists.
                    # we only need the first element in the list collection
                    tokens.append(tuple(token)[0])
                print token
        print "===== ending "

    return tuple(tokens)

tokens = scan()
print tokens
