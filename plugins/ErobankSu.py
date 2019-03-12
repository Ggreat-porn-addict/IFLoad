from plugins.ErobankSuBase import ErobankSuBase
from urlqueue import plugin

@plugin
class ErobankSu(ErobankSuBase):
    def __init__(self, config):
        super().__init__(__name__, config)

