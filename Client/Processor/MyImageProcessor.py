from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import mediapipe as mp

mpFacedetection = mp.solutions.face_detection.FaceDetection()

class ImageProcessor:
    def __init__(self, showWidget, detectFace=False):
        self.viewData = showWidget
        self.detect_face = detectFace
        self.face_exist = False
        self.current_img = None

    def showData(self, img):
        self.Ny, self.Nx, _ = img.shape  
        if(self.detect_face):
            img, self.face_exist = self.detectFace(img)
        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)
        self.current_img = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(img.data, self.Nx, self.Ny, QtGui.QImage.Format_RGB888)
        self.viewData.setPixmap(QtGui.QPixmap.fromImage(qimg))

    def encodeImg(self, img):
        img_encode = cv2.imencode('.png', img)[1]
        data_encode = np.array(img_encode)
        data_encode = data_encode.tolist()
        return data_encode

    def detectFace(self, img):
        color = (0, 255, 0)  
        rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = mpFacedetection.process(rgbImg)
        exist = False
        if res.detections:
            exist = True
            for _, dectection in enumerate(res.detections):
                box = dectection.location_data.relative_bounding_box
                h, w, c = rgbImg.shape
                my_box = int(box.xmin * w), int(box.ymin * h), \
                         int(box.width * w), int(box.height * h) 
                cv2.rectangle(img, my_box, color, 2)
        return img, exist