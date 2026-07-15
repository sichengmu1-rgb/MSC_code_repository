function [output] = NLmeansfilter(input, t, f, h)
% 标准NLM（非局部均值）图像去噪函数
%
% 输入:
%   input - 输入图像 (2D灰度图, double类型)
%   t      - 搜索窗口半径 (窗口大小 = 2*t+1)
%   f      - 相似窗口半径 (块大小 = 2*f+1)
%   h      - 平滑参数
%
% 输出:
%   output - 去噪后图像

    % 输入处理
    if ndims(input) == 3, input = input(:, :, 1); end
    if ~isa(input, 'double'), input = double(input); end
    t = round(t); f = round(f);
    if t < 1 || f < 1, error('t 和 f 必须 >= 1'); end
    if h <= 0, error('h 必须 > 0'); end

    [m, n] = size(input);
    output = zeros(m, n);
    input2 = padarray(input, [f f], 'symmetric');
    kernel = make_kernel(f);
    kernel = kernel / sum(sum(kernel));

    % 并行加速 (如果可用)
    has_parfor = license('test', 'Distrib_Computing_Toolbox');
    if has_parfor
        parfor i = 1:m
            for j = 1:n
                output(i, j) = nlm_pixel(i, j, input2, m, n, f, t, kernel, h);
            end%
        end%
    else
        for i = 1:m
            for j = 1:n
                output(i, j) = nlm_pixel(i, j, input2, m, n, f, t, kernel, h);
            end%
        end%
    end%
end%

function pixel_val = nlm_pixel(i, j, input2, m, n, f, t, kernel, h)
    i1 = i + f; j1 = j + f;
    W1 = input2(i1-f:i1+f, j1-f:j1+f);

    wmax = 0; average = 0; sweight = 0;

    rmin = max(i1-t, f+1);
    rmax = min(i1+t, m+f);
    smin = max(j1-t, f+1);
    smax = min(j1+t, n+f);

    for r = rmin:1:rmax
        for s = smin:1:smax
            if(r == i1 && s == j1), continue; end%
            W2 = input2(r-f:r+f, s-f:s+f);
            d = sum(sum(kernel .* (W1-W2) .* (W1-W2)));
            w = exp(-d / h^2);
            if w > wmax, wmax = w; end%
            sweight = sweight + w;
            average = average + w * input2(r, s);
        end%
    end%

    average = average + wmax * input2(i1, j1);
    sweight = sweight + wmax;

    if sweight > 0
        pixel_val = average / sweight;
    else
        pixel_val = input(i, j);
    end%
end%
