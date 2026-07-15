function [kernel] = make_kernel(f)
% 生成NLM相似度量的高斯权重核
%   kernel = make_kernel(f)
%
% 输入: f - 相似窗口半径
% 输出: (2f+1) x (2f+1) 高斯核矩阵

    kernel = zeros(2*f+1, 2*f+1);
    for d = 1:f
        value = 1 / (2*d+1)^2;
        for i = -d:d
            for j = -d:d
                kernel(f+1-i, f+1-j) = kernel(f+1-i, f+1-j) + value;
            end%
        end%
    end%
    kernel = kernel ./ f;
end%
