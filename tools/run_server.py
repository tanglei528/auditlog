#! /usr/bin/python
import os
import sys

root = os.path.join(os.path.dirname(__file__), '..')
if root not in sys.path:
    sys.path.append(root)

from auditlog.cli import api

if __name__ == '__main__':
    sys.exit(api())
