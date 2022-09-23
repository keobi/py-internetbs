import urllib.parse
import requests
from .endpoints import *


class InternetbsAPIClient(object):
    def __init__(self, api_key, password, response_type=None, is_test=False):
        if is_test:
            self.url = "https://testapi.internet.bs"
        else:
            self.url = "https://api.internet.bs"

        self.api_key = api_key
        self.password = password
        self.response_type = response_type or "JSON"

        self.endpoints = {
            "get_domain": DomainInfoEndpoint(),
            "list_domains": DomainListEndpoint(),
        }

    def __getattr__(self, key):
        if key not in self.endpoints:
            raise AttributeError(f"Endpoint not found: {key}")

        self.endpoint = self.endpoints[key]

        return self

    def __call__(self, *args, **kwargs):
        self.endpoint.load(*args, **kwargs)

        payload = self.execute()

        return self.endpoint._process_response(payload)

    def get_url(self):
        params = {
            "ApiKey": self.api_key,
            "Password": self.password,
            "ResponseFormat": self.response_type
        }

        endpoint_params = self.endpoint.get_url_params()

        if endpoint_params:
            params.update(
                endpoint_params
            )

        for key in params.keys():
            params[key] = urllib.parse.quote(params[key])

        return f"{self.url}/{self.endpoint.get_url()}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def execute(self):
        url = self.get_url()
        method = self.endpoint.get_method()

        kwargs = {}

        data = self.endpoint.get_request_data()

        if data:
            kwargs["json" if self.endpoint.is_request_data_json else "data"] = data

        print(f"Making {method.upper()} call to {url}")

        r = getattr(requests, method.lower())(
            url,
            **kwargs
        )

        try:
            return r.json()
        except Exception as e:
            print(r.text)
            raise
