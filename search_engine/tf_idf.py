from math import log
import os
from collections import defaultdict
import json

# Load the inverted index
with open('inverted_index.json', 'r', encoding='utf-8') as file:
    inverted_index = json.load(file)

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

# Function to compute IDF
def compute_idf(word, inverted_index, total_documents):
    return log(total_documents / len(inverted_index[word]))

# Function to compute TF-IDF
def compute_tf_idf(documents, inverted_index, total_documents):
    tf_idf = {}
    for word, docs in inverted_index.items():
        idf = compute_idf(word, inverted_index, total_documents)
        for doc in docs:
            word_count = documents[doc].count(word)
            total_words = len(documents[doc].split())
            tf = word_count / total_words
            tf_idf[(doc, word)] = tf * idf
    return tf_idf

tf_idf = compute_tf_idf(documents, inverted_index, total_documents)

# Save the TF-IDF dictionary as a JSON file
# with open('tf_idf.json', 'w', encoding='utf-8') as f:
#     json.dump(tf_idf, f, ensure_ascii=False, indent=4)

# Convert tuple keys to string
tf_idf_str_keys = {f"{doc_id}::{word}": value for (doc_id, word), value in tf_idf.items()}

# Save the modified TF-IDF dictionary
with open('tf_idf.json', 'w', encoding='utf-8') as f:
    json.dump(tf_idf_str_keys, f, ensure_ascii=False, indent=4)