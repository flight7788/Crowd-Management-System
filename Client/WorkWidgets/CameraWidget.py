from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent

import time
from datetime import datetime
from Camera.MyCamera import Camera
from CardReader.MyCardReader import CardReader
from Processor.MyImageProcessor import ImageProcessor
from Processor.MyServerProcessor import ServerProcessor

class CameraWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("camera_widget")
        self.MyReader = None
        self.ProcessCam = None
        self.SocketClient = None
        
        self.my_setting = {}
    
        self.menu_widget = MenuWidget()
        self.status_widget = StatusWidget()

        self.menu_widget.stu_ID_lineEdit.mousePressEvent = self.stuID_lineEditEvent
        self.menu_widget.checkIn_button.clicked.connect(self.manualEnterEvent)
        self.menu_widget.checkOut_button.clicked.connect(self.manualLeaveEvent)

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

        self.image_processor = ImageProcessor(self.viewData, True)
        self.server_processor = None
    
    def setNewSetting(self, new_setting: dict):
        self.my_setting = new_setting
        
    def readerCallEvent(self, data):
        if self.SocketClient != None and self.server_processor.checkWithServer(data) and \
                self.image_processor.face_exist:
            t = time.localtime()
            date_time = time.strftime("%Y/%m/%d %H:%M:%S", t)
            recv_data = self.server_processor.sendPassToServer(data, \
                                                date_time, \
                                                self.image_processor.encodeImg(self.image_processor.current_img))
            if recv_data != False:
                self.status_widget.showPass('Enter' if recv_data['status']=='in' else 'Leave')
                self.status_widget.Name_val_label.setText(recv_data['student_name'])
                self.status_widget.ID_val_label.setText(recv_data['student_id'])
                self.MyReader.sendPass()
            else:
                self.status_widget.showFail()
                self.MyReader.sendFail()
        else:
          self.MyReader.sendFail()
          self.status_widget.showFail()
    
    def stuID_lineEditEvent(self, event):
        self.menu_widget.checkIn_button.setDisabled(False)
        self.menu_widget.checkOut_button.setDisabled(False)

    def manualEnterEvent(self):
        if self.SocketClient != None and self.MyReader != None:
            if self.menu_widget.stu_ID_lineEdit.text() != '' and \
                self.image_processor.face_exist:
                t = time.localtime()
                date_time = time.strftime("%Y/%m/%d %H:%M:%S", t)
                recv_data = self.server_processor.sendManualPassToServer(
                        self.menu_widget.stu_ID_lineEdit.text(), 
                        date_time,
                        self.image_processor.encodeImg(self.image_processor.current_img),
                        'in')

                if recv_data != False:
                    self.MyReader.sendPass()
                    self.status_widget.showPass('Enter')
                    self.status_widget.Name_val_label.setText(recv_data)
                    self.status_widget.ID_val_label.setText(self.menu_widget.stu_ID_lineEdit.text())
                else:
                    self.MyReader.sendFail()
                    self.status_widget.showFail()
            else:
                self.MyReader.sendFail()
                self.status_widget.showFail()
        self.menu_widget.checkIn_button.setDisabled(True)
        self.menu_widget.checkOut_button.setDisabled(True)
        self.menu_widget.stu_ID_lineEdit.setText('')
          
    def manualLeaveEvent(self):
        if self.SocketClient != None and self.MyReader != None:
            if self.menu_widget.stu_ID_lineEdit.text() != '' and \
                self.image_processor.face_exist:
                t = time.localtime()
                date_time = time.strftime("%Y/%m/%d %H:%M:%S", t)
                recv_data = self.server_processor.sendManualPassToServer(
                        self.menu_widget.stu_ID_lineEdit.text(), 
                        date_time,
                        self.image_processor.encodeImg(self.image_processor.current_img),
                        'out')
                if recv_data != False:
                    self.MyReader.sendPass()
                    self.status_widget.showPass('Leave')
                    self.status_widget.Name_val_label.setText(recv_data)
                    self.status_widget.ID_val_label.setText(self.menu_widget.stu_ID_lineEdit.text())
                else:
                    self.MyReader.sendFail()
                    self.status_widget.showFail()
            else:
                self.MyReader.sendFail()
                self.status_widget.showFail()
        self.menu_widget.checkIn_button.setDisabled(True)
        self.menu_widget.checkOut_button.setDisabled(True)
        self.menu_widget.stu_ID_lineEdit.setText('')
    
    def load(self):
        if self.my_setting != {}:
            if self.my_setting['COM'] != None:
                self.MyReader = CardReader()
                self.MyReader.uid.connect(self.readerCallEvent)
                self.MyReader.open(self.my_setting['COM'], 115200) 
                self.MyReader.start()
                self.menu_widget.checkIn_button.setDisabled(False)
                self.menu_widget.checkOut_button.setDisabled(False)
            else:
                self.menu_widget.checkIn_button.setDisabled(True)
                self.menu_widget.checkOut_button.setDisabled(True)

            if self.my_setting['CAM'] != None:
                self.ProcessCam = Camera(selected_CAM=self.my_setting['CAM'])
                self.ProcessCam.rawdata.connect(self.image_processor.showData) 
                self.ProcessCam.open()
                self.ProcessCam.start()

            if self.my_setting['Server'] != None:
                self.SocketClient = self.my_setting['Server']
                self.server_processor =  ServerProcessor(self.SocketClient)
        self.menu_widget.checkIn_button.setDisabled(True)
        self.menu_widget.checkOut_button.setDisabled(True)
    
    def disconnectAll(self):
        if(self.MyReader != None and self.MyReader.connect):
            self.MyReader.close()
        if(self.ProcessCam != None and self.ProcessCam.connect):
            self.ProcessCam.close()
        if(self.SocketClient != None):
            self.SocketClient.client_socket.close()


class MenuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("menu_widget")
        main_layout = QtWidgets.QVBoxLayout()
        stu_ID_label = LabelComponent(16, 'Your ID:')
        self.stu_ID_lineEdit = LineEditComponent('', length=15)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(stu_ID_label, stretch=1, alignment=Qt.AlignRight)
        layout.addWidget(self.stu_ID_lineEdit, stretch=1, alignment=Qt.AlignLeft)
        main_layout.addLayout(layout, stretch=1)
        layout = QtWidgets.QHBoxLayout()
        self.checkIn_button = ButtonComponent("Check In")
        self.checkOut_button = ButtonComponent("Check Out")
        self.checkIn_button.setDisabled(True)
        self.checkOut_button.setDisabled(True)
        layout.addWidget(self.checkIn_button, stretch=1)
        layout.addWidget(self.checkOut_button, stretch=1)
        main_layout.addLayout(layout, stretch=1)
        self.setLayout(main_layout)


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
        self.Name_val_label = LabelComponent(14, "")

        ID_label = LabelComponent(14, "ID: ")
        self.ID_val_label = LabelComponent(14, "")

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
        layout.addWidget(ID_label, 3, 0, 1, 1)   
        layout.addWidget(self.ID_val_label, 3, 1, 1, 2)       
        layout.addWidget(Status_label, 4, 0, 1, 2)   
        layout.addWidget(self.Status_val_label, 5, 0, 1, 4)     
        layout.addWidget(self.msg_val_label, 6, 0, 1, 4)       
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
        self.Name_val_label.setText('')
        self.ID_val_label.setText('')
        self.Status_ShowTime = 0

    def resetStatus(self):
        self.Status_val_label.setText('')
        self.Status_val_label.setStyleSheet('background-color:rgb(33, 43, 51)')
        self.msg_val_label.setText('')
        self.Name_val_label.setText('')
        self.ID_val_label.setText('')