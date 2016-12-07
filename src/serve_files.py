#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serve current folder files in a HTTP webserver.
"""
import socketserver

from threading import Thread
from http.server import SimpleHTTPRequestHandler

PORT = 8000


def start_http_server(port=PORT):
    httpd = socketserver.TCPServer(("", port), SimpleHTTPRequestHandler)    
    thread = Thread(target = httpd.serve_forever)
    thread.start()
    return thread


if __name__ == '__main__':
    thread = start_http_server()
    thread.join()
