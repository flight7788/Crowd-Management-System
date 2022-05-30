from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from Camera.Camera import Camera

import numpy as np
import cv2


face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class CameraWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("camera_widget")
        
        menu_widget = MenuWidget()
        status_widget = StatusWidget()

        self.viewData = QtWidgets.QLabel('this is an image', self)
        self.viewData.setGeometry(QtCore.QRect(0, 0, 650, 650))
        self.viewData.setMinimumSize(QtCore.QSize(650, 650))
        self.viewData.setMaximumSize(QtCore.QSize(650, 650))
        self.viewData.setText("")
        
        layout_center = QtWidgets.QVBoxLayout()
        layout_center.addWidget(self.viewData)
        layout_center.addWidget(menu_widget)

        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_center, stretch=60)
        layout.addWidget(status_widget, stretch=40)
        
        layout.setAlignment(Qt.AlignCenter) 
        self.setLayout(layout)

        self.detect_face = False

        self.ProcessCam = Camera() 
        if self.ProcessCam.connect:
            self.ProcessCam.rawdata.connect(self.showData) 
            self.ProcessCam.open()
            self.ProcessCam.start()
    
    def showData(self, img):
        self.Ny, self.Nx, _ = img.shape  
        img_new = np.zeros_like(img)
        img_new[...,0] = img[...,2]
        img_new[...,1] = img[...,1]
        img_new[...,2] = img[...,0]
        img = img_new

        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)

        if(self.detect_face):
            img = self.detectFace(img)

        qimg = QtGui.QImage(img.data, self.Nx, self.Ny, QtGui.QImage.Format_RGB888)
        self.viewData.setPixmap(QtGui.QPixmap.fromImage(qimg))

    def detectFace(self, img):
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        color = (0, 255, 0)  
        faceRects = face_classifier.detectMultiScale(grayImg, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
       

        if len(faceRects):  
            for faceRect in faceRects: 
                x, y, w, h = faceRect
            cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
        return img

    def load(self):
        pass
        

class MenuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("menu_widget")
        
        layout = QtWidgets.QHBoxLayout()
        checkIn_button = ButtonComponent("Check In")
        checkOut_button = ButtonComponent("Check Out")
        #start_button.clicked.connect()
        #stop_button.clicked.connect()
        

        layout.addWidget(checkIn_button, stretch=1)
        layout.addWidget(checkOut_button, stretch=1)

        self.setLayout(layout)


class StatusWidget(QtWidgets.QWidget):
    def __init__(self,):
        super().__init__()
        self.setObjectName("status_widget")
        
        layout = QtWidgets.QGridLayout()
        Date_label = LabelComponent(14, "Date: ")
        self.Date_val_label = LabelComponent(14, "")
       
        Time_label = LabelComponent(14, "Time: ")
        self.Time_val_label = LabelComponent(14, "")

        Name_label = LabelComponent(14, "Name: ")
        self.Name_val_label = LabelComponent(14, "XX")

        Status_label = LabelComponent(14, "Status: ")
        self.Status_val_label = LabelComponent(45, "PASS")
        self.Status_val_label.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.Status_val_label.setMinimumSize(QtCore.QSize(400, 200))
        self.Status_val_label.setStyleSheet('background-color:rgb(0,255,0)')
        self.Status_val_label.setAlignment(Qt.AlignCenter) 

        self.msg_val_label = LabelComponent(24, "You can enter school now !!")
        self.msg_val_label.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.msg_val_label.setMinimumSize(QtCore.QSize(400, 200))
        self.msg_val_label.setAlignment(Qt.AlignCenter) 
        self.msg_val_label.setStyleSheet("color: rgb(255, 255, 255); border: 3px solid rgb(120, 157, 186)")

        layout.addWidget(Date_label, 0, 0, 1, 1)   
        layout.addWidget(self.Date_val_label, 0, 1, 1, 3)  
        layout.addWidget(Time_label, 1, 0, 1, 1)   
        layout.addWidget(self.Time_val_label, 1, 1, 1, 2)       
        layout.addWidget(Name_label, 2, 0, 1, 1)   
        layout.addWidget(self.Name_val_label, 2, 1, 1, 2)       
        layout.addWidget(Status_label, 3, 0, 1, 2)   
        layout.addWidget(self.Status_val_label, 4, 0, 1, 4)     
        layout.addWidget(self.msg_val_label, 5, 0, 1, 4)       
        layout.setAlignment(Qt.AlignLeft|Qt.AlignTop)     
        layout.setVerticalSpacing(20)

        self.setLayout(layout)

        QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.english = QtCore.QLocale()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def showTime(self):
        current_date = QtCore.QDate.currentDate()
        self.Date_val_label.setText(self.english.toString(current_date))
        current_time = QtCore.QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.Time_val_label.setText(label_time)