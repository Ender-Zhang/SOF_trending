from math import log
import os
from collections import defaultdict
import json

# Function to compute IDF for BM25
def compute_idf(word, inverted_index, total_documents):
    return log((total_documents - len(inverted_index[word]) + 0.5) / (len(inverted_index[word]) + 0.5) + 1)

# Function to compute BM25
def compute_bm25(documents, inverted_index, total_documents, avgdl, k1, b):
    bm25 = {}
    for word, docs in inverted_index.items():
        idf = compute_idf(word, inverted_index, total_documents)
        for doc in docs:
            word_count = documents[doc].split().count(word)
            doc_length = len(documents[doc].split())
            tf = word_count / doc_length
            normalized_tf = tf * (k1 + 1) / (tf + k1 * (1 - b + b * doc_length / avgdl))
            bm25[(doc, word)] = idf * normalized_tf
    return bm25

# Preprocessed folder path
preprocessed_folder_path = 'preprocessed'

# Load preprocessed documents
documents = {}
for filename in os.listdir(preprocessed_folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(preprocessed_folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            documents[filename] = file.read()

# Compute the total number of documents
total_documents = len(documents)

# Average document length
avgdl = sum(len(doc.split()) for doc in documents.values()) / total_documents

# Parameters for BM25
k1 = 1.5
b = 0.75

# Initialize inverted index
inverted_index = defaultdict(set)

# Create inverted index
for doc_id, content in documents.items():
    for word in content.split():
        inverted_index[word].add(doc_id)

# Calculate BM25 scores
bm25 = compute_bm25(documents, inverted_index, total_documents, avgdl, k1, b)

# Convert tuple keys to string for BM25
bm25_str_keys = {f"{doc_id}::{word}": value for (doc_id, word), value in bm25.items()}

# Save the modified BM25 dictionary
with open('bm25.json', 'w', encoding='utf-8') as f:
    json.dump(bm25_str_keys, f, ensure_ascii=False, indent=4)
