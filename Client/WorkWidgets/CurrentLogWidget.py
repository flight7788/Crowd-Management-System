from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent

from Processor.MyServerProcessor import ServerProcessor
import csv


class CurrentLogWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("currentLog_widget")

        self.my_setting = {}
        self.SocketClient = None
        self.server_processor = None
        self.log_data = []

        header_label = LabelComponent(32, "Currnt Log")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("border: 5px solid rgb(255, 255, 255); color: rgb(255, 255, 255)")

        self.search_button = ButtonComponent("Search")
        self.save_button = ButtonComponent("Save as")
        self.save_button.setDisabled(True)

        search_label = LabelComponent(16, "Your ID:")
        search_label.setAlignment(Qt.AlignCenter)
        self.ID_lineEdit = LineEditComponent()
        self.ID_lineEdit.setAlignment(Qt.AlignCenter)
        self.info_label = LabelComponent(12, "")
        self.info_label.setStyleSheet("color: rgb(255, 255, 255); padding: 5px;")
        
        self.search_button.clicked.connect(self.searchEvent)
        self.save_button.clicked.connect(self.saveEvent)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(self.info_label)
        scroll.setWidgetResizable(True)

        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(header_label, 0, 0, 1, 2)
        main_layout.addWidget(self.search_button, 1, 0, 1, 1)
        main_layout.addWidget(self.save_button, 1, 1, 1, 1)
        main_layout.addWidget(search_label, 1, 2, 1, 1, alignment=Qt.AlignRight)
        main_layout.addWidget(self.ID_lineEdit, 1, 3, 1, 1, alignment=Qt.AlignLeft)
        main_layout.addWidget(scroll, 2, 0, 10, 4)
        main_layout.setVerticalSpacing(20)
        self.setLayout(main_layout)

    def searchEvent(self):
        self.info_label.setStyleSheet("color: rgb(255, 0, 0); padding: 5px;")
        if self.SocketClient == None:
            self.info_label.setText('No server set up !!')
        else:    
            if self.ID_lineEdit.text() != '':
                recv_data = self.server_processor.checkStuWithServer(self.ID_lineEdit.text())
                if recv_data == False:
                    self.info_label.setText('ID is not exist !!')
                else:
                    self.info_label.setStyleSheet(" color: rgb(255, 255, 255); padding: 5px;")
                    self.log_data = recv_data
                    info = ''
                    for data in recv_data:
                        info += "Time: {},  Name: {},  Card_No: {},  Status: {} \n".format(\
                                data['swipe_time'], data['student_name'],
                                data['card_no'], data['status'])
                    self.info_label.setText(info)
                    self.save_button.setDisabled(False)
            else:
                self.info_label.setText('ID is empty !!')
        self.ID_lineEdit.setText('')
        
    def saveEvent(self):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filter='csv(*.csv)')
        if file and self.log_data != []:
            with open(file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.log_data[0].keys())
                writer.writeheader()
                writer.writerows(self.log_data)
        
    def setNewSetting(self, new_setting: dict):
        self.my_setting = new_setting

    def load(self):
        self.info_label.setText('')
        self.ID_lineEdit.setText('')
        self.save_button.setDisabled(True)
        if self.my_setting != {}:
            if self.my_setting['Server'] != None:
                self.SocketClient = self.my_setting['Server']
                self.server_processor =  ServerProcessor(self.SocketClient)
        self.log_data = []
            

