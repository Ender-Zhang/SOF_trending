import json
from collections import defaultdict
from fuzzywuzzy import process

# 加载倒排索引
def load_inverted_index(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# 加载TF-IDF或BM25数据
def load_scoring_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        scoring_str_keys = json.load(file)
    return {tuple(key.split('::')): value for key, value in scoring_str_keys.items()}

# 倒排索引搜索
def search_inverse_index(query, inverted_index):
    query_words = query.lower().split()
    results = set()
    for word in query_words:
        if word in inverted_index:
            if not results:
                results = set(inverted_index[word])
            else:
                results &= set(inverted_index[word])
    return results

# TF-IDF搜索
def search_tf_idf(query, inverted_index, tf_idf):
    query_words = query.lower().split()
    doc_scores = defaultdict(float)
    for word in query_words:
        if word in inverted_index:
            for doc in inverted_index[word]:
                doc_scores[doc] += tf_idf.get((doc, word), 0)
    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

# BM25搜索
def search_bm25(query, inverted_index, bm25):
    query_words = query.lower().split()
    doc_scores = defaultdict(float)
    for word in query_words:
        if word in inverted_index:
            for doc in inverted_index[word]:
                doc_scores[doc] += bm25.get((doc, word), 0)
    return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

# BM25模糊搜索
def search_bm25_fuzzy(query, inverted_index, bm25_scores, top_n=10):
    query_words = query.lower().split()
    doc_scores = defaultdict(float)

    # Calculate BM25 score for each document that contains words from the query
    for word in query_words:
        # Find close matches to the word in the index
        close_matches = process.extract(word, inverted_index.keys(), limit=top_n)
        for match, score in close_matches:
            if match in inverted_index:
                for doc_id in inverted_index[match]:
                    doc_scores[doc_id] += bm25_scores.get((doc_id, match), 0)

    # Sort documents by score in descending order
    sorted_documents = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_documents