import cv2 as cv
import numpy as np

def setHsv(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print("HSV is", hsv_video[y, x])
        cv.setTrackbarPos('H_l', 'image', hsv_video[y, x][0] - HSVvalue if (hsv_video[y, x][0] - HSVvalue > 0) else 0)
        cv.setTrackbarPos('H_h', 'image',
                           hsv_video[y, x][0] + HSVvalue if (hsv_video[y, x][0] + HSVvalue < 180) else 180)
        cv.setTrackbarPos('S_l', 'image', hsv_video[y, x][1] - HSVvalue if (hsv_video[y, x][1] - HSVvalue > 0) else 0)
        cv.setTrackbarPos('S_h', 'image',
                           hsv_video[y, x][1] + HSVvalue if (hsv_video[y, x][1] + HSVvalue < 255) else 255)
        cv.setTrackbarPos('V_l', 'image', hsv_video[y, x][2] - HSVvalue_ if (hsv_video[y, x][2] - HSVvalue_ > 0) else 0)
        cv.setTrackbarPos('V_h', 'image',
                           hsv_video[y, x][2] + HSVvalue_ if (hsv_video[y, x][2] + HSVvalue_ < 255) else 255)

def nothing(x):
    pass

def createbars():
    cv.createTrackbar("H_l", "image", 0, 180, nothing)
    cv.createTrackbar("H_h", "image", 0, 180, nothing)
    cv.createTrackbar("S_l", "image", 0, 255, nothing)
    cv.createTrackbar("S_h", "image", 0, 255, nothing)
    cv.createTrackbar("V_l", "image", 0, 255, nothing)
    cv.createTrackbar("V_h", "image", 0, 255, nothing)


cap = cv.VideoCapture(1)
cap.set(3, 320)
cap.set(4, 240)
cv.namedWindow("image")
lower = np.array([56, 204, 192])  # 设置初始值，改成矩阵形式
upper = np.array([156, 255, 255])
HSVvalue = 50
HSVvalue_ = 60
createbars()


while True:

    ret, video = cap.read()
    video = cv.GaussianBlur(video, (5, 5), 0)
    hsv_video = cv.cvtColor(video, cv.COLOR_BGR2HSV)  # 转hsv

    lower[0] = cv.getTrackbarPos("H_l", "image")  # 获取"H_l"滑块的实时值，下面原理一样
    upper[0] = cv.getTrackbarPos("H_h", "image")
    lower[1] = cv.getTrackbarPos("S_l", "image")
    upper[1] = cv.getTrackbarPos("S_h", "image")
    lower[2] = cv.getTrackbarPos("V_l", "image")
    upper[2] = cv.getTrackbarPos("V_h", "image")

    # 神奇的变化
    mask = cv.inRange(hsv_video, lower, upper)  # cv2.inrange()函数通过设定的最低、最高阈值获得图像的掩膜
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    #mask = cv.erode(mask, None, iterations=1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=4)

    img = video.copy()
    cv.imshow("img", img)
    cv.setMouseCallback("img", setHsv)  # 点击屏幕中需要追踪的颜色 设置HSV大概的范围值
    cv.imshow("mask", mask)

    none, contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        area = cv.contourArea(cnt)
        print(area)
        epsilon = 0.05 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        imgcor = len(approx)
        x, y, w, h = cv.boundingRect(approx)

        if area > 80 and w > 10 and h > 10:
            cv.rectangle(video, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv.putText(video, 'enemy', (x+6, y-3), cv.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 0), 1)
    cv.imshow("result", video)


    if cv.waitKey(1) & 0xff == 27:
        break
cap.release()
cv.destroyAllWindows()