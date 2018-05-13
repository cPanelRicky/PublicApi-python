#!/usr/bin/env python

from __future__ import all_feature_names
import requests
from .exceptions import (
    PublicApiException, AuthError, InvalidParams, PrivilegeError)


class PublicApi:

    def __init__(self, user, token, host, ssl=True):
        self.user = user
        self.token = token
        self.scheme = "https" if ssl else "http"
        self.host = host
        self.api_versions = dict(
            whmapi1="api.version=1",
            cpapi1=1,
            cpapi2=2,
            uapi=3
        )
        self.port = 2087 if ssl else 2086
        self.header = dict(Authorization="whm {}:{}".format(self.user, self.token))

    # We only need to pass the function name, if it's a cpapi or uapi call the default will be used since the
    # actual api functions for those are sent as parameters and not part of the URL.


    @classmethod
    def error_parser(cls, response):
        # parse the error and raise the proper exception here
        pass

    def api_url(self, function="cpanel"):
        params=dict(scheme=self.scheme,host=self.host, port=self.port, func=function)
        return "{scheme}://{host}:{port}/json-api/{func}".format(**params)

    # This method is used for making CPAPI and UAPI calls from the WHMAPI ** Here there be dragons **
    def cpanel_api_call(self, service,  method, user, module, function, **kwargs):

        ## Generate our standard parameters object
        params = dict(cpanel_jsonapi_user=user,
                      cpanel_jsonapi_apiversion=self.api_versions[service],
                      cpanel_jsonapi_module=module,
                      cpanel_jsonapi_func=function
                      )

        # Add our function specific parameters to our request
        for k,v in kwargs.items():
            params[k] = v

        response = requests.request(method, self.api_url(), headers=self.header, params=params)

        # Need to implement error message checking that raises custom exceptions from our
        # PublicApiExceptions class based on the errors encountered.

        if response.status_code == 200:
            return response.json()
        else:
            raise PublicApiException(function, response.json())

    def whm_api_call(self, method, function, **parameters):

        response = requests.request(method, self.api_url(function=function), headers=self.header, params=parameters)

        # Need to implement error message checking that raises custom exceptions from our
        # PublicApiExceptions class based on the errors encountered.

        if response.status_code == 200:
            return response.json()
        else:
            raise PublicApiException(function, response.json())

