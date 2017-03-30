"""
simplewebcontrol.py
Controls PiFace Digital through a web browser. Returns the status of the
input port and the output port in a JSON string. Set the output with GET
variables.

Copyright (C) 2013 Thomas Preston <thomas.preston@openlx.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import subprocess
import urllib.parse
import http.server
import pifacedigitalio


JSON_FORMAT = "{{'relay': {num}, 'status': {status}}}"
DEFAULT_PORT = 8000
OUTPUT_PORT_GET_STRING = "relay"
GET_IP_CMD = "hostname -I"


class PiFaceWebHandler(http.server.BaseHTTPRequestHandler):
    """Handles PiFace web control requests"""
    def do_GET(self):
        """GET Handler"""
        # parse the query string
        qss = urllib.parse.urlparse(self.path).query
        query_components = urllib.parse.parse_qs(qss)

        relay = self.get_relay_value(query_components)
        status = self.get_status_value(query_components)
        print("Request Relay:{} Status:{}.".format(relay, status))
        #'No valid status!'

        if relay >= 0 and status >= 0:
            self.set_relay(relay, status)
            self.response(relay, status)
            return
        if int(relay) < 0:
            if relay == -1:
                relay = 'No relay given!'
            if relay == -2:
                relay = 'No valid relay!'
            status = 'Status unused!'
            self.error_response(relay, status)
            return
        if int(status) < 0:
            if status == -1:
                status = self.get_relay(relay)
            if status == -2:
                status = 'No valid status!'
            self.error_response(relay, status)

    def response(self, relay, status):
        """Response to client"""
        # reply with JSON
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(JSON_FORMAT.format(
            num=relay,
            status=status,
        ), 'UTF-8'))

    def error_response(self, relay, status):
        """Response to client"""
        # reply with JSON
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(JSON_FORMAT.format(
            num=relay,
            status=status,
        ), 'UTF-8'))

    def get_relay_value(self, query_components):
        """Gets the relay query value."""
        if 'relay' not in query_components:
            return -1
        relay = query_components["relay"][0]
        try:
            relay_num = int(relay)
            if relay_num > 1 or relay_num < 0:
                raise ValueError('relay out of range!')
        except ValueError:
            return -2
        return relay_num

    def get_status_value(self, query_components):
        """Gets the status query value."""
        if 'status' not in query_components:
            return -1
        status = query_components["status"][0]
        try:
            port_value = int(status)  # dec
            if port_value > 1 or port_value < 0:
                raise ValueError('status out of range!')
        except ValueError:
            return -2
        return port_value

    def set_relay(self, relay, port_value):
        """Sets the relay status value."""
        print("Setting relay {} to {}.".format(relay, port_value))
        self.pifacedigital.relays[relay].value = port_value

    def get_relay(self, relay):
        """Gets the relay status value."""
        return self.pifacedigital.relays[relay].value

def get_my_ip():
    """Returns this computers IP address as a string."""
    ips = subprocess.check_output(GET_IP_CMD, shell=True).decode('utf-8')[:-1]
    return ips.strip()


if __name__ == "__main__":
    # get the port
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    else:
        PORT = DEFAULT_PORT

    # set up PiFace Digital
    PiFaceWebHandler.pifacedigital = pifacedigitalio.PiFaceDigital()

    print("Starting simple PiFace web control at:\n\n"
          "\thttp://{addr}:{port}\n\n"
          .format(addr=get_my_ip(), port=PORT))

    # run the server
    SERVER_ADDRESS = ('', PORT)
    try:
        HTTPD = http.server.HTTPServer(SERVER_ADDRESS, PiFaceWebHandler)
        HTTPD.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        HTTPD.socket.close()
