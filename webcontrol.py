#!/usr/bin/python
""" webcontrol """
import sys
from urllib import parse
from http import server
from motorcontrol import set_pin

JSON_FORMAT = "{{'motor': {num}, 'status': {status}}}"
DEFAULT_PORT = 8000
GET_IP_CMD = "hostname -I"


class PiFaceWebHandler(server.BaseHTTPRequestHandler):
    """Handles PiFace web control requests"""
    def parse_path(self, path):
        """Parse URL-Path"""
        return parse.parse_qs(parse.urlparse(path).query)

    def do_GET(self):
        """GET Handler"""
        # parse the query string
        query_components = self.parse_path(self.path)
        print(query_components)

        message = ""
        try:
            motor = self.get_value(query_components, 'motor')
        except ValueError as err:
            message += 'Motor: '+str(err)+'\n'
        try:
            status = self.get_value(query_components, 'status')
        except ValueError as err:
            message += 'Status: '+str(err)+'\n'

        if message == '' and (motor <= 0 or motor >= 3):
            message += 'Motor: Value not in range!'

        if message != '':
            self.error_response(message)
            return

        print("Request Motor:{} Status:{}.".format(motor, status))

        set_pin(motor, status)
        self.success_response(motor, status)

    def success_response(self, motor, status):
        """Response with SUCCESS"""
        message = JSON_FORMAT.format(num=motor, status=status)
        self.response(200, message)

    def error_response(self, message):
        """Response with ERROR"""
        self.response(404, message)

    def response(self, code, message):
        """Response to client"""
        # reply with JSON
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(message, 'UTF-8'))

    def get_value(self, query, name):
        """Gets the query value."""
        if name not in query:
            raise ValueError('Value not given!')
        value = query[name][0]
        try:
            num = int(value)
        except ValueError:
            raise ValueError('Given Value is not valid!')
        return num

def get_my_ip():
    """Returns this computers IP address as a string."""
    #ips = subprocess.check_output(GET_IP_CMD, shell=True).decode('utf-8')[:-1]
    #return ips.strip()
    return 'localhost'

if __name__ == "__main__":
    # get the port
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    else:
        PORT = DEFAULT_PORT

    # set up PiFace Digital

    print("Starting simple PiFace web control at:\n\n"
          "\thttp://{addr}:{port}\n\n"
          .format(addr=get_my_ip(), port=PORT))

    # run the server
    SERVER_ADDRESS = ('', PORT)
    try:
        HTTPD = server.HTTPServer(SERVER_ADDRESS, PiFaceWebHandler)
        HTTPD.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        HTTPD.socket.close()
