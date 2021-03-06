
import os
import sys
import time
import base64

from urldownloader import UrlDownloader
from urldownloader import UrlDownloadTask
from urldownloader import UrlDownloaderMonitor
from pbsloader import PbsUrlLoader
from pbsloader import PbsProductsAnalyser
from urlfileinfo import UrlFileInfo
from user import User
from jconfig import JConfig




class PbsProductGetter:

    PBS_URL = 'http://suwon.qb.sec.samsung.net'


    def __init__(self, pbsNumber,
                 user,
                 downloadHeaderlist,
                 outputDir,
                 monitorInterval = UrlDownloaderMonitor.DEF_TIME_INTERVAL,
                 pbsUrl = PBS_URL):

        self._pbsUrl = pbsUrl;
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


    def getPbsUrl(self):
        return self._pbsUrl


    def _waitForBuilding(self, analyser, timeInterval):
        if analyser == None:
            return

        while analyser.getPercentage() >= 0:
            sys.stdout.write("\n-------------------------------\n")
            sys.stdout.write('building in progress: '
                             + str(analyser.getPercentage())
                             + '%\n')
            sys.stdout.write('\n-------------------------------\n')
            time.sleep(timeInterval)



    def _prepare(self):
        urlLoader = PbsUrlLoader(url = self.getPbsUrl(),
                                 user = self._user,
                                 pageId = self._pbsNumber)
        analyser = PbsProductsAnalyser(urlLoader)
        if analyser.analyse() == False:
            self._waitForBuilding(analyser,
                                  self._downloaderMonitor.getMonitoringInterval())

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
        self._downloadedSize = 0


    def _onBeforeStartMonitoring(self):
        sys.stdout.write('download started\n')


    def _onMonitoringRoundStart(self, aliveTaskList):
        sys.stdout.write('\n-------------------------------\n')
        self._downloadedSize = 0


    def _onMonitoringRoundEnd(self, aliveTaskList):
        totalSize = self.getDownloader().getSizeToDownload()
        percent = self._downloadedSize / totalSize * 100

        sys.stdout.write('[total %.2f' % percent + '%] '
                         + str(len(aliveTaskList))
                         + ' of ' + str(len(self.getDownloader().getTaskList()))
                         + ' left')
        sys.stdout.write('\n-------------------------------\n')
        sys.stdout.flush()


    def _onMonitoringTask(self, task):
        info = task.getUrlFileInfo()
        downloaded = task.getDownloadedSize()
        total = info.getFileSize()
        percent = downloaded / total * 100
        self._downloadedSize += downloaded

        sys.stdout.write(''
                         + '[%.2f' % percent + '%] '
                         + info.getFileName() + '\n')


    def _onFinishMoniting(self):
        sys.stdout.write('download finished\n')






def print_help():

    helpInfo = 'usage:\n\tpget [config=value ..] {cmd / pbs number}\n\
\n\
configs probably are:\n\
pbsurl=url\n\
configfile=filepath\n\
outputdir=dir\n\
\n\
cmds are:\n\
-h    show this message\n\
-v    show version\n\
'

    sys.stdout.write(helpInfo)
    sys.stdout.flush()


def print_version():
    version = 'pget v0.1\n'
    sys.stdout.write(version)
    sys.stdout.flush()


def arg_get_config_key(arg):
    index = arg.replace(' ', '').find('=')
    if index < 0:
        return None
    return arg[0:index]


def arg_get_config_value(arg):
    index = arg.replace(' ', '').find('=')
    if index < 0:
        return None
    return arg[index + 1:]


def report_error_arg_value(value):
    sys.stdout.write('error: used error config value: ' + value + '\n')
    sys.stdout.flush()


def report_error_arg_cmd(cmd):
    sys.stdout.write('error: unknown cmd: ' + cmd + '\n')
    sys.stdout.flush()


def is_pbs_number(number):
    try:
        num = int(number)
        return True
    except:
        return False


def encrypt_user_password(config):
    password = config.get('password')
    if password == None:
        return

    password = base64.encodestring(password)
    password = password.replace('\n', '')
    password = password.replace('\r', '')
    config.set('password', password)




if __name__ == '__main__':
    configFile = 'pget.config'
    outputDir = '.'
    pbsNumber = ''
    pbsUrl = PbsProductGetter.PBS_URL
    downloadHeaderList = []

    argc = len(sys.argv)
    if argc <= 1:
        print_help()
        exit(-1)

    for i in range(1, argc):
        arg = sys.argv[i]
        configKey = arg_get_config_key(arg)
        if configKey != None:
            configVal = arg_get_config_value(arg)
            if configVal == None:
                report_error_arg_value(configVal)
                exit(1)

            if configKey == 'pbsurl':
                pbsUrl = configVal
            elif configKey == 'configfile':
                configFile = configVal
            elif configKey == 'outputdir':
                outputDir = configVal
            else:
                report_error_arg_value(configVal)
                exit(-1)
        else:
            if arg == '-h':
                print_help()
                exit(0)
            elif arg == '-v':
                print_version()
                exit(0)
            else:
                if is_pbs_number(arg):
                    pbsNumber = arg
                else:
                    report_error_arg_cmd(arg)
                    exit(-1)


    config = JConfig()
    config.loadFromFile(configFile)
    print(os.getcwd())
    print('loading config from ' + configFile)
    print(config.toString())

    userName = config.get('user')
    password = config.get('password')

    if config.get('download-header') != None:
        downloadHeaders = str(config.get('download-header'))
        downloadHeaderList = downloadHeaders.split('|')

    if config.get('output-dir') != None:
        outputDir = config.get('output-dir')

    try:
        decodePassword = base64.decodestring(password)
    except:
        encrypt_user_password(config)
        decodePassword = password

    user = User()
    user.set('userName', userName)
    user.set('password', decodePassword)

    if len(downloadHeaderList) == 0:
        report_error_arg_value('download-header')
        exit(0)

    config.saveToFile(configFile)

    outputDir += '/' + str(pbsNumber)
    if os.path.isdir(outputDir) == False:
        os.mkdir(outputDir)

    print(downloadHeaderList)
    getter = PbsProductGetter(pbsNumber,
                              user,
                              downloadHeaderList,
                              outputDir,
                              1.0)

    getter.startDownloading()
