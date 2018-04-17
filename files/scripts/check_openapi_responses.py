#!/usr/bin/env python3

# -*- coding: utf-8 -*-
from colors import color
import requests
import sys
import yaml
from openapi_core import create_spec
from openapi_core.validators import RequestValidator, ResponseValidator
from openapi_core.wrappers import BaseOpenAPIRequest, BaseOpenAPIResponse
from werkzeug.datastructures import ImmutableMultiDict
from urllib.parse import urlparse, parse_qsl


class RequestsOpenAPIRequest(BaseOpenAPIRequest):
    def __init__(self, request):
        self.request = request
        self.url = urlparse(request.url)

    @property
    def host_url(self):
        return self.url.scheme + '://' + self.url.netloc

    @property
    def path(self):
        return self.url.path

    @property
    def method(self):
        return self.request.method.lower()

    @property
    def path_pattern(self):
        return self.url.path

    @property
    def parameters(self):
        return {
            'path': self.url.path,
            'query': ImmutableMultiDict(parse_qsl(self.url.query)),
            'headers': self.request.headers,
            'cookies': self.request.cookies,
        }

    @property
    def body(self):
        return ''

    @property
    def mimetype(self):
        return ''


class RequestsOpenAPIResponse(BaseOpenAPIResponse):

    def __init__(self, response):
        self.response = response

    @property
    def data(self):
        return self.response.text

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def mimetype(self):
        return self.response.headers.get('content-type')


def validate(openapi_file):
    with open(openapi_file, 'r') as myfile:
        spec_dict = yaml.safe_load(myfile)
        spec = create_spec(spec_dict)
        server_url = 'http://88.198.13.202:9051'

        for path, path_object in spec.paths.items():
            if '{' not in path:
                print()
                print(path)
                req = requests.Request('GET', server_url + path)
                openapi_request = RequestsOpenAPIRequest(req)
                validator = RequestValidator(spec)
                result = validator.validate(openapi_request)
                request_errors = result.errors

                r = req.prepare()
                s = requests.Session()
                res = s.send(r)

                openapi_response = RequestsOpenAPIResponse(res)
                validator = ResponseValidator(spec)
                result = validator.validate(openapi_request, openapi_response)
                response_errors = result.errors

                print('Request errors: {} Response errors: {}'.format(request_errors, response_errors))
                if request_errors or response_errors:
                    print(color(' [FAIL] {:d} errors found '.format(len(request_errors) + len(response_errors)),
                                fg='white', bg='red', style='bold'))
                else:
                    print(color(' [PASS] No errors found ', fg='white', bg='green', style='bold'))
            else:
                print(path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Specify path to openapi.yaml file!")
        exit(1)
    else:
        validate(sys.argv[1])
