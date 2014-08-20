import threading
import time
import urllib
import os

import time

from user import User
from urlloader import UrlLoader
from pbsloader import PbsUrlLoader

import urlfileinfo
from urlfileinfo import UrlFileInfo




class UrlDownloader:
    '''
    specified url downloader

    '''


    def __init__(self):
        self._taskList = []


    def appendUrlFileInfo(self, info, output = None):
        task = UrlDownloadTask(info, output)
        self._taskList.append(task)


    def append(self, task):
        self._taskList.append(task)

    def getTaskList(self):
        return self._taskList


    def startDownload(self):
        taskList = self.getTaskList()
        for task in taskList:
            task.start()


    def getSizeToDownload(self):
        res = 0
        taskList = self.getTaskList()
        for task in taskList:
            info = task.getUrlFileInfo()
            res += info.getFileSize()

        return res


    def getActivatedTasks(self):
        res = []
        taskList = self.getTaskList()

        for task in taskList:
            thread = task.getThread()
            if thread == None:
                continue

            if thread.isAlive():
                res.append(task)
        return res




class UrlDownloadTask:
    '''
    async single task for downloading
    '''

    GLOBAL_ID = 0

    STATUS_UNKNOWN = 'status_unknown'
    STATUS_READY = 'status_ready'
    STATUS_WORKING = 'status_working'
    STATUS_PENDING = 'status_pending'
    STATUS_FINISH = 'status_finish'
    STATUS_ERROR = 'status_error'


    def __init__(self, urlFileInfo, target = None):
        self._id = UrlDownloadTask.GLOBAL_ID
        UrlDownloadTask.GLOBAL_ID += 1

        self._status = UrlDownloadTask.STATUS_READY
        self._urlFileInfo = urlFileInfo
        self._target = target

        args = {self._urlFileInfo}
        self._thread = threading.Thread(target = self._download, args = args)


    def getId(self):
        return self._id


    def getStatus(self):
        return self._status


    def _setStatus(self, status):
        self._status = status


    def getThread(self):
        return self._thread


    def getUrlFileInfo(self):
        return self._urlFileInfo


    def getTarget(self):
        return self._target


    def setTarget(self, target):
        self._target = target


    def getDownloadedSize(self):
        target = self.getTarget()

        if target == None:
            return 0

        if os.path.exists(target) == False:
            return 0

        size = os.path.getsize(self.getTarget())

        return size


    def __downloadNormalUrl(self, url, target):
        rfp = None
        fp = None
        res = True
        try:
            rfp = urllib.urlopen(url)
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


    def _download(self, remoteFile):
        self._setStatus(UrlDownloadTask.STATUS_WORKING)

        if remoteFile == None:
            self._setStatus(UrlDownloadTask.STATUS_ERROR)
            return

        url = remoteFile.getRemotePath()
        if url == None:
            self._setStatus(UrlDownloadTask.STATUS_ERROR)
            return

        target = self.getTarget()
        if target == None:
            target = remoteFile.getFileName()

        if target == None:
            self._setStatus(UrlDownloadTask.STATUS_FINISH)
            return

        urlLoader = remoteFile.getUrlLoader()

        if urlLoader == None:
            if self.__downloadNormalUrl(url, target) == False:
                self._setStatus(UrlDownloadTask.STATUS_ERROR)
        else:
            if urlLoader.downloadAsFile(url, target) == False:
                self._setStatus(UrlDownloadTask.STATUS_ERROR)

        self._setStatus(UrlDownloadTask.STATUS_FINISH)


    def start(self):
        thread = self.getThread()
        if thread is None:
            self._setStatus(UrlDownloadTask.STATUS_ERROR)
            return False

        thread.setName('downloading id' + str(self.getId()))
        thread.setDaemon(True)
        thread.start()

        return True




class UrlDownloaderMonitor:

    DEF_TIME_INTERVAL = 1.0

    def __init__(self, downloader,
                 monitoringInterval = DEF_TIME_INTERVAL):
        self._downloader = downloader
        self._monitoringInterval = monitoringInterval


    def getDownloader(self):
        return self._downloader


    def getMonitoringInterval(self):
        return self._monitoringInterval


    def setMonitoringInterval(self, interval):
        self._monitoringInterval = interval


    def _onBeforeStartMonitoring(self):
        pass


    def _onMonitoringRoundStart(self, aliveTaskList):
        pass


    def _onMonitoringRoundEnd(self, aliveTaskList):
        pass


    def _onMonitoringTask(self, task):
        pass


    def _onFinishMoniting(self):
        pass


    def startMonitoring(self):
        self._onBeforeStartMonitoring()

        downloader = self.getDownloader()
        if downloader == None:
            return

        while True:
            taskList = downloader.getActivatedTasks()
            count = len(taskList)
            if count <= 0:
                break;

            self._onMonitoringRoundStart(taskList)

            for task in taskList:
                self._onMonitoringTask(task)

            self._onMonitoringRoundEnd(taskList)
            time.sleep(self.getMonitoringInterval())

        self._onFinishMoniting()





if __name__ == '__main__':
    #loader = UrlLoader()

    user = User()
    user.loadFromFile('test.user', )
    loader = PbsUrlLoader(url = 'http://suwon.qb.sec.samsung.net',
                      user = user,
                      pageId = '2024322')
    loader.loginByUser(user)

    f = urlfileinfo.createUrlFileInfoByUrl(
        'http://suwon.qb.sec.samsung.net/rest/ads/download/2024322?filename=BL_G5309WKEE0ANH2_96457_REV00_eng_mid_noship_MULTI_CERT.tar.md5&source=10.252.244.233',
        'xxxxx.tar.md5',
        0,
        loader)

    task = UrlDownloadTask(f)
    task.start()


