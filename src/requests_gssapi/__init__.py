"""
requests GSSAPI authentication library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. This library
adds optional GSSAPI authentication support and supports mutual
authentication. Basic GET usage:

    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth
    >>> r = requests.get("http://example.org", auth=HTTPSPNEGOAuth())

The entire `requests.api` should be supported.
"""

import logging

from .compat import HTTPKerberosAuth, NullHandler
from .exceptions import MutualAuthenticationError
from .gssapi_ import DISABLED, OPTIONAL, REQUIRED, SPNEGO, HTTPSPNEGOAuth  # noqa

logging.getLogger(__name__).addHandler(NullHandler())

__all__ = (
    "HTTPSPNEGOAuth",
    "HTTPKerberosAuth",
    "MutualAuthenticationError",
    "SPNEGO",
    "REQUIRED",
    "OPTIONAL",
    "DISABLED",
)
__version__ = "1.3.0"
