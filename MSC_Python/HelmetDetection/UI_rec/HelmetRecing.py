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
import argparse
import os
import random
import time
from os import getcwd

import cv2
import numpy as np
import torch
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Helmet.label_name import Chinese_name
from models.experimental import attempt_load
from tools.BeautyUI import QBeautyUI
from utils.datasets import letterbox
from utils.general import (
    check_img_size, non_max_suppression, scale_coords)
from utils.torch_utils import select_device, time_synchronized


# 忽略警告
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# warnings.filterwarnings(action='ignore')


class Helmet_MainWindow(QBeautyUI):
    def __init__(self, *args, obj=None, **kwargs):
        super(Helmet_MainWindow, self).__init__(*args, **kwargs)
        self.author_flag = False  # 是否输出信息
        self.pass_flag = True  # 是否需要跳过登录界面

        self.setupUi(self)  # 界面生成
        self.retranslateUi(self)  # 界面控件
        self.setUiStyle(window_flag=True, transBack_flag=True)  # 设置界面样式

        self.path = getcwd()
        self.video_path = getcwd()

        self.timer_camera = QtCore.QTimer()  # 定时器
        self.timer_video = QtCore.QTimer()  # 视频定时器
        self.flag_timer = ""  # 用于标记正在进行的功能项（视频/摄像）

        self.LoadModel()  # 加载预训练模型
        self.slot_init()  # 定义槽函数
        self.files = []  #
        self.cap_video = None  # 视频流对象
        self.CAM_NUM = 0  # 摄像头标号
        self.cap = cv2.VideoCapture(self.CAM_NUM)  # 屏幕画面对象

        self.detInfo = []
        self.current_image = []
        self.detected_image = None
        # self.dataset = None
        self.count = 0  # 表格行数，用于记录识别识别条目
        self.res_set = []  # 用于历史结果记录的列表
        self.c_video = 0

    def slot_init(self):
        self.toolButton_file.clicked.connect(self.choose_file)
        self.toolButton_folder.clicked.connect(self.choose_folder)
        self.toolButton_video.clicked.connect(self.button_open_video_click)
        self.timer_video.timeout.connect(self.show_video)
        self.toolButton_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.toolButton_model.clicked.connect(self.choose_model)
        self.comboBox_select.currentIndexChanged.connect(self.select_obj)
        self.tableWidget.cellPressed.connect(self.table_review)
        self.toolButton_saveing.clicked.connect(self.save_file)
        self.toolButton_settings.clicked.connect(self.setting)
        self.toolButton_author.clicked.connect(self.disp_website)
        self.toolButton_version.clicked.connect(self.disp_version)

    def table_review(self, row, col):
        try:
            if col == 0:  # 点击第一列时
                this_path = self.tableWidget.item(row, 1)  # 表格中的文件路径
                res = self.tableWidget.item(row, 2)  # 表格中记录的识别结果
                axes = self.tableWidget.item(row, 3)  # 表格中记录的坐标

                if (this_path is not None) & (res is not None) & (axes is not None):
                    this_path = this_path.text()
                    if os.path.exists(this_path):
                        res = res.text()
                        axes = axes.text()

                        image = self.cv_imread(this_path)  # 读取选择的图片
                        image = cv2.resize(image, (850, 500))

                        axes = [int(i) for i in axes.split(",")]
                        confi = float(self.tableWidget.item(row, 4).text())

                        # print(axes)
                        # image = self.drawRectBox(image, axes, res)
                        image = self.drawRectEdge(image, axes, alpha=0.2, addText=res)
                        # 在Qt界面中显示检测完成画面
                        self.display_image(image)  # 在界面中显示画面

                        # 在界面标签中显示结果
                        self.label_xmin_result.setText(str(int(axes[0])))
                        self.label_ymin_result.setText(str(int(axes[1])))
                        self.label_xmax_result.setText(str(int(axes[2])))
                        self.label_ymax_result.setText(str(int(axes[3])))
                        # self.label_score_result.setText(str(round(confi * 100, 2)) + "%")
                        # self.label_plate_result.setText(str(res))
                        QtWidgets.QApplication.processEvents()
        except:
            self.label_display.setText('重现车牌记录时出错，请检查表格内容！')
            self.label_display.setStyleSheet("border-image: url(:/newPrefix/images_test/ini-image.png);")

    def LoadModel(self, model_path=None):
        """
        读取预训练模型
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--weights', nargs='+', type=str, default='../weights/helmet-best.pt',
                            help='model.pt path(s)')  # 模型路径仅支持.pt文件
        parser.add_argument('--img-size', type=int, default=480, help='inference size (pixels)')  # 检测图像大小，仅支持480
        parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')  # 置信度阈值
        parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')  # NMS阈值
        # 选中运行机器的GPU或者cpu，有GPU则GPU，没有则cpu，若想仅使用cpu，可以填cpu即可
        parser.add_argument('--device', default='',
                            help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser.add_argument('--save-dir', type=str, default='inference', help='directory to save results')  # 文件保存路径
        parser.add_argument('--classes', nargs='+', type=int,
                            help='filter by class: --class 0, or --class 0 2 3')  # 分开类别
        parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')  # 使用NMS
        self.opt = parser.parse_args()  # opt局部变量，重要
        out, weight, imgsz = self.opt.save_dir, self.opt.weights, self.opt.img_size  # 得到文件保存路径，文件权重路径，图像尺寸
        self.device = select_device(self.opt.device)  # 检验计算单元,gpu还是cpu
        self.half = self.device.type != 'cpu'  # 如果使用gpu则进行半精度推理
        if model_path:
            weight = model_path
        self.model = attempt_load(weight, map_location=self.device)  # 读取模型
        self.imgsz = check_img_size(imgsz, s=self.model.stride.max())  # 检查图像尺寸
        if self.half:  # 如果是半精度推理
            self.model.half()  # 转换模型的格式
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names  # 得到模型训练的类别名
        # self.names = [Chinese_name[i] for i in self.names]
        for i, v in enumerate(self.names):
            if v in Chinese_name.keys():
                self.names[i] = Chinese_name[v]
        # hex = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
        #        '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        color = [[132, 56, 255], [82, 0, 133], [203, 56, 255], [255, 149, 200], [255, 55, 199],
                 [72, 249, 10], [146, 204, 23], [61, 219, 134], [26, 147, 52], [0, 212, 187],
                 [255, 56, 56], [255, 157, 151], [255, 112, 31], [255, 178, 29], [207, 210, 49],
                 [44, 153, 168], [0, 194, 255], [52, 69, 147], [100, 115, 255], [0, 24, 236]]
        self.colors = color if len(self.names) <= len(color) else [[random.randint(0, 255) for _ in range(3)] for _ in
                                                                   range(len(self.names))]  # 给每个类别一个颜色
        img = torch.zeros((1, 3, self.imgsz, self.imgsz), device=self.device)  # 创建一个图像进行预推理
        _ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # 预推理

    def choose_model(self):
        self.timer_camera.stop()
        self.timer_video.stop()
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.cap_video:
            self.cap_video.release()  # 释放视频画面帧

        self.comboBox_select.clear()  # 下拉选框的显示
        self.comboBox_select.addItem('所有目标')  # 清除下拉选框
        self.clearUI()  # 清除UI上的label显示
        self.flag_timer = ""
        # 调用文件选择对话框
        fileName_choose, filetype = QFileDialog.getOpenFileName(self.centralwidget,
                                                                "选取图片文件", getcwd(),  # 起始路径
                                                                "Model File (*.pt)")  # 文件类型
        # 显示提示信息
        if fileName_choose != '':
            self.toolButton_model.setToolTip(fileName_choose + ' 已选中')
        else:
            fileName_choose = None  # 模型默认路径
            self.toolButton_model.setToolTip('使用默认模型')
        self.LoadModel(fileName_choose)

    def select_obj(self):
        QtWidgets.QApplication.processEvents()
        if self.flag_timer == "video":
            # 打开定时器
            self.timer_video.start(30)
        elif self.flag_timer == "camera":
            self.timer_camera.start(30)

        ind = self.comboBox_select.currentIndex() - 1
        ind_select = ind
        if ind <= -1:
            ind_select = 0
        # else:
        #     ind_select = len(self.detInfo) - ind - 1
        if len(self.detInfo) > 0:
            if len(self.detInfo[ind_select][0]) > 7:
                font = QtGui.QFont()
                font.setPointSize(14)
            else:
                font = QtGui.QFont()
                font.setPointSize(16)
            # self.label_class_result.setFont(font)
            # self.label_class_result.setText(self.detInfo[ind_select][0])  # 显示类别
            # self.label_score_result.setText(str(self.detInfo[ind_select][2]))  # 显示置信度值
            # 显示位置坐标
            self.label_xmin_result.setText(str(int(self.detInfo[ind_select][1][0])))
            self.label_ymin_result.setText(str(int(self.detInfo[ind_select][1][1])))
            self.label_xmax_result.setText(str(int(self.detInfo[ind_select][1][2])))
            self.label_ymax_result.setText(str(int(self.detInfo[ind_select][1][3])))

        image = self.current_image.copy()
        count = 0
        if len(self.detInfo) > 0:
            for i, box in enumerate(self.detInfo):  # 遍历所有标记框
                if box[3] == 1:
                    count += 1
                if ind != -1:
                    if ind != i:
                        continue
                # 在图像上标记目标框

                label = '%s %.0f%%' % (box[0], float(box[2]) * 100)
                # label = str(box[0]) + " " + str(float(box[2])*100)
                # 画出检测到的目标物
                # self.names. box[0]
                image = self.drawRectBox(image, box[1], addText=label, color=self.colors[0])

            self.label_class_result.setText(str(count))
            self.label_score_result.setText(str(len(self.detInfo) - count))
            # 在Qt界面中显示检测完成画面
            self.display_image(image)
            # self.label_display.display_image(image)

    def choose_folder(self):
        self.timer_camera.stop()
        self.timer_video.stop()
        self.c_video = 0
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.cap_video:
            self.cap_video.release()  # 释放视频画面帧

        self.comboBox_select.clear()  # 下拉选框的显示
        self.comboBox_select.addItem('所有目标')  # 清除下拉选框
        self.clearUI()  # 清除UI上的label显示

        self.flag_timer = ""
        # 选择文件夹
        dir_choose = QFileDialog.getExistingDirectory(self.centralwidget, "选取文件夹", self.path)
        self.path = dir_choose  # 保存路径
        if dir_choose != "":
            self.textEdit_pic.setText(dir_choose + '文件夹已选中')
            self.label_display.setText('正在启动识别系统...\n\nleading')
            QtWidgets.QApplication.processEvents()

            rootdir = os.path.join(self.path)
            for (dirpath, dirnames, filenames) in os.walk(rootdir):
                for filename in filenames:
                    temp_type = os.path.splitext(filename)[1]
                    if temp_type == '.png' or temp_type == '.jpg' or temp_type == '.jpeg':
                        img_path = dirpath + '/' + filename
                        image = self.cv_imread(img_path)  # 读取选择的图片
                        image = cv2.resize(image, (850, 500))
                        img0 = image.copy()
                        img = letterbox(img0, new_shape=self.imgsz)[0]
                        img = np.stack(img, 0)
                        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
                        img = np.ascontiguousarray(img)

                        img = torch.from_numpy(img).to(self.device)  # 把图像矩阵移至到训练单元中(GPU中或CPU中)
                        img = img.half() if self.half else img.float()  # 如果是半精度则转换图像格式
                        img /= 255.0  # 归一化
                        if img.ndimension() == 3:  # 如果图像时三维的添加1维变成4维
                            img = img.unsqueeze(0)
                        t1 = time_synchronized()  # 推理开始时间
                        pred = self.model(img, augment=False)[0]  # 前向推理
                        pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres,
                                                   classes=self.opt.classes,
                                                   agnostic=self.opt.agnostic_nms)  # NMS过滤
                        t2 = time_synchronized()  # 结束时间
                        det = pred[0]

                        p, s, im0 = None, '', img0
                        self.current_image = img0.copy()
                        # save_path = str(Path(self.opt.save_dir) / Path(p).name)  # 文件保存路径
                        if det is not None and len(det):  # 如果有检测信息则进入
                            self.label_numer_result.setText(str(len(det)))  # 将检测个数放置到主界面中
                            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()  # 把图像缩放至im0的尺寸
                            number_i = 0  # 类别预编号
                            self.detInfo = []

                            count = 0
                            for *xyxy, conf, cls in reversed(det):  # 遍历检测信息
                                c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                                # 将检测信息添加到字典中
                                self.detInfo.append(
                                    [self.names[int(cls)], [c1[0], c1[1], c2[0], c2[1]], '%.2f' % conf, int(cls)])
                                number_i += 1  # 编号数+1

                                # self.label_class_result.setText(str(self.names[int(cls)]))
                                if int(cls) == 1:
                                    count += 1
                                # self.label_score_result.setText('%.2f' % conf)
                                label = '%s %.0f%%' % (self.names[int(cls)], conf * 100)

                                # 画出检测到的目标物
                                # print(xyxy)
                                im0 = self.drawRectBox(im0, xyxy, alpha=0.2, addText=label, color=self.colors[int(cls)])
                                self.label_xmin_result.setText(str(c1[0]))
                                self.label_ymin_result.setText(str(c1[1]))
                                self.label_xmax_result.setText(str(c2[0]))
                                self.label_ymax_result.setText(str(c2[1]))

                                # 将结果记录至列表中
                                res_all = [self.names[int(cls)], conf.item(), [c1[0], c1[1], c2[0], c2[1]]]
                                self.res_set.append(res_all)
                                self.change_table(img_path, res_all[0], res_all[2], res_all[1])

                            self.label_class_result.setText(str(count))
                            self.label_score_result.setText(str(len(det) - count))
                            # 更新下拉选框
                            self.comboBox_select.currentIndexChanged.disconnect(self.select_obj)
                            self.comboBox_select.clear()
                            self.comboBox_select.addItem('所有目标')
                            for i in range(len(self.detInfo)):
                                text = "{}-{}".format(self.detInfo[i][0], i + 1)
                                self.comboBox_select.addItem(text)
                            self.comboBox_select.currentIndexChanged.connect(self.select_obj)

                            image = im0.copy()
                            InferenceNms = t2 - t1  # 单张图片推理时间
                            self.label_time_result.setText(str(round(InferenceNms, 2)))  # 将推理时间放到右上角

                        else:
                            # 清除UI上的label显示
                            self.label_numer_result.setText("0")
                            self.label_class_result.setText('0')
                            font = QtGui.QFont()
                            font.setPointSize(14)
                            self.label_class_result.setFont(font)
                            self.label_score_result.setText("0")  # 显示置信度值
                            # 清除位置坐标
                            self.label_xmin_result.setText("0")
                            self.label_ymin_result.setText("0")
                            self.label_xmax_result.setText("0")
                            self.label_ymax_result.setText("0")

                        # 在Qt界面中显示检测完成画面
                        self.detected_image = image.copy()
                        self.display_image(image)  # 在界面中显示画面
                        QtWidgets.QApplication.processEvents()
                        # self.label_display.display_image(image)

        else:
            self.clearUI()

    def choose_file(self):
        """
        图像检测
        """
        self.timer_camera.stop()
        self.timer_video.stop()
        self.c_video = 0
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.cap_video:
            self.cap_video.release()  # 释放视频画面帧

        self.comboBox_select.clear()  # 下拉选框的显示
        self.comboBox_select.addItem('所有目标')  # 清除下拉选框
        self.clearUI()  # 清除UI上的label显示

        self.flag_timer = ""
        # 使用文件选择对话框选择图片
        fileName_choose, filetype = QFileDialog.getOpenFileName(
            self.centralwidget, "选取图片文件",
            self.path,  # 起始路径
            "图片(*.jpg;*.jpeg;*.png)")  # 文件类型
        self.path = fileName_choose  # 保存路径

        if fileName_choose != '':
            self.flag_timer = "image"
            self.textEdit_pic.setText(fileName_choose + '文件已选中')
            # self.textEdit_pic.setStyleSheet("{background-color: transparent;\n"
            #                                 "color: rgb(0, 170, 255);;\n"
            #                                 "border:1px solid black;\n"
            #                                 "border-color: rgb(120, 120, 120);"
            #                                 "font: regular 12pt \"华为仿宋\";}\n")
            self.label_display.setText('正在启动识别系统...\n\nleading')
            QtWidgets.QApplication.processEvents()

            image = self.cv_imread(self.path)  # 读取选择的图片
            image = cv2.resize(image, (850, 500))
            img0 = image.copy()
            img = letterbox(img0, new_shape=self.imgsz)[0]
            img = np.stack(img, 0)
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)

            img = torch.from_numpy(img).to(self.device)  # 把图像矩阵移至到训练单元中(GPU中或CPU中)
            img = img.half() if self.half else img.float()  # 如果是半精度则转换图像格式
            img /= 255.0  # 归一化
            if img.ndimension() == 3:  # 如果图像时三维的添加1维变成4维
                img = img.unsqueeze(0)
            t1 = time_synchronized()  # 推理开始时间
            pred = self.model(img, augment=False)[0]  # 前向推理
            pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes,
                                       agnostic=self.opt.agnostic_nms)  # NMS过滤
            t2 = time_synchronized()  # 结束时间
            det = pred[0]

            p, s, im0 = None, '', img0
            self.current_image = img0.copy()
            # save_path = str(Path(self.opt.save_dir) / Path(p).name)  # 文件保存路径
            if det is not None and len(det):  # 如果有检测信息则进入
                self.label_numer_result.setText(str(len(det)))  # 将检测个数放置到主界面中
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()  # 把图像缩放至im0的尺寸
                number_i = 0  # 类别预编号
                self.detInfo = []

                count = 0
                for *xyxy, conf, cls in reversed(det):  # 遍历检测信息
                    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                    # 将检测信息添加到字典中
                    self.detInfo.append([self.names[int(cls)], [c1[0], c1[1], c2[0], c2[1]], '%.2f' % conf, int(cls)])
                    number_i += 1  # 编号数+1

                    # self.label_class_result.setText(str(self.names[int(cls)]))
                    if int(cls) == 1:
                        count += 1
                    # self.label_score_result.setText('%.2f' % conf)
                    label = '%s %.0f%%' % (self.names[int(cls)], conf * 100)

                    # 画出检测到的目标物
                    # print(xyxy)
                    im0 = self.drawRectBox(im0, xyxy, alpha=0.2, addText=label, color=self.colors[int(cls)])
                    self.label_xmin_result.setText(str(c1[0]))
                    self.label_ymin_result.setText(str(c1[1]))
                    self.label_xmax_result.setText(str(c2[0]))
                    self.label_ymax_result.setText(str(c2[1]))

                    # 将结果记录至列表中
                    res_all = [self.names[int(cls)], conf.item(), [c1[0], c1[1], c2[0], c2[1]]]
                    self.res_set.append(res_all)
                    self.change_table(self.path, res_all[0], res_all[2], res_all[1])

                self.label_class_result.setText(str(count))
                self.label_score_result.setText(str(len(det) - count))
                # 更新下拉选框
                self.comboBox_select.currentIndexChanged.disconnect(self.select_obj)
                self.comboBox_select.clear()
                self.comboBox_select.addItem('所有目标')
                for i in range(len(self.detInfo)):
                    text = "{}-{}".format(self.detInfo[i][0], i + 1)
                    self.comboBox_select.addItem(text)
                self.comboBox_select.currentIndexChanged.connect(self.select_obj)

                image = im0.copy()
                InferenceNms = t2 - t1  # 单张图片推理时间
                self.label_time_result.setText(str(round(InferenceNms, 2)))  # 将推理时间放到右上角

            else:
                # 清除UI上的label显示
                self.label_numer_result.setText("0")
                self.label_class_result.setText('0')
                font = QtGui.QFont()
                font.setPointSize(14)
                self.label_class_result.setFont(font)
                self.label_score_result.setText("0")  # 显示置信度值
                # 清除位置坐标
                self.label_xmin_result.setText("0")
                self.label_ymin_result.setText("0")
                self.label_xmax_result.setText("0")
                self.label_ymax_result.setText("0")

            # 在Qt界面中显示检测完成画面
            self.detected_image = image.copy()
            self.display_image(image)  # 在界面中显示画面
            # self.label_display.display_image(image)
        else:
            self.clearUI()

    def button_open_video_click(self):
        self.c_video = 0
        if self.timer_camera.isActive():
            self.timer_camera.stop()

        if self.cap:
            self.cap.release()

        self.clearUI()  # 清除显示
        QtWidgets.QApplication.processEvents()

        if not self.timer_video.isActive():  # 检查定时状态
            # 弹出文件选择框选择视频文件
            fileName_choose, filetype = QFileDialog.getOpenFileName(self.centralwidget, "选取视频文件",
                                                                    self.video_path,  # 起始路径
                                                                    "视频(*.mp4;*.avi)")  # 文件类型
            self.video_path = fileName_choose

            if fileName_choose != '':
                self.flag_timer = "video"
                self.textEdit_video.setText(fileName_choose + '文件已选中')
                self.setStyleText(self.textEdit_video)

                self.label_display.setText('正在启动识别系统...\n\nleading')
                QtWidgets.QApplication.processEvents()

                try:  # 初始化视频流
                    self.cap_video = cv2.VideoCapture(fileName_choose)
                except:
                    print("[INFO] could not determine # of frames in video")

                self.timer_video.start(30)  # 打开定时器

            else:
                # 选择取消，恢复界面状态
                self.flag_timer = ""
                self.clearUI()

        else:
            # 定时器未开启，界面回复初始状态
            self.flag_timer = ""
            self.timer_video.stop()
            self.cap_video.release()
            self.label_display.clear()
            time.sleep(0.5)
            self.clearUI()
            self.comboBox_select.clear()
            self.comboBox_select.addItem('所有目标')
            QtWidgets.QApplication.processEvents()

    def show_video(self):
        # 定时器槽函数，每隔一段时间执行
        flag, image = self.cap_video.read()  # 获取画面

        if flag:
            image = cv2.resize(image, (850, 500))
            self.current_image = image.copy()

            img0 = image.copy()
            img = letterbox(img0, new_shape=self.imgsz)[0]
            img = np.stack(img, 0)
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)

            pred, useTime = self.predict(img)

            self.label_time_result.setText(str(useTime))
            QtWidgets.QApplication.processEvents()

            det = pred[0]
            p, s, im0 = None, '', img0
            count = 0
            if det is not None and len(det):  # 如果有检测信息则进入
                self.label_numer_result.setText(str(len(det)))  # 将检测个数放置到主界面中
                det[:, :4] = scale_coords(img.shape[1:], det[:, :4], im0.shape).round()  # 把图像缩放至im0的尺寸
                number_i = 0  # 类别预编号
                self.detInfo = []
                for *xyxy, conf, cls in reversed(det):  # 遍历检测信息
                    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                    # 将检测信息添加到字典中
                    self.detInfo.append([self.names[int(cls)], [c1[0], c1[1], c2[0], c2[1]], '%.2f' % conf, int(cls)])
                    number_i += 1  # 编号数+1

                    if int(cls) == 1:
                        count += 1
                    # self.label_class_result.setText(str(self.names[int(cls)]))
                    # self.label_score_result.setText('%.2f' % conf)
                    # label = '%s %.2f' % (self.names[int(cls)], conf)
                    label = '%s %.0f%%' % (self.names[int(cls)], conf * 100)

                    # 画出检测到的目标物
                    image = self.drawRectBox(image, xyxy, addText=label, color=self.colors[int(cls)])
                    self.label_xmin_result.setText(str(c1[0]))
                    self.label_ymin_result.setText(str(c1[1]))
                    self.label_xmax_result.setText(str(c2[0]))
                    self.label_ymax_result.setText(str(c2[1]))

                    # 将结果记录至列表中
                    self.c_video += 1
                    if self.c_video % 10 == 0:
                        res_all = [self.names[int(cls)], conf.item(), [c1[0], c1[1], c2[0], c2[1]]]
                        self.res_set.append(res_all)
                        self.change_table(str(self.count), res_all[0], res_all[2], res_all[1])

                self.label_class_result.setText(str(count))
                self.label_score_result.setText(str(len(det) - count))
                # 更新下拉选框
                self.comboBox_select.currentIndexChanged.disconnect(self.select_obj)
                self.comboBox_select.clear()
                self.comboBox_select.addItem('所有目标')
                for i in range(len(self.detInfo)):
                    text = "{}-{}".format(self.detInfo[i][0], i + 1)
                    self.comboBox_select.addItem(text)
                self.comboBox_select.currentIndexChanged.connect(self.select_obj)
            else:
                # 清除UI上的label显示
                self.label_numer_result.setText("0")
                self.label_class_result.setText('0')
                font = QtGui.QFont()
                font.setPointSize(14)
                self.label_class_result.setFont(font)
                self.label_score_result.setText("0")  # 显示置信度值
                # 清除位置坐标
                self.label_xmin_result.setText("0")
                self.label_ymin_result.setText("0")
                self.label_xmax_result.setText("0")
                self.label_ymax_result.setText("0")

            self.detected_image = image.copy()
            # 在Qt界面中显示检测完成画面
            QtWidgets.QApplication.processEvents()
            self.display_image(image)
            # self.label_display.display_image(image)
        else:
            self.timer_video.stop()

    def button_open_camera_click(self):
        self.c_video = 0
        if self.timer_video.isActive():
            self.timer_video.stop()
        # self.timer_camera.stop()
        QtWidgets.QApplication.processEvents()

        if self.cap_video:
            self.cap_video.release()  # 释放视频画面帧

        if not self.timer_camera.isActive():  # 检查定时状态
            flag = self.cap.open(self.CAM_NUM)  # 检查相机状态
            if not flag:  # 相机打开失败提示
                QtWidgets.QMessageBox.warning(self.centralwidget, u"Warning",
                                              u"请检测相机与电脑是否连接正确！ ",
                                              buttons=QtWidgets.QMessageBox.Ok,
                                              defaultButton=QtWidgets.QMessageBox.Ok)
                self.flag_timer = ""
            else:
                # 准备运行识别程序
                self.flag_timer = "camera"
                self.clearUI()

                self.textEdit_camera.setText('实时摄像已启动')
                self.setStyleText(self.textEdit_camera)
                self.label_display.setText('正在启动识别系统...\n\nleading')
                QtWidgets.QApplication.processEvents()

                self.timer_camera.start(30)  # 打开定时器
        else:
            # 定时器未开启，界面回复初始状态
            self.flag_timer = ""
            self.timer_camera.stop()
            if self.cap:
                self.cap.release()
            self.clearUI()
            QtWidgets.QApplication.processEvents()

    def show_camera(self):
        # 定时器槽函数，每隔一段时间执行
        # if self.flag:
        flag, image = self.cap.read()  # 获取画面
        if flag:
            self.current_image = image.copy()

            s = np.stack([letterbox(x, new_shape=self.imgsz)[0].shape for x in [image]], 0)
            rect = np.unique(s, axis=0).shape[0] == 1
            img0 = [image].copy()
            img = [letterbox(x, new_shape=self.imgsz, auto=rect)[0] for x in img0]
            img = np.stack(img, 0)
            img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB, to bsx3x416x416
            img = np.ascontiguousarray(img)

            pred, useTime = self.predict(img)
            self.label_time_result.setText(str(useTime))

            det = pred[0]
            p, s, im0 = None, '', img0

            if det is not None and len(det):  # 如果有检测信息则进入
                self.label_numer_result.setText(str(len(det)))  # 将检测个数放置到主界面中

                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0[0].shape).round()  # 把图像缩放至im0的尺寸

                number_i = 0  # 类别预编号
                self.detInfo = []
                count = 0
                for *xyxy, conf, cls in reversed(det):  # 遍历检测信息
                    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                    # 将检测信息添加到字典中
                    self.detInfo.append([self.names[int(cls)], [c1[0], c1[1], c2[0], c2[1]], '%.2f' % conf, int(cls)])
                    number_i += 1  # 编号数+1

                    if int(cls):
                        count += 1
                    # image = im0[0].copy()
                    # self.label_class_result.setText(str(self.names[int(cls)]))
                    # self.label_score_result.setText('%.2f' % conf)
                    # label = '%s %.2f' % (self.names[int(cls)], conf)
                    label = '%s %.0f%%' % (self.names[int(cls)], conf * 100)
                    # 画出检测到的目标物
                    image = self.drawRectBox(image, xyxy, addText=label, color=self.colors[int(cls)])
                    self.label_xmin_result.setText(str(c1[0]))
                    self.label_ymin_result.setText(str(c1[1]))
                    self.label_xmax_result.setText(str(c2[0]))
                    self.label_ymax_result.setText(str(c2[1]))

                    # 将结果记录至列表中
                    self.c_video += 1
                    if self.c_video % 10 == 0:
                        res_all = [self.names[int(cls)], conf.item(), [c1[0], c1[1], c2[0], c2[1]]]
                        self.res_set.append(res_all)
                        self.change_table(str(self.count), res_all[0], res_all[2], res_all[1])

                self.label_class_result.setText(str(count))
                self.label_score_result.setText(str(len(det) - count))
                # 更新下拉选框
                self.comboBox_select.currentIndexChanged.disconnect(self.select_obj)
                self.comboBox_select.clear()
                self.comboBox_select.addItem('所有目标')
                for i in range(len(self.detInfo)):
                    text = "{}-{}".format(self.detInfo[i][0], i + 1)
                    self.comboBox_select.addItem(text)
                self.comboBox_select.currentIndexChanged.connect(self.select_obj)

            else:
                # 清除UI上的label显示
                self.label_numer_result.setText("0")
                # self.label_time_result.setText('0 s')
                self.label_class_result.setText('0')
                font = QtGui.QFont()
                font.setPointSize(14)
                self.label_class_result.setFont(font)
                self.label_score_result.setText("0")  # 显示置信度值
                # 清除位置坐标
                self.label_xmin_result.setText("0")
                self.label_ymin_result.setText("0")
                self.label_xmax_result.setText("0")
                self.label_ymax_result.setText("0")

            self.detected_image = image.copy()
            # 在Qt界面中显示检测完成画面
            self.display_image(image)
            # self.label_display.display_image(image)
        else:
            self.timer_video.stop()

    def predict(self, img):
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        t1 = time_synchronized()
        pred = self.model(img, augment=False)[0]
        pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes,
                                   agnostic=self.opt.agnostic_nms)
        t2 = time_synchronized()
        InferNms = round((t2 - t1), 2)

        return pred, InferNms

    def save_file(self):
        if self.detected_image is not None:
            now_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            cv2.imwrite('./pic_' + str(now_time) + '.png', self.detected_image)
            QMessageBox.about(self.centralwidget, "保存文件", "\nSuccessed!\n文件已保存！")
        else:
            QMessageBox.about(self.centralwidget, "保存文件", "saving...\nFailed!\n请先选择检测操作！")

    def setting(self):
        QMessageBox.about(self.centralwidget, "Bilibili", "<A href='https://space.bilibili.com/456667721'>"
                                                          "https://space.bilibili.com/456667721</a>")

    def disp_version(self):
        QMessageBox.about(self.centralwidget, "面包多", "<A href='https://mbd.pub/o/wuxian/'>"
                                                     "https://mbd.pub/o/wuxian/</a>")

    def disp_website(self):
        QMessageBox.about(self.centralwidget, "CSDN博客", "<A href='https://wuxian.blog.csdn.net'>"
                                                        "https://wuxian.blog.csdn.net</a>")
