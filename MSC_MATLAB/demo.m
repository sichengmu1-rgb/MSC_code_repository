%% demo.m - 两阶段NLM去噪算法演示
%  直接运行即可看到去噪效果对比
%
% 输出: 命令行显示PSNR指标, 弹出对比图像窗口

clc; close all;

fprintf('=== 两阶段NLM去噪演示 ===\n\n');

% 1. 准备测试图像
fprintf('[1/3] 准备测试图像...\n');
I_original = double(imread('low.tif'));

% 转为灰度
if size(I_original, 3) == 3
    I_original = rgb2gray(I_original) * 255;
elseif max(I_original(:)) <= 1
    I_original = I_original * 255;
end%
I_original = double(I_original);

% 2. 添加高斯噪声
sigma = 25;
rng(42);  % 固定随机种子
I_noisy = I_original + sigma * randn(size(I_original));

psnr_noisy = psnr_value(I_original, I_noisy);
fprintf('  噪声水平: sigma=%d, PSNR=%.2f dB\n', sigma, psnr_noisy);

% 3. 标准NLM去噪
fprintf('\n[2/3] 运行标准NLM...\n');
t1 = 10; f1 = 2;
h_nlm = sigma;

tic;
I_nlm = NLmeansfilter(I_noisy, t1, f1, h_nlm);
I_nlm = max(0, min(255, I_nlm));
t_nlm = toc;

psnr_nlm = psnr_value(I_original, I_nlm);
fprintf('  标准NLM: PSNR=%.2f dB, 耗时%.1fs\n', psnr_nlm, t_nlm);

% 4. 两阶段NLM去噪
fprintf('\n[3/3] 运行两阶段NLM...\n');

params.wavelet    = 'sym4';
params.t1         = 10;
params.f1         = 2;
params.t2         = 3;
params.f2         = 2;
params.k_low      = 1.0;
params.k_high     = 0.7;
params.k_final    = 0.5;
params.fusion     = 'sum';
params.h_mode     = 'paper';
params.use_stage2 = true;

tic;
[I_two, ~, ~] = two_stage_nlm(I_noisy, sigma, params);
t_two = toc;

psnr_two = psnr_value(I_original, I_two);
fprintf('  两阶段NLM: PSNR=%.2f dB, 耗时%.1fs\n', psnr_two, t_two);
fprintf('  性能提升: %+.2f dB\n\n', psnr_two - psnr_nlm);

% 显示结果
fprintf('===== 结果对比 =====\n');
fprintf('%-12s %10s %10s\n', '方法', 'PSNR(dB)', '提升');
fprintf('----------------------------------------\n');
fprintf('%-12s %10.2f %10s\n', '含噪图像', psnr_noisy, '-');
fprintf('%-12s %10.2f %10s\n', '标准NLM', psnr_nlm, '-');
fprintf('%-12s %10.2f %+10.2f\n', '两阶段NLM', psnr_two, psnr_two-psnr_nlm);
fprintf('===========================\n');

% 可视化
figure('Name', '去噪效果对比', 'Position', [100, 100, 1200, 300], 'Color', 'white');
subplot(1, 4, 1); imshow(I_original, [0 255]); title('原始图像', 'FontSize', 12);
subplot(1, 4, 2); imshow(I_noisy, [0 255]); title(sprintf('含噪 sigma=%d\nPSNR=%.2fdB', sigma, psnr_noisy), 'FontSize', 11);
subplot(1, 4, 3); imshow(I_nlm, [0 255]); title(sprintf('标准NLM\nPSNR=%.2fdB', psnr_nlm), 'FontSize', 11);
subplot(1, 4, 4); imshow(I_two, [0 255]); title(sprintf('两阶段NLM\nPSNR=%.2fdB (+%.1fdB)', psnr_two, psnr_two-psnr_nlm), 'FontSize', 11);
sgtitle('两阶段NLM去噪效果对比', 'FontSize', 14, 'FontWeight', 'bold');

fprintf('\n演示完成! 请查看对比图像窗口.\n');

% ===== 辅助函数: PSNR计算 =====
function v = psnr_value(ref, img)
    mse_val = mean((double(ref(:)) - double(img(:))).^2);
    if mse_val < 1e-10, v = 100;
    else, v = 10 * log10(255^2 / mse_val); end%
end%
