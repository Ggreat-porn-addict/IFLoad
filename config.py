from os import path
from time import time
### ImageFap Gallery Downloader configuration

### default config
useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
baseurl = 'www.imagefap.com'
php = '/gallery.php'
pics = '/pictures/'
GalleryLink1 = 'www.imagefap.com/gallery.php?gid='
GalleryLink2 = 'www.imagefap.com/pictures/'
GalleryLink3 = 'xhamster.com/photos/gallery/'
GalleryLink4 = 'www.imagefap.com/gallery/'
IFUserLink = 'www.imagefap.com/profile/'
IFFolder1 = 'www.imagefap.com/organizer/'
IFFolder2 = 'folderid='
MainDirectory = 'Galleries'
UserDirectory = 'UserFolders'
clipboard = 'clipboard'

def LoadConfig(filename):
    ### load configuration from config file and overwrite default
    ### values with values from the file
    
    global stamp
    stamp = [ int(time()) ]
    from shelve import open as dbmopen
    with dbmopen(clipboard, 'c') as dummy:
        pass

    if (path.exists(filename)):
        f = open(filename,'r')
        ConfigFileContent = []
        ConfigFileContent = f.readlines()
   
        for j in range(len(ConfigFileContent)):
            paramstr = ConfigFileContent[j]
            index_equal = paramstr.find('=')
            if (index_equal!=-1):
                par = paramstr[:index_equal].replace(' ','') 
                _pvalue = paramstr[index_equal+1:]
                val_start = _pvalue.find('"')
                val_end = _pvalue.find('"',val_start+1)
                pvalue = _pvalue[val_start+1:val_end]
                
                if (par=='useragent'):
                    global useragent
                    useragent = pvalue
                if (par=='baseurl'):
                    global baseurl
                    baseurl = pvalue
                if (par=='php'):
                    global php
                    php = pvalue
                if (par=='pics'):
                    global pics
                    pics = pvalue
                if (par=='MainDirectory'):
                    global MainDirectory
                    MainDirectory = pvalue
                if (par=='UserDirectory'):
                    global UserDirectory
                    UserDirectory = pvalue
                    
                if (par=='GalleryLink1'):
                    global GalleryLink1
                    GalleryLink1 = pvalue
                if (par=='GalleryLink2'):
                    global GalleryLink2
                    GalleryLink2 = pvalue
                if (par=='GalleryLink3'):
                    global GalleryLink3
                    GalleryLink3 = pvalue
                if (par=='IFUserLink'):
                    global IFUserLink
                    IFUserLink = pvalue
                if (par=='GalleryLink4'):
                    global GalleryLink4
                    GalleryLink4 = pvalue
                if (par=='IFFolder1'):
                    global IFFolder1
                    IFFolder1 = pvalue
                if (par=='IFFolder2'):
                    global IFFolder2
                    IFFolder2 = pvalue
        f.close()
    else:
        print(filename + " not found; using default configuration\n")
