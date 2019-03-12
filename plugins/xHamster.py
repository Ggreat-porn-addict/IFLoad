from request import Request
from gallery import Gallery
from urlqueue import plugin

@plugin
class xHamster(Gallery):
    _defaults = {
        'ForceLatin1': 'False',
        'GalleryLink' : 'xhamster.com/photos/gallery/'
    }

    def __init__(self, config):
        super().__init__(__name__, config)
        from requests_html import HTMLSession
        self._session = HTMLSession()


    def Detect(self, url):
        """Check if url looks like a gallery url"""
        return (url.find(self._config[self.configKey()]['GalleryLink'])!=-1)


    def getGalleryTitle(self, PageTitle):
        """Format the gallery title.""" 
        return PageTitle[:len(PageTitle)-15]


    def GetGalleryId(self, url, gidtype):
        """gidtype: 1=xhamster"""

        if (gidtype==1):
            start = url.find('gallery')+8
            end = url.find('/',start)
            gid = url[start:end]

        return gid


    def GetImageList(self,url,gid):
        """Returns list of images in xhamster gallery"""
        UrlList=[]
        request = Request(self._config)
        PageContent = request.ReqUrl(url, 'utf-8')

        imglink_begin=0
        imglink_end=0
        pics = []

        while True:
            """find location of image page link"""
            index_link = PageContent.find("photo-container photo-thumb",imglink_end)
            if (index_link==-1): break 
            imglink_begin = PageContent.find("href=",index_link)+6
            imglink_end = PageContent.find("\"",imglink_begin)
            pic = PageContent[imglink_begin:imglink_end]
            if (len(pic)>1): pics+=[pic]
        UrlList+=pics
        return UrlList


    def ReopenSession(self, url):
        from requests_html import HTMLSession
        self._session = HTMLSession() 
        return self._session.get(url)


    def GetImageUrl(self, UrlList, UrlNum):
        """Get image source URL."""
        from pyppeteer.errors import PageError
        #PageContent = request.ReqUrl(UrlList[UrlNum], 'utf-8')
        r = self._session.get(UrlList[UrlNum])
        try:
            r.html.render(timeout=90)
        except ConnectionError as e:
                r.html.render(timeout=90)
        except PageError as e:
            r = self.ReopenSession(UrlList[UrlNum])
            r.html.render(timeout=90)
        except Exception as e:
            print("Unknown exception!", str(e))
            r = self.ReopenSession(UrlList[UrlNum])
            r.html.render(timeout=90)

        PageContent = r.html.html
        url_index = PageContent.find("fotorama__loaded--img")
        url_start = PageContent.find("https://",url_index)
        url_end = PageContent.find("\"",url_start)
        return PageContent[url_start:url_end]
    
