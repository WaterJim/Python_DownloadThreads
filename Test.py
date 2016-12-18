import DownloadTask
import threading
import time
import random

downloadUrl = "http://i0.hdslb.com/bfs/archive/ac6ad98e868f313a332eb757634ddc9fcd5d7753.jpg@.webp"
downloadPath = "G:/Picture/"


def testDownload():
    countIndex = 0
    while countIndex < 50:
        print('add download mission : index = ' + str(countIndex))
        DownloadTask.addDownloadTask(
            DownloadTask.DownloadMission(DownloadTask.DownloadMission.MISSION_NOMAL,
                                         downloadUrl, downloadPath + "pic_" + str(countIndex) + ".jpg@.webp"))
        sleepTime = random.random()
        print("sleep time : " + str(sleepTime))
        time.sleep(sleepTime)
        countIndex += 1

    DownloadTask.addDownloadTask(
        DownloadTask.DownloadMission(DownloadTask.DownloadMission.MISSION_STOP,
                                     downloadUrl, downloadPath + "pic_" + str(countIndex) + ".jpg@.webp"))


if __name__ == '__main__':
    DownloadTask.startDownload()
    testDownload()
