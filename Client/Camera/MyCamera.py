import cv2
import time
import numpy as np
from PyQt5 import QtCore
import os


class Camera(QtCore.QThread):  
    rawdata = QtCore.pyqtSignal(np.ndarray)  
    def __init__(self, selected_CAM=0, parent=None):
        super().__init__(parent)
        self.cam = cv2.VideoCapture(selected_CAM, cv2.CAP_DSHOW)

        if self.cam is None or not self.cam.isOpened():
            self.connect = False
        else:
            self.connect = True
        self.running = False

    def run(self):
        while self.connect:
            ret, img = self.cam.read()   
            if ret:
                self.rawdata.emit(img)   
            else:    
                print("Warning!!!")
                self.connect = False
            self.running = True

    def open(self):
        if self.connect != True:
            self.connect = True    

    def close(self):
        if self.connect:
            self.connect = False   
            self.running = False
            while(self.running): pass
            self.cam.release()      

    def get_list_CAM(self, maxNum=5):
        index = 0
        arr = []
        while index < maxNum:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            ret, _ = cap.read()
            if ret:
                arr.append({'index':index, 'Name':'CAM{}'.format(index)})
                cap.release()
            index += 1
        return arr
        

if __name__ == '__main__':
  MyCAM = Camera()
  for i in MyCAM.get_list_CAM():
    print(i['Name'])
  