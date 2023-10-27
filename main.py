import os
import subprocess
from threading import Thread
import time

start_time = time.time() 

#prompt for using webcam: python webcam.py alarm_threshold_min alarm_threshold_max threshold_sum time
#time: >0 - cycle time for running subprogram in minutes (default: 1 minute)

def thread1():
    global result
    while True:
        result = subprocess.run(["python", "webcam.py", "1", "2", "3", "1"], capture_output=True, text=True)

def thread2():

    while True:   
        print("--- %s seconds ---" % (round(time.time() - start_time))) 
        try:
            None
            #print(bool(result.stdout)) # true if motion detected, works only on rising edge and env variables should be used here

        except:
            #print("initializing")
            None
        time.sleep(1)

Thread(target = thread1).start() 
Thread(target = thread2).start()
