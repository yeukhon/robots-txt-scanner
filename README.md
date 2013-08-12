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
>>> from robots_scanner import scanner
>>> print scanner.scan("User-agent: Google\nDisallow: *")
(('\\USER_AGENT_VALUE/', 'User-agent: Google'), ('\\DISALLOW_VALUE/', 'Disallow: '))
```

Changelog
=========

August 11, 2013 - v0.1.3
-------------------------

* Added support for ``Visit-time``, 
  ``Crawl-delay`` and ``Request-rate`` directives.

