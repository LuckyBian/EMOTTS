import os

def remove_non_wav_files(directory):
    # 遍历指定目录的所有文件
    for file in os.listdir(directory):
        # 检查文件扩展名是否不是 .wav
        if not file.endswith('.wav'):
            # 构建完整的文件路径
            file_path = os.path.join(directory, file)
            # 如果是文件，则删除
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file}")

# Replace 'path_to_directory' with the path to your directory
remove_non_wav_files('/aifs4su/data/weizhen/data/zh-en-yue/all/wavs')
