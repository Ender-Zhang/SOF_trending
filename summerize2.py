import os
import glob
from transformers import pipeline

# 初始化摘要模型
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 指定要读取txt文件的文件夹路径
input_folder = 'data/content/'
# 指定保存摘要的文件夹路径
output_folder = 'data/summaries/'

# 创建输出文件夹，如果不存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取文件夹中所有的txt文件
txt_files = glob.glob(input_folder + '*.txt')

# 循环处理每个文件
for file_path in txt_files:
    with open(file_path, 'r') as file:
        content = file.read()
    
    # 生成摘要
    summary = summarizer(content, max_length=130, min_length=30, do_sample=False)
    summary_text = summary[0]['summary_text']

    # 获取原始文件名，并构建新的输出文件路径
    filename = os.path.basename(file_path)
    output_path = os.path.join(output_folder, 'summary_' + filename)

    # 将摘要写入新文件
    with open(output_path, 'w') as output_file:
        output_file.write(summary_text)

print("Summaries are generated and saved.")