"""ImageFap Gallery Downloader
General purpose download function."""

from os import path, makedirs
from request import Request
from time import sleep

def DownloadImage(config,url,Dir,attempts=3):
    success = False
    r = Request(config)
    for k in range(attempts):
        pic = r.ReqUrl(url)
        if pic is not None and pic!=[]:
            success = True
            break
        else:
            sleep(1)

    if success:    
        """create output directory if it doesn't exist"""
        if not path.exists(Dir):
            makedirs(Dir)
        i=0
        while True:
            _i = i
            i = url.find('/',i+1)
            if (i==-1): break

        fname = url[_i+1:]
        _path = Dir+'/'+fname

        while True:
            """check if file already exists, in which case progressing numbers are added to the new filename to avoid overwriting of older files."""
            pic_num = 0
            if not pic:
                return False

            if not path.exists(_path):
                f = open(_path,'wb')
                f.write(pic)
                f.close()
                break
            else:
                pic_num+=1
                k = fname.find('.')
                fn1 = fname[:k]
                ext = fname[k:]
                fname = fn1+str(pic_num)+ext
                _path = Dir+'/'+fname
        return True
    else:
        return False
