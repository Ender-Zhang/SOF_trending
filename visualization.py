from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import os

# 读取 JSON 文件来获取文件组
with open('similar_files_groups.json', 'r') as file:
    file_groups = json.load(file)

summary_folder = 'data/summaries/'  # 假设所有文本文件都在这个文件夹中

# 为每个文件组生成词云
for group in file_groups:
    group_text = ''
    for file_name in group:
        # 构造每个文件的完整路径
        file_path = os.path.join(summary_folder, file_name)
        # 读取文件内容
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                group_text += ' ' + content  # 将所有文件的内容合并

    # 生成词云
    wordcloud = WordCloud(width=800, height=400).generate(group_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
