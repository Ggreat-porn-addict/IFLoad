from request import Request
from gallery import Gallery
from urlqueue import plugin

@plugin
class HentaiComic(Gallery):
    _defaults = {
        'GalleryLink' : 'hentai-comic.com',
        'ForceLatin1' : 'False'
    }

    def __init__(self, config):
        super().__init__(__name__, config)


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
#https://fr.hentai-comic.com/image/my-aunts-body-is-irresistible--her-hole-is-the-best--bonus--oba-san-no-karada-ga-kimochi-yosugiru-kara--boku-no-oba-san-wa-chou-meiki-datta-
        gid_index = url.find('/image/')
        gid = url[gid_index+7:]

        return gid


    def _NextPage(self,PageContent,gid,currentpage):
        """Check for a link to the next page of a gallery.
        returns 0 if no link is found, otherwise returns
        a string containing the url."""
        np_index_start = PageContent.find('page='+str(currentpage+1))
        if (np_index_start==-1):
            return 0
        else:
            np_index_start = PageContent.find(self._config[self.configKey()]['GalleryLink2'])
            np_index_end = PageContent.find("'",np_index_start)
            url1 = PageContent[np_index_start:np_index_end]
            url2 = '?gid='+str(gid)+'&page='+str(currentpage+1)+'&view=0'
            return url1+url2

    def GetImageList(self,url,gid):
        """Returns list of images in gallery page content"""
        UrlList=[]

        request = Request(self._config)
        PageContent = request.ReqUrl(url, 'utf-8')

        p = 0
    
        while True:
            """iterate through gallery pages"""
            index_begin=0
            index_end=0
            pics = []
            while True:
                """Find html entries with 'idx=' string indicating image link."""
                print(PageContent)
                index_begin = PageContent.find('idx=',index_end)
                if (index_begin==-1): break
            
                index_end = PageContent.find('"',index_begin)
                i = index_begin
                while (PageContent[i]!='"'):
                    i=i-1
                pic = PageContent[i+1:index_end]
                if (len(pic)>1): pics+=[str(self._config[self.configKey()]['baseurl'])+pic]
            UrlList+=pics
        
            np_url = self._NextPage(PageContent,gid,p)
        
            if (np_url==0):
                break
            else:
                url = np_url
                #print url
                p+=1
                PageContent = request.ReqUrl(url, 'utf-8')
        return UrlList


    def GetImageUrl(self, UrlList, UrlNum):
        """Get image source URL"""
        request = Request(self._config)
        PageContent = request.ReqUrl(UrlList[UrlNum], 'utf-8')
        url_index = PageContent.find('contentUrl')
        url_start = PageContent.find('https://',url_index)
        url_end = PageContent.find('"',url_start)
        return PageContent[url_start:url_end]



