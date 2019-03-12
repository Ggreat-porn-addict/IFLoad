#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

### ImageFap Gallery Downloader 0.4
### main module
### Working with Python 2.7; not tested with other versions

import config
import urlqueue
import gallery
from time import sleep

version = '0.4'

def main():
    print('ImageFap Gallery Downloader '+version)
    config.LoadConfig('IFLoad.config')
    print('Ready\n')
   
    from sys import argv
    if len(argv) > 1:
        from shelve import open as dbmopen
        from sys import exit
        with dbmopen(config.clipboard, 'c') as clipboard:
            clipboard[str(config.stamp[0])] = argv[1]
        exit(0)

    while True:
        ### fetch clipboard content and check for new url; add to queue if valid url is detected
        urlqueue.CheckClipboard()
            
        ### check if queue contains a url
        if len(urlqueue.queue): gallery.DownloadGallery()
            
        sleep(0.5)

main()
        
