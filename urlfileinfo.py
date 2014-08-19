
def createUrlFileInfoByUrl(url, fileName = None, fileSize = 0, urlLoader = None):
    name = fileName
    if name == None:
        name = ''

    info = UrlFileInfo(remotePath = url,
                       fileName = name,
                       fileSize = fileSize,
                       urlLoader = urlLoader)

    return info

        

class UrlFileInfo:
    '''
    keep remote downloading file information
    '''

    def __init__(self, remotePath = '', fileName = '', fileSize = 0,
                 urlLoader = None):
        self.setFileName(fileName)
        self.setRemotePath(remotePath)
        self.setFileSize(fileSize)
        self.setUrlLoader(urlLoader)

    def getRemotePath(self):
        return self._remotePath

    def setRemotePath(self, path):
        self._remotePath = path

    def setFileName(self, name):
        self._fileName = name

    def getFileName(self):
        return self._fileName

    def setUrlLoader(self, loader):
        self._urlLoader = loader

    def getUrlLoader(self):
        return self._urlLoader

    # unit 'Byte'
    def getFileSize(self):
        return self._size
    
    def setFileSize(self, size):
        self._size = size

    def toString(self):
        res = ''
        res += '[url file]\n'
        res += 'name:' + self.getFileName() + '\n'
        res += 'size:' + str(self.getFileSize()) + '\n'
        res += 'remote path:' + self.getRemotePath() + '\n'
        res += 'url loader:' + str(self.getUrlLoader()) + '\n'

        return res
