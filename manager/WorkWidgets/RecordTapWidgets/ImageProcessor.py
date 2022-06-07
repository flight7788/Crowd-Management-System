import os
import cv2
import numpy as np
from datetime import datetime

class ImageProcessor:
    def __init__(self,img_binary):
        self.img_binary = img_binary
        
    def decodeImg(self):
        time_stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        filename = './{}.png'.format(time_stamp)
        img = np.asarray(self.img_binary, dtype = 'uint8')
        img_decode  = cv2.imdecode(img, cv2.IMREAD_COLOR)
        cv2.imwrite(filename , img_decode)
        return filename
        