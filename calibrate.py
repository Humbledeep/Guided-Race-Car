# example adapted from opencv docs

import cv2 as cv
import numpy as np
import glob

checkerboardSize = (9, 6)
frameSize = (480, 640)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((checkerboardSize[0] * checkerboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:checkerboardSize[0],0:checkerboardSize[1]].T.reshape(-1,2)

# objp = objp * checkerboardSquareSize_mm

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space

imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.

imagesL = glob.glob('calibrationImages/left/*.png')
imagesR = glob.glob('calibrationImages/right/*.png')


for l_img, r_img in zip(imagesL, imagesR):
    imgL = cv.imread(l_img)
    imgR = cv.imread(r_img)

    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    retL, cornersL = cv.findChessboardCorners(grayL, checkerboardSize, None)
    retR, cornersR = cv.findChessboardCorners(grayR, checkerboardSize, None)

    # If found, add object points, image points (after refining them)
    if retL and retR:
        objpoints.append(objp)

        cornersL = cv.cornerSubPix(grayL,cornersL, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL)

        cornersR = cv.cornerSubPix(grayR,cornersR, (11,11), (-1,-1), criteria)
        imgpointsR.append(cornersR)


        # Draw and display the corners
        cv.drawChessboardCorners(imgL, checkerboardSize, cornersL, retL)
        cv.imshow('imgL', imgL)
        cv.drawChessboardCorners(imgR, checkerboardSize, cornersR, retR)
        cv.imshow('imgR', imgR)

        cv.waitKey(10)
cv.destroyAllWindows()


# Obtaining calibration params

retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))


# Stereo vision calib

flags = 0
flags |= cv.CALIB_FIX_INTRINSIC
criteria_stereo= (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)

with open('camera_intrinsics.txt', 'w') as file:
    file.write(str(newCameraMatrixL))
    file.write('\n')
    file.write(str(distL))
    file.write('\n')
    file.write(str(newCameraMatrixR))
    file.write('\n')
    file.write(str(distR))
    file.write('\n')

print(newCameraMatrixL, '\n')
print(distL, '\n')
print(newCameraMatrixR, '\n')
print(distR, '\n')