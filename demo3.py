import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体或其他支持的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
# 提供的数据
data1 = pd.read_excel('./floor1/floor.xlsx')
# 去除第一行
data2 = data1.iloc[1:]
data3 = np.array(data2)
# 创建数据表
data = pd.DataFrame(data3, columns=['步数', '人数（左）', '人数（右）'])
# 散点图
plt.scatter(data['步数'], data['人数（左）'], label='人数（左）')
plt.scatter(data['步数'], data['人数（右）'], label='人数（右）')
plt.xlabel('步数')
plt.ylabel('人数')
plt.title('步数与人数之间的趋势散点图')
plt.legend()
# 设置横坐标刻度间隔为5个单位增大
data_array = np.array(data)
X = data_array[:, 0].reshape(-1, 1)
plt.xticks(np.arange(0, X.max()+1, 5))
# 存图片
plt.savefig('./image2/步数与人数之间的趋势散点图' + '.png', dpi=300)
plt.show()

# 折线图
plt.plot(data['步数'], data['人数（左）'], label='人数（左）')
plt.plot(data['步数'], data['人数（右）'], label='人数（右）')
plt.xlabel('步数')
plt.ylabel('人数')
plt.title('步数与人数之间的趋势折线图')
plt.legend()
# 设置横坐标刻度间隔为5个单位增大
data_array = np.array(data)
X = data_array[:, 0].reshape(-1, 1)
plt.xticks(np.arange(0, X.max()+1, 5))
# 存图片
plt.savefig('./image2/步数与人数之间的趋势折线图' + '.png', dpi=300)
plt.show()
