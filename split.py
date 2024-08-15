import os
import random

def split_data(input_path, output_folder, train_ratio, valid_ratio):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 读取所有数据
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 打乱数据顺序
    random.shuffle(lines)
    
    # 计算分割点
    total_count = len(lines)
    train_count = int(total_count * train_ratio)
    valid_count = int(total_count * valid_ratio)
    
    # 分割数据
    train_data = lines[:train_count]
    valid_data = lines[train_count:train_count + valid_count]
    test_data = lines[train_count + valid_count:]
    
    # 写入数据到文件
    with open(os.path.join(output_folder, 'train.txt'), 'w', encoding='utf-8') as file:
        file.writelines(train_data)
    with open(os.path.join(output_folder, 'valid.txt'), 'w', encoding='utf-8') as file:
        file.writelines(valid_data)
    with open(os.path.join(output_folder, 'test.txt'), 'w', encoding='utf-8') as file:
        file.writelines(test_data)

# 使用示例
input_file_path = '/home/weizhenbian/vits_emo/filelists/all.txt' # 原始数据文件路径
output_directory = '/home/weizhenbian/vits_emo/filelists' # 输出文件夹路径
train_ratio = 0.8
valid_ratio = 0.19

split_data(input_file_path, output_directory, train_ratio, valid_ratio)
