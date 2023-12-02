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

import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# 设置 k 的值
k = 2  # k 的选择取决于您的数据集和 DBSCAN 参数

# 使用 NearestNeighbors 计算每个点的第 k 近邻
neigh = NearestNeighbors(n_neighbors=k)
nbrs = neigh.fit(embeddings)
distances, indices = nbrs.kneighbors(embeddings)

# 对距离进行排序并绘制 k-距离图
sorted_distances = np.sort(distances[:, k-1], axis=0)
plt.plot(sorted_distances)
plt.xlabel("Points sorted by distance to k-th nearest neighbor")
plt.ylabel("k-th nearest neighbor distance")
plt.title(f"k-Distance Graph (k={k})")
plt.show()
