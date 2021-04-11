'''Request class for detecting HTTP request header information

   Tom Söderlund <tom.soderlund@iki.fi> 2021-04-21'''

from chunk import Chunk
from parser import Parser

class Request:
    '''Detect HTTP request header fields'''
    def __init__(self, parser: Parser):
        self.parser = parser
        self.buf = Chunk()
        self.start_parsed = False
        self.headers_parsed = False
        self.body_unparsed = 0

    def push(self, data: bytes):
        '''Push received data at the end of buffer'''
        self.buf.push(data)
        self.parse()

    def parse(self):
        '''Parse so far received buffer'''
        if not self.start_parsed:
            self.parse_start()
        elif not self.headers_parsed:
            self.parse_headers()
        elif self.body_unparsed:
            data = self.buf.pop_all()
            self.body_unparsed -= len(data)
            self.parser.on_body(data)
            self.parse()
        else:
            self.parser.on_finished()

    def parse_start(self):
        '''Parse the starting line of the HTTP request'''
        line = self.buf.pop(separator=b"\r\n")
        if line is not None:
            method, url, version = line.strip().split()
            self.start_parsed = True
            self.parser.on_method(method, url, version)
            self.parse()

    def parse_headers(self):
        '''Parse the subsequent header name-value pairs of the HTTP request'''
        line = self.buf.pop(separator=b"\r\n")
        if line is not None:
            if line:
                name, value = line.strip().split(b": ", maxsplit=1)
                if name.lower() == b"content-length":
                    self.body_unparsed = int(value.decode("utf-8"))
                self.parser.on_header(name, value)
            else:
                self.headers_parsed = True
            self.parse()
