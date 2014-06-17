Audit Log
=============

Auditlog is a service to collect, query operations of users in tenants.
It filters each request to the Openstack API services and stores them.
Now, it supports all the API services that Openstack provides.


Quick Start
=============

Run the command to prepare virtualenv:

python tools/install_venv.py


Run tests
============

Auditlog uses tox to manage virtualenv for testing and uses unittest as
the main test framework.
To run all tests, run:

tox

To do code style check, run:

tox -e pep8

Debug source code
============

Insert this line into the location you want to break:

import pdb; pdb.set_trace()

Run all tests, then the programe will break into pdb debugger environment.
