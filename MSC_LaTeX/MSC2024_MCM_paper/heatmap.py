import numpy as np
import matplotlib.pyplot as plt

# 参数设定
r_M = 0.04  # 雄性海七鳃鳗的繁殖率
m_M = 0.02  # 雄性海七鳃鳗的自然死亡率
b_M = 0.002  # 雄性海七鳃鳗的捕食效率

r_F = 0.03  # 雌性海七鳃鳗的繁殖率
m_F = 0.02  # 雌性海七鳃鳗的自然死亡率
b_F = 0.001  # 雌性海七鳃鳗的捕食效率

r_P = 0.1  # 猎物的自然增长率
a = 0.001  # 猎物被捕食的概率

# 初始条件
M0 = 50  # 雄性海七鳃鳗的初始种群数量
F0 = 50  # 雌性海七鳃鳗的初始种群数量
P0 = 300  # 猎物的初始种群数量

K = 3000 # 种群容量

# 时间设定
dt = 0.05  # 时间步长
T = 100  # 总模拟时间
N = int(T / dt)  # 总步数

# 初始化数组
M = np.zeros(N)
F = np.zeros(N)
P = np.zeros(N)
M[0] = M0
F[0] = F0
P[0] = P0

# 新增初始化数组
gender_ratio = np.zeros(N)  # 性别比例数组
prey_consumed = np.zeros(N)  # 每个时间点被捕食者的数量

# 模拟过程
for t in range(N - 1):
    M[t + 1] = M[t] + (r_M * M[t] * (1 - M[t] / K ) - m_M * M[t] + b_M * a * P[t] * M[t]) * dt
    F[t + 1] = F[t] + (r_F * F[t] * (1 - F[t] / K ) - m_F * F[t] + b_F * a * P[t] * F[t]) * dt
    P[t + 1] = P[t] + (r_P * P[t] * (1 - P[t] / K ) - a * P[t] * (M[t] + F[t])) * dt

# 计算性别比例和被捕食者数量
for t in range(N):
    gender_ratio[t] = M[t] / (M[t] + F[t]) if (M[t] + F[t]) > 0 else 0
    prey_consumed[t] = a * P[t] * (M[t] + F[t])

# 创建热力图数据矩阵
heatmap_data = np.vstack((gender_ratio, prey_consumed)).T

import numpy as np
import matplotlib.pyplot as plt

# ... (省略之前的模拟代码) ...

# 创建热力图数据矩阵
heatmap_data = np.vstack((gender_ratio, prey_consumed)).T

# 显示热力图
plt.figure(figsize=(12, 9))
im = plt.imshow(heatmap_data, aspect='auto', cmap='GnBu', extent=[0, 1, 0, T], interpolation='nearest')

# 添加颜色条
cbar = plt.colorbar(im, fraction=0.015, pad=0.04)
cbar.set_label('Scale', size=14, weight='bold', labelpad=10)
cbar.ax.tick_params(labelsize=12)

# 设置轴标签和标题
plt.xlabel('Variables (0=Gender Ratio, 1=Prey Consumed)', fontsize=14, weight='bold', labelpad=10)
plt.ylabel('Time', fontsize=14, weight='bold', labelpad=10)
plt.title('Heatmap of Gender Ratio and Prey Consumed over Time', fontsize=16, weight='bold', pad=20)

# 网格线已被注释掉，因此不会显示在热力图上
plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5, color='white', alpha=0.7)


# 设置轴刻度大小
plt.xticks(fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')

# 调整轴刻度的颜色和样式
ax = plt.gca()
ax.tick_params(axis='x', colors='darkblue', which='both', width=2)
ax.tick_params(axis='y', colors='darkblue', which='both', width=2)

# 显示图形
plt.show()

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

# ... (省略之前的模拟代码) ...

# 时间数组
time = np.arange(0, T, dt)

# 气泡大小缩放因子，需要根据数据具体调整以便于观察
size_factor = 100  # 调整这个因子来改变气泡的大小

# 气泡大小（使用被捕食者数量，并进行适当的缩放）
bubble_sizes = prey_consumed * size_factor

plt.figure(figsize=(12, 9))

# 绘制气泡图，使用蓝色色调的颜色映射 'Blues'
scatter = plt.scatter(time, gender_ratio, s=bubble_sizes, c=bubble_sizes, cmap='Blues', alpha=0.6, edgecolors='skyblue', linewidth=0.5)

# 添加颜色条
cbar = plt.colorbar(scatter)
cbar.set_label('Prey Consumed', size=14, weight='bold', labelpad=10)
cbar.ax.tick_params(labelsize=12)

# 设置轴标签和标题
plt.xlabel('Time', fontsize=14, weight='bold', labelpad=10)
plt.ylabel('Gender Ratio (Males/(Males+Females))', fontsize=14, weight='bold', labelpad=10)
plt.title('Bubble Plot of Gender Ratio vs. Time with Prey Consumed as Bubble Size', fontsize=16, weight='bold', pad=20)

# 设置背景颜色
plt.gca().set_facecolor('lightgrey')

# 设置网格线
plt.grid(True, which='both', axis='both', linestyle='-', color='white', linewidth=1, alpha=0.7)

# 显示图形
plt.show()

