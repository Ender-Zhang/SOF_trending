import json
from sklearn.metrics.pairwise import cosine_similarity

import os
import glob
from sklearn.cluster import DBSCAN
import numpy as np

# 指定包含总结文件的文件夹路径
summary_folder = 'data/summaries/'

# 读取所有txt文件的内容
summaries = []
file_names = []
for file_path in glob.glob(summary_folder + '*.txt'):
    with open(file_path, 'r') as file:
        summaries.append(file.read())
        file_names.append(os.path.basename(file_path))


from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 加载模型
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# 生成嵌入向量
embeddings = model.encode(summaries)

similarity_threshold = 0.4  # 设置一个相似度阈值

for i in range(len(embeddings)):
    for j in range(i+1, len(embeddings)):
        similarity = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
        # print(f"文件 {file_names[i]} 和 文件 {file_names[j]} 的相似度为: {similarity}")
        # if similarity > similarity_threshold:
            # print(f"文件 {file_names[i]} 和 文件 {file_names[j]} 的相似度为: {similarity}")

# 计算余弦相似度矩阵
cos_sim_matrix = cosine_similarity(embeddings)

# 计算距离矩阵
distance_matrix = 1 - cos_sim_matrix

# 确保距离矩阵中没有负值
distance_matrix[distance_matrix < 0] = 0

# 应用DBSCAN算法
db = DBSCAN(eps=0.8, min_samples=2, metric="precomputed").fit(distance_matrix)
labels = db.labels_


# 将文件分组，确保将 NumPy 数据类型转换为 Python 数据类型
groups = {}
for file, cluster in zip(file_names, labels):
    if cluster == -1:
        continue  # -1 表示噪声点
    # 转换 NumPy int64 类型为 Python int 类型
    cluster = int(cluster)
    if cluster not in groups:
        groups[cluster] = []
    groups[cluster].append(file)

# 将分组结果写入 JSON 文件
with open('file_groups.json', 'w') as outfile:
    json.dump(groups, outfile, indent=4)



