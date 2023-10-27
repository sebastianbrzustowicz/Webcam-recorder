import threading
import winsound

import cv2
import imutils

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
alarm_mode = False
alarm_counter = 0

#alarm function triggered when motion is detected 
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        winsound.Beep(2500, 1000)
    alarm = False
print("Hello")
#cycle of program
while True:

    #new frame with each iteration, resize it
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    #if alarm mode is active: turn in bw, smooth it, calc differences between frames, add or subtract 1 to alarm_counter, show threshold or frame
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 300: #tweak it for more/less sensitive frames diff threshold: 10 very sensitive, 1000 weak sensitivity
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    #trigger this function if enough diffed frames was counted up
    if alarm_counter > 20: # tweak it for longer/shorter detection time
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    #keys: t - start/stop alarm mode, q - turn off program
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()
