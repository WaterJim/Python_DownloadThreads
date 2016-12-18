# 处理下载模块
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import time

'''
主要有两个功能
1. 向队列中添加下载任务（注意锁）
2. 从队列中取出任务，并进行下载（注意锁）
3. 下载完成后，将结果存放到磁盘中
'''

# lock = threading.Lock()
queue = queue.Queue(maxsize=1000)  # 最多保存1000个下载任务


def addDownloadTask(task):
    '''
    向队列中添加任务（生产者）
    一旦队列满了，则会堵塞调用线程
    :return:
    '''
    queue.put(task, 1)


def getDownloadTaskFromQueue():
    '''
    从队列中获取任务（消费者）
    一旦队列为空，则堵塞调用线程
    :return:
    '''
    return queue.get(True)


def downloadAndSave(url, savePath):
    print("start download:")
    print("url = " + url)
    print("save path = " + savePath)
    urllib.request.urlretrieve(url, savePath)
    pass


def startDownload():
    downloadThread = DownloadThread()
    downloadThread.start()


class DownloadMission(object):
    MISSION_STOP = 1
    MISSION_NOMAL = 2

    def __init__(self, type, url='', path=''):
        self.url = url
        self.savePath = path
        self.missionType = type


# 启动线程，不断地从队列中获取任务
class DownloadThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.flag = True
        self.downloadThreadPool = ThreadPoolExecutor(32)
        pass

    def run(self):
        while self.flag == True:
            task = getDownloadTaskFromQueue()
            if task != None:
                # 设置停止任务
                if task.missionType == DownloadMission.MISSION_STOP:
                    self.flag = False
                    continue
                thread = self.downloadThreadPool.submit(
                    downloadAndSave, task.url, task.savePath)
        print("Download task stop!")


if __name__ == '__main__':
    downloadThread = DownloadThread()
    downloadThread.start()
