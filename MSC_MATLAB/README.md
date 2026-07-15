# 基于小波变换的两阶段NLM图像去噪算法

毕业设计核心算法代码 - 2026年

## 算法简介

本算法结合小波变换的多尺度分解特性与两阶段滤波思想，提出一种改进的非局部均值（NLM）图像去噪方法。

**核心步骤：**
1. 对含噪图像进行单层小波分解，得到低频子带和高频子带
2. 将三个高频子带融合为统一高频分量
3. 对低频和高频分别执行NLM去噪（使用不同平滑参数）
4. 小波逆变换重构得到第一阶段结果
5. 对第一阶段结果执行第二阶段精细去噪

## 文件列表

| 文件 | 说明 |
|:-----|:-----|
| `two_stage_nlm.m` | 核心算法：两阶段NLM去噪 |
| `NLmeansfilter.m` | 标准NLM滤波函数 |
| `make_kernel.m` | 高斯核生成函数 |
| `demo.m` | 使用示例脚本 |
| `README.md` | 本说明文档 |

## 使用方法

### 最简单：运行demo脚本

```matlab
% 直接运行demo.m即可看到去噪效果对比
demo
```

### 在代码中使用算法

```matlab
% 1. 读取图像并添加噪声
I = imread('your_image.png');
I = rgb2gray(I);  % 转为灰度
I(I);
sigma = 25;  % 噪声标准差
I_noisy = double(I) + sigma * randn(size(I));

% 2. 设置算法参数
params.wavelet = 'sym4';  % 小波基
params.t1 = 10;  % 第一阶段搜索窗半径
params.f1 = 2;   % 第一阶段相似窗半径
params.t2 = 3;   % 第二阶段搜索窗半径
params.f2 = 2;   % 第二阶段相似窗半径
params.k_low = 1.0;   % 低频平滑参数
params.k_high = 0.7;  % 高频平滑参数
params.k_final = 0.5; % 第二阶段平滑参数
params.fusion = 'sum';  % 高频融合方式
params.h_mode = 'paper'; % h计算模式
params.use_stage2 = true; % 是否启用第二阶段

% 3. 调用算法
[I_denoised, I_stage1, info] = two_stage_nlm(I_noisy, sigma, params);

% 4. 保存结果
imwrite(uint8(I_denoised), 'result.png');
```

## 参数说明

| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| `sigma` | 25 | 噪声标准差 |
| `params.k_low` | 1.0 | 低频去噪强度（越大去噪越强） |
| `params.k_high` | 0.7 | 高频去噪强度（越小保留细节越多） |
| `params.k_final` | 0.5 | 第二阶段精细去噪强度 |
| `params.use_stage2` | ` 是否启用第二阶段 |

## 依赖要求

- MATLAB（推荐R2018b或更高版本）
- Wavelet Toolbox（小波工具箱）
- Image Processing Toolbox（可选，用于图像读写）

---
*毕业设计 2026*
