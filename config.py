from os import path
from yaml import load

"""ImageFap Gallery Downloader configuration."""

class Config:
    def __init__(self, filename):
        """Load configuration from config file and overwrite default
        values with values from the file."""
        self._config = {} 
### default config
        self._configKey = 'common'
        self._defaults = {
            'clipboard' : 'clipboard',
            'useragent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
            'MainDirectory' : 'Galleries',
            'UserDirectory' : 'UserFolders'
        }

        if (not path.exists(filename)):
            print(filename + " not found; using default configuration\n")
            return

        with open(filename, "r") as f:
            self._config = load(f)
            self.merge(self._configKey, self._defaults)


        from shelve import open as dbmopen
        with dbmopen(self._config['common']['clipboard'], 'c') as dummy:
            pass


    def merge(self, configKey, defaults):
        for k in defaults.keys():
            if k not in self._config[configKey]:
                self._config[configKey][k] = defaults[k]


    def get(self):
        return self._config

