CORGI Integrator
================

Simple Tornado server that listens for webhook events and
processes them giving configured services a chance to
react.

Requirements
------------

    python-dateutil
    simplejson
    tornado
    configobj
    blinker

Each installed service may have its own requirements.

Installation
------------

1. Clone the repository:

        git clone git@github.com:glencoesoftware/corgi.git

2. Use [virtualenv](https://pypi.python.org/pypi/virtualenv) to create an isolated Python environment for required libraries:

        curl -O -k https://raw.github.com/pypa/virtualenv/master/virtualenv.py
        python virtualenv.py corgi-virtualenv
        source corgi-virtualenv/bin/activate
        pip install -r requirements.txt

3. Install services

    Each inidividual service must be installed on the PYTHONPATH.
    See each for installation instructions, configuartion, and
    possible hook registration.

4. Start ./server.py
