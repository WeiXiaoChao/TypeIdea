#coding=gbk
# ����ʹ�� python3���ϰ汾

# ��껭�����Ŀ�����и���(ÿ��һ�������һ��enter��)


import numpy as np
import cv2
import sys
import time


# ������ͷ����ȡ��һ֡ͼ��
cv2.namedWindow("tracking")
#camera = cv2.VideoCapture("2.avi")
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ok_cam, image_pre = camera.read()
if not ok_cam:
    print('Failed to read video')
    exit()

img_h, img_w, c = image_pre.shape
image = cv2.resize(image_pre, (int(img_w/2), int(img_h/2)))

# ��ʼ��num_obj��Ŀ��
num_obj = 20
bbox_list = []
tracker_list = []

for i in range(0, num_obj):
    bbox_tmp = cv2.selectROI('tracking', image)
    bbox_list.append(bbox_tmp)

    tracker_tmp = cv2.TrackerMOSSE_create()
    ok_tmp = tracker_tmp.init(image, bbox_tmp)
    tracker_list.append(tracker_tmp)


# ѭ������
while camera.isOpened():

    ok_cam, image_pre = camera.read()

    if not ok_cam:
        print('no image to read')
        break

    img_h, img_w, c = image_pre.shape
    image = cv2.resize(image_pre, (int(img_w / 2), int(img_h / 2)))

    bbox_info = []

    # ���¸��ٽ��
    pre = time.time()
    for tracker in tracker_list:
        ok_t, bbox_t = tracker.update(image)
        bbox_info.append((ok_t, bbox_t))
    print(time.time() - pre, '*********')

    # ��ͼ������ʾ���ٽ��
    for tmp_info in bbox_info:
        newbox = tmp_info[1]
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (200,0,0))

    cv2.imshow('tracking', image)
    k = cv2.waitKey(1)
    if k == 27 : break # esc pressed



