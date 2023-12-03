from sentence_transformers import SentenceTransformer
from datasketch import MinHash, MinHashLSH
import os
import glob

# 加载模型
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# 指定文件夹路径
summary_folder = 'data/summaries/'

# 读取文件并生成嵌入向量
file_names = []
embeddings = []
for file_path in glob.glob(summary_folder + '*.txt'):
    with open(file_path, 'r') as file:
        content = file.read()
        embeddings.append(model.encode(content, convert_to_tensor=True))
        file_names.append(os.path.basename(file_path))

# 创建LSH
lsh = MinHashLSH(threshold=0.1, num_perm=128)

# 创建MinHash对象
minhashes = {}
for i, emb in enumerate(embeddings):
    minhash = MinHash(num_perm=128)
    for d in emb.tolist():
        minhash.update(str(d).encode('utf8'))
    lsh.insert(file_names[i], minhash)
    minhashes[file_names[i]] = minhash

# 搜索相似项，并排除与自己相同的文件
for name, minhash in minhashes.items():
    similar_files = lsh.query(minhash)
    # # 确保要移除的文件名在列表中
    # if name in similar_files:
    #     similar_files.remove(name)  # 移除与自己相同的文件名
    # 检查剩余相似文件的数量，排除长度为0的情况
    # if len(similar_files) > 0:
    print(f"{name} 相似的文件: {similar_files}")
