import subprocess

# 读取文件内容
with open('env.txt', 'r') as file:
    lines = file.readlines()

# 遍历每一行，提取包名和版本并安装
for line in lines:
    # 分割包名和版本号
    package, version = line.strip().split()
    # 生成安装命令
    install_command = f"pip install {package}=={version}"
    # 执行安装命令
    subprocess.run(install_command, shell=True)
