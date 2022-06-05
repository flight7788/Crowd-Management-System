import cv2
import numpy as np
from datetime import datetime

class ImageProcessor:

    def encodeImg(self, img_file):
        img_arr = cv2.imread(img_file)
        img_encode = cv2.imencode('.png', img_arr)[1]
        data_encode = np.array(img_encode)
        data_encode = data_encode.tolist()
        return data_encode
    
    
    def decodeImg(self , img_binary):
        time_stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        filename = './Swipe_Images/{}.png'.format(time_stamp)
        img = np.asarray(img_binary, dtype = 'uint8')
        img_decode  = cv2.imdecode(img, cv2.IMREAD_COLOR)
        cv2.imwrite(filename , img_decode)
        
        return filename
        