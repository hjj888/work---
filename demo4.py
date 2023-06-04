import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as m_colors
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体或其他支持的字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
# 读取数据
# df = pd.read_excel('./floor2/floor1_50_1.xlsx')
df = pd.read_excel('./floor2/标志视野正确方向.xlsx')
print(df)
# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(15, 12))
# 创建自定义颜色映射
cmap = plt.cm.get_cmap('rainbow', 21)  # 彩虹颜色映射有21个级别，包括缺失值
# 设置大于等于20的值的填充色为浅灰色
# cmap.set_over('lightgray')
cmap.set_over('#005E3F')
# 设置小于等于0的值的填充色为白色
cmap.set_under('white')
# 设置缺失值的填充色为"#005E3F"
cmap.set_bad('#005E3F')
# 创建颜色标准化器
# norm = m_colors.Normalize(vmin=0, vmax=20)
norm = m_colors.Normalize(vmin=0.001, vmax=1)
# 处理缺失值
df_with_nan = df.copy()  # 创建副本以保留原始数据
df_with_nan = df_with_nan.replace(200, np.nan)  # 将200替换为NaN
# 绘制热图
im = ax.imshow(df_with_nan.values, cmap=cmap, norm=norm)
# 创建颜色条
cbar = plt.colorbar(im, ax=ax, shrink=0.8)  # 设置颜色条长度为16
# 设置颜色条标签
cbar.set_label('')
# 显示数据值
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        value = df.values[i, j]
        if np.isnan(value):
            text_color = 'black'
            value = 200
        # elif value > 20:
        elif value > 1:
            text_color = 'black'
        else:
            text_color = 'black'
        ax.text(j, i, f'{value:.2f}', ha='center', va='center', color=text_color)
# 设置坐标轴标签
ax.set_xlabel('长')
ax.set_ylabel('宽')
# 设置图标题
ax.set_title('房间热力图')
# 存图片
plt.savefig('./image2/标志视野正确方向' + '.png', dpi=800)
plt.show()