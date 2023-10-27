import threading
import winsound
import datetime
import sys
import time
import os

import cv2
import imutils

def webcam():
    #create camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    #set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    #create initial starting frame, turn into bw, smoothen with the gaussian blur
    _, start_frame = cap.read()
    start_frame = imutils.resize(start_frame, width=500)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    #define alarm parameters
    alarm = False
    alarm_mode = True # False if "t" keyword function enabled
    alarm_counter = 0
    alarm_settled = False

    # --- these are important --- #
    alarm_threshold_min = 10 #num of summed frames to record frame
    alarm_threshold_max = 30 #max sum
    threshold_sum = 100 #pixels amount to trigger frame+
    minutes = 1
    # --------------------------- #

    # take them externally if provided
    if len(sys.argv) > 3:
        alarm_threshold_min = int(sys.argv[1])
        alarm_threshold_max = int(sys.argv[2])
        threshold_sum = int(sys.argv[3])
        if len(sys.argv) > 4:
            minutes = int(sys.argv[4])
        

    #define recording parameters
    recording = True
    frame_size = (int(cap.get(3)), int(cap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter("video.mp4", fourcc, 20, frame_size)    

    

    #alarm function triggered when motion is detected 
    def beep_alarm():
        global alarm
        for _ in range(5):
            if not alarm_mode:
                break
            #print("ALARM")
            winsound.Beep(2500, 1000)
        alarm = False
    #print("Hello")

    #cycle of program
    t_end = time.time() + 60 * minutes
    while time.time() < t_end:

        #new frame with each iteration, resize it
        _, frame = cap.read()

        #record colored frames with data
        if alarm_counter > alarm_threshold_min and recording:
            frame_rec = frame.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX #describe the font type
            date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) #get current date and time  
            frame_rec = cv2.putText(frame_rec, date_time,(10, 450),font, 1,(0, 0, 0), 4, cv2.LINE_4)
            out.write(frame_rec) # write frame to video

        frame = imutils.resize(frame, width=500)

        #if alarm mode is active: turn in bw, smooth it, calc differences between frames, add or subtract 1 to alarm_counter, show threshold or frame
        if alarm_mode:
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
            difference = cv2.absdiff(frame_bw, start_frame)
            threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
            start_frame = frame_bw

            if threshold.sum() > threshold_sum and alarm_counter < alarm_threshold_max: #tweak it for more/less sensitive frames diff threshold: 10 very sensitive, 1000 weak sensitivity
                alarm_counter += 1
            else:
                if alarm_counter > 0:
                    alarm_counter -= 1

            #cv2.imshow("Cam", threshold)
        else:
            #cv2.imshow("Cam", frame)
            None

        #trigger this function if enough diffed frames was counted up
        if alarm_counter > alarm_threshold_min: # tweak it for longer/shorter detection time

            if not alarm:
                alarm_settled = True
                alarm = True
                threading.Thread(target=beep_alarm).start()

        #keys: t - start/stop alarm mode, q - turn off program
        key_pressed = cv2.waitKey(30)
        #if key_pressed == ord("t"):
        #    alarm_mode = not alarm_mode
        #    alarm_counter = 0
        if key_pressed == ord("q"):
            alarm_mode = False
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()

    video_num=1
    while bool(os.path.isfile("video"+str(video_num)+".mp4")):
        video_num+=1
    if (alarm_settled):
        os.rename("video.mp4","video"+str(video_num)+".mp4")
    
    return alarm_settled

result = webcam()
print(result)
