#coding=gbk
import cv2
import numpy as np

camera = cv2.VideoCapture(0)  # ����0��ʾ��һ������ͷ
# �ж���Ƶ�Ƿ��
if (camera.isOpened()):
    print('Open')
else:
    print('����ͷδ��')

# ������,�鿴��Ƶsize
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('size:' + repr(size))

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
kernel = np.ones((5, 5), np.uint8)
background = None

while True:
    # ��ȡ��Ƶ��
    grabbed, frame_lwpCV = camera.read()
    # ��֡����Ԥ������ת�Ҷ�ͼ���ٽ��и�˹�˲���
    # �ø�˹�˲�����ģ���������д����ԭ��ÿ���������Ƶ��������Ȼ�𶯡����ձ仯��������ͷ�����ԭ�����������������������ƽ����Ϊ�˱������˶��͸���ʱ�����������
    gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
    gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

    # ����һ֡����Ϊ��������ı���
    if background is None:
        background = gray_lwpCV
        continue
    # ����ÿ���ӱ���֮���ȡ��֡����������뱱��֮��Ĳ��죬���õ�һ�����ͼ��different map����
    # ����ҪӦ����ֵ���õ�һ���ڰ�ͼ�񣬲�ͨ��������������ͣ�dilate��ͼ�񣬴Ӷ��Կף�hole����ȱ�ݣ�imperfection�����й�һ������
    diff = cv2.absdiff(background, gray_lwpCV)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]  # ��ֵ����ֵ����
    diff = cv2.dilate(diff, es, iterations=2)  # ��̬ѧ����

    # ��ʾ���ο�
    image, contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)  # �ú�������һ��ͼ����Ŀ�������
    for c in contours:
        if cv2.contourArea(c) < 1500:  # ���ھ�������ֻ��ʾ���ڸ�����ֵ������������һЩ΢С�ı仯������ʾ�����ڹ��ղ���������͵�����ͷ�ɲ��趨������С�ߴ����ֵ
            continue
        (x, y, w, h) = cv2.boundingRect(c)  # �ú���������εı߽��
        cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('contours', frame_lwpCV)
    cv2.imshow('dis', diff)

    key = cv2.waitKey(1) & 0xFF
    # ��'q'���˳�ѭ��
    if key == ord('q'):
        break
# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()