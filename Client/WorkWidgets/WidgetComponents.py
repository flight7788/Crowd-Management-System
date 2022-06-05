from PyQt5 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setFont(QtGui.QFont("微軟正黑體", font_size, QtGui.QFont.Bold))
        self.setText(content)
        self.setStyleSheet("padding: 1px;\
                            color: rgb(255, 255, 255)")

class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setStyleSheet("border: 1px solid rgb(255, 255, 255); \
                            border-width: 1px;\
                            border-color: rgb(255, 255, 255);\
                            color: rgb(255, 255, 255)")

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setStyleSheet("color: rgb(255, 255, 255)")
        self.setStyleSheet(\
            "QPushButton{\
                border: 1px solid rgb(255, 255, 255); \
                background-color: rgb(61, 80, 95);\
                border-width: 2px;\
                border-radius:5px;\
                border-color: beige;\
                padding: 3px;\
                color: rgb(255, 255, 255);}" 
		    "QPushButton:hover{ background-color:white; color: black;}"  
		    "QPushButton:pressed{ background-color:rgb(85, 170, 255); border-style: inset; }"
            "QPushButton:disabled{ background-color:rgb(37, 48, 57); \
                                   border-color: rgb(153, 153, 153);\
                                   color: rgb(153, 153, 153);}"
        )

