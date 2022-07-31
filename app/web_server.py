import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class WebserverValidationException(Exception):
    pass


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self, *args, **kwargs):
        parsed_url = urlparse(self.path)
        if parsed_url.path == HTTPRequestHandler._path:
            query = parse_qs(parsed_url.query)
            if 'code' in query:
                HTTPRequestHandler._code = query.get('code')[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return self.wfile.write(
                    '<html><body><p>You may now close this window.</p></body></html>'.encode('utf-8')
                )
        self.send_error(400, "Unrecognised response")
        raise WebserverValidationException


def webserver_for_code(url: str) -> str:
    parsed_url = urlparse(url)
    ip_address = socket.gethostbyname(parsed_url.hostname)
    port = parsed_url.port if parsed_url.port is not None else 80
    if port == 80 and parsed_url.scheme == 'https':
        port = 443

    HTTPRequestHandler._path = parsed_url.path

    httpd = HTTPServer((ip_address, port), HTTPRequestHandler)
    httpd.handle_request()

    return HTTPRequestHandler._code
