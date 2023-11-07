import os
from gensim.corpora import Dictionary
from gensim.models.bm25model import OkapiBM25Model

from collections import Counter

# 假设 tech_terms 是我们感兴趣的技术名词集合
tech_terms = {"python", "java", "selenium", "xpath", "html", "css", "javascript", "sql"}

# 预处理文本文件的目录路径
folder_path = 'data/preprocessed'

# 创建一个列表来保存所有文档
texts = []

# 读取预处理后的文本文件
for filename in os.listdir(folder_path):
    if filename.startswith('preprocessed_'):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read().split()
            # 只保留技术名词
            text = [word for word in text if word in tech_terms]
            texts.append(text)

# 创建字典和语料库
dictionary = Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 创建 BM25 模型
# bm25 = BM25(corpus)
bm25_model = OkapiBM25Model(corpus=corpus, dictionary=dictionary)

# 可以使用 bm25 对给定查询计算得分
# ...

# 计算语料库中技术名词的出现频率
term_freq = Counter()
for doc in corpus:
    for word_id, freq in doc:
        term_freq[dictionary[word_id]] += freq

# 显示出现频率最高的技术名词
print("Most common technical terms:")
for term, freq in term_freq.most_common():
    print(f"{term}: {freq}")

# 显示最常见的技术名词的 BM25 分数
# print("\nBM25 scores for most common technical terms:")
# for term, freq in term_freq.most_common():
#     print(f"{term}: {bm25_model.get_term_weights(term)[0]}")

# 假设您有一个查询
# query = "python selenium automation"

# # 将查询转换为与语料库相同格式的词袋
# query_bow = dictionary.doc2bow(query.lower().split())

# # 使用 BM25 模型计算查询与每个文档的得分
# scores = bm25_model.get_scores(query_bow)

# # 打印查询与每个文档的BM25得分
# for doc_id, score in enumerate(scores):
#     print(f"Document {doc_id} has BM25 score of {score}")

# # 如果您想找到得分最高的文档，可以这样做：
# best_doc_id = scores.index(max(scores))
# print(f"Document with id {best_doc_id} has the highest BM25 score.")
