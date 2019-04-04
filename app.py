#!/usr/bin/python
## Example CDR receiver code for Cisco Meeting Server
## No support, warranty or liability exists for this code
from __future__ import print_function
import BaseHTTPServer
import sys
import getopt
import ssl

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    handler = BaseHTTPServer.BaseHTTPRequestHandler
    handler.protocol_version = 'HTTP/1.1'
    print('using protocol version:', handler.protocol_version)

    def do_GET(self):
        print('received request for GET', self.path)
        self.send_response(200)
        self.end_headers()
    def do_POST(self):
        print('received request for POST', self.path)
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        print('data:', post_data)
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        return

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'p:c:k:')
        port = [val for opt,val in opts if opt=='-p'][0]
        assert(len(port) > 0)
        certfile_name = ''
        keyfile_name = ''
        for opt,val in opts :
            if opt=='-c' :
                certfile_name = val
            if opt=='-k' :
                keyfile_name = val
    except:
        print('usage: app.py -p <port> [-c <certfile path>] [-k <keyfile path>]')
        sys.exit(2)

    server_address = ('', int(port))
    httpd = BaseHTTPServer.HTTPServer(server_address, RequestHandler)
    if (len(certfile_name) > 0):
        print('HTTPS mode with certfile', certfile_name)
        httpd.socket = ssl.wrap_socket (httpd.socket, keyfile=keyfile_name, certfile=certfile_name, server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == "__main__":
    main(sys.argv[1:])
