from plugins.ErobankSuBase import ErobankSuBase
from urlqueue import plugin
from request import Request

@plugin
class ErobankSuModel(ErobankSuBase):
    def __init__(self, config):
        super().__init__(__name__, config)

    def enqueue(self, queue, url, urltype):
        request = Request(self._config)
        PageContent = request.ReqUrl(url, 'CP1251', proto="http://")

        """iterate through gallery pages"""
        index_begin=0
        index_end=0
        while True:
            """Find html entries with 'idx=' string indicating image link."""
            index_begin = PageContent.find('<div class="galleryThumb">',index_end)
            if (index_begin==-1): break
            index_begin = PageContent.find('<a href="', index_begin)
            if (index_begin==-1): break

            index_end = PageContent.find('" onmouseout="',index_begin)
            i = index_end-1
            while (PageContent[i]!='"'):
                i=i-1
            pic = PageContent[i+1:index_end]
            if (len(pic)>1):
                super().enqueue(queue, self._config[self.configKey()]['baseurl'] + pic, 1)
