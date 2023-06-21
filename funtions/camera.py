from pyflycap2.interface import CameraContext
from pyflycap2.interface import Camera as Cam
import cv2
import numpy as np


class Camera:
    def __init__(self,width=2448,height=2048,type="RGB"):
        self.width = width
        self.height = height
        self.type = type
        self.cap = None
        self.try_cout = 0
        self.try_max = 3

    def check_connect(self,):
        cc = CameraContext()
        cc.rescan_bus()
        self.cam_serials=cc.get_gige_cams()
        if len(self.cam_serials) == 0:
            return False
        return True  
    def connect_camera(self):
        self.cap = Cam(serial=self.cam_serials[0])
        self.cap.connect()
        self.cap.start_capture()
    
    def read(self):
        try:
            if self.try_cout >= self.try_max:
                self.ui.message("Thất bại", "Kết nối camera thất bại")
                return None
            self.cap.read_next_image()
            image = self.cap.get_current_image()
            rows = image['rows']
            cols = image['cols']
            stride = image['stride']
            data_size = image['data_size']
            pix_fmt = image['pix_fmt']
            buffer = image['buffer']        
            image_data = np.frombuffer(buffer, dtype=np.uint8, count=data_size)
            if self.type == "RGB":
                image = image_data.reshape(rows, cols,3)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            elif self.type=="YUV_442":
                image = image_data.reshape(rows, cols,2)
                image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_YUYV)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.resize(image,(self.width,self.height))
            self.try_cout = 0
            return image
        except:
            self.try_cout += 1
            return self.read()
        
    def stop(self):
        if(self.cap is not None):
            self.cap.disconnect()
