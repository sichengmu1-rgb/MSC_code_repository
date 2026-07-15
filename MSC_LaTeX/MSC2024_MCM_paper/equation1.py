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

K = 3000 #种群容量

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

# 模拟过程
for t in range(N - 1):
    M[t + 1] = M[t] + (r_M * M[t] * (1 - M[t] / K ) - m_M * M[t] + b_M * a * P[t] * M[t]) * dt
    F[t + 1] = F[t] + (r_F * F[t] * (1 - F[t] / K ) - m_F * F[t] + b_F * a * P[t] * F[t]) * dt
    P[t + 1] = P[t] + (r_P * P[t] * (1 - P[t] / K ) - a * P[t] * (M[t] + F[t])) * dt

# 绘制图形
time = np.linspace(0, T, N)
plt.figure(figsize=(12, 6))
plt.fill_between(time, M, color='blue', alpha=0.3, label='Male Sea Lampreys')
plt.fill_between(time, F, color='red', alpha=0.3, label='Female Sea Lampreys')
plt.fill_between(time, P, color='grey', alpha=0.3, label='Prey')
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Structured Population Model Simulation')
plt.legend()
plt.show()
