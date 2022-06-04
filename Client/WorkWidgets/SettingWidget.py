from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from Camera.MyCamera import Camera
from CardReader.MyCardReader import CardReader
from SocketClient.socket_client import SocketClient

class SettingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("setting_widget")

        header_label = LabelComponent(32, "Setting")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("border: 5px solid rgb(255, 255, 255); color: rgb(255, 255, 255)")

        self.refresh_button = ButtonComponent("Refresh")
        self.refresh_button.clicked.connect(self.refreshEvent)

        self.status_label = LabelComponent(24, "")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 3px; color: rgb(255, 0, 0);")

        selectIP_label = LabelComponent(16, "Please select your Server IP: ")
        self.IP_widget = IPWidget()
        selectPort_label = LabelComponent(16, "Please select your Server port: ")
        self.Port_widget = LineEditComponent()
        self.Port_widget.setValidator(QtGui.QIntValidator(0,65535)) 
        selectCAM_label = LabelComponent(16, "Please select your CAM: ")

        self.combo_box_selectCAM = QtWidgets.QComboBox()
        self.combo_box_selectCAM.setFont(QtGui.QFont("微軟正黑體", 12))
        self.combo_box_selectCAM.setStyleSheet("color: rgb(255, 255, 255);\
                                    border: 1px solid rgb(255, 255, 255)")

        selectCOM_label = LabelComponent(16, "Please select your CardReader: ")

        self.combo_box_selectCOM = QtWidgets.QComboBox()
        self.combo_box_selectCOM.setFont(QtGui.QFont("微軟正黑體", 12))
        self.combo_box_selectCOM.setStyleSheet("color: rgb(255, 255, 255);\
                                    border: 1px solid rgb(255, 255, 255)")
    
        self.confirm_button = ButtonComponent("Confirm")
        self.confirm_button.clicked.connect(self.confirmEvent)
       
        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(header_label, 0, 0, 1, 2)
        main_layout.addWidget(self.status_label, 1, 0, 1, 3)
       
        main_layout.addWidget(self.refresh_button, 2, 0, 1, 1)

        main_layout.addWidget(selectIP_label, 3, 0, 1, 3)
        layout_H1 = QtWidgets.QHBoxLayout()
        layout_H1.addWidget(LabelComponent(16, " "), stretch=4)
        layout_H1.addWidget(self.IP_widget, stretch=96, alignment=Qt.AlignLeft)
        main_layout.addLayout(layout_H1, 4, 0, 1, 3)

        main_layout.addWidget(selectPort_label, 5, 0, 1, 3)
        layout_H2 = QtWidgets.QHBoxLayout()
        layout_H2.addWidget(LabelComponent(16, " "), stretch=5)
        layout_H2.addWidget(self.Port_widget, stretch=95, alignment=Qt.AlignLeft)
        main_layout.addLayout(layout_H2, 6, 0, 1, 3)

        main_layout.addWidget(selectCAM_label, 7, 0, 1, 3)
        layout_H3 = QtWidgets.QHBoxLayout()
        layout_H3.addWidget(LabelComponent(16, " "), stretch=5)
        layout_H3.addWidget(self.combo_box_selectCAM, stretch=95)
        main_layout.addLayout(layout_H3, 8, 0, 1, 3)

        main_layout.addWidget(selectCOM_label, 9, 0, 1, 3)
        layout_H4 = QtWidgets.QHBoxLayout()
        layout_H4.addWidget(LabelComponent(16, " "), stretch=5)
        layout_H4.addWidget(self.combo_box_selectCOM, stretch=95)
        main_layout.addLayout(layout_H4, 10, 0, 1, 3)

        main_layout.addWidget(self.confirm_button, 11, 3, 1, 1)
        main_layout.setVerticalSpacing(20)
        
        self.setLayout(main_layout)

        self.MyReader = CardReader()
        self.ProcessCam = Camera() 

        self.COM_list = []
        self.CAM_list = []
        self.selected_COM = None
        self.selected_CAM = None
        self.selected_ip = None
        self.selected_port = None
        self.select_socket_client = None

    def updateComboBox(self):
        self.combo_box_selectCAM.clear()
        self.CAM_list = self.ProcessCam.get_list_CAM()
        for device in self.CAM_list:
            self.combo_box_selectCAM.addItem(device['Name'])
        
        self.combo_box_selectCOM.clear()
        self.COM_list = self.MyReader.device.get_list_port()
        for device in self.COM_list: 
            self.combo_box_selectCOM.addItem(device.description)
       
    def refreshEvent(self):
        self.updateComboBox()
        self.status_label.setText('')
        self.IP_widget.IP_lineEdit.setText('')
        self.Port_widget.setText('')

    def confirmEvent(self):
        status = True
        try:
            self.MyReader = CardReader()
            self.selected_COM = self.COM_list[self.combo_box_selectCOM.currentIndex()].name
            self.MyReader.open(self.selected_COM, 115200)
        except:
            if self.selected_COM != None:
                print('{} is unable to connect.'.format(self.selected_COM))
                self.status_label.setText('{} is unable to connect.'.format(self.selected_COM))
            else:
                print('No available CardReader exist !!')
                self.status_label.setText('No available CardReader exist !!')
            status = False

        try:
            self.detect_face = False
            self.selected_CAM = self.CAM_list[self.combo_box_selectCAM.currentIndex()]['index']
            self.ProcessCam = Camera(selected_CAM=self.selected_CAM) 
            self.ProcessCam.open()
        except:
            if self.selected_CAM != None:
                print('{} is unable to connect.'.format(self.combo_box_selectCAM.currentData()))
                self.status_label.setText('{} is unable to connect.'.format(self.combo_box_selectCAM.currentData()))
            else:
                print('No available Camera exist !!')
                self.status_label.setText('No available Camera exist !!')
            status = False

        if self.validateIP(self.IP_widget.IP_lineEdit.text()):
            self.selected_ip = self.IP_widget.IP_lineEdit.text()
            if self.validatePort(self.Port_widget.text()):
                self.selected_port = int(self.Port_widget.text())
                try:
                    print("IP: {}, Port: {}".format(self.selected_ip, self.selected_port))
                    self.select_socket_client = SocketClient(self.selected_ip, self.selected_port)
                except:
                    print('Unable reach server !!')
                    self.status_label.setText('Unable reach server !!')
                    status = False
            else:
                print('Port format error !!')
                self.status_label.setText('Port format error !!')
                status = False
        else:
            print('IP format error !!')
            self.status_label.setText('IP format error !!')
            status = False

        if status:
            self.status_label.setText('New setting is sucess !!')

    def validateIP(self, my_ip: str):
        status = True
        ip = my_ip.split('.')
        if len(ip) != 4:
            return False
        for sub_ip in ip:
            try:
                num = int(sub_ip)
                if num > 255 or num < 0:
                    status = False
            except:
                return False
        return status

    def validatePort(self, my_port: str):
        try:
            num = int(my_port)
            if num > 65535 or num < 0:
                return False
        except:
            return False
        return True

    def getNewSetting(self):
        my_setting = {
            "COM": self.selected_COM,
            "CAM": self.selected_CAM,
            "Server": self.select_socket_client
        }
        return my_setting

    def load(self):
        self.updateComboBox()
        self.status_label.setText('')
       
    def disconnectAll(self):
        if(self.MyReader != None and self.MyReader.connect):
            self.MyReader.close()
        if(self.ProcessCam != None and self.ProcessCam.connect):
            self.ProcessCam.close()
 
class IPWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ip_widget")
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"   
        ipRegex = QtCore.QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QtGui.QRegExpValidator(ipRegex, self)   
 
        self.IP_lineEdit = LineEditComponent("", length=15, width=250)
        self.IP_lineEdit.setAlignment(Qt.AlignCenter)
        self.IP_lineEdit.setValidator(ipValidator)      
        self.IP_lineEdit.setInputMask("000.000.000.000;_")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.IP_lineEdit)
        self.setLayout(layout)
        
   