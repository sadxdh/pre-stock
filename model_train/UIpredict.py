import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error


def LSTMPre(stock_name):
    # 读取数据
    data = pd.read_csv(f'data/stocks_data/{stock_name}.csv')  # 假设数据存储在名为stock_data.csv的文件中

    # 选择需要使用的特征列
    selected_features = ['close']  # 假设这是您要使用的特征列名称

    # 提取特征列数据
    features = data[selected_features].values

    # 提取目标变量（收盘价）
    target = data['close'].values

    # 归一化数据
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_features = scaler.fit_transform(features)
    scaled_target = scaler.fit_transform(target.reshape(-1, 1))

    # 创建训练集和测试集
    train_size = int(len(scaled_features) * 0.8)
    train_features = scaled_features[:train_size]
    train_target = scaled_target[:train_size]
    test_features = scaled_features[train_size:]
    test_target = scaled_target[train_size:]

    # 定义滑动窗口大小
    window_size = 10

    # 创建输入序列和输出序列
    X_train, y_train = [], []
    for i in range(window_size, len(train_features)):
        X_train.append(train_features[i - window_size:i])
        y_train.append(train_target[i])
    X_train, y_train = np.array(X_train), np.array(y_train)

    # 转换为LSTM可接受的输入格式 [样本数，时间步数，特征数]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], X_train.shape[2]))

    # 构建LSTM模型
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 训练模型
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # 创建测试集的输入序列
    inputs = scaled_features[len(scaled_features) - len(test_features) - window_size:]
    X_test = []
    for i in range(window_size, len(inputs)):
        X_test.append(inputs[i - window_size:i])
    X_test = np.array(X_test)

    # 转换为LSTM可接受的输入格式 [样本数，时间步数，特征数]
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], X_test.shape[2]))

    # 使用模型进行预测
    predicted_prices = model.predict(X_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)

    # 反归一化预测结果
    actual_prices = scaler.inverse_transform(test_target)

    # 绘制实际收盘价和预测收盘价的走势
    plt.figure(figsize=(16, 9))
    plt.plot(actual_prices, label='Actual')
    plt.plot(predicted_prices, label='Predicted')
    plt.title('Stock Price - Actual vs Predicted Closing Prices')
    plt.xlabel('Time')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.savefig(f"Visualization/模型预测图表/{stock_name}预测.png")

    # 计算均方误差（MSE）
    mse = mean_squared_error(actual_prices, predicted_prices)

    # 计算均方根误差（RMSE）
    rmse = np.sqrt(mse)

    print("均方误差 (MSE): ", mse)
    print("均方根误差 (RMSE): ", rmse)