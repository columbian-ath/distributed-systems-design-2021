from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from io import BytesIO
import uuid
import requests


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        r = requests.get(url="http://localhost:8081")   # GET request to logging-service
        r1 = requests.get(url="http://localhost:8082")  # GET request to messages-service
        self.wfile.write("[{}]: {}\n".format(r.text, r1.text).encode('utf-8'))  # formatting r and r1 responses and
        # returning to client

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        UUID = str(uuid.uuid1())  #generate random message id
        body = str(body.decode("utf-8"))  #prepare request body
        r = requests.post("http://localhost:8081", json={'UUID': UUID, 'txt': body})  # send POST to LoggingService


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
