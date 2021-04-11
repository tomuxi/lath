'''Session class for handling HTTP request-response sessions

   Tom Söderlund <tom.soderlund@iki.fi> 2021-04-21'''

from datetime import datetime
from parser import Parser
from request import Request
from response import Response

class Session:
    '''Session for a spefific client attempting HTTP request'''
    def __init__(self, scheduler, sock, addr):
        self.scheduler = scheduler
        self.cli_sock = sock
        self.cli_addr = addr
        self.responded = False
        self.parser = Parser(self.respond)
        self.request = Request(self.parser)

    def read_request(self, event):
        '''Attemt to gather the request in small chunks'''
        del event
        data = self.cli_sock.recv(4096)
        if data:
            self.request.push(data)
        else:
            print('closing', self.cli_sock)
            self.scheduler.unregister(self.cli_sock)

    def respond(self):
        '''Respond to a HTTP request'''
        body = b"<html><body>Response</body></html>\r\n"
        resp = Response()
        resp.add_header(b"Server", b"lat-httpd")
        resp.add_header(b"Date", datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT").encode())
        self.cli_sock.send(resp.gen(body))
        print("responded.")
        self.responded = True
