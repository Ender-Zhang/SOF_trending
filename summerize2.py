import os
import glob
from transformers import pipeline

# 初始化摘要模型
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 指定文件夹路径
input_folder = 'data/content/'
output_folder = 'data/summaries/'

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取所有txt文件
txt_files = glob.glob(input_folder + '*.txt')

# 处理每个文件
for file_path in txt_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 截断文本以符合模型的最大长度限制（1024 tokens）
    truncated_content = content[:1024]  # 这里需要适当调整以确保正确的截断

    # 动态设置max_length
    max_length = min(130, len(truncated_content) // 2)

    # 生成摘要
    summary = summarizer(truncated_content, max_length=max_length, min_length=30, do_sample=False)
    summary_text = summary[0]['summary_text']

    # 保存摘要
    filename = os.path.basename(file_path)
    output_path = os.path.join(output_folder, 'summary_' + filename)
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(summary_text)

print("摘要生成并保存完毕。")
