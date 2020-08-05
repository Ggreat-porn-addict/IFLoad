from request import Request
from gallery import Gallery
from urlqueue import plugin

@plugin
class NudeCollect(Gallery):
    _defaults = {
        'GalleryLink' : 'gesek.net/album/',
        'BaseUrl' : 'http://www.gesek.net/',
        'ForceLatin1' : 'False'
    }

    def __init__(self, config):
        super().__init__(__name__, config)
        self._url = None


    def Detect(self, url):
        """Check if url looks like a gallery url"""
        detected = url.find(self._config[self.configKey()]['GalleryLink'])!=-1
        if detected:
            baseUrl = self._config[self.configKey()]['BaseUrl']
            section = url.replace(baseUrl, '')
            i = 0
            while section[i] != '/':
                i += 1
            self._url = baseUrl + section[:i + 1] 
        return detected 


    def getGalleryTitle(self, PageTitle):
        """Format the gallery title.""" 
        q = PageTitle.find(' - Gesek.Net')
        if (q!=-1):
            return PageTitle[:q]
        else:
            return PageTitle


    def GetGalleryId(self, url, gidtype):
        gid_index = url.find('/album/')
        gid = url[gid_index+7:]
        return gid


    def GetImageList(self,url,gid):
        """Returns list of images in gallery page content"""
        UrlList=[]

        request = Request(self._config)
        PageContent = request.ReqUrl(url, 'utf-8')

#        print(PageContent)
        index_end = PageContent.find('class=\'image\'')
        while True:
            """Find html entries with 'idx=' string indicating image link."""
            index_begin = PageContent.find('href="',index_end)
            if (index_begin==-1): break
            index_begin += 6
        
            index_end = PageContent.find('"',index_begin)
            pic = PageContent[index_begin:index_end]
            if (len(pic)>1) and pic.startswith('http'): UrlList.append(pic)
        
        return UrlList


    def GetImageUrl(self, UrlList, UrlNum):
        """Get image source URL"""
        return UrlList[UrlNum]

