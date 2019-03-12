from request import Request
from gallery import RemoveBlank
from plugins.IFUserBase import IFUserBase 
from urlqueue import plugin

@plugin
class IFFolder(IFUserBase):
    _defaults = {
        'IFFolder1' : 'www.imagefap.com/organizer/',
        'IFFolder2' : 'folderid='
    }


    def Detect(self,url):
        if (url.find(self._config[self.configKey()]['IFFolder1'])!=-1):
            return 5 #IFFolder1
        elif (url.find(self._config[self.configKey()]['IFFolder2'])!=-1):
            return 6 #IFFolder2
        else:
            return 0


    def enqueue(self, queue, FolderUrl, urltype):
        UserName, FolderName, Galleries = self._ListFolderGalleries(FolderUrl)
        for _gal in Galleries:
            queue.AddToQueue(self,_gal,3,
                self._config['common']['MainDirectory'] + "/" +
                self._config['common']['UserDirectory'] + "/" +
                UserName + "/" + FolderName)


    def _GetFolderName(self, htmldata):
        folderid="folderid=0"
        j=0
        k=0
        while (folderid == "folderid=0"):
            j = htmldata.find("folderid=",k)
            k = htmldata.find('"',j)
            folderid=htmldata[j:k]
        j = htmldata.find("<b>",k)
        k = htmldata.find("</b>",j)
        return htmldata[j+3:k]

    
    def _ListFolderGalleries(self, FolderUrl):
        request = Request(self._config)
        htmldata = request.ReqUrl(FolderUrl, 'utf-8')
        UserName = self._GetUsername(htmldata)
        FolderName = self._GetFolderName(htmldata)
        Galleries = []
        j=0
        k=0
        while True:
            j = htmldata.find("/gallery/",k)
            if (j==-1):break
            k = htmldata.find('"',j)
            GalleryUrl = self._config[self.configKey()]['baseurl']+htmldata[j:k]

            if not(GalleryUrl in Galleries):
                Galleries+=[GalleryUrl]
            
        return RemoveBlank(UserName), RemoveBlank(FolderName), Galleries

