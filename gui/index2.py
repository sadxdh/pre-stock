# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui---2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from index3 import Ui_Form as Ui_Form3


class Ui_Form(object):
    def __init__(self, stock_name):
        self.stock_name = stock_name

    def setupUi(self, Form):
        Form.setObjectName("Form")  # Form (QWidget): 主窗体
        Form.resize(1150, 830)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)  # resize() 方法用于设置窗体的尺寸
        Form.setMinimumSize(QtCore.QSize(1150, 830))  # setObjectName() 方法用于设置对象名称
        Form.setMaximumSize(QtCore.QSize(1150, 800))
        Form.setStyleSheet("QWidget{background:url(GUI/image/bg222.png)}")  # setStyleSheet() 方法用于设置窗体的样式表
        self.frame_5 = QtWidgets.QFrame(Form)  # frame_5 (QFrame): 顶部框架
        self.frame_5.setGeometry(QtCore.QRect(10, 10, 1131, 41))  # setGeometry() 方法用于设置框架的位置和大小
        self.frame_5.setStyleSheet("background-image:url(:/background/bg12.jpg);\n"  # setStyleSheet() 方法用于设置框架的样式表
                                   "border: 2px solid white;")  # setFrameShape() 方法用于设置框架的形状
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)  # setFrameShadow() 方法用于设置框架的阴影
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)  # setObjectName() 方法用于设置对象名称
        self.frame_5.setObjectName("frame_5")
        self.label = QtWidgets.QLabel(self.frame_5)  # label (QLabel): 顶部标签
        self.label.setGeometry(QtCore.QRect(360, 0, 411, 71))  # setGeometry() 方法用于设置标签的位置和大小
        self.label.setStyleSheet("border:none;")  # setStyleSheet() 方法用于设置标签的样式表
        self.label.setObjectName("label")  # setObjectName() 方法用于设置对象名称
        self.widget = QtWidgets.QWidget(Form)  # widget (QWidget): 主窗体中的容器部件
        self.widget.setGeometry(QtCore.QRect(10, 60, 1131, 681))  # setGeometry() 方法用于设置容器部件的位置和大小
        self.widget.setObjectName("widget")  # setObjectName() 方法用于设置对象名称

        self.gridLayout = QtWidgets.QGridLayout(self.widget)  # gridLayout (QGridLayout): 网格布局管理器
        self.gridLayout.setContentsMargins(0, 0, 0, 0)  # setContentsMargins() 方法用于设置布局的边距
        self.gridLayout.setObjectName("gridLayout")  # setContentsMargins() 方法用于设置布局的边距

        self.frame = QtWidgets.QFrame(self.widget)  # frame, frame_2, frame_3, frame_4 (QFrame): 四个框架部件
        self.frame.setStyleSheet(f"image:url(Visualization/股票数据可视化图表/{self.stock_name}-均线图.png);\n"
                                 "background-size: cover;\n"
                                 "border: 2px solid white;")  # setStyleSheet() 方法用于设置框架的样式表
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)  # setFrameShape() 方法用于设置框架的形状
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)  # setFrameShadow() 方法用于设置框架的阴影
        self.frame.setObjectName("frame")  # setObjectName() 方法用于设置对象名称
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.widget)
        self.frame_2.setStyleSheet(f"image:url(Visualization/股票数据可视化图表/{self.stock_name}-MACD.png);\n"
                                   "background-size: cover;\n"
                                   "border: 2px solid white;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.widget)
        self.frame_3.setStyleSheet(f"image:url(Visualization/股票数据可视化图表/{self.stock_name}-RSI.png);\n"
                                   "background-size: cover;\n"
                                   "border: 2px solid white;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.widget)
        self.frame_4.setStyleSheet(f"image:url(Visualization/股票数据可视化图表/{self.stock_name}-交易量.png);\n"
                                   "background-size: cover;\n"
                                   "border: 2px solid white;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout.addWidget(self.frame_4, 1, 1, 1, 1)

        # 位于 self.frame_6 内的按钮，用于开始预测。对象名称："pushButton" 文本：开始预测 点击事件连接到 self.goToNextPage2 方法
        self.pushButton = QtWidgets.QPushButton('开始预测', Form)
        self.pushButton.setGeometry(QtCore.QRect(530, 780, 91, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.goToIndex3)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form",
                                      f"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{self.stock_name}股票预测</span><br/></p></body></html>"))

    def goToIndex3(self):
        # 创建并显示 index2 页面
        self.index3_page = QtWidgets.QWidget()
        self.index3_ui = Ui_Form3(self.stock_name)
        self.index3_ui.setupUi(self.index3_page)
        self.index3_page.show()


if __name__ == "__main__":
    import sys
    stock_name = '默认名称'
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form(stock_name)
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
