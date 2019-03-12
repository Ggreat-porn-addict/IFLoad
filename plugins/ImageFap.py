from plugins.ImageFapBase import ImageFapBase
from urlqueue import plugin

@plugin
class ImageFap(ImageFapBase):
    def __init__(self, config):
        super().__init__(__name__, config)

