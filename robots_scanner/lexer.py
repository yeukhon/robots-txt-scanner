import re
from collections import namedtuple

Token = namedtuple('Token',
    ['type', 'value', 'lineno', 'columno', 'predicate',
     'unique']
)

def get_tokens(source, definitions, ignore_case=True):
    """Yield a token if part of the source matched one
    of the token definitions."""
    re_definitions = []
    for t_def in definitions:
        regex = re.compile(t_def[0], re.I)
        re_definitions.append(
            (regex, t_def[1], t_def[2], t_def[3])
        )

    # Break sources into lines
    lines = source.split("\n")
    for lineno, line in enumerate(lines):
        columno = 0
        while columno < len(line):
            match = None
            for t_def, t_type, t_pred, t_uniq in re_definitions:
                match = t_def.match(line, columno)
                if match:
                    yield Token(type=t_type, value=match.group(0),
                        lineno=lineno, columno=columno,
                        predicate=t_pred, unique=t_uniq)
                    # match.end() is always the last match char +1
                    columno = match.end()
                    break
            # We started with a character we can't match with
            # so we mark it unknown and try again with the next
            # character.
            if not match:
                yield Token(type="UNKNOWN_TOKEN", value=line[columno],
                    lineno=lineno, columno=columno, predicate=None,
                    unique=t_uniq)
                columno += 1
