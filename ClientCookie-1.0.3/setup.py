#!/usr/bin/env python
"""Client-side HTTP cookie handling.

ClientCookie is a Python module for handling HTTP cookies on the
client side, useful for accessing web sites that require cookies to be
set and then returned later.  It also provides some other (optional)
useful stuff: HTTP-EQUIV and Refresh handling, automatic adding of the
Referer [sic] header, robots.txt observance and lazily-seek()able
responses.  These extras are implemented using an extension that makes
it easier to add new functionality to urllib2 (now part of urllib2, as
of Python 2.4).  It has developed from a port of Gisle Aas' Perl
module HTTP::Cookies, from the libwww-perl library.
"""

from ClientCookie import VERSION
NAME = "ClientCookie"
PACKAGE = True
LICENSE = "BSD"
PLATFORMS = ["any"]
CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: System :: Networking :: Monitoring
Topic :: System :: Systems Administration
"""

#-------------------------------------------------------
# the rest is constant for most of my released packages:

import sys, string
from distutils.core import setup

_setup = setup
def setup(**kwargs):
    if not hasattr(sys, "version_info") or sys.version_info < (2, 3):
        # Python version compatibility
        # XXX probably download_url came in earlier than 2.3
        for key in ["classifiers", "download_url"]:
            if kwargs.has_key(key):
                del kwargs[key]
    # Only want packages keyword if this is a package,
    # only want py_modules keyword if this is a single-file module,
    # so get rid of packages or py_modules keyword as appropriate.
    if kwargs["packages"] is None:
        del kwargs["packages"]
    else:
        del kwargs["py_modules"]
    apply(_setup, (), kwargs)

if PACKAGE:
    packages = [NAME]
    py_modules = None
else:
    py_modules = [NAME]
    packages = None

doclines = string.split(__doc__, "\n")

setup(name = NAME,
      version = VERSION,
      license = LICENSE,
      platforms = PLATFORMS,
      classifiers = filter(None, string.split(CLASSIFIERS, "\n")),
      author = "John J. Lee",
      author_email = "jjl@pobox.com",
      description = doclines[0],
      url = "http://wwwsearch.sourceforge.net/%s/" % NAME,
      download_url = ("http://wwwsearch.sourceforge.net/%s/src/"
                      "%s-%s.tar.gz" % (NAME, NAME, VERSION)),
      long_description = string.join(doclines[2:], "\n"),
      py_modules = py_modules,
      packages = packages,
      )
