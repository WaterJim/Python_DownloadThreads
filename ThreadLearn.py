from threading import Thread
import time


# def countDown(n):
#     while n > 0:
#         print('T-minus', n)
#         n -= 1
#         time.sleep(5)
#
# t = Thread(target=countDown, args=(10,))
# t.start()

def doWaiting():
    print('start waiting1: ' + time.strftime('%H:%M:%S') + "\n")
    time.sleep(5)
    print('stop waiting1: ' + time.strftime('%H:%M:%S') + "\n")


def doWaiting1():
    print('start waiting2: ' + time.strftime('%H:%M:%S') + "\n")
    time.sleep(8)
    print('stop waiting2: ', time.strftime('%H:%M:%S') + "\n")


tsk = []
thread1 = Thread(target=doWaiting)
thread1.start()
tsk.append(thread1)
thread2 = Thread(target=doWaiting1)
thread2.start()
tsk.append(thread2)

for tt in tsk:
    print('start join: ' + time.strftime('%H:%M:%S') + "\n")
    tt.join()
print('end join: ' + time.strftime('%H:%M:%S') + "\n")
