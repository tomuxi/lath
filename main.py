'''lath - Light asynchronous threadless HTTP server

   Tom Söderlund <tom.soderlund@iki.fi> 2021-04-10'''

import sys
import socket
import selectors
from session import Session

VERSION = b'v0.0.1'
scheduler = selectors.DefaultSelector()

def srv_accept(sock, event):
    '''Accept a new connection and create a session for it'''
    del event
    cli_sock, cli_addr = sock.accept()
    print('accepted', cli_sock, 'from', cli_addr)
    cli_sock.setblocking(False)
    sess = Session(cli_sock, cli_addr, VERSION)
    scheduler.register(cli_sock, selectors.EVENT_READ, sess)

def lath(addr, port):
    '''Main scheduler loop and creating server socket for accepting connections'''
    sock = socket.socket(socket.AF_INET6)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0) # Usable also for IPv4
    sock.setblocking(False)
    sock.bind((addr, port))
    sock.listen()
    scheduler.register(sock, selectors.EVENT_READ)

    while True:
        events = scheduler.select()
        for key, mask in events:
            sess = key.data
            if not sess:
                srv_accept(key.fileobj, mask)
            else:
                if not sess.read_request(mask) or sess.responded:
                    scheduler.unregister(sess.cli_sock)
                    sess.cli_sock.close()
                    del sess

if len(sys.argv) > 3:
    print('Usage:', sys.argv[0], '[address] [port]')
    sys.exit(1)

srv_addr = ''
srv_port = 51551

if len(sys.argv) >= 2:
    srv_addr = sys.argv[1]

if len(sys.argv) == 3:
    srv_port = int(sys.argv[2])

if __name__ == "__main__":
    lath(srv_addr, srv_port)
