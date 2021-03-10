from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from io import BytesIO
import json



class S(BaseHTTPRequestHandler):
    message_dict = {}
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        resp = ",".join(S.message_dict.values())  # Get all values from dict and place in 1 comma-separated str
        self.wfile.write(resp.encode('utf-8'))  #return response to facadeservice

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        temp_dict = json.loads(body)  #load request body to temp dict for further extraction
        S.message_dict[temp_dict["UUID"]] = temp_dict['txt']  # writes data into message storage (hashmap -> dict)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        #self.wfile.write(response.getvalue())
        logging.info('Message ("UUID": {}, "msg": {})'.format(temp_dict["UUID"], temp_dict['txt']))


def run(server_class=HTTPServer, handler_class=S, port=8081):
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
