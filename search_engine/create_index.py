import os
from collections import defaultdict
import json

# 文件夹路径
preprocessed_folder_path = 'preprocessed'  # 保存预处理文本的文件夹

# 读取预处理过的文本文件
documents = {}
for filename in os.listdir(preprocessed_folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(preprocessed_folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            documents[filename] = file.read()


from collections import defaultdict

# 初始化倒排索引
inverted_index = defaultdict(set)

# 对每个文档进行分词
for doc_id, text in documents.items():
    for word in text.split():  # 假设文本已经被分词，用空格分隔
        inverted_index[word].add(doc_id)

# 打印倒排索引
# for word, doc_ids in inverted_index.items():
#     print(f"Word: {word}, Documents: {doc_ids}")


# 首先将倒排索引转换为可以序列化的格式（把集合转换为列表）
serializable_inverted_index = {word: list(doc_ids) for word, doc_ids in inverted_index.items()}

# 将倒排索引保存为JSON文件
with open('inverted_index.json', 'w', encoding='utf-8') as file:
    json.dump(serializable_inverted_index, file, ensure_ascii=False, indent=4)
