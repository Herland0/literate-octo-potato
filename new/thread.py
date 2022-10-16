import _thread
import time

def ptime(TName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(TName, time.ctime(time.time()))

try:
    _thread.start_new_thread(ptime, ("Thread-1",1,))
    _thread.start_new_thread(ptime, ("Thread-2",2,))
except:
    print("Error unable to start thread")

while True:
    pass