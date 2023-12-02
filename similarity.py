import os
import glob

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
        if similarity > similarity_threshold:
            print(f"文件 {file_names[i]} 和 文件 {file_names[j]} 的相似度为: {similarity}")
