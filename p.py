import re

def user_agent(scanner, token):
    return "\USER_AGENT/", token

def user_agent_value(scanner, token):
    return "\USER_AGENT_VALUE/", token

def comment(scanner, token):
    return "\COMMENT/", token

def newline(scanner, token):
    return "\NEWLINE/", token

scanner = re.Scanner([
    ("User-agent: |User-agent:", user_agent),
    ("\*|[a-zA-Z_]+", user_agent_value),
    ("#\w+", comment)])
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
        "#This is a comment\n#Second comment\nUser-agent: *\n"]


for tc in test_cases:
    print "===== beginning ", tc

    lines = tc.split("\n")
    for line in lines:
        if line:
            print "working on ", line
            token, rem = scanner.scan(line)
            print token
    print "===== ending "


