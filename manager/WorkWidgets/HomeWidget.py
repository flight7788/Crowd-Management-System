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
        
        header_label = LabelComponent(24,"人員進出紀錄管理系統")
        person_botton = ButtonComponent("人員管理")
        tapcard_botton = ButtonComponent("刷卡報表")
        person_botton.clicked.connect(lambda: self.update_widget_callback("ManageStu"))
        tapcard_botton.clicked.connect(lambda: self.update_widget_callback("RecodeTap"))
        
        header_label.setAlignment(QtCore.Qt.AlignHCenter)
        header_label.setStyleSheet("""
            color: rgb(255, 255, 255);
            border: 1px solid rgb(255, 255, 255)
            """)
        person_botton.setObjectName('person_botton')
        person_botton.setStyleSheet(
            """
            QPushButton#person_botton {
                background-color: #2B5DD1;
                color: #FFFFFF;
                border-style: outset;
                padding: 100px;
                font: bold 40px;
                border-width: 6px;
                border-radius: 10px;
                border-color: #2752B8;
            }
            QPushButton#person_botton:hover {
                background-color: lightgreen;
            }
            QPushButton#person_botton:pressed {
                background-color: lightgreen;
            }
            """
        )
        tapcard_botton.setObjectName('tapcard_botton')
        tapcard_botton.setStyleSheet(
            """
            QPushButton#tapcard_botton {
                background-color: #2B5DD1;
                color: #FFFFFF;
                border-style: outset;
                padding: 100px;
                font: bold 40px;
                border-width: 6px;
                border-radius: 10px;
                border-color: #2752B8;
            }
            QPushButton#tapcard_botton:hover {
                background-color: lightgreen;
            }
            QPushButton#tapcard_botton:pressed {
                background-color: lightgreen;
            }
            """
        )
        function_layout.addWidget(person_botton,alignment=QtCore.Qt.AlignCenter)
        function_layout.addWidget(tapcard_botton,alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(header_label, stretch=1)
        layout.addLayout(function_layout,stretch=9)
        self.setLayout(layout)
    
    def load(self):
        pass