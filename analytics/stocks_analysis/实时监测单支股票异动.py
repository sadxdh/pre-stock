import efinance as ef
from collections import deque
import csv
import time
import datetime


def get_stock_data(stock_code, freq=1):
    # return ef.stock.get_quote_history(stock_code, klt=freq)
    df = ef.stock.get_quote_history(stock_code, klt=freq)
    latest_data = df.iloc[-1] if not df.empty else None
    return latest_data


def hander_data(stock_code, nowdate, data_queue, row):
    with open(f'{stock_code}-{nowdate}.csv', 'a', encoding='utf-8-sig', newline='') as file:
        csv_writer = csv.writer(file)
        # 如果文件为空，写入表头
        if file.tell() == 0:
            header = [
                '股票名称', '股票代码', '日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额',
                '振幅', '涨跌幅', '涨跌额', '换手率', '3_分钟涨幅', '5_分钟涨幅', '10_分钟涨幅',
                '20_分钟涨幅', '30_分钟涨幅', '60_分钟涨幅'
            ]
            csv_writer.writerow(header)
        close_price = row['收盘']  # 假设收盘价这一列为 '收盘'
        row_data = row.copy()  # 复制该行数据
        # 计算不同时间段的涨幅并添加到该行数据中
        for interval in [3, 5, 10, 20, 30, 60]:
            if len(data_queue) >= (interval - 1):
                data_slice = list(data_queue)[-(interval - 1)]
                price_change = (close_price - data_slice) / data_slice * 100
                row_data[f'{interval}_分钟涨幅'] = price_change
                # 检查涨幅是否超过阈值，假设阈值为5%
                if abs(price_change) > 5:
                    message = f"警告：{interval}分钟涨幅超过5%！"
                    # send_sms(message)  # 发送短信通知
        # 将该行数据插入队列
        data_queue.append(close_price)
        # 写入CSV文件
        csv_writer.writerow(row_data)
        data_queue.clear()


if __name__ == '__main__':
    stock_code = '600519'
    data_queue = deque(maxlen=60)  # 长度设置为60，涵盖1分钟到60分钟涨幅
    # 循环执行
    while True:
        current_time = datetime.datetime.now()
        nowdate = current_time.strftime("%Y-%m-%d")
        start_trading_time = current_time.replace(hour=9, minute=30, second=0, microsecond=0)  # 开盘时间为每天 9:30 AM
        end_trading_time = current_time.replace(hour=15, minute=00, second=0, microsecond=0)  # 收盘时间为每天 3:00 PM
        print(current_time)
        if start_trading_time <= current_time <= end_trading_time:
            print("Executing trading operations...")
            today_data = get_stock_data(stock_code, freq=1)
            hander_data(stock_code, nowdate, data_queue, today_data)
        time.sleep(60)  # 暂停一分钟后再继续循环
