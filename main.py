import site
site.USER_BASE=""
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QMessageBox
from funtions import (
    DeviceUI,
    LoginUI,
    CameraTestingThread,
    get_old_data,
)
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QAction


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("ui/main.ui", self)
        self.config, self.is_full = get_old_data()
        print(self.config)
        self.menu_frames = [
            self.frame_login,
            self.frame_device,
            self.frame_camtesting,
        ]
        self.menu_btns = [
            self.bn_login,
            self.bn_device_manager,
            self.bn_camtesting,
        ]
        self.show()
        self.init_ui()

    def init_ui(self):
        self.stackedWidget.setCurrentWidget(self.page_login)
        self.current_index = 0
        self.show_login()
        self.bn_device_manager.clicked.connect(self.show_device_manager)
        self.bn_login.clicked.connect(self.show_login)
        self.bn_camtesting.clicked.connect(self.show_cam_testing)
        self.device_manager = DeviceUI(self.page_device, self)
        self.login_manager = LoginUI(self.page_login, self)
        self.cam_testing = CameraTestingThread(self.page_cam_testing, self)
        self.toodle.clicked.connect(self.toodle_menu)
        self.frame_device.hide()
        self.frame_camtesting.hide()
        self.hide_text_button()
        self.showMaximized()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def hide_text_button(self):
        for btn in self.menu_btns:
            btn.setText("")

    def show_text_button(self):
        self.bn_login.setText("Đăng nhập")
        self.bn_device_manager.setText("Thiết lập thiết bị")
        self.bn_camsetting.setText("Thiết lập tọa độ")

    def reset_menu(self):
        default_style = """QPushButton {\n	border: none;\n	background-color: rgba(0,0,0,0);\n}\nQPushButton:hover {\n	background-color: rgb(91,90,90);\n}\nQPushButton:pressed {	\n	background-color: rgba(0,0,0,0);\n}"""
        for frame in self.menu_frames:
            frame.setEnabled(True)
            frame.setStyleSheet(default_style)

    def change_frame_style(self, qframe):
        qframe.setStyleSheet(
            """
                QFrame {
                    background-color: #66FF66;
                    color: #66FF66;
                  
                    border: none;
                }
                """
        )

    def show_device_manager(self):
        self.clear_page()
        self.current_index = 1
        self.reset_menu()
        self.change_frame_style(self.frame_device)
        self.frame_device.setEnabled(False)
        if "CAMERA" in self.config:
            self.device_manager.setup_camera_config(
                self.config["CAMERA"], self.is_admin
            )

        self.stackedWidget.setCurrentWidget(self.page_device)

    def show_login(self):
        self.clear_page()
        self.current_index = 0
        self.reset_menu()
        self.change_frame_style(self.frame_login)
        self.frame_login.setEnabled(False)
        self.stackedWidget.setCurrentWidget(self.page_login)


    def show_cam_testing(self):
        self.clear_page()
        self.current_index = 3
        self.reset_menu()
        self.change_frame_style(self.frame_camtesting)
        self.cam_testing.init()
        self.cam_testing.status = True
        self.cam_testing.start()
        self.frame_camtesting.setEnabled(False)
        self.stackedWidget.setCurrentWidget(self.page_cam_testing)

    def toodle_menu(self):
        max_width = 160
        min_width = 80
        if self.frame_bottom_west.width() == max_width:
            new_width = min_width
            self.hide_text_button()
            for bn in self.menu_btns:
                bn.setMinimumWidth(min_width)
        else:
            self.show_text_button()
            new_width = max_width
            for bn in self.menu_btns:
                bn.setMinimumWidth(max_width)
        self.animation = QPropertyAnimation(self.frame_bottom_west, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(self.frame_bottom_west.width())
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)

        # Set message box style based on the title
        if title == "Thất bại":
            msg.setStyleSheet(
                """
                    QMessageBox {
                        background-color: #FFCCCC;
                        color: #FF0000;
                        font-size: 12px;
                        font-family: Arial, sans-serif;
                    }
                    
                    QMessageBox QLabel {
                        color: #FF0000;
                    }
                    
                    QMessageBox QPushButton {
                        background-color: #FF6666;
                        color: #FFFFFF;
                        padding: 5px 10px;
                        border: none;
                    }
                    
                    QMessageBox QPushButton:hover {
                        background-color: #FF5555;
                    }
                """
            )
        elif title == "Thành công":
            msg.setStyleSheet(
                """
                    QMessageBox {
                        background-color: #CCFFCC;
                        color: #006600;
                        font-size: 12px;
                        font-family: Arial, sans-serif;
                    }
                    
                    QMessageBox QLabel {
                        color: #006600;
                    }
                    
                    QMessageBox QPushButton {
                        background-color: #66FF66;
                        color: #FFFFFF;
                        padding: 5px 10px;
                        border: none;
                    }
                    
                    QMessageBox QPushButton:hover {
                        background-color: #55FF55;
                    }
                """
            )

        msg.exec_()


    def pause_cam_testing(self):
        self.cam_testing.status = False
        self.cam_testing.wait()
        self.cam_testing.quit()

    def closeEvent(self, event):
        self.pause_cam_testing()
        event.accept()

    def clear_page(self):
        if self.current_index == 3:
            self.pause_cam_testing()
            self.cam_testing.cap.stop()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
