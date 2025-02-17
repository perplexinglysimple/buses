import time
import  urllib.request, json 
import os

class RotatingFileOpener:
    def __init__(self, path, mode='a', prepend="", append=""):
        if not os.path.isdir(path):
            raise FileNotFoundError("Can't open directory '{}' for data output.".format(path))
        self._path = path
        self._prepend = prepend
        self._append = append
        self._mode = mode
        self._day = '04'
    def __enter__(self):
        self._filename = self._format_filename()
        self._file = open(self._filename, self._mode)
        return self
    def __exit__(self, *args):
        return getattr(self._file, '__exit__')(*args)
    def _day_changed(self):
        return self._day == time.strftime('%H')
    def _format_filename(self):
        return os.path.join(self._path, "{}{}{}".format(self._prepend, time.strftime("%Y%m%d"), self._append))
    def write(self, *args):
        if self._day_changed():
            self._file.close()
            self._file = open(self._format_filename(), self.mode)
        return getattr(self._file, 'write')(*args)
    def __getattr__(self, attr):
        return getattr(self._file, attr)
    def __iter__(self):
        return iter(self._file)


#https://github.com/perplexinglysimple/buses
bus_codes = ['HWA','HWB','HWD','CRC']

file = RotatingFileOpener('./', prepend='bus_data-', append='.txt')
with file as logger:
    while True:
      try:
        for items in bus_codes:
          with urllib.request.urlopen("https://commonlayer.bt4u.org/routes/" + items) as url:
            data = url.read()
            print("data read for time" + str(time.time()))
            logger.write(data.decode("utf-8"))
      except urllib.error.URLError:
        print("url failed")
      time.sleep(500)
