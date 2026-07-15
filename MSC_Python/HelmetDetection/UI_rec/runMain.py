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

from sys import argv, exit
from PyQt5.QtWidgets import QApplication
from HelmetRecing import Helmet_MainWindow

if __name__ == '__main__':
    # 忽略警告
    # os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    # warnings.filterwarnings(action='ignore')

    app = QApplication(argv)

    win = Helmet_MainWindow()
    win.showTime()
    exit(app.exec_())
