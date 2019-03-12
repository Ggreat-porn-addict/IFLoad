#!/usr/bin/env python
from shelve import open as dbmopen
from time import time
from json import dumps
from sys import argv,exit

if len(argv) < 4:
    print("%s <url> <title> <src>" % (argv[0],))
    exit(0)

stamp = str(int(time()))

entry = { 'type': 'mp4',
          'url': argv[1],
          'title': argv[2],
          'src': argv[3]
        }

with dbmopen('clipboard', 'w') as dbm:
    dbm[stamp] = dumps(entry)

