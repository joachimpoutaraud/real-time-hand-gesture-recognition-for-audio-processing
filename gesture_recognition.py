import threading
import os
import ctypes

import cv2
import mediapipe as mp
from pythonosc.udp_client import SimpleUDPClient

def pdopen(patch):

    # Set your pd path below (for Mac) 
    pd_path = '/Applications/Pd-0.51-4.app'

    if os.sys.platform == 'darwin':
        pd_executable = pd_path + '/Contents/Resources/bin/pd' # for Mac
    elif os.sys.platform == 'win32':
        pd_executable = '"C:\\Program Files\\Pd\\bin\\pd.exe"' # for Windows

    pd_patch = patch
    command = pd_executable + ' -open ' + pd_patch + ' -nogui'
    os.popen(command)

# Declare pd patch to use
pd_patch = 'audio_processing.pd'
# Open pd on thread so that main continues, passing patch as argument
t1 = threading.Thread(target=pdopen, args=(pd_patch,))
t1.start()
# Declare client on local host
client = SimpleUDPClient('127.0.0.1', 8006) 

# 0 is built-in webcam
capture = cv2.VideoCapture(0)

# Full screen mode
cv2.namedWindow('Full Integration', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Full Integration', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# Get Screen Size
CAPTURE_WIDTH = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
CAPTURE_HEIGHT = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Setting up mediapipe tools for getting and drawing hand landmarks
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils
# Declare the finger coordinates
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)

while True:
    # Get image from webcam and flip it
    _, image = capture.read()
    image = cv2.flip(image, 1)

    # Get results of hand landmark detection using RGB-converted image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = hands.process(image_rgb)

    # Set the number of vertical marker on the webcam image
    markers = 6
    division_width = CAPTURE_WIDTH / markers 

    if results.multi_hand_landmarks:
        detected_hand = results.multi_hand_landmarks[0] # we use only one hand
        # 8 is the index for index fingertip landmark. For more, see
        # https://google.github.io/mediapipe/solutions/hands.html
        index_tip_landmark = detected_hand.landmark[8]

        handList = []
        mp_draw.draw_landmarks(image, detected_hand, mp_hands.HAND_CONNECTIONS)
        for idx, lm in enumerate(detected_hand.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            handList.append((cx, cy))
        upCount = 0
        for coordinate in finger_Coord:
            if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
            upCount += 1

        # If the number of fingers is equal to 5 then Pure Data dsp will be either on or off
        # if upCount == 5:
        #     client.send_message('/action', 1)

        # Send inverted y finger positions to Pure Data and scale to effect range
        if index_tip_landmark.x < division_width:
            client.send_message('/pitch', (1 - index_tip_landmark.y)*127)
        if index_tip_landmark.x > division_width*2 and index_tip_landmark.x < division_width*3:         
            client.send_message('/reverb', (1 - index_tip_landmark.y)*120)
        if index_tip_landmark.x > division_width*3 and index_tip_landmark.x < division_width*4:         
            client.send_message('/delay', (1 - index_tip_landmark.y)*1500)
        if index_tip_landmark.x > division_width*5 and index_tip_landmark.x < 1:         
            client.send_message('/modulation', (1 - index_tip_landmark.y)*1000)   

        # Draw landmark positions and wireframe connections
        mp_draw.draw_landmarks(image,detected_hand,mp_hands.HAND_CONNECTIONS)   
    
    for i in range(1, markers):
        # Set different colors to separate the effects
        if i == 1:
            line_color = (255, 255, 0)
        elif i == 5:
            line_color = (255, 0, 255) 
        else: 
            line_color = (0, 255, 0)       
        x = round(division_width * i)
        cv2.line(img=image,pt1=(x, 0),pt2=(x, CAPTURE_HEIGHT),color=line_color,thickness=3)
    
    # Add text
    def vertical_text(text, y_start, color, scale=40):
        for i, line in enumerate(text.split('\n')):
            y = i*scale
            cv2.putText(image, line, (y_start, scale+y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 5)

    vertical_text('P\nI\nT\nC\nH', int(division_width-60), (255, 255, 0)) 
    vertical_text('R\nE\nV\nE\nR\nB', int((division_width*3)-60), (0, 255, 0)) 
    vertical_text('D\nE\nL\nA\nY', int((division_width*4)-60), (0, 255, 0)) 
    vertical_text('M\nO\nD\nU\nL\nA\nT\nI\nO\nN', int((division_width*6)-60), (255, 0, 255)) 

    cv2.imshow('MCT Webcam Effects 2022', image)
    key =  cv2.waitKey(1)
    # keep pressing space to break 
    if key == 32:
        client.send_message('/quit', 1)
        break


