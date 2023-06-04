import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
"""绘制时间序列图"""
# 读取数据
data = pd.read_excel('./floor1/floor.xlsx')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体或其他支持的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

# 提供的数据
data1 = pd.read_excel('./floor1/floor.xlsx')
# 去除第一行
data2 = data1.iloc[1:]
data3 = np.array(data2)
# 创建数据表
data = pd.DataFrame(data3, columns=['步数', '人数（左）', '人数（右）'])

'''计算移动平均值'''
# 计算人数（左）的5个观测值的移动平均值
data['人数（左）移动平均值'] = data['人数（左）'].rolling(window=5).mean()
# 计算人数（右）的5个观测值的移动平均值
data['人数（右）移动平均值'] = data['人数（右）'].rolling(window=5).mean()
# 创建画布和子图
fig, ax = plt.subplots(figsize=(10, 5))
# 绘制人数（左）和人数（左）移动平均值的折线图
ax.plot(data['步数'], data['人数（左）'], label='人数（左）')
ax.plot(data['步数'], data['人数（左）移动平均值'], label='人数（左）移动平均值')
# 绘制人数（右）和人数（右）移动平均值的折线图
ax.plot(data['步数'], data['人数（右）'], label='人数（右）')
ax.plot(data['步数'], data['人数（右）移动平均值'], label='人数（右）移动平均值')
# 设置标题和标签
ax.set_xlabel('步数')
ax.set_ylabel('人数')
ax.set_title('人数（左）和人数（右）及移动平均趋势图')
# 添加图例
ax.legend()
# 存图片
plt.savefig('./image2/人数（左）和人数（右）及移动平均趋势图' + '.png', dpi=300)
# 显示图形
plt.show()

'''计算自相关性和偏相关性：'''
# 创建画布
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# 绘制人数（左）的自相关图像
plot_acf(data['人数（左）'], lags=32, ax=axs[0, 0])
axs[0, 0].set_xlabel('Lag')
axs[0, 0].set_ylabel('Autocorrelation')
axs[0, 0].set_title('Autocorrelation Function (ACF) of 人数（左）')

# 绘制人数（右）的自相关图像
plot_acf(data['人数（右）'], lags=32, ax=axs[0, 1])
axs[0, 1].set_xlabel('Lag')
axs[0, 1].set_ylabel('Autocorrelation')
axs[0, 1].set_title('Autocorrelation Function (ACF) of 人数（右）')

# 绘制人数（左）的偏自相关图像
plot_pacf(data['人数（左）'], lags=32, method='ywm', ax=axs[1, 0])
axs[1, 0].set_xlabel('Lag')
axs[1, 0].set_ylabel('Partial Autocorrelation')
axs[1, 0].set_title('Partial Autocorrelation Function (PACF) of 人数（左）')

# 绘制人数（右）的偏自相关图像
plot_pacf(data['人数（右）'], lags=32, method='ywm', ax=axs[1, 1])
axs[1, 1].set_xlabel('Lag')
axs[1, 1].set_ylabel('Partial Autocorrelation')
axs[1, 1].set_title('Partial Autocorrelation Function (PACF) of 人数（右）')

# 调整子图间距
plt.tight_layout()
# 存图片
plt.savefig('./image2/自相关性和偏相关性' + '.png', dpi=300)
# 显示图像
plt.show()

