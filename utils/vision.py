import cv2
import numpy as np

yellow = [0, 255, 255]
red = [0, 0, 0]

def color_limits(color):
    c = np.uint8([[color]])
    hsvColor = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLim = np.array((hsvColor[0][0][0] - 10, 100, 100), dtype=np.uint8)
    upperLim = np.array((hsvColor[0][0][0] + 10, 255, 255), dtype=np.uint8)
    return lowerLim, upperLim

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower, upper = color_limits(yellow)
    lower2, upper2 = color_limits(red)

    mask = cv2.inRange(hsv_frame, lower, upper)
    mask2 = cv2.inRange(hsv_frame, lower2, upper2)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for c in contours:
            if cv2.contourArea(c) > 300:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 4)


    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('mask2', mask2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()