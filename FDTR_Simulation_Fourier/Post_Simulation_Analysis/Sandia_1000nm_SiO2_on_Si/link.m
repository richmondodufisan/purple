function [ data ] = link( data )
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
threshold  = 100;
for i = 2:length(data)
    if data(i) - data(i-1) > threshold
        data(i:end) = data(i:end) - 360;
    elseif data(i) - data(i-1) < - threshold
        data(i:end) = data(i:end) + 360;
    end
end
end

