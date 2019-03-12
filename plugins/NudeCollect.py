from request import Request
from gallery import Gallery
from urlqueue import plugin

@plugin
class NudeCollect(Gallery):
    _defaults = {
        'GalleryLink' : 'nudecollect.com',
        'BaseUrl' : 'http://www.nudecollect.com/',
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


    def _getFullUrl(self, url):
        sane = url.replace('../', '')
        return self._url + sane 


    def getGalleryTitle(self, PageTitle):
        """Format the gallery title.""" 
        q = PageTitle.find(' | Nude Collect')
        if (q!=-1):
            return PageTitle[:q]
        else:
            return PageTitle


    def GetGalleryId(self, url, gidtype):
        gid_index = url.find('/category/')
        gid = url[gid_index+10:]
        return gid


    def _nextPage(self,PageContent):
        """Check for a link to the next page of a gallery.
        returns 0 if no link is found, otherwise returns
        a string containing the url."""
        pagination_bar = PageContent.find('pagination pagination-centered')
        if (pagination_bar==-1):
            return
        else:
            np_index_end = PageContent.find('" rel="next"', pagination_bar)
            if np_index_end == -1: np_index_end = PageContent.find('>Next<', pagination_bar)
            np_index_start = np_index_end - 1
            while PageContent[np_index_start] != '"':
                np_index_start-=1
            np_index_start += 1
            url1 = PageContent[np_index_start:np_index_end]
            if url1 == '#':
                return

            return self._getFullUrl(url1)


    def GetImageList(self,url,gid):
        """Returns list of images in gallery page content"""
        UrlList=[]

        request = Request(self._config)
        PageContent = request.ReqUrl(url, 'utf-8')

        while True:
            """iterate through gallery pages"""
            index_begin=0
            index_end=0
            pics = []
            while True:
                """Find html entries with 'idx=' string indicating image link."""
#                print(PageContent)
                img_class = PageContent.find('class="col-thumbnail"',index_end)
                index_begin = PageContent.find('href="',img_class)
                if (index_begin==-1): break
                index_begin += 6
            
                index_end = PageContent.find('"',index_begin)
                pic = PageContent[index_begin:index_end]
                if (len(pic)>1): pics+=[self._getFullUrl(pic)]
            UrlList+=pics
        
            np_url = self._nextPage(PageContent)
        
            if np_url is None:
                break
            else:
                url = np_url
                #print url
                PageContent = request.ReqUrl(url, 'utf-8')
        return UrlList


    def GetImageUrl(self, UrlList, UrlNum):
        """Get image source URL"""
        request = Request(self._config)
        PageContent = request.ReqUrl(UrlList[UrlNum], 'utf-8')
        url_index = PageContent.find('theImage')
        url_start = PageContent.find('img src="',url_index)
        url_start += 9
        url_end = PageContent.find('"',url_start)
        return self._getFullUrl(PageContent[url_start+1:url_end])

