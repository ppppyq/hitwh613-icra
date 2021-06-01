import cv2 as cv
import numpy as np
import os

global adress,img_1,img_2
global real_x, real_y
global click_points_1, click_points_2
'''摄像头1透视变换所需要的点'''
click_points_1 = []
'''摄像头2透视变换所需要的点'''
click_points_2 = []

''' 鼠标事件，要点四次，分别是左上，右上，左下，右下'''
def return_adress():
    global adress

    return adress

def mouse_1(event, x, y, flags, param):
    global click_points_1
    global img_1
    list_xy = []
    if event == cv.EVENT_LBUTTONDOWN:
        xy = '%d,%d' % (x, y)
        list_xy.append(x)
        list_xy.append(y)
        print(list_xy)
        cv.circle(img_1, (x, y), 1, (0, 0, 255), thickness=-1)
        cv.imshow('img_1', img_1)
        click_points_1.append(list_xy)

def mouse_2(event, x, y, flags, param):
    global click_points_2
    global img_2
    list_xy = []
    if event == cv.EVENT_LBUTTONDOWN:
        xy = '%d,%d' % (x, y)
        list_xy.append(x)
        list_xy.append(y)
        print(list_xy)
        cv.circle(img_2, (x, y), 1, (0, 0, 255), thickness=-1)
        cv.imshow('img_2', img_2)
        click_points_2.append(list_xy)


def begin():
    global adress
    global img_1,img_2

#if __name__ == '__main__':
cap_1 = cv.VideoCapture(1)
cap_1.set(3, 448)
cap_1.set(4, 404)
ret_1, img_1 = cap_1.read()
img_2 = img_1.copy()

'''cap_2 = cv.VideoCapture(1)
    cap_2.set(3, 448)
    cap_2.set(4, 404)
    ret_2, img_2 = cap_2.read()'''

'''摄像头1'''

cv.namedWindow('img_1')
cv.setMouseCallback('img_1', mouse_1)
cv.imshow('img_1', img_1)

'''摄像头2'''

cv.namedWindow('img_2')
cv.setMouseCallback('img_2', mouse_2)
cv.imshow('img_2', img_2)

''' 暂停程序使坐标点保存'''

print('按下任意键')
key = cv.waitKey()
if key != -1:
    print('透视变换所需坐标点已保存')

while True:

        '''摄像头1的透视变换'''

        ret_1, img_1 = cap_1.read()
        pts1 = np.float32(click_points_1)
        pts2 = np.float32([[0, 0], [404, 0], [0, 448], [808, 448]])
        M_1 = cv.getPerspectiveTransform(pts1, pts2)
        dst_1 = cv.warpPerspective(img_1, M_1, (404, 448))

        '''摄像头2的透视变换'''

        #ret_2, img_2 = cap_2.read()
        img_2 = img_1.copy()
        pts1_ = np.float32(click_points_2)
        pts2_ = np.float32([[0, 0], [404, 0], [0, 448], [808, 448]])
        M_2 = cv.getPerspectiveTransform(pts1_, pts2_)
        dst_2 = cv.warpPerspective(img_2, M_2, (404, 448))

        original_img_1 = dst_1.copy()
        hsv_img_1 = cv.cvtColor(original_img_1, cv.COLOR_BGR2HSV)  # 摄像头1转hsv
        original_img_2 = dst_2.copy()
        hsv_img_2 = cv.cvtColor(original_img_2, cv.COLOR_BGR2HSV)  # 摄像头2转hsv

        '''该hsv上下限根据另外一个程序先跑，用鼠标点击获取实时上下限后再回来这边修改上下限'''

        lower = np.array([[0, 67, 91],
                          [60, 176, 148],   # 蓝车
                          [32, 113, 134]])  # 红车
        upper = np.array([[70, 167, 211],
                          [160, 255, 255],  # 蓝车
                          [132, 213, 254]])  # 红车

        img = []
        original_img = []
        hsv_img = []
        adress = []
        adress_1 = []
        adress_2 = []

        original_img.append(original_img_1)
        original_img.append(original_img_2)

        hsv_img.append(hsv_img_1)
        hsv_img.append(hsv_img_2)

        img.append(img_1)
        img.append(img_2)

        adress.append(adress_1)
        adress.append(adress_2)

        '''开始搜寻小车'''

        for k in range(2):
                mask = cv.inRange(hsv_img[k], lower[0], upper[0])  # 定向hsv图像掩膜
                kernel = np.ones((10, 10), np.uint8)
                closed = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=1)
                opened = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel, iterations=3)

                im0, contours, hierarchy = cv.findContours(opened, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    area = cv.contourArea(cnt)
                    epsilon = 0.05 * cv.arcLength(cnt, True)
                    approx = cv.approxPolyDP(cnt, epsilon, True)
                    imgcor = len(approx)
                    x, y, w, h = cv.boundingRect(approx)

                    if area > 1500 and w > 20 and h > 20:
                            if k == 0:
                                adress[k].append(((x+w)/200))
                                adress[k].append(((y+h)/200))
                            else:
                                adress[k].append(((x+w)/200))
                                adress[k].append(((y+h+404)/200))

                            judge = original_img[k][x:x + w, y:y + h]
                            judge = cv.cvtColor(original_img[k], cv.COLOR_BGR2HSV)
                            mask_b = cv.inRange(judge, lower[1], upper[1])
                            kernel_b = np.ones((10, 10), np.uint8)
                            closed_b = cv.morphologyEx(mask_b, cv.MORPH_CLOSE, kernel_b, iterations=2)
                            opened_b = cv.morphologyEx(closed_b, cv.MORPH_OPEN, kernel_b, iterations=2)
                            none_b, contours_b, hierarchy_b = cv.findContours(opened_b, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                            for cnt_b in contours_b:
                                area_b = cv.contourArea(cnt_b)
                                '''if area_b > 500:
                                    cv.putText(original_img[k], f'blue ({adress[k]})', (x, y-3),
                                               cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
                                    cv.rectangle(original_img[k], (x, y), (x+w, y+h), (0, 0, 255), 1)
                                    print(adress[k])  # 打印车中心坐标blue'''

                            mask_r = cv.inRange(judge, lower[2], upper[2])
                            kernel_r = np.ones((10, 10), np.uint8)
                            closed_r = cv.morphologyEx(mask_b, cv.MORPH_CLOSE, kernel_r, iterations=2)
                            opened_r = cv.morphologyEx(closed_r, cv.MORPH_OPEN, kernel_r, iterations=2)
                            none_r, contours_r, hierarchy_r = cv.findContours(opened_r, cv.RETR_EXTERNAL,
                                                                              cv.CHAIN_APPROX_SIMPLE)
                            for cnt_r in contours_r:
                                area_r = cv.contourArea(cnt_r)
                                '''if area_r > 500:
                                    cv.putText(original_img[k], f'red ({adress[k]})', (x, y-3),
                                               cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
                                    cv.rectangle(original_img[k], (x, y), (x+w, y+h), (0, 0, 255), 1)
                                    print(adress[k])  # 打印车中心坐标red'''

                cv.imshow(f'result{k}', original_img[k])
        if cv.waitKey(1) & 0xff == 27:
            break
cv.destroyAllWindows()

