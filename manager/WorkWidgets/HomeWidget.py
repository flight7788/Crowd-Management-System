from turtle import color
from webbrowser import BackgroundBrowser
from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

class HomeWidget(QtWidgets.QWidget):
    def __init__(self,update_widget_callback):
        super().__init__()
        self.update_widget_callback = update_widget_callback
        layout = QtWidgets.QVBoxLayout()
        function_layout = QtWidgets.QHBoxLayout()
        
        header_label = LabelComponent(20,"Student Access Management System")
        person_botton = ButtonComponent(" Crew\n Management")
        tapcard_botton = ButtonComponent("Swipe Report")
        person_botton.clicked.connect(lambda: self.update_widget_callback("ManageStu"))
        tapcard_botton.clicked.connect(lambda: self.update_widget_callback("RecodeTap"))
        person_botton.setIcon(QtGui.QIcon('./icon/personnel_management.png'))
        person_botton.setIconSize(QtCore.QSize(50,50))
        tapcard_botton.setIcon(QtGui.QIcon('./icon/material.png'))
        tapcard_botton.setIconSize(QtCore.QSize(50,50))
        
        header_label.setAlignment(QtCore.Qt.AlignHCenter)
        header_label.setStyleSheet("""
            color: rgb(255, 255, 255);
            border: 3px solid rgb(255, 255, 255);
            border-radius: 5px;
            """)
        person_botton.setObjectName('person_botton')
        person_botton.setStyleSheet(
            """
            QPushButton#person_botton {
                color: #FFFFFF;
                border: 5px solid rgb(255, 255, 255);
                border-radius: 10px;
                padding: 40px;
                font: bold 32px;
            }
            QPushButton#person_botton:hover {
                background-color: rgb(200, 200, 200);
                color: black;
            }
            """
        )
        tapcard_botton.setObjectName('tapcard_botton')
        tapcard_botton.setStyleSheet(
            """
            QPushButton#tapcard_botton {
                color: #FFFFFF;
                border: 5px solid rgb(255, 255, 255);
                border-radius: 10px;
                padding: 50px;
                font: bold 36px;
            }
            QPushButton#tapcard_botton:hover {
                background-color: rgb(200, 200, 200);
                color: black;
            }
            """
        )
        function_layout.addWidget(person_botton,alignment=QtCore.Qt.AlignCenter)
        function_layout.addWidget(tapcard_botton,alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(header_label, stretch=1)
        layout.addStretch()
        layout.addLayout(function_layout,stretch=9)
        layout.addStretch()
        self.setLayout(layout)
    
    def load(self):
        pass