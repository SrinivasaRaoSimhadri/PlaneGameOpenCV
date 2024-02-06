# importing requirements
import cv2 as cv
import mediapipe as mp
import math
from KeyControls import *

# creation of video capture object for reading video.
video = cv.VideoCapture(0)

# setting window size.
video.set(cv.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

# creation of pose estimation object.
pose = mp.solutions.pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
draw = mp.solutions.drawing_utils
PressKey(up_key)


def ReleaseAllKeys():
    ReleaseKey(left_key)
    ReleaseKey(right_key)


while True:

    # flipping video for better user interaction.
    success, frame = video.read()
    frame = cv.flip(frame, 1)

    # processing the image for getting pose landmarks.
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = pose.process(image)
    if results.pose_landmarks:
        L = []
        for _, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = frame.shape
            xc, yc = int(lm.x * w), int(lm.y * h)
            L.append([xc, yc])

        # basing on distance between different landmarks on controlling of keys can be done.
        shoulder_x_distance = L[11][0] - L[12][0]
        shoulder_y_distance = L[11][1] - L[12][1]
        shoulder_distance = int(math.sqrt(shoulder_x_distance ** 2 + shoulder_y_distance ** 2))

        wrist_x_distance = L[15][0] - L[16][0]
        wrist_y_distance = L[15][1] - L[16][1]
        wrist_distance = int(math.sqrt(wrist_x_distance ** 2 + wrist_y_distance ** 2))

        right_hip_x_distance = L[15][0] - L[23][0]
        right_hip_y_distance = L[15][1] - L[23][1]
        right_hip_distance = int(math.sqrt(right_hip_x_distance ** 2 + right_hip_y_distance ** 2))

        left_hip_x_distance = L[16][0] - L[24][0]
        left_hip_y_distance = L[16][1] - L[24][1]
        left_hip_distance = int(math.sqrt(left_hip_x_distance ** 2 + left_hip_y_distance ** 2))

        ReleaseAllKeys()

        # setting the key controls based on the distance.
        if wrist_distance < 180:
            ReleaseKey(up_key)
        elif left_hip_distance > 180:
            PressKey(left_key)
        elif right_hip_distance > 180:
            PressKey(right_key)
        elif wrist_distance > shoulder_distance:
            PressKey(up_key)
        # draw.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
    cv.imshow("video", frame)
    if cv.waitKey(13) == ord('q'):
        break
