'''Parser class for handling the HTTP request header fields

   Tom Söderlund <tom.soderlund@iki.fi> 2021-04-21'''

class Parser:
    '''Hooks for HTTP request header handling'''
    def __init__(self, respond):
        self.respond = respond
        self.headers = []
        self.version = b""

    def on_method(self, method: bytes, url: bytes, version: bytes):
        '''Handle the method line'''
        print("http method:", method, "url:", url, "version:", version)
        self.version = version

    def on_header(self, name: bytes, value: bytes):
        '''Handle the header name-value pairs'''
        print("header name:", name, "value:", value)
        self.headers.append((name, value))

    def on_body(self, body: bytes):
        '''Handle the body'''
        print("body:", body)

    def on_finished(self):
        '''Handle finishing'''
        print("request received.")
        self.respond()
