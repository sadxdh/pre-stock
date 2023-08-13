from PyQt5 import QtCore, QtWidgets
from index2 import Ui_Form as Ui_Form2
from data_collection.stocks_collection import getFromTushare
from analytics.stocks_analysis import data_clearn
from model_train import UIpredict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import csv
import os


class Ui_Form(object):

    def __init__(self):
        self.stock_name = ''
        self.stock_code = ''
        self.exchange =''
        self.stock_list = self.read_stocks_csv()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1150, 800)
        Form.setWindowTitle("股票预测系统")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1150, 800))
        Form.setMaximumSize(QtCore.QSize(1150, 800))
        Form.setStyleSheet("QWidget{background:url(GUI/image/bg222.png)}")

        # 窗体上方框架，用于放置标题栏
        self.frame_5 = QtWidgets.QFrame(Form)
        self.frame_5.setGeometry(QtCore.QRect(10, 10, 1131, 60))
        self.frame_5.setStyleSheet("background-image:url(:/background/bg2.png);\n"
                                   "border: 2px solid white;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        # self.label 是一个 QLabel，它位于 self.frame_5 内，显示标题文本
        self.label = QtWidgets.QLabel(self.frame_5)
        self.label.setGeometry(QtCore.QRect(360, 0, 411, 70))
        self.label.setStyleSheet("border:none;")
        self.label.setObjectName("label")

        # 位于窗体左侧的框架，用于放置选择股票和股票代码的部分。样式表设置：背景图像和白色边框。
        self.frame_6 = QtWidgets.QFrame(Form)
        self.frame_6.setGeometry(QtCore.QRect(10, 70, 241, 671))
        self.frame_6.setStyleSheet("background-image:url(:/background/bg12.jpg);\n"
                                   "border: 2px solid white;")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")

        # 搜索框
        self.searchLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.searchLineEdit.setGeometry(QtCore.QRect(20, 90, 200, 30))
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchLineEdit.setText("请输入股票名称或代码")
        # 搜索按钮
        self.searchButton = QtWidgets.QPushButton('搜索', self.frame_6)
        self.searchButton.setGeometry(QtCore.QRect(110, 130, 111, 30))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.searchStock)

        # 位于 self.frame_6 内的标签，显示"选择股票"文本。样式表设置：无边框。
        self.label_2 = QtWidgets.QLabel(self.frame_6)
        self.label_2.setGeometry(QtCore.QRect(20, 250, 110, 30))
        self.label_2.setStyleSheet("border:none;")
        self.label_2.setObjectName("label_2")
        # 位于 self.frame_6 内的标签，显示"股票代码"文本。样式表设置：无边框。
        self.label_5 = QtWidgets.QLabel(self.frame_6)
        self.label_5.setGeometry(QtCore.QRect(20, 300, 110, 30))
        self.label_5.setStyleSheet("border:none;")
        self.label_5.setObjectName("label_5")
        # 位于 self.frame_6 内的标签，显示"股票代码"文本。样式表设置：无边框。
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setGeometry(QtCore.QRect(20, 350, 110, 30))
        self.label_3.setStyleSheet("border:none;")
        self.label_3.setObjectName("label_3")

        # 股票名称
        self.stockNameLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.stockNameLineEdit.setGeometry(QtCore.QRect(90, 250, 120, 30))
        self.stockNameLineEdit.setObjectName("stockNameLineEdit")
        self.stockNameLineEdit.setReadOnly(True)
        self.stockNameLineEdit.setText("默认股票名称")
        # 交易所代码
        self.exchangeLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.exchangeLineEdit.setGeometry(QtCore.QRect(90, 300, 120, 30))
        self.exchangeLineEdit.setObjectName("stockCodeLineEdit")
        self.exchangeLineEdit.setReadOnly(True)
        self.exchangeLineEdit.setText("默认交易所代码")
        # 股票代码
        self.stockCodeLineEdit = QtWidgets.QLineEdit(self.frame_6)
        self.stockCodeLineEdit.setGeometry(QtCore.QRect(90, 350, 120, 30))
        self.stockCodeLineEdit.setObjectName("stockCodeLineEdit")
        self.stockCodeLineEdit.setReadOnly(True)
        self.stockCodeLineEdit.setText("默认股票代码")

        # 位于 self.frame_6 内的按钮，用于开始预测。对象名称："pushButton" 文本：开始预测 点击事件连接到 self.goToNextPage2 方法
        self.pushButton = QtWidgets.QPushButton('开始分析', self.frame_6)
        self.pushButton.setGeometry(QtCore.QRect(80, 440, 91, 31))
        self.pushButton.setObjectName("pushButton")
        # 位于窗体右侧的框架，用于显示股票走势。样式表设置：背景图像和白色边框。
        self.frame_7 = QtWidgets.QFrame(Form)
        self.frame_7.setLayout(QtWidgets.QVBoxLayout())
        self.frame_7.setGeometry(QtCore.QRect(250, 70, 881, 671))
        self.frame_7.setStyleSheet("background-image:url(:/background/bg12.jpg);\n"
                                   "border: 2px solid white;")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")

        self.canvas.setGeometry(QtCore.QRect(10, 10, 861, 651))
        self.canvas.setObjectName("canvas")
        self.canvas.draw()

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.goToIndex2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:26pt; font-weight:600;\">基于LSTM的股票预测系统</span><br/></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt;\">股票名称：</span></p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt;\">交易所：</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt;\">股票代码：</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "开始预测"))

    def read_stocks_csv(self):
        path = 'stockcode'
        # 读取指定路径下的所有 CSV 文件
        file_list = os.listdir(path)
        self.triplets_list = []
        for file_name in file_list:
            if file_name.endswith('.csv'):
                file_path = os.path.join(path, file_name)
                exchange = file_name[:2]
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) == 2:
                            stock_name = row[0]
                            stock_code = row[1]
                            self.triplets_list.append((stock_name, stock_code, exchange))
        print(self.triplets_list)
        print(len(self.triplets_list))
        return self.triplets_list

    def searchStock(self):
        search_text = self.searchLineEdit.text().strip()
        # stock_list = [("股票A", "001"), ("股票B", "002"), ("股票C", "003")]  # 股票名称和代码列表，示例数据
        for stock_name, stock_code, exchange in self.stock_list:
            if search_text in stock_name or search_text in stock_code:
                print(stock_name, stock_code, exchange)
                self.stock_name = stock_name
                self.stock_code = stock_code
                self.exchange = exchange
                self.stockNameLineEdit.setText(self.stock_name)
                self.stockCodeLineEdit.setText(self.stock_code)
                self.exchangeLineEdit.setText(self.exchange)
                self.getStocksData()
                return
        # 如果没有找到匹配的股票，清空文本框内容
        self.stockNameLineEdit.setText("未找到匹配的股票名称")
        self.stockCodeLineEdit.setText("未找到匹配的股票代码")

    # 获取股票数据
    def getStocksData(self):
        try:
            start_time = '2005-05-05'
            # self, code, start_time, exchange, stock_name
            getFromTushare.GetData(self.stock_code, start_time, self.exchange, self.stock_name)
            df = pd.read_csv(f'data/stocks_data/{self.stock_name}.csv')['close']
            # 绘制图表
            self.figure.clear()  # 清空图表内容
            ax = self.figure.add_subplot(111)
            # 在 ax 上绘制您的图表，例如：
            ax.plot(df.index, df)
            ax.set_xlabel("X Label")
            ax.set_ylabel("Y Label")
            # 刷新 frame_7，使图表显示
            self.frame_7.layout().addWidget(self.canvas)
            self.canvas.draw()
            data_clearn.main(self.stock_name)
        except Exception as e:
            print("Exception occurred:", str(e))
        UIpredict.LSTMPre(self.stock_name)

    def goToIndex2(self):
        # 创建并显示 index2 页面
        self.index2_page = QtWidgets.QWidget()
        self.index2_ui = Ui_Form2(self.stock_name)
        self.index2_ui.setupUi(self.index2_page)
        self.index2_page.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
