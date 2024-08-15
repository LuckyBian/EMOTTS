import numpy as np
import os

def scale_and_map_npy(file_path, min_val=0, max_val=238):
    # 加载 .npy 文件
    data = np.load(file_path)
    
    # 获取原始数据的最小值和最大值
    original_min = np.min(data)
    original_max = np.max(data)
    
    # 映射数据到新的范围 [min_val, max_val]
    scaled_data = (data - original_min) / (original_max - original_min) * (max_val - min_val) + min_val
    
    # 将数据四舍五入为最接近的整数
    mapped_data = np.rint(scaled_data).astype(int)
    
    # 覆盖保存文件
    np.save(file_path, mapped_data)

# 指定包含 .npy 文件的文件夹路径
folder_path = '/aifs4su/data/weizhen/data/emo/spk'

# 遍历文件夹中所有的 .npy 文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.npy'):
        file_path = os.path.join(folder_path, file_name)
        scale_and_map_npy(file_path)
        print(f"Processed and updated {file_path}")
