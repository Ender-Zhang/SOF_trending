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
lsh = MinHashLSH(threshold=0.4, num_perm=128)

# 创建MinHash对象
minhashes = {}
for i, emb in enumerate(embeddings):
    minhash = MinHash(num_perm=128)
    for d in emb.tolist():
        minhash.update(str(d).encode('utf8'))
    lsh.insert(file_names[i], minhash)
    minhashes[file_names[i]] = minhash

# 搜索相似项
for name, minhash in minhashes.items():
    result = lsh.query(minhash)
    print(f"{name} 相似的文件: {result}")
