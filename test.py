'''Test module for some classes

   Tom Söderlund <tom.soderlund@iki.fi> 2021-04-11'''

import socket
from time import sleep
from random import randint
from chunk import Chunk
from parser import Parser
from request import Request

def test_chunk():
    '''Test the separator based FIFO chunk buffer'''
    fifo = Chunk()
    fifo.push(b"testing-")
    fifo.push(b"again-")
    fifo.push(b"and")
    fifo.push(b"-yet-")
    assert fifo.pop(separator=b"-") == b"testing"
    assert fifo.pop(separator=b"-") == b"again"
    fifo.push(b"-again")
    assert fifo.pop(separator=b"-") == b"and"
    assert fifo.pop(separator=b"-") == b"yet"
    assert fifo.pop(separator=b"-") == b""
    assert fifo.pop(separator=b"-") is None
    assert fifo.pop_all() == b"again"

def test_parser_easy():
    '''Test the parser mechanism'''
    parse = Parser()
    req = Request(parse)
    data = b"GET /foo.html HTTP/1.1\r\nHost: ip6-localhost:51551\r\nUser-Agent: curl/7.61.1\r\nAccept: */*\r\n\r\n"
    req.push(data)
    assert parse.method == b"GET"
    assert parse.url == b"/foo.html"
    assert parse.version == b"HTTP/1.1"
    assert parse.headers == [
        (b"Host", b"ip6-localhost:51551"),
        (b"User-Agent", b"curl/7.61.1"),
        (b"Accept", b"*/*")
    ]
    assert parse.body == b""

def test_parser_hard():
    '''Test the parser mechanisms with incoherently chunky input'''
    parse = Parser()
    req = Request(parse)
    blobs = [
        b"GET /fo",
        b"o.html HTTP/1.",
        b"1\r\nHost: ip6-",
        b"localhost:51551\r",
        b"\nUser-Agent: curl/7.61.1\r\nA",
        b"ccept: */*\r\n",
        b"\r",
        b"\n"
    ]

    for data in blobs:
        req.push(data)
        sleep(randint(1,3))

    assert parse.method == b"GET"
    assert parse.url == b"/foo.html"
    assert parse.version == b"HTTP/1.1"
    assert parse.headers == [
        (b"Host", b"ip6-localhost:51551"),
        (b"User-Agent", b"curl/7.61.1"),
        (b"Accept", b"*/*")
    ]
    assert parse.body == b""

def test_server():
    '''Test the server over actual network connection'''
    sock = socket.socket()
    sock.connect(("localhost", 51551))
    data = b"GET /foo.html HTTP/1.1\r\nHost: ip6-localhost:51551\r\nUser-Agent: curl/7.61.1\r\nAccept: */*\r\n\r\n"
    sock.sendall(data)
    data = sock.recv(4096)
    assert data.startswith(b"HTTP/1.1 200 OK")

if __name__ == "__main__":
    test_chunk()
    test_parser_easy()
    test_parser_hard()
#   test_server()
