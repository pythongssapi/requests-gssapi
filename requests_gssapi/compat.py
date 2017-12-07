"""
Compatibility library for older versions of python and requests_kerberos
"""
import sys

from .gssapi_ import REQUIRED, HTTPSPNEGOAuth  # noqa

# python 2.7 introduced a NullHandler which we want to use, but to support
# older versions, we implement our own if needed.
if sys.version_info[:2] > (2, 6):
    from logging import NullHandler
else:
    from logging import Handler

    class NullHandler(Handler):
        def emit(self, record):
            pass


class HTTPKerberosAuth(HTTPSPNEGOAuth):
    """Deprecated compat shim; see HTTPSPNEGOAuth instead."""
    def __init__(self, mutual_authentication=REQUIRED, service="HTTP",
                 delegate=False, force_preemptive=False, principal=None,
                 hostname_override=None, sanitize_mutual_error_response=True):
        HTTPSPNEGOAuth.__init__(
            self,
            mutual_authentication=mutual_authentication,
            service=service,
            delegate=delegate,
            opportunistic_auth=force_preemptive,
            principal=principal,
            hostname_override=hostname_override,
            sanitize_mutual_error_response=sanitize_mutual_error_response)

    def generate_request_header(self, response, host, is_preemptive=False):
        # This method needs to be shimmed because `host` isn't exposed to
        # __init__() and we need to derive things from it
        return HTTPSPNEGOAuth.generate_request_header(self, response, host,
                                                      is_preemptive)
