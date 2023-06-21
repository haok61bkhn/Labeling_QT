from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
import cv2
from PyQt5.QtGui import QImage, QPixmap
import time
from .tools import save_config
import numpy as np
import random
from .camera import Camera
STEP = 100
OBJ_WIDTH = 20
OBJ_HEIGHT = 50
import os

class CameraTestingThread(QThread):
    def __init__(self, parent, ui):
        QThread.__init__(self, parent)
        self.ui = ui
        parent.hide()
        self.status = False
        self.roi_maps = {
            self.ui.sl_left: self.ui.bt_left,
            self.ui.sl_top: self.ui.bt_top,
            self.ui.sl_width: self.ui.bt_width,
            self.ui.sl_height: self.ui.bt_height,
        }
        self.reverse_roi_maps = {y: x for x, y in self.roi_maps.items()}
        for sl in self.roi_maps:
            sl.valueChanged.connect(self.sl_changed)
        for bn in self.roi_maps.values():
            bn.editingFinished.connect(self.bn_changed)
        self.bn_label_list = [self.ui.bn_label1, self.ui.bn_label2, self.ui.bn_label3]
        
        self.data_dir ="DATASET"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.ui.bn_save_roi.clicked.connect(self.save_config)
        
        
    def save_image(self):
        self.capture = True
        text = self.sender().text()
        image_file = os.path.join(self.data_dir, text, text+"_"+str(time.time()) + ".jpg")
        time.sleep(0.1)
        image = self.image.copy()
        x1=int(float(self.x))
        y1=int(float(self.y))
        x2= x1+int(float(self.w))
        y2= y1+int(float(self.h))
        image = image[y1:y2, x1:x2]
        cv2.imwrite(image_file,image)
        self.image = None

    


    def set_value_bn(self, bn, value):
        bn.setText(str(float(value)))

    def set_value_sl(self, sl, value):
        sl.setValue(int(float(value)) * STEP)

    def check_pos(self):
        x = self.ui.bt_left.text()
        y = self.ui.bt_top.text()
        w = self.ui.bt_width.text()
        h = self.ui.bt_height.text()
        if x != "" and w != "":
            if float(x) + float(w) > self.cam_width:
                self.set_value_sl(self.ui.sl_width, self.cam_width - float(x))
                self.set_value_bn(self.ui.bt_width, self.cam_width - float(x))
        if y != "" and h != "":
            if float(y) + float(h) > self.cam_height:
                self.set_value_sl(self.ui.sl_height, self.cam_height - float(y))
                self.set_value_bn(self.ui.bt_height, self.cam_height - float(y))


    def bn_changed(self):
        bn = self.sender()
        sl = self.reverse_roi_maps[bn]
        self.set_value_sl(sl, bn.text())
        self.check_pos()

    def sl_changed(self):
        sl = self.sender()
        bn = self.roi_maps[sl]
        self.set_value_bn(bn, sl.value() / STEP)
        self.check_pos()


    def enable_all(self):
        for sl in self.roi_maps:
            sl.setEnabled(True)
        for bn in self.reverse_roi_maps:
            bn.setEnabled(True)
        self.ui.bn_save_roi.setEnabled(True)

    def disable_all(self):
        for sl in self.roi_maps:
            sl.setEnabled(False)
        for bn in self.reverse_roi_maps:
            bn.setEnabled(False)
        self.ui.bn_save_roi.setEnabled(False)


    def disable_roi(self):
        for sl in self.roi_maps:
            sl.setEnabled(False)
        for bn in self.reverse_roi_maps:
            bn.setEnabled(False)




    def init(self):
        self.cap = Camera()
        self.capture = False
        check_connect = self.cap.check_connect()
        if check_connect == False:
            self.ui.message("Lỗi", "Không tìm thấy camera")
        else:
            self.cap.connect_camera()
        self.testing = False
        self.cam_width = int(self.ui.config["CAMERA"]["WIDTH"])
        self.cam_height = int(self.ui.config["CAMERA"]["HEIGHT"])
        self.ui.sl_left.setRange(0, STEP * self.cam_width)
        self.ui.sl_left.setSliderDown(True)
        self.ui.sl_left.setTracking(True)
        self.ui.sl_top.setRange(0, STEP * self.cam_height)
        self.ui.sl_top.setSliderDown(True)
        self.ui.sl_top.setTracking(True)
        self.ui.sl_width.setRange(0, STEP * self.cam_width)
        self.ui.sl_width.setSliderDown(True)
        self.ui.sl_width.setTracking(True)
        self.ui.sl_height.setRange(0, STEP * self.cam_height)
        self.ui.sl_height.setSliderDown(True)
        self.ui.sl_height.setTracking(True)
        for lb in self.bn_label_list:
            lb.hide()
            lb.clicked.connect(self.save_image)
        
        if "ROI" in self.ui.config:
            if "x" in self.ui.config["ROI"]:
                self.ui.sl_left.setValue(int(float(self.ui.config["ROI"]["x"]) * STEP))
            if "y" in self.ui.config["ROI"]:
                self.ui.sl_top.setValue(int(float(self.ui.config["ROI"]["y"]) * STEP))
            if "width" in self.ui.config["ROI"]:
                self.ui.sl_width.setValue(
                    int(float(self.ui.config["ROI"]["width"]) * STEP)
                )
            if "height" in self.ui.config["ROI"]:
                self.ui.sl_height.setValue(
                    int(float(self.ui.config["ROI"]["height"]) * STEP)
                )
        if "LABELS" in self.ui.config:
            if "label1" in self.ui.config["LABELS"]:
                if self.ui.config["LABELS"]["label1"] != "":
                    self.ui.bt_label1.setText(self.ui.config["LABELS"]["label1"])
                else:
                    del self.ui.config["LABELS"]["label1"]
            if "label2" in self.ui.config["LABELS"]:
                if self.ui.config["LABELS"]["label2"] != "":
                    self.ui.bt_label2.setText(self.ui.config["LABELS"]["label2"])
                else:
                    del self.ui.config["LABELS"]["label2"]
            if "label3" in self.ui.config["LABELS"]:
                if self.ui.config["LABELS"]["label3"] != "":
                    self.ui.bt_label3.setText(self.ui.config["LABELS"]["label3"])
                else:
                    del self.ui.config["LABELS"]["label3"]
                    
            


    def get_point(self, bt_x, bt_y):
        x = bt_x.text()
        y = bt_y.text()
        if x == "" or y == "":
            return None, None
        return int(float(x)), int(float(y))

    def draw_object(self, center_x, center_y, width, height, angle, frame):
        box = cv2.boxPoints(((center_x, center_y), (width, height), angle))
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

    def run(self):
        while self.status:
            frame = self.cap.read()
            
            if frame is None:
                self.status = False
                continue
            if self.capture == True:
                self.image = frame.copy()
                self.capture = False
            p_x, p_y = self.get_point(self.ui.bt_left, self.ui.bt_top)
            p_w, p_h = self.get_point(self.ui.bt_width, self.ui.bt_height)
            if (
                p_x is not None
                and p_y is not None
                and p_w is not None
                and p_h is not None
            ):
                cv2.rectangle(frame, (p_x, p_y), (p_x + p_w, p_y + p_h), (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.strides[0],
                QImage.Format_RGB888,
            )
            self.ui.lb_cam_testing.setPixmap(QPixmap.fromImage(frame))

    def save_config(self):
        x = self.ui.bt_left.text()
        y = self.ui.bt_top.text()
        w = self.ui.bt_width.text()
        h = self.ui.bt_height.text()
        label1 = self.ui.bt_label1.text()
        label2 = self.ui.bt_label2.text()
        label3 = self.ui.bt_label3.text()
        if x != "" and y != "" and w != "" and h != "" and (label1 != "" or label2 != "" or label3 != ""):
            if "ROI" not in self.ui.config:
                self.ui.config["ROI"] = {}
            self.ui.config["ROI"]["x"] = x
            self.ui.config["ROI"]["y"] = y
            self.ui.config["ROI"]["width"] = w
            self.ui.config["ROI"]["height"] = h
            if "LABELS" not in self.ui.config:
                self.ui.config["LABELS"] = {}
            if label1 != "":
                self.ui.config["LABELS"]["label1"] = label1
                self.ui.bn_label1.show()
                self.ui.bn_label1.setText(label1)
                if os.path.exists(os.path.join(self.data_dir, label1)) == False:
                    os.makedirs(os.path.join(self.data_dir, label1))
            else:
                    del self.ui.config["LABELS"]["label1"]
            if label2 != "":
                self.ui.config["LABELS"]["label2"] = label2
                self.ui.bn_label2.show()
                self.ui.bn_label2.setText(label2)
                if os.path.exists(os.path.join(self.data_dir, label2)) == False:
                    os.makedirs(os.path.join(self.data_dir, label2))
            else:
                    del self.ui.config["LABELS"]["label2"]
            if label3 != "":
                self.ui.config["LABELS"]["label3"] = label3
                self.ui.bn_label3.show()
                self.ui.bn_label3.setText(label3)
                if os.path.exists(os.path.join(self.data_dir, label3)) == False:
                    os.makedirs(os.path.join(self.data_dir, label3))
            else:
                    del self.ui.config["LABELS"]["label3"]
            save_config(self.ui.config)
            self.ui.message("Thành công", "Lưu cấu hình thành công")
            self.disable_roi()
            self.ui.bn_save_roi.setEnabled(False)
            self.x=x
            self.y=y
            self.w=w
            self.h=h
        else:
            self.ui.message("Thất bại", "Vui lòng nhập đầy đủ thông tin")



