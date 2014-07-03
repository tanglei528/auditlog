Audit Log
=============

Auditlog is a service to collect, query operations of users in tenants.
It filters each request to the Openstack API services and stores them.
Now, it supports all the API services that Openstack provides.


Quick Start
=============

Run the command to prepare virtualenv:

python tools/install_venv.py

Copy etc/auditlog/auditlog.conf into /etc/auditlog/, and change owner to you.

Edit auditlog.conf according to your environment, such as auditlog_connection, auth_host etc.

Run this command to start api server.

source .venv/bin/activate
python tools/run_server.py

Then your can access api through http://localhost:8800/v1/

Run tests
============

Auditlog uses tox to manage virtualenv for testing and uses unittest as
the main test framework.
To run all tests, run:

tox --develop

To do code style check, run:

tox -e pep8

To analyse test code coverage, run:

tox- e cover --develop

Then open cover/index.html in your favorite browser.

Debug source code
============

Insert this line into the location you want to break:

import pdb; pdb.set_trace()

Run all tests, then the programe will break into pdb debugger environment.

CAUTION:
DON'T LEAVE ANY DEBUG LINE IN THE CODE, IT WILL CAUSE RUNTIME ERROR.
