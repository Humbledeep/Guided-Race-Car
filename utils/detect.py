import cv2
import numpy as np

def detect(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    centres = []

    if len(contours) != 0:
        for c in contours:
            if cv2.contourArea(c) > 200:
                x, y, w, h = cv2.boundingRect(c)
                centres.append((int(x+w/2), int(y+h/2)))
                # cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 4)
    
    return centres