from .schemas import *
from .exceptions import *


class EndpointBase(object):
    url = None
    schema_class = None
    required_params = list()
    required_data = list()
    method = "GET"
    url_params = None
    request_data = None
    is_request_data_json = True

    def load(self, *args, **kwargs):
        for required_param in self.required_params:
            if required_param in self.url_params:
                continue
            raise MissingRequiredParameter("url_params", required_param)

        for required_param in self.required_data:
            if required_param in self.request_data:
                continue
            raise MissingRequiredParameter("request_data", required_param)

    def get_url(self):
        return self.url

    def get_method(self):
        return self.method

    def get_url_params(self):
        return self.url_params

    def get_request_data(self):
        return self.request_data

    def get_schema(self):
        if not self.schema_class:
            return

        return self.schema_class()

    def process_response(self, payload):
        raise NotImplementedError("Must implement process_response or set schema")

    def _process_response(self, payload):
        if not self.get_schema():
            return self.process_response(payload)

        return self.get_schema().load(payload)


class DomainInfoEndpoint(EndpointBase):
    url = "Domain/Info"
    schema_class = DomainSchema
    required_params = [
        "domain"
    ]

    def load(self, *args, **kwargs):
        self.url_params = {
            "domain": None
        }

        if len(args):
            self.url_params["domain"] = args[0]
        elif "domain" in kwargs:
            self.url_params["domain"] = kwargs["domain"]

        super().load(*args, **kwargs)


class DomainListEndpoint(EndpointBase):
    url = "Domain/List"
    schema_class = DomainsSchema
