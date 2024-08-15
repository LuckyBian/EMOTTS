import os

# 指定文件夹路径
folder_wav = '/aifs4su/data/weizhen/data/emo/wavs'
folder_txt1 = '/aifs4su/data/weizhen/data/emo/text'
folder_txt2 = '/aifs4su/data/weizhen/data/emo/emo'
output_file = '/home/weizhenbian/vits_emo/filelists/all.txt'

# 创建输出文件并准备写入
with open(output_file, 'w', encoding='utf-8') as f_out:
    # 遍历包含 WAV 文件的文件夹
    for filename in os.listdir(folder_wav):
        if filename.endswith('.wav'):
            # 构建每个文件的完整路径
            wav_path = os.path.join(folder_wav, filename)
            txt1_path = os.path.join(folder_txt1, filename.replace('.wav', '.txt'))
            txt2_path = os.path.join(folder_txt2, filename.replace('.wav', '.txt'))

            # 检查文件是否存在
            if not os.path.exists(txt1_path):
                print(f"文件不存在: {txt1_path}")
            else:
                print(f"文件存在: {txt1_path}")

            
            # 读取对应的 TXT 文件内容
            with open(txt1_path, 'r', encoding='utf-8') as f_txt1, \
                 open(txt2_path, 'r', encoding='utf-8') as f_txt2:
                txt1_content = f_txt1.read().strip()
                txt2_content = f_txt2.read().strip()
                
            # 写入整理后的数据到输出文件
            f_out.write(f"{wav_path}|{txt1_content}|{txt2_content}\n")
