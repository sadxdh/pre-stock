import pandas as pd
import talib as ta
import analytics.stocks_analysis.PeakDetection
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main(filename):
    df = pd.read_csv(f"data/stocks_data/{filename}.csv")
    # df.index = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # # 假设您已经有了一个名为df的DataFrame对象，其中包含日期（在df.index中）和收盘价（在df['close']中）
    # # 创建新列来存储五日均线和十日均线
    df['5日均线'] = ta.SMA(df['close'], timeperiod=5)
    df['10日均线'] = ta.SMA(df['close'], timeperiod=10)
    def Kline(df):
        plt.rcParams['font.sans-serif'] = 'SimHei'  # 指定中文字体，如宋体或黑体
        plt.figure(figsize=(16, 8))
        data = df[-200:]
        plt.title(f'{filename}-均线图')
        data['close'].plot(legend=True)
        data['5日均线'].plot(legend=True)
        data['10日均线'].plot(legend=True)
        plt.savefig(f"Visualization/股票数据可视化图表/{filename}-均线图.png")
    Kline(df)

    def v(df):
        plt.rcParams['font.sans-serif'] = 'SimHei'  # 指定中文字体，如宋体或黑体
        plt.figure(figsize=(16, 8))
        data = df[-200:]
        plt.title(f'{filename}-交易量')
        data['volume'].plot(legend=True)  # 交易量与股价走势 相关性
        plt.savefig(f"Visualization/股票数据可视化图表/{filename}-交易量.png")
    v(df)
    # # 假设您已经有了一个名为df的DataFrame对象，其中包含日期（在df.index中）和收盘价（在df['close']中）
    # # 创建新列来存储涨跌幅度
    # df = df.tail(100)
    df['涨跌幅'] = (df['close'] - df['close'].shift(5)) / df['close'].shift(5)
    def rise(df):
        plt.figure(figsize=(16, 8))
        plt.title(f'{filename}-涨跌幅')
        # 添加0基准线
        plt.axhline(0, color='red', linestyle='--')
        data = df[-200:]
        data['涨跌幅'].plot(legend=True)  # 交易量与股价走势 相关性
        plt.rcParams['axes.unicode_minus'] = False
        plt.savefig(f"Visualization/股票数据可视化图表/{filename}-涨跌幅.png")
    rise(df)

    # 假设您已经有了一个名为df的DataFrame对象，其中包含日期（在df.index中）和收盘价（在df['close']中）
    # 相对强弱指标RSI基本原理： 
    # 通过测量一段时间间内股价上涨总幅度占股价变化总幅度平均值的百分比来评估多空力量的强弱程度， 其能够反映出市场在一定时期内的景气程度
        # RSI（Relative Strength Index）是一种常用的技术分析指标，用于衡量价格走势的强弱程度，常用于股票、期货、外汇等市场。

        # 以下是RSI指标的计算方式：
        # 计算价格涨跌：
        # 记录每个交易日的收盘价。假设共有n个交易日，记为close[i]，其中i=0,1,...,n-1。
        # 计算每个交易日的价格涨跌：delta[i] = close[i] - close[i-1]，其中i>0。当i=0时，delta[0]的值通常为0或者忽略不计。
        # 计算平均涨幅和平均跌幅：

        # 计算n个交易日中的平均涨幅（average_gain）和平均跌幅（average_loss）：
        # 首先，计算n个交易日中所有正的价格涨跌值的平均值：average_gain = sum(delta[i] for i in range(1, n) if delta[i] > 0) / n。
        # 然后，计算n个交易日中所有负的价格涨跌值的平均值的绝对值：average_loss = abs(sum(delta[i] for i in range(1, n) if delta[i] < 0) / n)。
        # 计算相对强弱指数（RSI）：

        # 使用平均涨幅和平均跌幅计算相对强弱指数（RSI）：RSI = 100 - (100 / (1 + (average_gain / average_loss)))。
        # RSI的取值范围通常在0到100之间。
        # 通过计算RSI指标，可以判断价格走势的强弱程度。一般来说，RSI值高于70表示市场超买，可能出现价格下跌的反转信号；RSI值低于30表示市场超卖，可能出现价格上涨的反转信号。同时，还可以观察RSI值的变化趋势，例如RSI值的背离现象等，来辅助判断价格走势的变化。
    df['RSI'] = ta.RSI(df['close'], timeperiod=14)
    def R(df):
        plt.title(f'{filename}-RSI')
        plt.figure(figsize=(16, 8))
        data = df[-200:]
        data['RSI'].plot(legend=True)
        plt.savefig(f"Visualization/股票数据可视化图表/{filename}-RSI.png")

    # 计算MACD指标
        # 计算MACD线：
        # MACD线是短期指数移动平均线（EMA）减去长期指数移动平均线（EMA）的差异。通常，常用的时间周期是12天和26天。

        # 计算短期EMA（12天）：将过去12个交易日的收盘价计算出指数移动平均值，常用的平滑因子为2 / (12 + 1)。
        # 计算长期EMA（26天）：将过去26个交易日的收盘价计算出指数移动平均值，常用的平滑因子为2 / (26 + 1)。
        # 计算MACD线：MACD线 = 短期EMA - 长期EMA。
        # 计算MACD信号线：
        # MACD信号线是MACD线的9天指数移动平均值。常用的平滑因子为2 / (9 + 1)。

        # 计算MACD信号线：MACD信号线 = 9天MACD线的指数移动平均值。
        # 计算MACD柱状图：
        # MACD柱状图表示MACD线和MACD信号线之间的差异。

        # 计算MACD柱状图：MACD柱状图 = MACD线 - MACD信号线。
            # 平滑因子的作用
            # 平滑因子在MACD指标中起到平滑价格数据的作用。指数移动平均（EMA）是一种加权移动平均方法，它对最近的价格赋予较高的权重，对较早期的价格赋予较低的权重。平滑因子决定了EMA对不同时间点的价格赋予的权重大小。
            # 在MACD指标中，有三个地方使用了平滑因子：
            # 计算短期EMA和长期EMA：通过选择适当的平滑因子，可以决定短期EMA和长期EMA对价格变动的敏感度。较小的平滑因子将使EMA更加敏感，更快地反应价格的变化；较大的平滑因子将使EMA更加平滑，减小了价格短期波动的影响。
            # 计算MACD信号线：MACD信号线是MACD线的指数移动平均值，使用了平滑因子来确定MACD信号线对MACD线的平滑程度。较小的平滑因子将使MACD信号线更加敏感，更快地跟随MACD线的变化；较大的平滑因子将使MACD信号线更加平滑，减小了噪音和短期波动的影响。
            # 计算MACD柱状图：MACD柱状图表示MACD线和MACD信号线之间的差异，平滑因子会影响MACD柱状图的变化速度和平滑程度。
            # 总的来说，平滑因子决定了指数移动平均对价格的响应速度和平滑程度。较小的平滑因子使指标更加敏感，更快地反应价格变化，但也更容易受到噪音的干扰；较大的平滑因子使指标更加平滑，减小了噪音的影响，但也降低了指标对价格变化的敏感度。在实际应用中，可以根据具体的分析需求和市场特点选择合适的平滑因子。
    # MACD线、信号线（signal line,MACD线的9日指数移动均线）、离差图（divergence histogram）
    # macd（对应diff）
    # macdsignal（对应dea）
    # macdhist（对应macd）
    # 然后按照下面的原则判断买入还是卖出。       
    # 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。       
    # 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。       
    # 3.DEA线与K线发生背离，行情反转信号。       
    # 4.分析MACD柱状线，由正变负，卖出信号；由负变正，买入信号。
    # 参考链接：https://juejin.cn/post/6914195121487478791
    macd, macdsignal, macdhist = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd
    df['MACD_Signal'] = macdsignal
    df['MACD_Histogram'] = macdhist

    def M(df):
        # MACD指标
        data = df[-200:]
        # 创建图形对象和子图对象
        fig, ax = plt.subplots(figsize=(16, 6))
        # 绘制MACD线
        ax.plot(data.index, data['MACD'], label='macd（对应diff）')
        # 绘制信号线
        ax.plot(data.index, data['MACD_Signal'], label='macdsignal（对应dea）')
        # 绘制柱状图
        ax.bar(data.index, data['MACD_Histogram'], label='macdhist（对应macd）', color='gray')
        # 设置图表标题和轴标签
        ax.set_title('MACD', fontsize=14)
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        ax.set_xticklabels(df.index, rotation=90)
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('MACD', fontsize=12)
        # 设置图例
        ax.legend()
        # 自动调整日期显示格式
        fig.autofmt_xdate()
        plt.savefig(f"Visualization/股票数据可视化图表/{filename}-MACD.png")
    M(df)
    # 保存到文件
    clean_filename = f'{filename}_clean'
    filename = f'data/stocks_data/{clean_filename}.csv'
    df.to_csv(filename)
    return clean_filename


if __name__ == '__main__':
    stock = '浦发银行'
    clean_filename = main(stock)
    # analytics.PeakDetection.PeakDetection(clean_filename)


'''
    SMA：简单移动平均，简单的按照一定的周期计算出的移动平均线。
    EMA：指数移动平均，根据某一特定的指数来计算出的移动平均线。
    WMA：加权移动平均，把更新的数据赋予更多的权重，使其在计算移动平均线时，具有更大的影响力。
    DEMA：双指数移动平均，是对EMA的一种改进，它以某种方式抵消了EMA所产生的滞后性。
    TEMA：三指数移动平均，是对DEMA的一种改进，其计算公式与DEMA基本相同，只是改变了加权因子。
    TRIMA：三角形移动平均，与EMA相比，它更加均衡地分配权重，使得计算更加精准。
    KAMA：考夫曼自适应移动平均，基于市场变化的持续性和变化的速度，自适应地调整自身的参数。
    MAMA：MESA自适应移动平均，是一种强大的自适应移动平均，使用不同的周期来处理市场中的趋势和波动。
    T3：拓展三指数移动平均，是对TEMA的一种改进，它使用一个额外的因子来调整移动平均线的反应速度。
'''
