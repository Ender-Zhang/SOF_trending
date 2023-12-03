import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import glob

# 指定包含总结文件的文件夹路径
summary_folder = 'data/summaries/'

# 读取所有txt文件的内容，并生成文件名列表和对应的嵌入向量
file_names = []
summaries = []
for file_path in glob.glob(summary_folder + '*.txt'):
    with open(file_path, 'r') as file:
        summaries.append(file.read())
        file_names.append(os.path.basename(file_path))

# 加载模型
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# 生成嵌入向量
embeddings = model.encode(summaries)

# 设置一个相似度阈值
similarity_threshold = 0.3

# 初始化用于保存相似文件组的大列表
similar_files_groups = []

# 计算相似度矩阵
similarity_matrix = cosine_similarity(embeddings)

# 标记已访问的文件
visited = set()

# 根据相似度阈值分组文件
for i in range(len(file_names)):
    if i not in visited:
        similar_indices = [j for j, value in enumerate(similarity_matrix[i]) if value > similarity_threshold and j != i]
        if similar_indices:
            group = [file_names[i]] + [file_names[j] for j in similar_indices]
            similar_files_groups.append(group)
            visited.add(i)
            visited.update(similar_indices)

# 将相似文件组保存到JSON文件
with open('similar_files_groups.json', 'w', encoding='utf-8') as f:
    json.dump(similar_files_groups, f, ensure_ascii=False, indent=4)

print("相似文件组已保存到 'similar_files_groups.json'.")
