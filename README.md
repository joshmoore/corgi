Redmine Github Integration
==========================

Simple Tornado server that listens to Github pull request events and updates
referenced Redmine issues.

Requirements
------------

python-dateutil
simplejson
six
tornado
pyredminews
configobj

Installation
------------

1. Clone the repository:

        git clone git@github.com:glencoesoftware/corgi.git

2. Use [virtualenv](https://pypi.python.org/pypi/virtualenv) to create an isolated Python environment for required libraries:

        curl -O -k https://raw.github.com/pypa/virtualenv/master/virtualenv.py
        python virtualenv.py corgi-virtualenv
        source corgi-virtualenv/bin/activate
        pip install -r requirements.txt

3. Register hook

    See sample-subscribe.sh

4. Add user mappings

    In server.cfg, add a mapping for each GitHub user to the corresponding Redmine user

Startup
-------

[todo]
