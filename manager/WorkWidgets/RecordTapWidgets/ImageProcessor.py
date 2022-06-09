import cv2
import numpy as np
from datetime import datetime
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

class ImageProcessor(QtCore.QThread):
    return_sig = pyqtSignal(str)
    
    def __init__(self,img_binary):
        super().__init__()
        self.img_binary = img_binary
        
    def decodeImg(self):
        time_stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        filename = './{}.png'.format(time_stamp)
        img = np.asarray(self.img_binary, dtype = 'uint8')
        img_decode  = cv2.imdecode(img, cv2.IMREAD_COLOR)
        cv2.imwrite(filename , img_decode)
        return filename
    
    def run(self):
        result = self.decodeImg()
        self.return_sig.emit(result)
        