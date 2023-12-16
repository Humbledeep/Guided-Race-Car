import cv2

l_cap = cv2.VideoCapture(1)
r_cap = cv2.VideoCapture(2)
l_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
l_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
r_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
r_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

counter = 0

while l_cap.isOpened() and r_cap.isOpened():
    retL, l_img = l_cap.read()
    retR, r_img = r_cap.read()
    print(l_img.shape)
    print(r_img.shape)

    key = cv2.waitKey(30)

    if key == 27:
        break
    elif key == ord('s'):
        cv2.imwrite('calibrationImages/left/img_l_' + str(counter)+'.png', l_img)
        cv2.imwrite('calibrationImages/right/img_r_' + str(counter)+'.png', r_img)
        print(f'Saved {counter}')
        counter += 1

    cv2.imshow('Left', l_img)
    cv2.imshow('Right', r_img)