import cv2
import time
import numpy as np
from PyQt5 import QtCore


class Camera(QtCore.QThread):  
    rawdata = QtCore.pyqtSignal(np.ndarray)  
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        r, frame = self.cam.read()
        self.res_x = frame.shape[0]
        self.res_y = frame.shape[1]

        if self.cam is None or not self.cam.isOpened():
            self.connect = False
        else:
            self.connect = True
        self.running = False

    def run(self):
        while self.running and self.connect:
            ret, img = self.cam.read()   
            if ret:
                self.rawdata.emit(img)   
            else:    
                print("Warning!!!")
                self.connect = False

    def open(self):
        if self.connect:
            self.running = True    

    def stop(self):
        if self.connect:
            self.running = False    

    def close(self):
        if self.connect:
            self.running = False   
            time.sleep(1)
            self.cam.release()      
