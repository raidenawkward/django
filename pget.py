
import os
import sys

from urldownloader import UrlDownloader
from urldownloader import UrlDownloadTask
from urldownloader import UrlDownloaderMonitor
from pbsloader import PbsUrlLoader
from pbsloader import PbsProductsAnalyser
from urlfileinfo import UrlFileInfo
from user import User

class PbsProductGetter:

    PBS_URL = 'http://suwon.qb.sec.samsung.net'

    def __init__(self, pbsNumber, user,
                 downloadHeaderlist, outputDir,
                 monitorInterval = UrlDownloaderMonitor.DEF_TIME_INTERVAL):

        self._pbsNumber = pbsNumber
        self._user = user
        self._downloadHeaderlist = downloadHeaderlist
        self._outputDir = outputDir

        self._downloader = UrlDownloader()
        self._downloaderMonitor = PbsDownloadMonitor(self._downloader,
                                                    monitorInterval)


    def __isFileNeedToDownload(self, name):
        for header in self._downloadHeaderlist:
            if name.startswith(header):
                return True

        return False


    def _prepare(self):
        urlLoader = PbsUrlLoader(url = PbsProductGetter.PBS_URL,
                                 user = self._user,
                                 pageId = self._pbsNumber)
        analyser = PbsProductsAnalyser(urlLoader)
        if analyser.analyse() == False:
            pass # report error

        if self._outputDir == None:
            self._outputDir = ''
        else:
            self._outputDir += '/'

        products = analyser.getProducts()
        for p in products:
            if self.__isFileNeedToDownload(p.getFileName()):
                task = UrlDownloadTask(p,
                                       self._outputDir + p.getFileName())
                self._downloader.append(task)


    def startDownloading(self):
        self._prepare()

        self._downloader.startDownload()

        if self._downloaderMonitor != None:
            self._downloaderMonitor.startMonitoring()




class PbsDownloadMonitor(UrlDownloaderMonitor):

    def __init__(self, downloader,
             monitoringInterval = UrlDownloaderMonitor.DEF_TIME_INTERVAL):
        UrlDownloaderMonitor.__init__(self, downloader, monitoringInterval)


    def _onBeforeStartMonitoring(self):
        sys.stdout.write("download started\n")


    def _onMonitoringRoundStart(self, aliveTaskList):
        sys.stdout.write("\n-------------------------------\n")


    def _onMonitoringRoundEnd(self, aliveTaskList):
        sys.stdout.write('' + str(len(aliveTaskList))
                         + ' of ' + str(len(self.getDownloader().getTaskList()))
                         + ' left')
        sys.stdout.write("\n-------------------------------\n")


    def _onMonitoringTask(self, task):
        info = task.getUrlFileInfo()
        downloaded = task.getDownloadedSize()
        total = info.getFileSize()
        percent = downloaded / total * 100
        sys.stdout.write(''
                         + '[%.2f' % percent + '%] '
                         + info.getFileName() + '\n')


    def _onFinishMoniting(self):
        sys.stdout.write("download finished\n")
        pass




if __name__ == '__main__':
    user = User()
    user.loadFromFile('test.user')

    downloadList = ['BL_', 'CSC_']

    getter = PbsProductGetter('2024322',
                              user,
                              downloadList,
                              None,
                              1)

    getter.startDownloading()
