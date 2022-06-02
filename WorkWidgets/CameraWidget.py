from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from Camera.MyCamera import Camera
from CardReader.MyCardReader import CardReader

import numpy as np
import cv2
import mediapipe as mp


mpFacedetection = mp.solutions.face_detection.FaceDetection()

class CameraWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("camera_widget")
        
        menu_widget = MenuWidget()
        self.status_widget = StatusWidget()

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
        layout.addWidget(self.status_widget, stretch=40)
        
        layout.setAlignment(Qt.AlignCenter) 
        self.setLayout(layout)
    
        self.MyReader = CardReader()
        self.MyReader.uid.connect(self.Reader_callback) 
        self.MyReader.open('com6', 115200)
        self.MyReader.start()
      
        self.detect_face = False
        self.ProcessCam = Camera() 
        if self.ProcessCam.connect:
            self.ProcessCam.rawdata.connect(self.showData) 
            self.ProcessCam.open()
            self.ProcessCam.start()
    
    def showData(self, img):
        self.Ny, self.Nx, _ = img.shape  

        if(self.detect_face):
            img = self.detectFace(img)

        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(img.data, self.Nx, self.Ny, QtGui.QImage.Format_RGB888)
        self.viewData.setPixmap(QtGui.QPixmap.fromImage(qimg))

    def detectFace(self, img):
        color = (0, 255, 0)  
        rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = mpFacedetection.process(rgbImg)
        if res.detections:
            for _, dectection in enumerate(res.detections):
                box = dectection.location_data.relative_bounding_box
                h, w, c = rgbImg.shape
                my_box = int(box.xmin * w), int(box.ymin * h), \
                         int(box.width * w), int(box.height * h) 
                cv2.rectangle(img, my_box, color, 2)
        return img

    def load(self):
        pass
        
    def Reader_callback(self, data):
        if(data == '30a3557e'):
          self.MyReader.device.send_data('Card:PASS\n')
          self.status_widget.show_pass()
        else:
          self.MyReader.device.send_data('Card:FAIL\n')
          self.status_widget.show_fail()
    

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
        self.Status_val_label = LabelComponent(45, "")
        self.Status_val_label.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.Status_val_label.setMinimumSize(QtCore.QSize(400, 200))
        self.Status_val_label.setStyleSheet('background-color:rgb(33, 43, 51)')
        self.Status_val_label.setAlignment(Qt.AlignCenter) 
        self.Status_ShowTime = 0

        self.msg_val_label = LabelComponent(24, "")
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
        if(self.Status_ShowTime >= 3):
            self.Reset_status()
        else:
            self.Status_ShowTime += 1

    def show_pass(self):
        self.Status_val_label.setText('PASS')
        self.Status_val_label.setStyleSheet('background-color:rgb(0,255,0)')
        self.msg_val_label.setText('You can enter school now !!')
        self.Status_ShowTime = 0

    def show_fail(self):
        self.Status_val_label.setText('FAIL')
        self.Status_val_label.setStyleSheet('background-color:rgb(255,0,0)')
        self.msg_val_label.setText('Problem occur !!')
        self.Status_ShowTime = 0

    def Reset_status(self):
        self.Status_val_label.setText('')
        self.Status_val_label.setStyleSheet('background-color:rgb(33, 43, 51)')
        self.msg_val_label.setText('')