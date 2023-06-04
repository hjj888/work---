import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体或其他支持的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
# 提供的数据
data1 = pd.read_excel('./floor1/floor.xlsx')
# 去除第一行
data2 = data1.iloc[1:]
data3 = np.array(data2)
data = pd.DataFrame(data3, columns=['步数', '人数（左）', '人数（右）'])
data_array = np.array(data)

# 提取步数作为自变量X
X = data_array[:, 0].reshape(-1, 1)

# 提取人数（左）和人数（右）作为因变量Y1和Y2
Y1 = data_array[:, 1].reshape(-1, 1)
Y2 = data_array[:, 2].reshape(-1, 1)

# 创建线性回归模型
regression_model1 = LinearRegression()
regression_model2 = LinearRegression()

# 拟合数据
regression_model1.fit(X[:20], Y1[:20])
regression_model2.fit(X[:20], Y2[:20])

# 预测人数（左）和人数（右）
predicted_value1 = regression_model1.predict(X)
predicted_value2 = regression_model2.predict(X)

# 创建画布
plt.figure(figsize=(10, 6))

# 绘制人数（左）的实际数据和预测数据
plt.plot(X, Y1, label='实际数据（人数左）')
plt.plot(X, predicted_value1, label='预测数据（人数左）')

# 绘制人数（右）的实际数据和预测数据
plt.plot(X, Y2, label='实际数据（人数右）')
plt.plot(X, predicted_value2, label='预测数据（人数右）')

plt.xlabel('步数')
plt.ylabel('人数')
plt.title('人数（左）和人数（右）的实际数据与预测数据')
plt.legend()

# 设置横坐标刻度间隔为5个单位增大
plt.xticks(np.arange(0, X.max()+1, 5))
# 存图片
plt.savefig('./image2/人数（左）和人数（右）的实际数据与预测数据' + '.png', dpi=300)
# 显示图像
plt.show()