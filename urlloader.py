'''
    define connections for http downloading
'''


from user import User
import urllib


class UrlLoader:

    GLOBAL_ID = 0

    def __init__(self, url = '', user = None, proxy = {}):
        self._id = UrlLoader.GLOBAL_ID
        UrlLoader.GLOBAL_ID += 1

        self.setUrl(url)
        self._content = '' # may not be used
        self._user = user
        self._cookie = None
        self._loadFinished = False
        self._proxy = proxy


    def setUrl(self, url):
        self._url = url

    def getUrl(self):
        return self._url

    def getUser(self):
        return self._user

    def setUser(self, user):
        self._user = user

    def getContent(self):
        return self._content

    def getCookie(self):
        return self._cookie

    def addProxy(self, key, value):
        if key == None:
            return

        self._proxy[key] = value

    def getProxy(self):
        return self._proxy

    def loginByUser(self, user, url = None):
        self._user = user

        if url != None:
            self.setUrl(url)

        return True

    def _downloadUrl(self, url, cookie):
        return True

    def load(self, url = None, user = None):
        if url != None:
            self.setUrl(url)

        if user == None:
            user = self.getUser()

        if self.loginByUser(user, self.getUrl()) == False:
            return False

        self._content = self._downloadUrl(self.getUrl(), self.getCookie())

        return True

    def downloadAsFile(self, url, target):
        if url == None:
            if self.getUrl() == None:
                return False
            else:
                url = self.getUrl()

        if target == None:
            return False

        rfp = None
        fp = None
        res = True
        try:
            rfp = urllib.urlopen(url, proxies = self.getProxy())
            fp = open(target, 'w')
            for line in rfp:
                fp.write(line)
            fp.close()
            rfp.close()
        except:
            res = False
        finally:
            if fp != None:
                fp.close()
            if rfp != None:
                rfp.close()

        return res





if __name__ == '__main__':
    l = UrlLoader()
    l2 = UrlLoader()
    l3 = UrlLoader()
