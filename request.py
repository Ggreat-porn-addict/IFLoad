"""ImageFap Gallery Downloader
request url content."""

from urllib import request as rq

class Request:    
    def __init__(self, config):
        self._configKey = 'common'
        self._config = config


    def ReqUrl(self, urlstr, encoding=None, proto='https://'):
        if not urlstr.startswith('https://') and \
           not urlstr.startswith('http://'): urlstr=proto+urlstr
        req = rq.Request(urlstr)
        ### spoof user-agent and try to appear as mozilla firefox
        req.add_header('User-Agent', self._config[self._configKey]['useragent'])
        opnr = rq.build_opener()
        ### Request contents of url
        try:
            dat = opnr.open(req).read()
        except Exception as E:
            print("Exception: ", urlstr, str(E))
            return
        if encoding:
            return dat.decode(encoding)
        else:
            return dat

