# -*- coding: utf-8 -*-
"""
@Auth ： 思绪无限
博客园、知乎：思绪无限
Bilibili：思绪亦无限
公众号：AI技术研究与分享
代码地址见以下博客中给出:
https://www.cnblogs.com/sixuwuxian/
https://www.zhihu.com/people/sixuwuxian

@IDE ：PyCharm
运行本项目需要python3.8及以下依赖库（完整库见requirements.txt）：
    opencv-python==4.5.5.64
    tensorflow==2.9.1
    PyQt5==5.15.6
    scikit-image==0.19.3
    torch==1.8.0
    keras==2.9.0
    Pillow==9.0.1
    scipy==1.8.0
点击运行主程序runMain.py，程序所在文件夹路径中请勿出现中文
"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget, QHBoxLayout, QFormLayout, \
    QPushButton, QLineEdit, QMessageBox

from UI_rec.HelmetRecing import Helmet_MainWindow


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.text = "水域垃圾检测系统"
        self.led_workerid = QLineEdit()
        self.led_pwd = QLineEdit()
        self.btn_login = QPushButton("登录")
        self.btn_reg = QPushButton("注册")
        self.initUI()
        self.btn_login.clicked.connect(self.do_login)
        self.btn_reg.clicked.connect(self.do_reg)
        self.pwd_name_ini = {"admin": "123456", "test": "123456"}
        self.bird_main = self.Helmet_Main()

    class Helmet_Main(Helmet_MainWindow):
        pass

    def do_reg(self):
        name_edit = self.led_workerid.text()
        pwd_edit = self.led_pwd.text()

        if name_edit != "" and pwd_edit != "":
            if name_edit not in self.pwd_name_ini.keys():
                self.pwd_name_ini.update({name_edit: pwd_edit})
                QMessageBox.about(self, "注册信息",
                                  "用户 " + name_edit + " 已注册成功！\n\n请重新进入登录界面")
            else:
                QMessageBox.about(self, "注册信息",
                                  "用户 " + name_edit + " 已经被注册过！\n\n请重新输入用户信息")
        else:
            QMessageBox.about(self, "注册信息",
                              "您的信息填写不全！\n请重新输入用户名和密码")

    def do_login(self):
        name_edit = self.led_workerid.text()
        pwd_edit = self.led_pwd.text()

        if name_edit != "" and pwd_edit != "":
            if name_edit in self.pwd_name_ini.keys():
                ini_pwd = self.pwd_name_ini[name_edit]
                if pwd_edit == ini_pwd:
                    QMessageBox.about(self, "登录信息",
                                      "用户 " + name_edit + " 已成功登录！\n\n点击确定启动界面程序")
                    # self.close()
                    # QtWidgets.QApplication.processEvents()
                    # os.system("python runMain.py")
                    self.hide()
                    # win = Bird_MainWindow()
                    self.bird_main.show()
                else:
                    QMessageBox.about(self, "登录信息",
                                      "用户 " + name_edit + " 密码不正确！\n\n请重新输入密码")
            else:
                QMessageBox.about(self, "登录信息",
                                  "用户 " + name_edit + " 未经过注册！\n\n请重新输入用户信息")
        else:
            QMessageBox.about(self, "登录信息",
                              "您的信息填写不全！\n请重新输入用户名和密码")

    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.setObjectName("loginWindow")
        self.setStyleSheet('#loginWindow{background-color:white}')
        self.setFixedSize(650, 400)
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon('icons/bird-logo.png'))

        # 添加顶部logo图片
        pixmap = QPixmap("icons/back2.jpeg")
        scaredPixmap = pixmap.scaled(650, 150)
        label = QLabel(self)
        label.setPixmap(scaredPixmap)

        # 绘制顶部文字
        lbl_logo = QLabel(self)
        lbl_logo.setText(self.text)
        lbl_logo.setStyleSheet("QWidget{color:#a1afc9;font-weight:600;background: transparent;font-size:30px;}")
        lbl_logo.setFont(QFont("Microsoft YaHei"))
        lbl_logo.move(140, 50)
        lbl_logo.setAlignment(Qt.AlignCenter)
        lbl_logo.raise_()

        # 登录表单内容部分
        login_widget = QWidget(self)
        login_widget.move(0, 140)
        login_widget.setGeometry(0, 140, 650, 260)

        hbox = QHBoxLayout()
        # 添加左侧logo
        logolb = QLabel(self)
        logopix = QPixmap("icons/helmet.png")
        logopix_scared = logopix.scaled(120, 130)
        logolb.setPixmap(logopix_scared)
        logolb.setAlignment(Qt.AlignCenter)
        hbox.addWidget(logolb, 1)
        # 添加右侧表单
        fmlayout = QFormLayout()
        lbl_workerid = QLabel("用户名")
        lbl_workerid.setFont(QFont("Microsoft YaHei"))
        self.led_workerid.setFixedWidth(270)
        self.led_workerid.setFixedHeight(38)
        self.led_workerid.setFont(QFont("Microsoft YaHei"))
        self.led_workerid.setPlaceholderText("用户名")

        lbl_pwd = QLabel("密码")
        lbl_pwd.setFont(QFont("Microsoft YaHei"))
        self.led_pwd.setEchoMode(QLineEdit.Password)
        self.led_pwd.setFixedWidth(270)
        self.led_pwd.setFixedHeight(38)
        self.led_pwd.setFont(QFont("Microsoft YaHei"))
        self.led_pwd.setPlaceholderText("密码")

        self.btn_reg.setFixedWidth(130)
        self.btn_reg.setFixedHeight(40)
        self.btn_reg.setFont(QFont("Microsoft YaHei"))
        self.btn_reg.setObjectName("reg_btn")
        # btn_reg.setStyleSheet("#reg_btn{background-color:#2c7adf;color:#fff;border:5px;border-radius:4px;}")

        self.btn_login.setFixedWidth(130)
        self.btn_login.setFixedHeight(40)
        self.btn_login.setFont(QFont("Microsoft YaHei"))
        self.btn_login.setObjectName("login_btn")

        fmlayout.addRow(lbl_workerid, self.led_workerid)
        fmlayout.addRow(lbl_pwd, self.led_pwd)
        # fmlayout.addWidget(btn_login)

        flyout2 = QHBoxLayout()
        flyout2.addWidget(self.btn_reg)
        flyout2.addWidget(self.btn_login)

        fmlayout.addItem(flyout2)
        # flyout2.setHorizontalSpacing(20)
        flyout2.setSpacing(12)
        hbox.setAlignment(Qt.AlignCenter)
        # 调整间距
        fmlayout.setHorizontalSpacing(20)
        fmlayout.setVerticalSpacing(12)

        hbox.addLayout(fmlayout, 2)
        login_widget.setLayout(hbox)
        login_widget.setStyleSheet("QPushButton{background-color:#2c7adf;color:#fff;border:None;border-radius:4px;}\n"
                                   "\nQPushButton:hover{\n    border: 1px solid #3C80B1;\n    background-color: "
                                   "qconicalgradient(cx:0.5, cy:0.5, angle:180, stop:0.49999 rgba(181, 225, 250, "
                                   "255), stop:0.50001 rgba(222, 242, 251, 255));\n    "
                                   "border-radius:5px;\n}\nQPushButton:pressed{\n    border: 1px solid #5F92B2;\n    "
                                   "background-color: qconicalgradient(cx:0.5, cy:0.5, angle:180, stop:0.49999 rgba("
                                   "134, 198, 233, 255), stop:0.50001 rgba(206, 234, 248, 255));\n    "
                                   "border-radius:5px;\n}\n")

        self.center()
        # self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LoginForm()
    ex.show()

    sys.exit(app.exec_())
