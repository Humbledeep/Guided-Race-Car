import cv2
import numpy as np

def depth(point_left, point_right, b, l_intrinsics, r_intrinsics):
    x_l = point_left[0]
    x_r = point_right[0]

    f = l_intrinsics[0, 0]
    # f = 25

    d = x_l - x_r

    Z = (b*0.001*f)/d

    return abs(Z)

def objPos(point_left, point_right, b, l_intrinsics, r_intrinsics):
    x_l = point_left[0]
    x_r = point_right[0]
    # print(x_l, x_r)

    # c_l_x = l_intrinsics[0][2]
    # c_r_x = r_intrinsics[0][2]
    # x_l = abs(c_l_x - x_l)
    # x_r = abs(c_r_x - x_r)

    f = r_intrinsics[0, 0]

    d = x_l - x_r

    Z = (b*0.001*f)/d

    X = Z*x_l/f

    Y = Z*point_left[1]/f

    return (X, Y, Z)

