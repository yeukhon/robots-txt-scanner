robots-txt-scanner
##################

This scanner is primarily built for validating robots.txt 
as part of the [Minion](https://github.com/mozilla/minion)'s
[basic scan](https://github.com/mozilla/minion-backend/blob/master/minion/plugins/basic.py).


Quickstart
==========

It's easy. Just ``pip install robots-scanner``  (see 
[robots-scanner on pypi](https://pypi.python.org/pypi/robots-scanner).

Usage?

```
text = """
# COMMENT GOES HERE
User-agent: Google # inline comments
User-agent: Yahoo
Disallow: /admin
Disallow: /tmp/
Allow: /index.html

User-agent: Yahoo
# Some comments here
Disallow: /yahoo/

User-agent: Bing
Disallow: /bing/
"""
import pprint
pprint.pprint(
    tokens_to_ast(
        text_to_tokens(text)), indent=2)

r = Robotstxt()
r.parse(text)
pprint.pprint(r._tree)
```

And the output looks like this:

```
{ 'errors': [{ 14: 'Disallow rule accepts only relative path'}],
  'records': [ { 'agents': ['Google', 'Yahoo'],
                 'rules': { 'allow': ['/index.html'],
                            'disallow': ['/admin', '/tmp/']}},
               { 'agents': ['Yahoo'], 'rules': { 'disallow': ['/yahoo/']}},
               { 'agents': ['Bing'],
                 'rules': { 'disallow': ['/bing/', 'http://domain.org/bad']}}]}

{'Bing': {'disallow': ['/bing/', 'http://domain.org/bad']},
 'Google': {'allow': ['/index.html'], 'disallow': ['/admin', '/tmp/']},
 'Yahoo': {'allow': ['/index.html'],
           'disallow': ['/admin', '/tmp/', '/yahoo/']}}
```

The first dictionary is the AST of the robots.txt and the second
dictionary is a tree that user can query. See ``Robotstxt`` in parser.py
for the public API.

Changelog
=========

August 30, 2014 - v0.2.0a
------------------------

* Rewrite the entire scanner with a custom lexer and token.

* Support custom extensions added to the lexer and parser.

August 11, 2013 - v0.1.3
-------------------------

* Added support for ``Visit-time``, 
  ``Crawl-delay`` and ``Request-rate`` directives.

