#Copyright (c) 03.2020 @author  Hussam Soufi: hussam1soufi@gmail.com

#when you run the python script the camera will take a photo
#you need to choose two boxes (face & hand) that you don't want to collapse!
#Then press Enter to start tracking and ESC to Exit
#Have fun and stay healthy. Cheers! - Sam

import cv2 #pip install opencv-contrib-python
import numpy as np
import sys
import vlc # pip install python-vlc
#make sure to have VLC installed version x64! version x86 won't work!

#Get the detect xml
FrontalFaceDetect = cv2.CascadeClassifier('./frontalFace.xml')

#Get the alarm sound
AlarmPath = "./SamPrettyVoice.m4a"
sound = vlc.MediaPlayer(AlarmPath)
AlarmPlaying = False

#Capture Video
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
tracker = cv2.TrackerMIL_create()

# Read frames
ok, frame = cap.read()
ok, frame = cap.read()
if not ok:
    print('Cannot read video file, make sure to have VLC installed version x64! version x86 wont work')
    sys.exit()


# select box
bbox = cv2.selectROI(frame, False)

# Initialize tracker
ok = tracker.init(frame, bbox)

def hand_close_to_face(box_face, box_hand):
    x_overlap = max(0, min(box_face[0]+box_face[2], box_hand[0]+box_hand[2]) - max(box_face[0], box_hand[0]))
    y_overlap = max(0, min(box_face[1]+box_face[3], box_hand[1]+box_hand[3]) - max(box_face[1], box_hand[1]))
    return x_overlap * y_overlap > 0

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = FrontalFaceDetect.detectMultiScale(frame, 1.5, 2)
    if len(face)>0:
        face = face[0]
        cv2.rectangle(frame, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (255, 0, 0), 2)
        
        # Update tracker
        ok, bbox = tracker.update(frame)
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,0,255), 2)
            close = hand_close_to_face(face, bbox)


            if close:
                cv2.putText(img=frame, text='DONT TOUCH!', org=(int(100 / 2 - 20), int(100 / 2)), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255))
                if AlarmPlaying == False:
                    AlarmPlaying = True
                    sound.play()
            else:
                if AlarmPlaying == True:
                    AlarmPlaying = False
                    sound.stop()

    cv2.imshow('Driver_frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
