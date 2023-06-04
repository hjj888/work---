import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import random
from sklearn.linear_model import LinearRegression


class fun1(object):
    def __init__(self, Length=20, Width=16,
                 peo_left=6, peo_right=17, peo_up=0, peo_down=15,
                 peo_number=50,
                 left_location=7, right_location=7, sign_location=9,
                 left_parameter=1, right_parameter=7, fai=1):
        self.WALL_VALUE = 500  # 墙面的值
        self.DOOR_VALUE_left_before = 1  # 门的值
        self.DOOR_VALUE_right_before = 1  # 门的值
        self.DOOR_VALUE_left_after = left_parameter  # 门的值
        self.DOOR_VALUE_right_after = right_parameter  # 门的值
        self.SIGN_VALUE = 200  # 标志的值
        self.DISTANCE_MIN = 5  # 标志影响的最小距离
        self.DISTANCE_MAX = 15  # 标志影响的最大距离
        self.L = Length  # 房间长度
        self.L_half = int(Length / 2)
        self.W = Width  # 房间宽度
        self.W_half = int(Width / 2)
        # if (i > 6) and (i < 17) and (j > 0) and (j < 15):
        self.L_peo_left = peo_left  # 人数分布的左边距
        self.L_peo_right = peo_right  # 人数分布的左边距
        self.L_peo_up = peo_up  # 人数分布的左边距
        self.L_peo_down = peo_down  # 人数分布的左边距
        self.PEO_NUM = peo_number  # 房间内人数
        self.DOOR_LOCATION = [(left_location, 0), (right_location, Length - 1)]  # 门的位置
        self.SIGN_LOCATION = [(0, sign_location)]  # 标志的位置(假设向左的标志)
        self.FAI = fai

    def floorDemo_before(self, floor_shape):
        floor = np.zeros(floor_shape)
        # 设置墙的值
        floor[0:, 0] = self.WALL_VALUE
        floor[0:, -1] = self.WALL_VALUE
        floor[0, 0:] = self.WALL_VALUE
        floor[-1, 0:] = self.WALL_VALUE
        floor[5:7, 7] = self.WALL_VALUE
        floor[7, 7:12] = self.WALL_VALUE
        floor[10, 5:8] = self.WALL_VALUE
        floor[10:13, 10] = self.WALL_VALUE
        # 设置门的值
        floor[self.DOOR_LOCATION[0]] = self.DOOR_VALUE_left_before
        floor[self.DOOR_LOCATION[1]] = self.DOOR_VALUE_right_before
        return floor

    def floorDemo_after(self, floor_shape):
        floor = np.zeros(floor_shape)
        # 设置墙的值
        floor[0:, 0] = self.WALL_VALUE
        floor[0:, -1] = self.WALL_VALUE
        floor[0, 0:] = self.WALL_VALUE
        floor[-1, 0:] = self.WALL_VALUE
        # floor[7,2]=self.WALL_VALUE
        # floor[3:4, 4:13] = self.WALL_VALUE
        floor[5:7, 7] = self.WALL_VALUE
        floor[7, 7:12] = self.WALL_VALUE
        floor[10, 5:8] = self.WALL_VALUE
        floor[10:13, 10] = self.WALL_VALUE
        # 设置门的值
        floor[self.DOOR_LOCATION[0]] = self.DOOR_VALUE_left_after
        floor[self.DOOR_LOCATION[1]] = self.DOOR_VALUE_right_after
        return floor


    def sign_rule(self, dis_demo, dis):
        floor = dis_demo
        for row in range(1, self.W - 1):
            for column in range(1, self.SIGN_LOCATION[0][1]):
                dis_value = dis[row, column]
                if dis_value <= self.DISTANCE_MIN:
                    floor[row, column] = 1
                elif self.DISTANCE_MIN < dis_value <= self.DISTANCE_MAX:
                    floor[row, column] = (self.DISTANCE_MAX - dis_value) / (self.DISTANCE_MAX - self.DISTANCE_MIN)
                else:
                    floor[row, column] = 0
            for column in range(self.SIGN_LOCATION[0][1], self.L - 1):
                dis_value = dis[row, column]
                if dis_value <= self.DISTANCE_MIN:
                    floor[row, column] = 1
                elif self.DISTANCE_MIN < dis_value <= self.DISTANCE_MAX:
                    floor[row, column] = (self.DISTANCE_MAX - dis_value) / (self.DISTANCE_MAX - self.DISTANCE_MIN)
                else:
                    floor[row, column] = 0
        return floor


    def rule_right(self, floor, row, column):
        # floor场地矩阵，row为行，column为列
        cell = floor[row, column]  # 当前的单元格
        cell_right = cell + 1  # 右单元格
        cell_up = cell + 1  # 上单元格
        cell_down = cell + 1  # 下单元格
        cell_RU = cell + 1.5  # 右上角单元格
        cell_RD = cell + 1.5  # 右下角单元格
        # 设置上单元格
        if (floor[row - 1, column] != 500) and (floor[row - 1, column] != 1):  # 上单元格不为墙和门
            # 当然，由于门的设计，所以在floor[row, column] != 500的条件下，如果没有and及后面的条件，这个实验也同样成立
            if floor[row - 1, column] == 0:  # 上单元格目前为空
                floor[row - 1, column] = cell_up
            else:  # 上单元格已被填充
                if floor[row - 1, column] > cell_up:
                    floor[row - 1, column] = cell_up
        # 设置下单元格
        if (floor[row + 1, column] != 500) and (floor[row + 1, column] != 1):  # 下单元格不为墙和门
            if floor[row + 1, column] == 0:  # 下单元格目前为空
                floor[row + 1, column] = cell_down
            else:  # 下单元格已被填充
                if floor[row + 1, column] > cell_down:
                    floor[row + 1, column] = cell_down
        # 设置右单元格
        if (floor[row, column - 1] != 500) and (floor[row, column - 1] != 1):  # 右单元格不为墙和门
            if floor[row, column - 1] == 0:  # 右单元格目前为空
                floor[row, column - 1] = cell_right
            else:  # 右单元格已被填充
                if floor[row, column - 1] > cell_right:
                    floor[row, column - 1] = cell_right

        # 设置右上角单元格
        if (floor[row - 1, column - 1] != 500) and (floor[row - 1, column - 1] != 1):  # 右上角单元格不为墙和门
            if floor[row - 1, column - 1] == 0:  # 右上角单元格目前为空
                floor[row - 1, column - 1] = cell_RU
            else:  # 右上角单元格已被填充
                if floor[row - 1, column - 1] > cell_RU:
                    floor[row - 1, column - 1] = cell_RU

        # 设置右下角单元格
        if (floor[row + 1, column - 1] != 500) and (floor[row + 1, column - 1] != 1):  # 右下角单元格不为墙和门
            if floor[row + 1, column - 1] == 0:  # 右下角单元格目前为空
                floor[row + 1, column - 1] = cell_RD
            else:  # 右下角单元格已被填充
                if floor[row + 1, column - 1] > cell_RD:
                    floor[row + 1, column - 1] = cell_RD
        return floor

    def rule_left(self, floor, row, column):
        # floor场地矩阵，row为行，column为列
        cell = floor[row, column]  # 当前的单元格
        cell_left = cell + 1  # 左单元格
        cell_up = cell + 1  # 上单元格
        cell_down = cell + 1  # 下单元格
        cell_LU = cell + 1.5  # 左上角单元格
        cell_LD = cell + 1.5  # 左下角单元格
        # 设置上单元格
        if (floor[row - 1, column] != 500) and (floor[row - 1, column] != 1):  # 上单元格不为墙和门
            # 当然，由于门的设计，所以在floor[row, column] != 500的条件下，如果没有and及后面的条件，这个实验也同样成立
            if floor[row - 1, column] == 0:  # 上单元格目前为空
                floor[row - 1, column] = cell_up
            else:  # 上单元格已被填充
                if floor[row - 1, column] > cell_up:
                    floor[row - 1, column] = cell_up
        # 设置下单元格
        if (floor[row + 1, column] != 500) and (floor[row + 1, column] != 1):  # 下单元格不为墙和门
            if floor[row + 1, column] == 0:  # 下单元格目前为空
                floor[row + 1, column] = cell_down
            else:  # 下单元格已被填充
                if floor[row + 1, column] > cell_down:
                    floor[row + 1, column] = cell_down

        # 设置左单元格
        if (floor[row, column + 1] != 500) and (floor[row, column + 1] != 1):  # 左单元格不为墙和门
            if floor[row, column + 1] == 0:  # 左单元格目前为空
                floor[row, column + 1] = cell_left
            else:  # 左单元格已被填充
                if floor[row, column + 1] > cell_left:
                    floor[row, column + 1] = cell_left

        # 设置左上角单元格
        if (floor[row - 1, column + 1] != 500) and (floor[row - 1, column + 1] != 1):  # 左上角单元格不为墙和门
            if floor[row - 1, column + 1] == 0:  # 左上角单元格目前为空
                floor[row - 1, column + 1] = cell_LU
            else:  # 左上角单元格已被填充
                if floor[row - 1, column + 1] > cell_LU:
                    floor[row - 1, column + 1] = cell_LU

        # 设置左下角单元格
        if (floor[row + 1, column + 1] != 500) and (floor[row + 1, column + 1] != 1):  # 左下角单元格不为墙和门
            if floor[row + 1, column + 1] == 0:  # 左下角单元格目前为空
                floor[row + 1, column + 1] = cell_LD
            else:  # 左下角单元格已被填充
                if floor[row + 1, column + 1] > cell_LD:
                    floor[row + 1, column + 1] = cell_LD
        return floor

    def create_floor(self, floor_demo):
        floor = floor_demo.copy()
        # 从房间左上角开始遍历一遍房间，更新没有获取到值的方格
        while np.any(floor == 0):
            for row in range(1, floor.shape[0]):
                for column in range(1, floor.shape[1] - 1):
                    if (floor[row, column] != 500) and (floor[row, column] != 0):
                        floor = self.rule_left(floor, row, column)
                        floor[row, column] = floor[row, column]
                    else:
                        continue
        return floor

    def creat_fig_room(self, floor):
        cmap = mpl.colors.ListedColormap(['#F5F5F5', 'green', '#696969'])
        # # 设置标志的值
        # floor[SIGN_LOCATION[0]] = SIGN_VALUE
        plt.imshow(floor, cmap=cmap)
        for i in range(-1, self.L - 1):
            x = [i + 0.5, i + 0.5]
            y = [-0.5, self.W - 1 + 0.5]
            plt.plot(x, y, '-k', linewidth=0.5)
        for j in range(-1, self.W - 1):
            x = [-0.5, self.L - 1 + 0.5]
            y = [j + 0.5, j + 0.5]
            plt.plot(x, y, '-k', linewidth=0.5)

    # 生成行人布局
    def init_peo(self, floor):
        # 生成与房间等大的矩阵，用于表示每个cell的状态
        peo_room = np.zeros((self.W, self.L))
        # 随机生成行人
        list_cell = []
        # random.seed(SEED)  # 固定随机数
        list_peo = random.sample(list_cell, self.PEO_NUM)
        for peo in list_peo:
            peo_room[peo[0], peo[1]] = 1
        # print(peo_room)
        return peo_room

    # 绘制行人
    def plt_peo(self, peo_room):
        for (j, i), value in np.ndenumerate(peo_room):
            if value == 1:
                # plt.plot(i, j, 'og', markersize=6)
                plt.plot(i, j, 'ob', markersize=6)

    # rule1：行人下一步为八个方向floor_value值最小的cell，若存在两个最小值，50%
    def rule1(self, j, i, floor, peo_room):
        # cell八个方向的值，如果比本cell值小，且没有人，则为可跳转对象
        near_cell = {}
        if i == 0:  # 在门口   #i为列值
            return (j, -1)
        elif i == self.L - 1:
            return (j, self.L)
        else:  # 不在门口
            # 左上
            if (peo_room[j - 1, i - 1] == 0) and (floor[j - 1, i - 1] != 500) and (floor[j - 1, i - 1] < floor[j, i]):
                near_cell[(j - 1, i - 1)] = floor[j - 1, i - 1]
            # 上
            if (peo_room[j - 1, i] == 0) and (floor[j - 1, i] != 500) and (floor[j - 1, i] < floor[j, i]):
                near_cell[(j - 1, i)] = floor[j - 1, i]
            # 右上
            if (peo_room[j - 1, i + 1] == 0) and (floor[j - 1, i + 1] != 500) and (floor[j - 1, i + 1] < floor[j, i]):
                near_cell[(j - 1, i + 1)] = floor[j - 1, i + 1]
            # 左
            if (peo_room[j, i - 1] == 0) and (floor[j, i - 1] != 500) and (floor[j, i - 1] < floor[j, i]):
                near_cell[(j, i - 1)] = floor[j, i - 1]
            # 右
            if (peo_room[j, i + 1] == 0) and (floor[j, i + 1] != 500) and (floor[j, i + 1] < floor[j, i]):
                near_cell[(j, i + 1)] = floor[j, i + 1]
            # 左下
            if (peo_room[j + 1, i - 1] == 0) and (floor[j + 1, i - 1] != 500) and (floor[j + 1, i - 1] < floor[j, i]):
                near_cell[(j + 1, i - 1)] = floor[j + 1, i - 1]
            # 下
            if (peo_room[j + 1, i] == 0) and (floor[j + 1, i] != 500) and (floor[j + 1, i] < floor[j, i]):
                near_cell[(j + 1, i)] = floor[j + 1, i]
            # 右下
            if (peo_room[j + 1, i + 1] == 0) and (floor[j + 1, i + 1] != 500) and (floor[j + 1, i + 1] < floor[j, i]):
                near_cell[(j + 1, i + 1)] = floor[j + 1, i + 1]
            # 八个方向中的最小值
            if len(near_cell) != 0:
                min_value = min(near_cell.values())
                # print(min_value)
                # 最小值的坐标
                min_pos_list = []
                for k, v in near_cell.items():
                    # k是坐标，v是值
                    if v == min_value:
                        min_pos_list.append(k)
            else:
                return (j, i)


    # rule3:行人是否收到惊吓（5%可能）
    def rule3(self):
        feel_list = ['stop', 'go']
        feel = np.random.choice(feel_list, 1, p=[0.05, 0.95])
        return feel[0]

    # 行人运动规则
    def peo_rule(self, floor, peo_room, peo_left, peo_right):
        peo_room_next = np.zeros((self.W, self.L))  # 下一步行人分布数据
        # 所有行人坐标
        peo_list = []
        for (j, i), value in np.ndenumerate(peo_room):
            if value == 1:
                peo_list.append((j, i))
        return peo_room_next, peo_left, peo_right

    def run_time1(self, n):
        i = 0
        list_all = []
        list_step = ["step"]
        list_peo_left = ["peo_left"]
        list_peo_right = ["peo_right"]
        while i < n:
            floor_shape = (self.W, self.L)
            floor_demo_before = self.floorDemo_before(floor_shape)
            floor_demo_after = self.floorDemo_after(floor_shape)
            print('-------------------------------------------')
            dis_demo1 = np.zeros((self.W, self.L))
            dis_demo2 = np.zeros((self.W, self.L))
            floor2 = self.create_floor(floor_demo_before)
            floor3 = self.create_floor(floor_demo_after)
            floor = np.round((floor3 - floor2) + floor2, 2)
            peo_room = self.init_peo(floor)
            step = 0
            num = self.PEO_NUM
            peo_left = 0
            peo_right = 0
            while num > 0:
                peo_room, num, peo_left, peo_right = self.peo_rule(floor, peo_room, peo_left, peo_right)
                step = step + 1
                # while end
            list_step.append(step)
            list_peo_left.append(peo_left)
            list_peo_right.append(peo_right)
            i = i + 1
            # while  end
        list_all.append(list_step)
        list_all.append(list_peo_left)
        list_all.append(list_peo_right)
        data = pd.DataFrame(list_all)
        data.to_excel('./floor1/floor1_50_1.xlsx', index=False)
        data = data.T
        # 行列倒置
        return list_all

    def run_time2(self):
        floor_shape = (self.W, self.L)
        floor_demo_before = self.floorDemo_before(floor_shape)
        floor_demo_after = self.floorDemo_after(floor_shape)
        print('-------------------------------------------')
        dis_demo1 = np.zeros((self.W, self.L))
        dis_demo2 = np.zeros((self.W, self.L))
        floor2 = self.create_floor(floor_demo_before)
        floor3 = self.create_floor(floor_demo_after)
        floor = np.round((floor3 - floor2) + floor2, 2)
        data = pd.DataFrame(floor)
        data.to_excel('./floor2/floor1_50_1.xlsx', index=False)
        self.creat_fig_room(floor)
        peo_room = self.init_peo(floor)
        step = 0
        num = self.PEO_NUM
        peo_left = 0
        peo_right = 0
        return floor

    def run_time3(self):
        list_all = []
        list_step = ["步数"]
        list_peo_left = ["人数（左）"]
        list_peo_right = ["人数（右）"]
        floor_shape = (self.W, self.L)
        floor_demo_before = self.floorDemo_before(floor_shape)
        floor_demo_after = self.floorDemo_after(floor_shape)
        print('-------------------------------------------')
        dis_demo1 = np.zeros((self.W, self.L))
        dis_demo2 = np.zeros((self.W, self.L))
        floor2 = self.create_floor(floor_demo_before)
        floor3 = self.create_floor(floor_demo_after)
        floor = np.round((floor3 - floor2) + floor2 , 2)
        return floor


if __name__ == '__main__':
    # 房间
    L = 20
    W = 16
    # 人员分布
    peo_left = 6
    peo_right = 17
    peo_up = 0
    peo_down = 15
    # 人数
    peo_number = 50
    # 门的坐标
    left_location = 7
    right_location = 7
    # 标志位置
    sign_location = 9
    # 参数
    left_parameter = 1
    right_parameter = 10
    fai = 1
    # 次数
    a = 1
    con1 = fun1(L, W, peo_left, peo_right, peo_up, peo_down, peo_number, left_location, right_location,
                sign_location, left_parameter, right_parameter, fai)
    con1.run_time1(a)
    con1.run_time2()
    con1.run_time3()
