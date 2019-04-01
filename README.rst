requests GSSAPI authentication library
===============================================

Requests is an HTTP library, written in Python, for human beings. This library
adds optional GSSAPI authentication support and supports mutual
authentication.

It provides a fully backward-compatible shim for the old
python-requests-kerberos library: simply replace ``import requests_kerberos``
with ``import requests_gssapi``.  A more powerful interface is provided by the
HTTPSPNEGOAuth component, but this is of course not guaranteed to be
compatible.  Documentation below is written toward the new interface.

Basic GET usage:


.. code-block:: python

    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth
    >>> r = requests.get("http://example.org", auth=HTTPSPNEGOAuth())
    ...

The entire ``requests.api`` should be supported.

Authentication Failures
-----------------------

Client authentication failures will be communicated to the caller by returning
the 401 response.

Mutual Authentication
---------------------

REQUIRED
^^^^^^^^

By default, ``HTTPSPNEGOAuth`` will require mutual authentication from the
server, and if a server emits a non-error response which cannot be
authenticated, a ``requests_gssapi.errors.MutualAuthenticationError`` will
be raised. If a server emits an error which cannot be authenticated, it will
be returned to the user but with its contents and headers stripped. If the
response content is more important than the need for mutual auth on errors,
(eg, for certain WinRM calls) the stripping behavior can be suppressed by
setting ``sanitize_mutual_error_response=False``:

.. code-block:: python

    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth, REQUIRED
    >>> gssapi_auth = HTTPSPNEGOAuth(mutual_authentication=REQUIRED, sanitize_mutual_error_response=False)
    >>> r = requests.get("https://windows.example.org/wsman", auth=gssapi_auth)
    ...


OPTIONAL
^^^^^^^^

If you'd prefer to not require mutual authentication, you can set your
preference when constructing your ``HTTPSPNEGOAuth`` object:

.. code-block:: python

    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth, OPTIONAL
    >>> gssapi_auth = HTTPSPNEGOAuth(mutual_authentication=OPTIONAL)
    >>> r = requests.get("http://example.org", auth=gssapi_auth)
    ...

This will cause ``requests_gssapi`` to attempt mutual authentication if the
server advertises that it supports it, and cause a failure if authentication
fails, but not if the server does not support it at all.

DISABLED
^^^^^^^^

While we don't recommend it, if you'd prefer to never attempt mutual
authentication, you can do that as well:

.. code-block:: python

    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth, DISABLED
    >>> gssapi_auth = HTTPSPNEGOAuth(mutual_authentication=DISABLED)
    >>> r = requests.get("http://example.org", auth=gssapi_auth)
    ...

Opportunistic Authentication
----------------------------

``HTTPSPNEGOAuth`` can be forced to preemptively initiate the GSSAPI
exchange and present a token on the initial request (and all
subsequent). By default, authentication only occurs after a
``401 Unauthorized`` response containing a Negotiate challenge
is received from the origin server. This can cause mutual authentication
failures for hosts that use a persistent connection (eg, Windows/WinRM), as
no GSSAPI challenges are sent after the initial auth handshake. This
behavior can be altered by setting  ``opportunistic_auth=True``:

.. code-block:: python
    
    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth, REQUIRED
    >>> gssapi_auth = HTTPSPNEGOAuth(mutual_authentication=REQUIRED, opportunistic_auth=True)
    >>> r = requests.get("https://windows.example.org/wsman", auth=gssapi_auth)
    ...

Hostname Override
-----------------

If communicating with a host whose DNS name doesn't match its
hostname (eg, behind a content switch or load balancer),
the hostname used for the GSSAPI exchange can be overridden by
passing in a custom name (string or ``gssapi.Name``):

.. code-block:: python

    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth, REQUIRED
    >>> gssapi_auth = HTTPSPNEGOAuth(target_name="internalhost.local")
    >>> r = requests.get("https://externalhost.example.org/", auth=gssapi_auth)
    ...

Explicit Principal
------------------

``HTTPSPNEGOAuth`` normally uses the default principal (ie, the user for whom
you last ran ``kinit`` or ``kswitch``, or an SSO credential if
applicable). However, an explicit credential can be in instead, if desired.

.. code-block:: python

    >>> import gssapi
    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth, REQUIRED
    >>> name = gssapi.Name("user@REALM", gssapi.NameType.hostbased_service)
    >>> creds = gssapi.Credentials(name=name, usage="initiate")
    >>> gssapi_auth = HTTPSPNEGOAuth(creds=creds)
    >>> r = requests.get("http://example.org", auth=gssapi_auth)
    ...

Delegation
----------

``requests_gssapi`` supports credential delegation (``GSS_C_DELEG_FLAG``).
To enable delegation of credentials to a server that requests delegation, pass
``delegate=True`` to ``HTTPSPNEGOAuth``:

.. code-block:: python

    >>> import requests
    >>> from requests_gssapi import HTTPSPNEGOAuth
    >>> r = requests.get("http://example.org", auth=HTTPSPNEGOAuth(delegate=True))
    ...

Be careful to only allow delegation to servers you trust as they will be able
to impersonate you using the delegated credentials.

Logging
-------

This library makes extensive use of Python's logging facilities.

Log messages are logged to the ``requests_gssapi`` and
``requests_gssapi.gssapi`` named loggers.

If you are having difficulty we suggest you configure logging. Issues with the
underlying GSSAPI libraries will be made apparent. Additionally, copious debug
information is made available which may assist in troubleshooting if you
increase your log level all the way up to debug.
