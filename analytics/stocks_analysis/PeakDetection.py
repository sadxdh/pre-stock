# 原著 https://www.mdpi.com/43264
# 数据峰值
# 股票极值（股票的最高点和最低点）在股票分析和交易中具有一定的用处。以下是一些股票极值的应用场景和用途：
# 趋势分析：股票的最高点和最低点可以用于分析趋势的形成和转折。最高点通常表示价格达到短期或长期的高点，可能标志着价格的下跌趋势开始或趋于结束。最低点通常表示价格达到短期或长期的低点，可能标志着价格的上涨趋势开始或趋于结束。通过观察和分析股票的极值，可以揭示市场的趋势和可能的转折点。
# 支撑和阻力水平：股票的最高点和最低点可以作为支撑和阻力水平的参考。支撑水平是指价格下跌时遇到的支撑点，可能导致价格反弹或停止下跌；阻力水平是指价格上涨时遇到的阻力点，可能导致价格回调或停止上涨。通过识别股票的最高点和最低点，可以确定潜在的支撑和阻力水平，用于决策买入和卖出的时机。
# 买卖信号：股票的最高点和最低点可以与其他技术指标结合使用，产生买卖信号。例如，当股票价格突破最高点时，可能发出买入信号，表示股票的上涨趋势可能加速；当股票价格跌破最低点时，可能发出卖出信号，表示股票的下跌趋势可能加速。通过结合股票的极值和其他技术指标，可以辅助判断买入和卖出的时机。
# 风险管理：股票的最高点和最低点可以作为风险管理的参考。当股票价格接近最高点时，可能存在高风险，因为价格可能出现回调或下跌；当股票价格接近最低点时，可能存在低风险，因为价格可能出现反弹或上涨。通过识别股票的极值，可以帮助投资者评估风险，并制定相应的风险管理策略。
# 总的来说，股票的极值对于趋势分析、支撑和阻力水平、买卖信号和风险管理都具有一定的用处。然而，需要结合其他技术指标和市场情况进行综合分析，以做出更准确的决策。
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class PeakDetection:
    def __init__(self, filename):
        self.filename = filename
        self.stock_week = None
        self.stock_train = None
        self.data = pd.read_csv(f"data/stocks_data/{self.filename}.csv", index_col=0, parse_dates=[0])
        print("已读取到数据", self.data)
        self.vis()

    def AMPD(self, data):
        """
        实现AMPD算法
        :param data: 1-D numpy.ndarray
        :return: 波峰所在索引值的列表
        """
        p_data = np.zeros_like(data, dtype=np.int32)
        count = data.shape[0]
        arr_rowsum = []
        for k in range(1, count // 2 + 1):
            row_sum = 0
            for i in range(k, count - k):
                if data[i] > data[i - k] and data[i] > data[i + k]:
                    row_sum -= 1
            arr_rowsum.append(row_sum)
        min_index = np.argmin(arr_rowsum)
        max_window_length = min_index
        for k in range(1, max_window_length + 1):
            for i in range(k, count - k):
                if data[i] > data[i - k] and data[i] > data[i + k]:
                    p_data[i] += 1
        return np.where(p_data == max_window_length)[0]

    def sim_data(self):
        x = self.data.index
        y = self.data['close']
        # print("x:", x)
        # print("y:", y)
        return x, y

    def vis(self):
        x, y = self.sim_data()
        plt.plot(x, y)
        px = x[self.AMPD(y)]
        print("长度：", px)
        self.data_extreme_value = self.data.copy()
        self.data_extreme_value['mixumum'] = pd.Series([])
        self.data_extreme_value['mixumum'] = self.data.index.isin(px)


        px = x[self.AMPD(-y)]
        print("长度：", px)
        self.data_extreme_value = self.data_extreme_value.copy()
        self.data_extreme_value['minumum'] = pd.Series([])
        self.data_extreme_value['minumum'] = self.data.index.isin(px)

        self.data_extreme_value.to_csv(f'data/stocks_data/{self.filename}_MaxMin.csv')


if __name__ == '__main__':
    filename = "海康威视"
    P = PeakDetection(filename)
