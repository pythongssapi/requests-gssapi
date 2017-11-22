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

from .gssapi_ import HTTPSPNEGOAuth, REQUIRED, OPTIONAL, DISABLED
from .exceptions import MutualAuthenticationError
from .compat import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

""" Deprecated compatability shim """
HTTPKerberosAuth = HTTPSPNEGOAuth

__all__ = ('HTTPKerberosAuth', 'HTTPSNPEGOAuth', 'MutualAuthenticationError',
           'REQUIRED', 'OPTIONAL', 'DISABLED')
__version__ = '0.11.0'
