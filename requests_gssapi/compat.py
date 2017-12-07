"""
Compatibility library for older versions of python and requests_kerberos
"""
import sys

import gssapi

from .gssapi_ import REQUIRED, HTTPSPNEGOAuth, SPNEGOExchangeError, log

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
        # put this here for later
        self.principal = principal

        HTTPSPNEGOAuth.__init__(
            self,
            mutual_authentication=mutual_authentication,
            service=service,
            delegate=delegate,
            opportunistic_auth=force_preemptive,
            creds=None,
            hostname_override=hostname_override,
            sanitize_mutual_error_response=sanitize_mutual_error_response)

    def generate_request_header(self, response, host, is_preemptive=False):
        # This method needs to be shimmed because `host` isn't exposed to
        # __init__() and we need to derive things from it.  Also, __init__()
        # can't fail, in the strictest compatability sense.
        try:
            if self.principal is not None:
                gss_stage = "acquiring credentials"
                name = gssapi.Name(self.principal)
                self.creds = gssapi.Credentials(name=name, usage="initiate")

            return HTTPSPNEGOAuth.generate_request_header(self, response,
                                                          host, is_preemptive)
        except gssapi.exceptions.GSSError as error:
            msg = error.gen_message()
            log.exception(
                "generate_request_header(): {0} failed:".format(gss_stage))
            log.exception(msg)
            raise SPNEGOExchangeError("%s failed: %s" % (gss_stage, msg))
