# -*- coding: utf-8 -*-

class PublicApiException(Exception):
    def __init__(self, *args, **kwargs):
        """Initialize PublicApiException with `function` and `message` objects."""
        self.function = kwargs.pop('function', None)
        self.message = kwargs.pop('message', None)


        super(PublicApiException, self).__init__(*args, **kwargs)


class AuthError(PublicApiException):
    """Authentication error occurred"""


class InvalidParams(PublicApiException):
    """Invalid parameters passed for the requested function"""


class PrivilegeError(PublicApiException):
    "User does not have the privileges needed for this call"
