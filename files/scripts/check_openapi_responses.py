#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from colors import color
import json
import requests
import sys
import yaml
from openapi_core import create_spec
from openapi_core.shortcuts import RequestValidator, ResponseValidator
from openapi_core.wrappers.base import BaseOpenAPIRequest, BaseOpenAPIResponse
from werkzeug.datastructures import ImmutableMultiDict
from urllib.parse import urlparse, parse_qsl


class RequestsOpenAPIRequest(BaseOpenAPIRequest):
    def __init__(self, request, path_pattern=None, path_params=None):
        self.request = request
        self.url = urlparse(request.url)
        self._path_pattern = path_pattern
        self._path_params = path_params if path_params is not None else {}

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
        if self._path_pattern is None:
            return self.url.path

        return self._path_pattern

    @property
    def parameters(self):
        return {
            'path': self._path_params,
            'query': ImmutableMultiDict(parse_qsl(self.url.query)),
            'headers': self.request.headers,
            'cookies': self.request.cookies,
        }

    @property
    def body(self):
        return self.request.data

    @property
    def mimetype(self):
        return self.request.headers.get('content-type')


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
        server_url = 'http://209.97.138.187:9052'
        total_errors_count = 0

        parameters = {
            'get': {
                'count': 2,
                'length': 123,
                'blockHeight': 20,
                'headerId': 'Ebo1riBazi8JpvmtqFnkbyhK29P8KXPawiTVyVFgAqhY',
            },
            'post': {
                # '/blocks': None,
                # '/transactions': None,
                '/peers/connect': '127.0.0.1:5673',
                # '/utils/hash/blake2b': '123qwe'
            }
        }

        for path, path_object in spec.paths.items():
            for method, operation in path_object.operations.items():
                print()

                if '{' not in path:
                    print('{} {}'.format(method.upper(), path))
                    new_path = path
                    path_pattern = None
                    path_params = {}
                else:
                    parameter_start = path.find('{')
                    parameter_end = path.find('}')
                    parameter = path[parameter_start + 1:parameter_end]
                    new_path = path[:parameter_start] + str(parameters['get'][parameter]) + path[parameter_end + 1:]
                    print('{} {} -> {}'.format(method.upper(), path, new_path))
                    path_pattern = path
                    path_params = {parameter: parameters['get'][parameter]}

                if method == 'get':
                    req = requests.Request('GET', server_url + new_path)
                elif method == 'post':
                    if new_path in parameters['post'] and parameters['post'][new_path]:
                        req = requests.Request('POST', server_url + new_path,
                                               data=json.dumps(parameters['post'][new_path]),
                                               headers={'content-type': 'application/json'})
                    else:
                        print('Skipping, POST method has no example payload to test')
                        continue
                else:
                    print('Skipping, no GET or POST methods for this path')
                    continue

                openapi_request = RequestsOpenAPIRequest(req, path_pattern, path_params)
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
                    errors_count = len(request_errors) + len(response_errors)
                    total_errors_count += errors_count
                    print(color(' [FAIL] {:d} errors found '.format(errors_count), fg='white', bg='red', style='bold'))
                    print("Response body: {}".format(res.text))
                else:
                    print(color(' [PASS] No errors found ', fg='white', bg='green', style='bold'))

        if total_errors_count:
            print()
            print(color(' [FAIL] Total {:d} errors found '.format(total_errors_count), fg='white', bg='red',
                        style='bold'))
            exit(total_errors_count)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Specify path to openapi.yaml file!")
        exit(1)
    else:
        validate(sys.argv[1])
