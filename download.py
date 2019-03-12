### ImageFap Gallery Downloader
### General purpose download function

from os import path, makedirs
import request
import time

def DownloadImage(url,Dir,attempts=3):
    success = 0
    for k in range(attempts):
        pic = request.ReqUrl(url)
        if (pic!=[]):
            success = 1
            break
        else:
            time.sleep(1)

    if success:    
        ### create output directory if it doesn't exist
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
            ### check if file already exists, in which case progressing numbers are added to the new filename to avoid overwriting of older files.
            pic_num = 0
            if not pic:
                return 0 

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
        return 1
    else:
        return 0
