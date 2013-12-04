try:
    import SimpleHTTPServer as http_server
    from BaseHTTPServer import HTTPServer
except ImportError:
    import http.server as http_server
    from http.server import HTTPServer
import socket
from pprint import pprint
import urlparse
import sys
import os

try:
    __file__
except NameError:
    __file__ = os.path.join(os.getcwd(), 'server.py')
baseDir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(baseDir, 'python'))

import githubInterface

class MyRequestHandler(http_server.SimpleHTTPRequestHandler):
    extensions_map = http_server.SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map.update({
        '.md': 'text/plain',
        })

    def do_POST(self):
        pprint(dict(self.headers))
        length = self.headers.getheader('content-length')
        if length:
            content = self.rfile.read(int(length))
            # print 'content:', content
            params = urlparse.parse_qs(content) # urllib.urlencode
            pprint(params)
            comment = params.get('comment', [''])[0]
            sourceCode = params.get('sourceCode', [''])[0]
        return self.do_GET()


def test(HandlerClass = MyRequestHandler,
         ServerClass = HTTPServer, protocol="HTTP/1.0", port=8000):
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the first command line
    argument).

    """
    server_address = ('', port)

    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        httpd.server_close()
        sys.exit(0)

def start_locally():
    print('Url: http://localhost:8000/')
    print('andere IPs: ')
    print(socket.gethostbyname_ex(socket.gethostname()))

    test(MyRequestHandler)

def start_internet():
    test(MyRequestHandler, port = 80)

if __name__ == '__main__':
    start_locally()

