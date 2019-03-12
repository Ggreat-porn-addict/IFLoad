# -*- coding: utf-8 -*-

"""ImageFap Gallery Downloader
image gallery processing."""

from download import DownloadImage
from request import Request
from sys import stdout
from os.path import splitext, join as pjoin, split as psplit


def RemoveBlank(string):
    Str = string
    while True:
        if (Str.startswith(' ')):
            Str = Str[1:]
        else: break

    while True:
        if (Str.endswith(' ')):
            Str = Str[:len(Str)-1]
        else: break

    return Str


class Gallery:
    def __init__(self, name, config):
        self._name = name
        config.merge(self.configKey(), self._defaults)
        self._config = config.get()


    def GetGalleryTitle(self,data):
        title_start = data.find('<title>')
        title_end = data.find('</title>',title_start)
        PageTitle = data[title_start+7:title_end]

        _galtitle = self.getGalleryTitle(PageTitle)

        ### remove forbidden characters so the title can be
        ### used as folder name
        gallerytitle=''

        # FIXME: isalnum() or something, via common config switch
        char_allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ДЦЬдць#+~.,-_^!§$%&()={}[]@ "
    
        for char in _galtitle:
            if self._config[self.configKey()]['ForceLatin1']=='True':
                if char in char_allowed:
                    gallerytitle+=char
            else:
                if char.isalnum() or char.isspace() or char in '#+~.,-_^!§$%&()={}[]@':
                    gallerytitle+=char

        ### remove blank characters from start and end of title string
        gallerytitle = RemoveBlank(gallerytitle)
    
        return gallerytitle


    def OpenGallery(self, Gal_Url, urltype, encoding='utf-8', proto='https://'):
        """Get gallery title and list of image URLs"""

        url = Gal_Url
        gid = self.GetGalleryId(url,urltype)
        request = Request(self._config)
        PageContent = request.ReqUrl(url, encoding, proto)
    
        ### read gallery title from html content
        GalTitle = self.GetGalleryTitle(PageContent)

        ### get image list from gallery page
        UrlList = self.GetImageList(url,gid)
    
        return GalTitle, UrlList


    def DownloadGallery(self, urlqueue):
        """Get first element from url queue."""
        Gal_Url = urlqueue.getUrl()
        urltype = urlqueue.getUrlType()
        destination_folder = urlqueue.getDestinationFolder()
        GalTitle, UrlList = self.OpenGallery(Gal_Url, urltype)
        output_dir = destination_folder+"/"+GalTitle

        urlqueue.CheckClipboard()

        N = len(UrlList)
        print("Downloading "+str(N)+" images from "+Gal_Url)

        for j in range(N):
            url = self.GetImageUrl(UrlList,j)

            if DownloadImage(self._config,url,output_dir):
                stdout.write(".")
            else:
                stdout.write("x")

            stdout.flush()
            urlqueue.CheckClipboard()

        ### remove element from url queue after download
        urlqueue.RemoveFromQueue()
        print("\n"+"Done"+"\n")


    def configKey(self):
        return self._name.split('.').pop()


    def GetDir(self, dir):
        return pjoin(dir, self.configKey())


    def enqueue(self, queue, url, urltype):
        """Add url to queue."""
        queue.AddToQueue(self,url,urltype,self.GetDir(self._config['common']['MainDirectory']))


    def getGalleryTitle(self, PageTitle):
        raise NotImplementedError("Must override getGalleryTitle.")


    def GetImageUrl(self,UrlList,j):
        raise NotImplementedError("Must override GetImageUrl.")


    def GetGalleryId(self, url, gidtype):
        raise NotImplementedError("Must override GetGalleryId.")


    def GetImageList(self,url,gid):
        raise NotImplementedError("Must override GetImageList.")


    def Detect(self,url):
        """Check if url looks like a gallery url"""
        raise NotImplementedError("Must override Detect.")

