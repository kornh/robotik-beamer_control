Simple Web Control
==================

You can control PiFace Digital from a web browser (or any network enabled
device) using the `webcontrol.py` tool.

You can start the tool by running the following command on your Raspberry Pi::

    $ python3 ./webcontrol.py

This will start a simple web server on port 8000 which you can access using
a web browser.

Access:
------------------

Type the following into the address bar of a browser on any machine in the
local network::

### Relay 0:

    http://192.168.178.69:8000/?relay=0

### Relay 1:

    http://192.168.178.69:8000/?relay=1


It will return a `JSON object <http://www.json.org/>`_ describing the current
state of PiFace Digital::

### Relay 0:

    {'relay': 0, 'status': 0}

or

    {'relay': 0, 'status': 1}

### Relay 1:

    {'relay': 1, 'status': 0}

or

    {'relay': 1, 'status': 1}

Controlling Output
------------------
You can set the output port using the URL::

### Relay 0:

    http://192.168.178.69:8000/?relay=0&status=0

or 

    http://192.168.178.69:8000/?relay=0&status=1

### Relay 1:

    http://192.168.178.69:8000/?relay=1&status=0
    
or

    http://192.168.178.69:8000/?relay=1&status=1

Changing Port
-------------
You can specify which port you would like ``webcontrol.py`` to use by
passing the port number as the first argument::

    $ python3 ./webcontrol.py 12345

 https://pypi.python.org/pypi/pifacedigitalio/

 http://piface.github.io/pifacedigitalio/pifacedigital.html
 
 http://piface.github.io/pifacedigitalio/simplewebcontrol.html