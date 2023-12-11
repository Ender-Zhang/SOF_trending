import os
import shutil
import re

# Regular expression pattern and replacement format
pattern = r"(\d+)_(\w+)\$(\w+)_questions_(\d+)_([a-zA-Z0-9-]+)"
replacement = r"https://\2.\3/questions/\4/\5"

def read_and_merge_directories(source_dirs, target_dir):
    # 确保目标文件夹存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    file_id = 1
    for source_dir in source_dirs:
        for filename in os.listdir(source_dir):
            # 检查是否为文件
            if os.path.isfile(os.path.join(source_dir, filename)):
                # 生成新的文件名
                new_filename = re.sub(r'\d+_stackoverflow', f'{file_id}_', filename)
                # new_filename = re.sub(pattern, replacement, filename)
                # 拷贝文件到目标文件夹
                shutil.copyfile(os.path.join(source_dir, filename), os.path.join(target_dir, new_filename))
                file_id += 1

# 定义源文件夹和目标文件夹
source_dirs = ['data/html1', 'data/html2','data/html3',"data/html4","data/html5"]
target_dir = 'data/html_all_raw'

# 执行合并操作
read_and_merge_directories(source_dirs, target_dir)
print('Finished merging files')