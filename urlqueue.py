"""ImageFap Gallery Downloader
download queue management."""

from shelve import open as dbmopen
from time import time
from json import loads


plugins = []


def plugin(p):
    if p not in plugins:
        plugins.append(p)


class UrlQueue:

    def __init__(self, config):
        self._configKey = 'common'
        self._stamp = int(time()) 
        self._cnf = config
        self._config = config.get()
        self._queue = []
#        self._last_clipboard = ''


    def getPlugin(self):
        return self._queue[0][0]


    def getUrl(self):
        return self._queue[0][1]


    def getUrlType(self):
        return self._queue[0][2]


    def getDestinationFolder(self):
        return self._queue[0][3]


    def Dispatch(self):
        if len(self._queue):
            self.getPlugin().DownloadGallery(self)


    def PollClipboard(self):
        """Retrieve the current clipboard content"""
        clipb = []
        maxk = self._stamp
        with dbmopen(self._config[self._configKey]['clipboard'], 'r') as clip:
            for k in clip:
                t = int(k) 
                if t > self._stamp:
                    entry = loads(clip[k])
                    if entry['type'] == 'picture':
                        clipb.append(entry['url'])
                    if t > maxk:
                        maxk = t
            self._stamp = maxk
        return clipb


    def PollClipboardTk(self): 
        try:
            from Tkinter import Tk
            clip = Tk()
            clip.withdraw()
            clipb = [ clip.clipboard_get() ]
            clip.destroy()
        except:
            clipb = [] 
        return clipb


    def AddToQueue(self,plugin, url,urltype,destination_folder):
        self._queue+=[[plugin,url,urltype,destination_folder]]


    def RemoveFromQueue(self):
        self._queue.remove(self._queue[0])


    def enqeue(self,url):    
        for p in plugins:
            plugin = p(self._cnf)
            urltype = plugin.Detect(url)
            if urltype:
                plugin.enqueue(self, url, urltype)
                break


    def CheckClipboard(self):
        """ Check if clipboard content has changed.
        Check if the new content is a valid url and add to queue."""
    
#        clipboard = PollClipboard()
            
#        if (clipboard!=self._last_clipboard):
#            self._last_clipboard=clipboard
        for clipboard in self.PollClipboard():
            self.enqeue(clipboard)
#    self._last_clipboard = PollClipboard()
