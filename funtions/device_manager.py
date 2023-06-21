from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from .tools import save_config, check_connect_camera, check_connect_plc
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtWidgets import QListView, QApplication


class DeviceUI(QtWidgets.QTabWidget):
    def __init__(self, parent, ui):
        super().__init__(parent)
        self.ui = ui
        self.hide()
        self.titles_table = ["Mã thiết bị", "Tên thiết bị", "Địa chỉ IP", "Trạng thái"]
        self.camera_status = False
        self.ui.bn_cam_connect.clicked.connect(self.connect_camera)
        self.ui.bt_save_config.clicked.connect(self.save_config)

    def init(self):
        self.ui.bt_type_cam.setEnabled(True)
        self.ui.bt_height_cam.setEnabled(True)
        self.ui.bt_width_cam.setEnabled(True)
        self.ui.bn_cam_connect.setEnabled(True)



    def set_index_port(self, index):
        column_index = 0
        index = self.model.index(index, column_index)
        self.ui.listport.setCurrentIndex(index)

    def setup_camera_config(self, config, is_admin):
        if "TYPE" in config:
            self.ui.bt_type_cam.setText(str(config["TYPE"]))
        if "HEIGHT" in config:
            self.ui.bt_height_cam.setText(str(config["HEIGHT"]))
        if "WIDTH" in config:
            self.ui.bt_width_cam.setText(str(config["WIDTH"]))
        if not is_admin:
            self.ui.bt_type_cam.setEnabled(False)
            self.ui.bt_height_cam.setEnabled(False)
            self.ui.bt_width_cam.setEnabled(False)

    def clear_infor_form(self):
        self.ui.device_id.setText("")
        self.ui.password.setText("")
        self.ui.device_ip.setText("")

    def connect_camera(self):
        type_cam = self.ui.bt_type_cam.text()
        height = self.ui.bt_height_cam.text()
        width = self.ui.bt_width_cam.text()
        if type_cam == "" or height == "" or width == "":
            self.ui.message("Thất bại", "Vui lòng nhập đầy đủ thông tin")
            return
        if height.isdigit() == False or width.isdigit() == False:
            self.ui.message("Thất bại", "Chiều cao và chiều rộng phải là số")
            return
        if type_cam not in ["RGB", "YUV_442"]:
            self.ui.message("Thất bại", "Loại camera không hợp lệ (RGB hoặc YUV_442)")
            return
        
        is_success = check_connect_camera()
        if is_success:
            self.ui.message("Thành công", "Kết nối camera thành công")
            self.ui.bn_cam_connect.setEnabled(False)
            self.ui.bt_type_cam.setEnabled(False)
            self.ui.bt_width_cam.setEnabled(False)
            self.ui.bt_height_cam.setEnabled(False)
            self.camera_status = True
        else:
            self.ui.message("Thất bại", "Kết nối camera thất bại")
            return
        if self.camera_status:
            self.ui.frame_camtesting.show()


    def save_config(self):

        # CAMERA
        type = self.ui.bt_type_cam.text()
        width = self.ui.bt_width_cam.text()
        height = self.ui.bt_height_cam.text()
        if "CAMERA" not in self.ui.config:
            self.ui.config["CAMERA"] = {}
        if type != "":
            self.ui.config["CAMERA"]["TYPE"] = str(type)
        else:
            if "TYPE" in self.ui.config["CAMERA"]:
                del self.ui.config["CAMERA"]["TYPE"]
        if width != "":
            self.ui.config["CAMERA"]["WIDTH"] = str(width)
        else:
            if "WIDTH" in self.ui.config["CAMERA"]:
                del self.ui.config["CAMERA"]["WIDTH"]
        if height != "":
            self.ui.config["CAMERA"]["HEIGHT"] = str(height)
        else:
            if "HEIGHT" in self.ui.config["CAMERA"]:
                del self.ui.config["CAMERA"]["HEIGHT"]

        save_config(self.ui.config)
        self.ui.message("Thành công", "Lưu cấu hình thành công")
