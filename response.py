'''Response class for creating HTTP responses

   Tom Söderlund <tom.soderlund@iki.fi'''

from status import PHRASE

class Response:
    '''Class for generating HTTP responses'''
    def __init__(self, code = 200):
        '''Initialization'''
        self.code = code
        self.version = b"HTTP/1.1"
        self.headers = []

    def gen_status(self):
        '''Generate the status line in a response'''
        return self.version + b" " + str(self.code).encode() + b" " + PHRASE[self.code].encode() + b"\r\n"

    def add_header(self, name: bytes, value: bytes):
        '''Add one header name-value pair into a response headers'''
        self.headers.append((name, value))

    def gen_headers(self):
        '''Generate header name-value pairs as string'''
        return b"".join([name + b": " + value + b"\r\n" for name, value in self.headers])

    def gen(self, body: bytes = b""):
        '''Generate response as string'''
        if body:
            self.headers.append((b"Content-Length", str(len(body)).encode("utf-8")))
        return b"".join([self.gen_status(), self.gen_headers(), b"\r\n" if body else b"", body])
