import sys
import re
from user import User
from urlloader import UrlLoader
from urlfileinfo import UrlFileInfo

sys.path.append('ClientCookie-1.0.3')
sys.path.append('ClientForm-0.1.17')

import ClientCookie
import ClientForm

class PbsUrlLoader(UrlLoader):
    ''' load pbs content '''

    def __init__(self, url, user, pageId):
        UrlLoader.__init__(self, url, user)
        self._id = pageId

    def getId(self):
        return self._id

    # override
    def loginByUser(self, user, url = None):
        res = True

        if UrlLoader.loginByUser(self, user, url) == False:
            return False;

        signinUrl = self.getUrl() + '/signin'

        try:
            cookieJar = ClientCookie.CookieJar()
            opener = ClientCookie.build_opener(
                ClientCookie.HTTPCookieProcessor(cookieJar))
            opener.addheaders = [("User-agent","Mozilla/5.0 (compatible)")]
            ClientCookie.install_opener(opener)
            fp = ClientCookie.urlopen(signinUrl)
            forms = ClientForm.ParseResponse(fp)
            fp.close()

            form = forms[0]
            form['userName'] = user.getAttr('userName')
            form['password'] = user.getAttr('password')

            self._cookie = ClientCookie

            fpTestOpen = ClientCookie.urlopen(form.click())
            fpTestOpen.close()

        except Exception, e:
            print('Error when login: ' + e.message)
            res = False

        if res == False:
            return res

        return True

    def _downloadUrl(self, url, cookie):
        if cookie == None:
            return False

        content = ''

        try:
            webUrl = url + '/build/' + str(self.getId())
            webFp = cookie.urlopen(webUrl)
            content = webFp.read()
            webFp.close()
        except:
            pass
        finally:
            if webFp != None:
                webFp.close()

        return content

    def downloadAsFile(self, url, target):
        if url == None:
            if self.getUrl() == None:
                return False
            else:
                url = self.getUrl()

        if target == None:
            return False

        cookie = self.getCookie()
        if cookie == None:
            return False

        res = True
        try:
            req = cookie.Request(url)
            fp = cookie.urlretrieve(req, target)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(e)
            res = False
        finally:
            pass

        return res





class PbsProductsAnalyser:
    '''
    peel pbs build products
    from pbs page
    '''

    def __init__(self, pageLoader):
        self._pageLoader = pageLoader
        self._products = []
        self._percentage = -1

    def getProducts(self):
        return self._products

    def getLoader(self):
        return self._pageLoader

    def getPercentage(self):
        return self._percentage

    def _analysePercentage(self, content):
        if content == None:
            return False

        percentList = re.findall(r'''progress-percentage">\d+%''', content)
        if len(percentList) == 0:
            return -1

        percentStr = percentList[0]
        percent = percentStr.replace('progress-percentage">', '')
        percent = percent.replace('%', '')
        return int(percent)

    def _loadAnalysingContent(self):
        pageLoader = self.getLoader()
        if pageLoader == None:
            return 0

        pageLoader.load()
        pageContent = pageLoader.getContent()

        return pageContent

    def __parseSizeStrToByte(self, mass):
        string = mass.upper()
        sizeList = string.split(' ')
        if len(sizeList) < 2:
            return 0

        try:
            size = float(sizeList[0])
        except ValueError:
            return 0

        unit = sizeList[1].replace('\n', '').replace('\r', '')

        if unit == 'TB':
            size = size * 1024 * 1024 * 1024 * 1024
        elif unit == 'GB':
            size = size * 1024 * 1024 * 1024
        elif unit == 'MB':
            size = size * 1024 * 1024
        elif unit == 'KB':
            size = size * 1024
        else:
            pass # size = size

        return size


    def _getInfoFromStr(self, mass):
        loader = self.getLoader()
        mass = mass.replace('amp;', '')

        markHref = '<a href="'
        hrefStart = mass.find(markHref)
        if hrefStart < 0:
            return None

        hrefStart += len(markHref)
        hrefEnd = mass.find('"', hrefStart + len(markHref))
        href = mass[hrefStart:hrefEnd].replace('\n', '').replace('\r','')

        nameMark = 'filename='
        nameStart = href.find(nameMark)
        if nameStart < 0:
            return None
        nameStart += len(nameMark)
        nameEnd = href.find('&source=')
        name = href[nameStart:nameEnd]

        markSize = '<td class="last table-column">'
        sizeStart = mass.find(markSize)
        sizeEnd = mass.find('<', sizeStart + len(markSize))
        sizeStr = mass[sizeStart + len(markSize):sizeEnd]

        info = UrlFileInfo(remotePath = loader.getUrl() + href,
                           fileName = name,
                           fileSize = self.__parseSizeStrToByte(sizeStr),
                           urlLoader = loader)

        return info

    def analyse(self):
        pageContent = self._loadAnalysingContent()
        self._percentage = self._analysePercentage(pageContent)
        self._products = []

        if self._percentage >= 0:
            return False

        lines = pageContent.split('\n')
        for line in lines:
            index = line.find('filename=')
            if index < 0:
                continue

            info = self._getInfoFromStr(line)

            if info != None:
                self._products.append(info)

        return True

    def getUrlList(self):
        infoList = self.getProducts()
        res = []

        for item in infoList:
            res.append(item.getRemotePath())

        return res

    def getFileNameList(self):
        infoList = self.getProducts()
        res = []

        for item in infoList:
            res.append(item.getFileName())

        return res




if __name__ == '__main__':
    user = User()
    user.loadFromFile('test1.user', )
    print(user.toString())

    pl = PbsUrlLoader(url = 'http://suwon.qb.sec.samsung.net',
                      user = user,
                      pageId = '2024322')
    an = PbsProductsAnalyser(pl)
    an.analyse()
    for item in an.getProducts():
        print(item.toString())

