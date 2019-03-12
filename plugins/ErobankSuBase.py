from request import Request
from gallery import Gallery
from urlqueue import plugin

class ErobankSuBase(Gallery):
    _defaults = {
        'GalleryLink' : 'erobank.su',
        'ForceLatin1' : 'False'
    }

    def __init__(self, name, config):
        super().__init__(name, config)


    def OpenGallery(self, url, urltype, encoding='CP1251', proto='http://'):
        return super().OpenGallery(url, urltype, encoding, proto)


    def Detect(self, url):
        """Check if url looks like a gallery url"""
        return url.find(self._config[self.configKey()]['GalleryLink'])!=-1


    def getGalleryTitle(self, PageTitle):
        """Format the gallery title.""" 
        q = PageTitle.find(' (Page')
        if (q!=-1):
            return PageTitle[13:q]
        else:
            return PageTitle


    def GetGalleryId(self, url, gidtype):
        urlhead = self._config[self.configKey()]['baseurl']+'/'
        gid_index = url.find(urlhead)
        gid = url[gid_index+len(urlhead):]

        return gid


    def GetImageList(self,url,gid):
        """Returns list of images in gallery page content"""
        UrlList=[]

        request = Request(self._config)
        PageContent = request.ReqUrl(url, 'CP1251', proto="http://")

        """iterate through gallery pages"""
        index_begin=0
        index_end=0
        while True:
            """Find html entries with 'idx=' string indicating image link."""
            index_begin = PageContent.find('<div class="pic">',index_end)
            if (index_begin==-1): break
            index_begin = PageContent.find('<a href="', index_begin)
            if (index_begin==-1): break

            index_end = PageContent.find('" target="_blank">',index_begin)
            i = index_end-1
            while (PageContent[i]!='"'):
                i=i-1
            pic = PageContent[i+1:index_end]
            if (len(pic)>1):
                UrlList.append(self._config[self.configKey()]['baseurl'] + pic)

        return UrlList


    def GetImageUrl(self, UrlList, UrlNum):
        """Get image source URL"""
        request = Request(self._config)
        PageContent = request.ReqUrl(UrlList[UrlNum], 'CP1251', proto='http://')
        url_index = PageContent.find('<img style="')
        url_start = PageContent.find(' src="',url_index) + 6
        url_end = PageContent.find('"',url_start)
        return 'http://' + self._config[self.configKey()]['baseurl'] + PageContent[url_start:url_end]

