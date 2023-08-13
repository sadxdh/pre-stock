import os
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

picpath = 'Visualization/股票数据可视化图表'


class GetData:
    def __init__(self, code, start_time, jiaoyisuo, stock_name):
        self.code = code
        self.start = start_time
        self.jiaoyisuo = jiaoyisuo
        self.code_info_resp = None
        self.stocks_name = stock_name

        if not os.path.exists(f"data\\stocks_data\\{self.stocks_name}.csv"):
            print("未在本地查询到数据。。")
            print("正在初始化数据。。")
            self.save()
        else:
            print("本地已存在")
            self.ori_data = pd.read_csv(f"data\\stocks_data\\{self.stocks_name}.csv")
            print("数据正在读取", self.ori_data)
        self.draw()

    def save(self):
        self.ori_data = ts.get_k_data(self.code, start=self.start)
        self.ori_data.index = pd.to_datetime(self.ori_data.date)
        self.ori_data = self.ori_data.sort_index()
        print(self.ori_data)
        self.ori_data.to_csv(f"data\\stocks_data\\{self.stocks_name}.csv", index=False, encoding='utf8')

    def draw(self):
        self.ori_data['close'].plot()
        plt.title("original data")
        plt.savefig(f'{picpath}/{self.stocks_name}.png')
        plt.show()

    def delData(self):
        if not os.path.exists(f"data\\stocks_data\\{self.stocks_name}.csv"):
            print("未在本地查询到数据文件")
        else:
            print(f"已获取到本地数据{self.stocks_name}.csv")
            print(f"{self.stocks_name}.csv 正在删除数据。。")
            self.ori_data = pd.read_csv(f"data\\stocks_data\\{self.stocks_name}.csv")
            print(f"{self.stocks_name}.csv 文件删除完毕")


def main(start_time):
    f = open('target', 'r', encoding='utf-8')
    stock_name = f.read().split('\n')
    print(stock_name)
    for s in stock_name:
        stock = s.split('（')[0]
        code = s.split('.')[-1].split('）')[0]
        exchange = s.split('（')[-1].split('.')[0].lower()
        print(stock)
        print(code)
        print(exchange)
        GetData(code, start_time, exchange, stock)


if __name__ == '__main__':
    start_time = '2005-05-05'
    main(start_time)
