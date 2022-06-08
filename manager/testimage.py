from PyQt5 import QtWidgets,QtWidgets
from PyQt5.QtGui import QPixmap
import sys

class ImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Picture")
        layout = QtWidgets.QVBoxLayout()
        test_label = QtWidgets.QLabel()
        test_label.setText("test")
        image_label = QtWidgets.QLabel()
        pixmap = QPixmap("./20220608032246.png") 
        image_label.setPixmap(pixmap)
        layout.addWidget(test_label)
        layout.addWidget(image_label)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ImageWidget()
    ex.show()
    sys.exit(app.exec_())
        