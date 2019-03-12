#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ImageFap Gallery Downloader 1.0
main module
Working with Python 3.6; not tested with other versions."""

from config import Config
from urlqueue import UrlQueue
from time import time, sleep
from glob import glob
from keyword import iskeyword
from os.path import dirname, join as pjoin, split as psplit, splitext

version = '1.0'

def main():
    print('ImageFap Gallery Downloader '+version)
    config = Config('IFLoad.yaml')


    basedir = dirname(__file__)


#    for name in glob(pjoin(basedir, 'plugins', '*.py')):
    for name in config.get():
        if name == 'common':
            continue

        module = splitext(psplit(name)[-1])[0]
        if not module.startswith('_') and module.isidentifier and not iskeyword(module):
            try:
                __import__('plugins.' + module)
            except:
                print("Failed to import ", 'plugins.' + module)
            else:
                print("Imported " + name)

    print('Ready\n')
   
    from sys import argv
    from json import dumps
    if len(argv) > 1:
        from shelve import open as dbmopen
        from sys import exit
        with dbmopen(config.get()['common']['clipboard'], 'c') as clipboard:
            stamp = str(int(time()))
            entry = { 'type': 'picture',
                      'url': argv[1]
                    }
            clipboard[stamp] = dumps(entry)
        exit(0)

    urlqueue = UrlQueue(config)

    while True:
        """fetch clipboard content and check for new url; add to queue if valid url is detected"""
        try:
            urlqueue.CheckClipboard()
            
            ### check if queue contains a url
            urlqueue.Dispatch()
            
            sleep(0.5)
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__=='__main__':
    main()
        
