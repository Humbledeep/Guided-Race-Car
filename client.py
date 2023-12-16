#!/usr/bin/env python3
import socket
import os
from time import sleep
from math import pi, cos, sin, sqrt, acos, asin, atan2, atan, isclose
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor, MoveTank

HOST = "169.254.245.219"
PORT = 8000

# steeringMotor = LargeMotor(OUTPUT_D)
tank_D = MoveTank(OUTPUT_B, OUTPUT_A)
tank_S = MoveTank(OUTPUT_D, OUTPUT_C)
gy = GyroSensor()
gy.reset()
gy.calibrate()

class Client:
    def __init__(self, host = HOST, port = PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.connect((host, port))
    
    def pollData(self):
        data = self.s.recv(128).decode("UTF-8")
        if data:
            print(data)
            return data

client = Client()

while True:
    print("GYRO ANGLE:", gy.angle)
    try:
        instruction = client.pollData().split(',')
        print(instruction)
        if instruction[0] == 'm':
            # tank_D.on_for_rotations(int(instruction[1]), int(instruction[1]), 0.1, brake=False,block=False)
            tank_D.on(left_speed = int(instruction[1]), right_speed = int(instruction[1]))
            tank_S.on(left_speed = -int(instruction[1]), right_speed = -int(instruction[1]))

        
        elif instruction[0] == 'stop':
            tank_D.off(brake=False)
        
        elif instruction[0] == 'stopt':
            tank_S.off(brake=False)

        elif instruction[0] == 't':
            if int(instruction[1]) < 0:
                print('left')
                speed = int(instruction[1])
                tank_S.on(left_speed=speed*-5, right_speed=speed*5)
                tank_D.on(left_speed=-100, right_speed=100)
            else:
                print('right')
                speed = int(instruction[1]) * -1
                tank_S.on(left_speed=5*speed, right_speed=speed*-5)
                tank_D.on(left_speed=100, right_speed=-100)
        # tank_D.run_forever(speed_sp = 200)
    except Exception as e:
        print("Error:", e)