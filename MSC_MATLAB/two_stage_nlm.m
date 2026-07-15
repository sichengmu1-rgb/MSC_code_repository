function [I_out, I_stage1, info] = two_stage_nlm(I_noisy, sigma, params)
% 基于小波变换的两阶段NLM图像去噪算法
%
% 输入:
%   I_noisy  - 含噪图像 (double, 2D灰度图)
%   sigma    - 噪声标准差
%   params   - 参数结构体 (可选)
%
% 输出:
%   I_out    - 最终去噪图像
%   I_stage1 - 第一阶段去噪结果
%   info     - 中间结果结构体
%
% 使用示例:
%   params.k_low = 1.0;   % 低频平滑参数
%   params.k_high = 0.7;  % 高频平滑参数
%   params.k_final = 0.5; % 第二阶段参数
%   [I_out, ~, ~] = two_stage_nlm(I_noisy, 25, params);

    if nargin < 3, params = struct(); end

    % 默认参数
    p.wavelet    = get_param(params, 'wavelet',    'sym4');
    p.t1         = get_param(params, 't1',         10);
    p.f1         = get_param(params, 'f1',         2);
    p.t2         = get_param(params, 't2',         3);
    p.f2         = get_param(params, 'f2',         2);
    p.k_low      = get_param(params, 'k_low',      1.2);
    p.k_high     = get_param(params, 'k_high',     0.8);
    p.k_final    = get_param(params, 'k_final',    0.5);
    p.fusion     = get_param(params, 'fusion',     'sum');
    p.use_stage2 = get_param(params, 'use_stage2', true);
    p.h_mode     = get_param(params, 'h_mode',     'paper');

    % 计算平滑参数h
    if strcmpi(p.h_mode, 'code')
        h_low   = sqrt(sigma) * p.k_low;
        h_high  = sqrt(sigma) * p.k_high;
        h_final = sigma * p.k_final;
    else % paper mode
        h_low   = sigma * p.k_low;
        h_high  = sigma * p.k_high;
        h_final = sigma * p.k_final;
    end

    % 确保图像尺寸为偶数
    [M, N] = size(I_noisy);
    if mod(M, 2) ~= 0, I_noisy = I_noisy(1:end-1, :); end
    if mod(N, 2) ~= 0, I_noisy = I_noisy(:, 1:end-1); end

    % ===== 第一阶段: 小波域分带去噪 =====
    [C, S] = wavedec2(I_noisy, 1, p.wavelet);

    % 重构各子带
    A = wrcoef2('a', C, S, p.wavelet, 1);
    H = wrcoef2('h', C, S, p.wavelet, 1);
    V = wrcoef2('v', C, S, p.wavelet, 1);
    D = wrcoef2('d', C, S, p.wavelet, 1);

    % 高频融合
    if strcmpi(p.fusion, 'max')
        [HVD, direction_map] = fuse_high_max(H, V, D);
        HVD_den = NLmeansfilter(HVD, p.t1, p.f1, h_high);
        [H_den, V_den, D_den] = backfill_high(HVD_den, direction_map);
    else % sum
        HVD = H + V + D;
        HVD_den = NLmeansfilter(HVD, p.t1, p.f1, h_high);
        H_den = HVD_den / 3;
        V_den = HVD_den / 3;
        D_den = HVD_den / 3;
    end

    % 低频去噪
    A_den = NLmeansfilter(A, p.t1, p.f1, h_low);

    % 重构
    I_stage1 = A_den + H_den + V_den + D_den;
    I_stage1 = max(min(I_stage1, 255), 0);

    % ===== 第二阶段: 空间域精细去噪 =====
    if p.use_stage2
        I_out = NLmeansfilter(I_stage1, p.t2, p.f2, h_final);
        I_out = max(min(I_out, 255), 0);
    else
        I_out = I_stage1;
    end

    % 收集中间信息
    info.A = A;        info.H = H;
    info.V = V;        info.D = D;
    info.HVD = HVD;    info.A_den = A_den;
    info.HVD_den = HVD_den;
    info.I_stage1 = I_stage1;
    info.params = p;
    info.h_low = h_low;
    info.h_high = h_high;
    info.h_final = h_final;

end%

% ===== 辅助函数 =====
function val = get_param(params, field, default)
    if isfield(params, field) && ~isempty(params.(field))
        val = params.(field);
    else
        val = default;
    end%
end%

function [HVD, direction_map] = fuse_high_max(H, V, D)
    absH = abs(H); absV = abs(V); absD = abs(D);
    [~, direction_map] = max(cat(3, absH, absV, absD), [], 3);
    HVD = H;
    HVD(direction_map == 2) = V(direction_map == 2);
    HVD(direction_map == 3) = D(direction_map == 3);
end%

function [H_den, V_den, D_den] = backfill_high(HVD_den, direction_map)
    H_den = zeros(size(HVD_den));
    V_den = zeros(size(HVD_den));
    D_den = zeros(size(HVD_den));
    H_den(direction_map == 1) = HVD_den(direction_map == 1);
    V_den(direction_map == 2) = HVD_den(direction_map == 2);
    D_den(direction_map == 3) = HVD_den(direction_map == 3);
end%
