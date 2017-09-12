from __future__ import print_function
import os
import time
import  urllib.request, json 
import git

class drive:
    def __init__(self):
        self.repo = git.Repo( './' )
    def upload_file(self, file, filename):
        self.repo.git.add(  filename )
        self.repo.git.commit( m= filename + ' Is the file for this day')
        self.repo.git.push()

class RotatingFileOpener:
    def __init__(self, path, mode='a', prepend="", append=""):
        if not os.path.isdir(path):
            raise FileNotFoundError("Can't open directory '{}' for data output.".format(path))
        self._path = path
        self._prepend = prepend
        self._append = append
        self._mode = mode
        self._day = time.localtime().tm_mday
        self.drive = drive()
    def __enter__(self):
        self._filename = self._format_filename()
        self._file = open(self._filename, self._mode)
        return self
    def __exit__(self, *args):
        return getattr(self._file, '__exit__')(*args)
    def _day_changed(self):
        return self._day != time.localtime().tm_mday
    def _format_filename(self):
        return os.path.join(self._path, "{}{}{}".format(self._prepend, time.strftime("%Y%m%d"), self._append))
    def write(self, *args):
        if self._day_changed():
            self._file.close()
            self.drive.upload_file(self._file, self._filename)
            self._file = open(self._format_filename(), self.mode)
        return getattr(self._file, 'write')(*args)
    def __getattr__(self, attr):
        return getattr(self._file, attr)
    def __iter__(self):
        return iter(self._file)


#https://github.com/perplexinglysimple/buses

file = RotatingFileOpener('./', prepend='bus_data-', append='.txt')
with file as logger:
    while True:
        with urllib.request.urlopen("https://commonlayer.bt4u.org/livemap?bt4uid=0x5796895884c00000&_=1504750958763") as url:
            data = url.read()
            print(data)
            logger.write(data.decode("utf-8"))
            time.sleep(45)
