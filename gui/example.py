from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


class ChartWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def update_chart(self, stock_name):
        # 在图表中绘制数据
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # 例如： ax.plot(x_values, y_values)
        # 注意：在这里根据您的数据进行适当的图表绘制操作
        datapath = 'data/stocks_data'
        df = pd.read_csv(f'{datapath}/{stock_name}.csv')['close']
        ax.plot(df.index, df)
        plt.title("original data")
        # 刷新图表显示
        self.canvas.draw()


class Ui_Form(object):
    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(1150, 755)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1150, 755))
        Form.setMaximumSize(QtCore.QSize(1150, 755))
        Form.setStyleSheet("QWidget{background:url(image/bg222.png)}")

        # Create the chart widget
        self.chart_widget = ChartWidget(Form)
        self.chart_widget.setObjectName("chart_widget")

        # Update the chart widget with the chart
        self.chart_widget.update_chart(triplets_list)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        # Translation code...
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


