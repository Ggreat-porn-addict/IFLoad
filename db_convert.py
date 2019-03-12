#!/usr/bin/env python
from shelve import open as dbmopen
from json import dumps
from sys import argv

if len(argv) > 1:
    with dbmopen('clipboard', 'w') as dbm:
        for k in dbm.keys():
            entry = { 'type': 'picture',
                      'url': dbm[k]
                    }
            dbm[k] = dumps(entry)
else:
    with dbmopen('clipboard', 'r') as dbm:
        for k in dbm.keys():
            print(k, '=', dbm[k])
