#!/usr/bin/env python

from sys import argv
from http.server import CGIHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from os import path, getcwd
from urllib import parse

DIR = ''

class ConcurrentServer(ThreadingMixIn, HTTPServer):
    pass

class CustomHttpRequestHandler(CGIHTTPRequestHandler):
    def do_HEAD(self):
        self.handle_request()

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def handle_request(self):
        url = parse.urlparse(self.path)
        whole_path = path.abspath(path.join(path.abspath(DIR), url.path[1:]))
        path.relpath(whole_path, getcwd())
        if path.isfile(whole_path):
            if whole_path.endswith('.cgi'):
                self.cgi_info = '', '{}?{}'.format(path.relpath(whole_path, getcwd()), url.query if url.query else '')
                self.run_cgi()
            else:
                size = path.getsize(whole_path)
                self.send_server_reply(response_data_length=size)
                file = open(whole_path, 'rb')
                file_data = file.read(1000)
                while file_data:
                    self.wfile.write(file_data)
                    file_data = file.read(1000)

        else:
            self.send_error_reply()

    def send_server_reply(self, code=200, response_data_length=None):
        self.send_response(code=code)
        if response_data_length:
            self.send_header('Content-Length', str(response_data_length))
        self.end_headers()

    def send_error_reply(self):
        self.send_error(code=404)


def main():
    global DIR
    if len(argv) != 3:
        raise ValueError('Wrong number of arguments passed')
    port = int(argv[1])
    DIR = argv[2]

    server_address = ('', port)
    server = ConcurrentServer(server_address, CustomHttpRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()