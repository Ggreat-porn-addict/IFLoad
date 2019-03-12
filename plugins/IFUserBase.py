from request import Request
from gallery import RemoveBlank
from plugins.ImageFapBase import ImageFapBase
from urlqueue import plugin

class IFUserBase(ImageFapBase):
    _defaults = {
        'IFUserLink' :  'www.imagefap.com/profile/',
    }


    def __init__(self, config):
        super().__init__('plugins.ImageFap', config) 


    def Detect(self,url):
        if (url.find(self._config[self.configKey()]['IFUserLink'])!=-1):
            return 7 #IFUser
        else:
            return 0


    def enqueue(self, queue, FolderUrl, urltype):
        Username, Folders = self._ListUserFolders(FolderUrl)
        for _folder in Folders:
             super().enqueue(queue, _folder[1], 3)


    def _ListUserFolders(self, ProfileUrl):
        request = Request(self._config)
        htmldata = request.ReqUrl(ProfileUrl, 'utf-8')
        Username = self._GetUsername(htmldata)
    
        galleries_searchstring = "/usergallery.php"
        start = htmldata.find(galleries_searchstring)
        end = htmldata.find('"',start)

        GalsUrl = self._config[self.configKey()]['baseurl']+htmldata[start:end]
        htmldata = request.ReqUrl(GalsUrl, 'utf-8')

        j=0
        k=0
    
        folderid = ''
        Folders = []
        while (folderid!="folderid=-1"):
            j = htmldata.find("folderid=",k)
            k = htmldata.find('"',j)
            folderid = htmldata[j:k]
            J = j
            l=-1
            while (l==-1):
                J=J-10
                l = htmldata[J:k].find("https:")
        
            FolderUrl = htmldata[l+J:k]

            if (folderid!="folderid=0" and len(folderid)>0):
                n = htmldata.find(">",k)
                m = htmldata.find("<",n)
                FolderName = htmldata[n+1:m]
                Folders+=[[FolderName,FolderUrl]]
            
        return Username, Folders


    def _GetUsername(self, htmldata):
        titlestr = "<title>"
        start = htmldata.find(titlestr)
        end = htmldata.find("&#039;",start)
        return htmldata[start+len(titlestr):end]

