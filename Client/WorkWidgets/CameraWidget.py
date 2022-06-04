from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from matplotlib.pyplot import text
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
        self.MyReader = None
        self.ProcessCam = None
        self.detect_face = False
        self.current_img = None
        self.my_setting = {}
        self.menu_widget = MenuWidget()
        self.status_widget = StatusWidget()

        self.menu_widget.checkIn_button.clicked.connect(self.manualEnter)
        self.menu_widget.checkOut_button.clicked.connect(self.manualLeave)

        self.viewData = QtWidgets.QLabel('this is an image', self)
        self.viewData.setGeometry(QtCore.QRect(0, 0, 650, 650))
        self.viewData.setMinimumSize(QtCore.QSize(650, 650))
        self.viewData.setMaximumSize(QtCore.QSize(650, 650))
        self.viewData.setText("")
        
        layout_center = QtWidgets.QVBoxLayout()
        layout_center.addWidget(self.viewData)
        layout_center.addWidget(self.menu_widget)

        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(layout_center, stretch=60)
        layout.addWidget(self.status_widget, stretch=40)
        
        layout.setAlignment(Qt.AlignCenter) 
        self.setLayout(layout)        
    
    def setNewSetting(self, new_setting: dict):
        self.my_setting = new_setting

    def showData(self, img):
        self.Ny, self.Nx, _ = img.shape  
        if(self.detect_face):
            img = self.detectFace(img)
        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.current_img = img
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
        
    def readerCallback(self, data):
        if(self.checkWithServer(data)):
          self.MyReader.device.send_data('Card:PASS\n')
          status = self.sendPassToServer(data)
          self.status_widget.showPass('Enter' if status=='in' else 'Leave')
        else:
          self.MyReader.device.send_data('Card:FAIL\n')
          self.status_widget.showFail()

    def checkWithServer(self, data):
        self.my_setting['Server'].send_command('query_card', {'card_no':data})
        #recv_data = self.my_setting['Server'].wait_response()
        #return recv_data['is_school_member']
        return True

    def sendPassToServer(self, data):
        self.my_setting['Server'].send_command('swipe', {   'card_no': data, \
                                                            'time': self.status_widget.Time_val_label.text(),  \
                                                            'img_binary': ' '})
        #recv_data = self.my_setting['Server'].wait_response()
        #self.status_widget.Name_val_label.setText(recv_data['student_name'])
        #return recv_data['status']
        return 'in'
    
    def manualEnter(self):
        self.MyReader.device.send_data('Card:PASS\n')
        self.status_widget.showPass('Enter')
    
    def manualLeave(self):
        self.MyReader.device.send_data('Card:PASS\n')
        self.status_widget.showPass('Leave')
    
    def load(self):
        if(self.my_setting['COM'] != None):
            self.MyReader = CardReader()
            self.MyReader.uid.connect(self.readerCallback)
            self.MyReader.open(self.my_setting['COM'], 115200) 
            self.MyReader.start()
            self.menu_widget.checkIn_button.setDisabled(False)
            self.menu_widget.checkOut_button.setDisabled(False)
        else:
            self.menu_widget.checkIn_button.setDisabled(True)
            self.menu_widget.checkOut_button.setDisabled(True)

        if(self.my_setting['CAM'] != None):
            self.ProcessCam = Camera(selected_CAM=self.my_setting['CAM'])
            self.ProcessCam.rawdata.connect(self.showData) 
            self.ProcessCam.open()
            self.ProcessCam.start()
    
    def disconnectAll(self):
        if(self.MyReader != None and self.MyReader.connect):
            self.MyReader.close()
        if(self.ProcessCam != None and self.ProcessCam.connect):
            self.ProcessCam.close()


class MenuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("menu_widget")
        layout = QtWidgets.QHBoxLayout()
        self.checkIn_button = ButtonComponent("Check In")
        self.checkOut_button = ButtonComponent("Check Out")
        layout.addWidget(self.checkIn_button, stretch=1)
        layout.addWidget(self.checkOut_button, stretch=1)

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
            self.resetStatus()
        else:
            self.Status_ShowTime += 1

    def showPass(self, status):
        self.Status_val_label.setText('PASS')
        self.Status_val_label.setStyleSheet('background-color:rgb(0,255,0)')
        if(status == 'Enter'):
            self.msg_val_label.setText('You can enter school now !!')
        if(status == 'Leave'):
            self.msg_val_label.setText('You can leave school now !!')
        self.Status_ShowTime = 0

    def showFail(self):
        self.Status_val_label.setText('FAIL')
        self.Status_val_label.setStyleSheet('background-color:rgb(255,0,0)')
        self.msg_val_label.setText('Problem occur !!')
        self.Status_ShowTime = 0

    def resetStatus(self):
        self.Status_val_label.setText('')
        self.Status_val_label.setStyleSheet('background-color:rgb(33, 43, 51)')
        self.msg_val_label.setText('')