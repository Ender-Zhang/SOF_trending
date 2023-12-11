import json
from collections import defaultdict
import os

# 加载倒排索引
# with open('inverted_index.json', 'r', encoding='utf-8') as file:
#     inverted_index = json.load(file)

# def search(query):
#     # 分词
#     query_words = query.lower().split()

#     # 查找每个查询词汇在倒排索引中的文档
#     results = set()
#     for word in query_words:
#         if word in inverted_index:
#             if not results:
#                 results = set(inverted_index[word])
#             else:
#                 results &= set(inverted_index[word])

#     return results

# # 示例查询
# query_result = search("import")
# print(query_result)

# For tf-idf
# Load the TF-IDF data
# with open('tf_idf.json', 'r', encoding='utf-8') as f:
#     tf_idf_str_keys = json.load(f)

# # Convert string keys back to tuples
# tf_idf = {tuple(key.split('::')): value for key, value in tf_idf_str_keys.items()}

# def search(query, inverted_index, tf_idf):
#     # 分词处理查询（这里假设查询已经是分词后的）
#     query_words = query.lower().split()

#     # 初始化文档分数
#     doc_scores = defaultdict(float)

#     # 计算每个文档的得分
#     for word in query_words:
#         if word in inverted_index:
#             for doc in inverted_index[word]:
#                 doc_scores[doc] += tf_idf.get((doc, word), 0)

#     # 按得分排序
#     sorted_scores = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

#     return sorted_scores

# with open('inverted_index.json', 'r', encoding='utf-8') as file:
#     inverted_index = json.load(file)

# # 示例查询
# query = "python import"
# query_result = search(query, inverted_index, tf_idf)
# print(query_result)


# For BM25
from collections import defaultdict

def search(query, inverted_index, bm25):
    # Process the query (simple split, assuming no stopwords and all words are relevant)
    query_words = query.lower().split()

    # Calculate scores for documents
    doc_scores = defaultdict(float)
    for word in query_words:
        if word in inverted_index:
            for doc in inverted_index[word]:
                # Accumulate BM25 scores for documents that contain the word
                doc_scores[doc] += bm25.get((doc, word), 0)

    # Sort documents by their scores in descending order
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_docs

# Example usage
with open('inverted_index.json', 'r', encoding='utf-8') as file:
    inverted_index = json.load(file)

# Load the BM25 data
with open('bm25.json', 'r', encoding='utf-8') as file:
    bm25_str_keys = json.load(file)
bm25 = {tuple(key.split('::')): value for key, value in bm25_str_keys.items()}

# Load preprocessed documents
# preprocessed_folder_path = 'preprocessed'
# documents = {}
# for filename in os.listdir(preprocessed_folder_path):
#     if filename.endswith('.txt'):
#         file_path = os.path.join(preprocessed_folder_path, filename)
#         with open(file_path, 'r', encoding='utf-8') as file:
#             documents[filename] = file.read()

# # Compute the total number of documents
# total_documents = len(documents)

# Example query
query = "java"
search_results = search(query, inverted_index, bm25)
print(search_results)
