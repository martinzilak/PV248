#!/usr/bin/env python
from pprint import pprint
from sys import argv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse, error
from urllib.request import Request, urlopen
import socket

UPSTREAM = ''


class CustomHttpRequestHandler(BaseHTTPRequestHandler):
    def send_error_reply(self, code):
        url_response = {}
        url_response['code'] = str(code)

        self.send_server_reply(200)
        self.wfile.write(json.dumps(url_response, indent=2).encode('UTF-8'))

    def send_server_reply(self, code=200, response_data_length=None):
        self.send_response(code=code)
        self.send_header('Content-Type', 'application/json')
        if response_data_length:
            self.send_header('Content-Length', str(response_data_length))
        self.end_headers()

    def build_url_response(self, response):
        status = response.status
        content = response.read().decode('ISO-8859-1')
        headers = response.getheaders()

        url_response = {}
        url_response['code'] = status
        url_response['headers'] = {}

        for header_name, header_value in headers:
            url_response['headers'][header_name] = header_value

        try:
            url_response['json'] = json.loads(content)
        except:
            url_response['content'] = content

        return url_response

    def do_GET(self):
        parameters = parse.urlparse(self.path).query

        request_url = UPSTREAM
        request_url += '?{}'.format(parameters) if parameters else ''

        request_headers = dict(self.headers)

        request = Request(url=request_url, data=None, headers=request_headers, method='GET')

        try:
            with urlopen(request, timeout=1) as response:
                url_response = self.build_url_response(response)

                self.send_server_reply(200, len(url_response))
                self.wfile.write(json.dumps(url_response, indent=2).encode('UTF-8'))
        except socket.timeout:
            return self.send_error_reply('timeout')
        except error.HTTPError as e:
            return self.send_error_reply(e.getcode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        try:
            post_data = json.loads(self.rfile.read(content_length).decode('UTF-8'))
        except:
            self.send_error_reply('invalid json')
            return

        request_url = post_data.get('url')
        request_data = post_data.get('content').encode('UTF-8') if 'content' in post_data else None

        if request_url is None or (post_data.get('type') == 'POST' and request_data is None):
            self.send_error_reply('invalid json')
            return

        request = Request(url=request_url, data=request_data, headers=post_data.get('headers'),
                          method=post_data.get('type', 'GET'))

        with urlopen(request, timeout=post_data.get('timeout')) as response:
            url_response = self.build_url_response(response)

            self.send_server_reply(200, len(url_response))
            self.wfile.write(json.dumps(url_response, indent=2).encode('UTF-8'))


def main():
    global UPSTREAM
    if len(argv) != 3:
        raise ValueError('Wrong number of arguments passed')
    port = int(argv[1])
    UPSTREAM = argv[2]

    server_address = ('', port)
    server = HTTPServer(server_address, CustomHttpRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
