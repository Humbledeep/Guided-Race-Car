import socket, time, math, logging, keyboard

import multiprocessing as mp

import cv2
import numpy as np

from utils.detect import detect
from utils.getWorldCoord import depth, objPos

HOST = "169.254.245.219"
PORT = 8000
logging.basicConfig(format='%(levelname)s - %(asctime)s:\t%(message)s')

class Server:
    def __init__(self, sock=None, host=HOST, port=PORT):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.sock.bind((host,port))
        
        self.sock.listen(1)

        self.conn, self.addr = self.sock.accept()
        print("Connected to: {}".format(self.addr))
    
    def logger(self, level, msg):
        func = getattr(logging, level)
        func(msg)
    
    def send(self, data):
        self.conn.send(data.encode("UTF-8"))

def color_limits(color):
    c = np.uint8([[color]])
    hsvColor = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLim = np.array((hsvColor[0][0][0] - 10, 100, 100), dtype=np.uint8)
    upperLim = np.array((hsvColor[0][0][0] + 10, 255, 255), dtype=np.uint8)
    return lowerLim, upperLim

def handleVision():
    l_intrinsics = np.matrix([[453.94061098, 0, 257.57924241],
                          [0, 508.99046337, 317.63282485],
                          [0, 0, 1]], dtype=np.float64)
    
    l_dist = np.array([[ 0.30771479, -2.10488081, -0.00574309,  0.01595141,  4.32072714]], dtype=np.float64)

    r_intrinsics = np.matrix([[446.77078183, 0, 258.4531829],
                            [0, 495.8307978, 315.72741114],
                            [0, 0, 1]], dtype=np.float64)
    
    r_dist = np.array([[ 0.28502244, -1.89144499, -0.00596839,  0.01670784,  3.75411371]], dtype=np.float64)

    yellow = [0, 255, 255]

    # TODO: Measure
    B = 60  # mm
    f = None
    fov = None

    l_cap = cv2.VideoCapture(1)
    r_cap = cv2.VideoCapture(2)
    l_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    l_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    r_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    r_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    while True:
        retL, frameL = l_cap.read()
        retR, frameR = r_cap.read()
        frameL = cv2.undistort(frameL, l_intrinsics, l_dist, None)
        frameR = cv2.undistort(frameR, r_intrinsics, r_dist, None)

        # HSV DETECTION

        if not retL or not retR:
            break

        hsv_frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2HSV)
        hsv_frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)

        lower, upper = color_limits(yellow)

        maskL = cv2.inRange(hsv_frameL, lower, upper)
        maskR = cv2.inRange(hsv_frameR, lower, upper)

        centresL = detect(maskL)
        centresR = detect(maskR)

        lineL = np.array(centresL)
        lineR = np.array(centresR)

        if len(centresL) > 1:
            # cv2.drawContours(frameL, [lineL], 0, (0, 255, 255), 3)
            for i, p in enumerate(centresL):
                if i == len(centresL) - 1:
                    break
                cv2.line(frameL,p,centresL[i+1], (0,255,255), 3)

        if len(centresR) > 1:
            # cv2.drawContours(frameR, [lineR], 0, (0, 255, 255), 3)
            for i, p in enumerate(centresR):
                if i == len(centresR) - 1:
                    break
                cv2.line(frameR,p,centresR[i+1], (0,255,255), 3)

        if len(centresL) != 0 and len(centresR) != 0:
            for cL, cR in zip(centresL, centresR):
                cv2.circle(frameL, cL, 2, (0, 255, 0), 5)
                cv2.circle(frameR, cR, 2, (0, 255, 0), 5)
                Z = objPos(cL, cR, B, l_intrinsics, r_intrinsics)
                print('X', Z[0], 'Y', Z[1])
                cv2.putText(frameL, text = str(Z[2])[:5], org = cL, color = (255, 0, 0), fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness = 1)
                cv2.putText(frameR, text = str(Z[2])[:5], org = cR, color = (255, 0, 0), fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale=1, thickness = 1)


        
        cv2.imshow('binL', frameL)
        cv2.imshow('binR', frameR)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def handleServer():
    print('awaiting conn')
    server = Server()
    
    w_held = False
    s_held = False
    d_held = False
    a_held = False


    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == 'w' and not w_held:
            w_held = True
            server.send('m,100')
        
        if event.event_type == keyboard.KEY_UP and event.name == 'w':
            w_held = False
            server.send('stop')
            server.send('stopt')

        if event.event_type == keyboard.KEY_DOWN and event.name == 's' and not s_held:
            s_held = True
            server.send('m,-100')

        if event.event_type == keyboard.KEY_UP and event.name == 's':
            s_held = False
            server.send('stop')
            server.send('stopt')

        if event.event_type == keyboard.KEY_DOWN and event.name == 'a' and not a_held:
            a_held = True
            server.send('t,-20')
        
        if event.event_type == keyboard.KEY_UP and event.name == 'a':
            a_held = False
            server.send('stopt')
            server.send('stop')
        
        if event.event_type == keyboard.KEY_DOWN and event.name == 'd' and not d_held:
            d_held = True
            server.send('t,20')
        
        if event.event_type == keyboard.KEY_UP and event.name == 'd':
            d_held = False
            server.send('stopt')
            server.send('stop')
        
        if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
            server.send('t,0')


if __name__ == "__main__":
    serverProcess = mp.Process(target=handleServer)
    serverProcess.start()

    visionProcess = mp.Process(target=handleVision)
    visionProcess.start()

    serverProcess.join()
    visionProcess.join()

    


    # TEST CALLS
