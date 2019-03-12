### ImageFap Gallery Downloader
### request url content

import config
import urllib.request
    
def ReqUrl(urlstr, encoding=None):
    if (urlstr[:8] != "https://"): urlstr="https://"+urlstr
    req = urllib.request.Request(urlstr)
    ### spoof user-agent and try to appear as mozilla firefox
    req.add_header('User-Agent', config.useragent)
    opnr = urllib.request.build_opener()
    ### Request contents of url
    try:
        dat = opnr.open(req).read()
    except Exception as E:
        print("Exception: ", urlstr, str(E))
        return
#        dat = []
    if encoding:
        return dat.decode(encoding)
    else:
        return dat

