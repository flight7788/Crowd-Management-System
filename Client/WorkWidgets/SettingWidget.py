from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from Camera.MyCamera import Camera
from CardReader.MyCardReader import CardReader

class SettingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("setting_widget")

        header_label = LabelComponent(45, "Setting")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("border: 5px solid rgb(255, 255, 255); color: rgb(255, 255, 255)")

        self.refresh_button = ButtonComponent("Refresh")
        self.refresh_button.clicked.connect(self.update_combo_box)

        self.status_label = LabelComponent(24, "")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 3px; color: rgb(255, 0, 0);")

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
        self.confirm_button.clicked.connect(self.confirm_event)
       
        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(header_label, 0, 0, 1, 3)
        main_layout.addWidget(self.status_label, 1, 0, 1, 3)

        layout = QtWidgets.QVBoxLayout()
        
        layout_H1 = QtWidgets.QHBoxLayout()
        layout_H1.addWidget(self.refresh_button, stretch=40)
        layout_H1.addWidget(LabelComponent(16, ""), stretch=60)
        layout.addLayout(layout_H1, stretch=33)
        
        layout_H2 = QtWidgets.QHBoxLayout()
        layout_H2.addWidget(selectCAM_label, stretch=45)
        layout_H2.addWidget(self.combo_box_selectCAM, stretch=55)
        layout.addLayout(layout_H2, stretch=33)

        layout_H3 = QtWidgets.QHBoxLayout()
        layout_H3.addWidget(selectCOM_label, stretch=45)
        layout_H3.addWidget(self.combo_box_selectCOM, stretch=55)
        layout.addLayout(layout_H3, stretch=33)

        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setSpacing(50)

        main_layout.addLayout(layout, 2, 0, 3, 3)
        main_layout.addWidget(self.confirm_button, 5, 3, 1, 1)
        main_layout.setVerticalSpacing(10)
        self.setLayout(main_layout)

        self.MyReader = CardReader()
        self.ProcessCam = Camera() 

        self.COM_list = []
        self.CAM_list = []
        self.selected_COM = None
        self.selected_CAM = None

    def update_combo_box(self):
        self.combo_box_selectCAM.clear()
        self.CAM_list = self.ProcessCam.get_list_CAM()
        for device in self.CAM_list:
            self.combo_box_selectCAM.addItem(device['Name'])
        
        self.combo_box_selectCOM.clear()
        self.COM_list = self.MyReader.device.get_list_port()
        for device in self.COM_list: 
            self.combo_box_selectCOM.addItem(device.description)
        self.status_label.setText('')

    def confirm_event(self):
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

        if(status):
            self.status_label.setText('New setting is Sucess')

    def load(self):
        self.update_combo_box()
        self.status_label.setText('')
       

   