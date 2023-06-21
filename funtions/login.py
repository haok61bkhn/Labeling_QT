from PyQt5 import QtWidgets
from .tools import login
from .device_manager import DeviceUI


class LoginUI(QtWidgets.QTabWidget):
    def __init__(self, parent, ui):
        super().__init__(parent)
        self.is_login = False
        self.parent = parent
        self.ui = ui
        self.ui.bt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.hide()
        self.ui.bt_login.clicked.connect(self.login)
        self.ui.bt_logout.clicked.connect(self.logout)
        self.ui.wg_logout.hide()

    def clear(self):
        if self.is_login:
            self.ui.bt_username.setText("")
            self.ui.bt_password.setText("")

    def login_success(self):
        self.ui.wg_logout.show()
        self.ui.bt_username.setEnabled(False)
        self.ui.bt_password.setEnabled(False)
        self.ui.wg_login.hide()
        self.ui.frame_device.show()
        self.ui.device_manager.init()

    def login(self):
        username = self.ui.bt_username.text()
        password = self.ui.bt_password.text()
        if username == "" or password == "":
            self.ui.message("Thất bại", "Vui lòng nhập đầy đủ thông tin")
            return
        success, is_admin = login(username, password)
        if not success:
            self.ui.message("Thất bại", "Sai tên đăng nhập hoặc mật khẩu")
            return

        if is_admin:
            self.ui.message("Thành công", "Đăng nhập thành công admin")
            self.ui.lab_user.setText("IMS Admin")
            self.ui.is_admin = True
            self.login_success()
        else:
            if not self.ui.is_full:
                self.ui.message(
                    "Thất bại",
                    "Thông tin chưa đầy đủ vui lòng đăng nhập admin để thiết lập",
                )
                return
            else:
                self.ui.message("Thành công", "Đăng nhập thành công")
                self.login_success()
                self.ui.lab_user.setText("IMS User")
                self.ui.is_admin = False

    def logout(self):
        self.ui.wg_logout.hide()
        self.ui.wg_login.show()
        self.ui.frame_device.hide()
        self.ui.frame_camsetting.hide()
        self.ui.frame_camtesting.hide()
        self.ui.message("Thành công", "Đăng xuất thành công")
        self.ui.bt_username.setEnabled(True)
        self.ui.bt_password.setEnabled(True)
        try:
            self.ui.plc.logout()
        except Exception as e:
            print(e)
