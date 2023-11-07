import os
import math
from collections import Counter, defaultdict

# Assuming `tech_terms` is the set of technical terms we are interested in.
tech_terms = {"python", "java", "selenium", "xpath", "html", "css", "javascript", "sql"}

# Directory path for the preprocessed text files.
folder_path = 'data/preprocessed'

# List to store all documents.
texts = []

# Ensure the folder exists.
if not os.path.exists(folder_path):
    print(f"The directory {folder_path} does not exist.")
else:
    # Read the preprocessed text files.
    for filename in os.listdir(folder_path):
        if filename.startswith('preprocessed_'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read().split()
                # Keep only technical terms.
                text = [word for word in text if word in tech_terms]
                texts.append(text)

    # The rest of your code goes here, assuming you have at least one preprocessed file.
    # ...

# Note: The rest of the code is omitted for brevity.
# Read the preprocessed text files.
for filename in os.listdir(folder_path):
    if filename.startswith('preprocessed_'):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read().split()
            # Keep only technical terms.
            text = [word for word in text if word in tech_terms]
            texts.append(text)

# Computing IDF values.
def compute_idf(doc_list):
    idf_scores = {}
    total_docs = len(doc_list)
    for doc in doc_list:
        for term in set(doc):
            idf_scores[term] = idf_scores.get(term, 0) + 1

    for term, doc_freq in idf_scores.items():
        idf_scores[term] = math.log((total_docs + 1) / (doc_freq + 1)) + 1

    return idf_scores

idf_scores = compute_idf(texts)

# Computing TF values.
def compute_tf(text):
    tf_scores = Counter(text)
    for term in tf_scores:
        tf_scores[term] /= len(text)
    return tf_scores

# BM25 calculation.
def bm25(tf, idf, average_doc_length, doc_length, k1=1.5, b=0.75):
    return idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / average_doc_length)))

# Calculate the average document length.
avg_dl = sum(len(doc) for doc in texts) / len(texts)

# # Compute BM25 scores for each term in each document.
doc_scores = []
for text in texts:
    tf_scores = compute_tf(text)
    doc_length = len(text)
    doc_score = defaultdict(float)
    for term, tf in tf_scores.items():
        if term in idf_scores:
            doc_score[term] = bm25(tf, idf_scores[term], avg_dl, doc_length)
    doc_scores.append(doc_score)

# Display BM25 scores for most common technical terms.
print("\nBM25 scores for most common technical terms:")
term_freq = Counter()
for text in texts:
    term_freq.update(text)
for term, freq in term_freq.most_common():
    term_score = sum(doc_score[term] for doc_score in doc_scores)
    print(f"{term}: {term_score}")

# Assuming you have a query.
query = "python selenium automation"

# Convert the query to the same bag-of-words format as the corpus.
query_terms = query.lower().split()
query_tf = compute_tf(query_terms)

# Calculate the BM25 score for the query against each document.
query_scores = []
for doc_id, doc_score in enumerate(doc_scores):  # Ensure doc_id is defined here.
    score = sum(bm25(query_tf[term], idf_scores[term], avg_dl, len(texts[doc_id]), k1=1.5, b=0.75) 
                for term in query_terms if term in doc_score)
    query_scores.append(score)

# Print BM25 scores for the query against each document.
for doc_id, score in enumerate(query_scores):
    print(f"Document {doc_id} has BM25 score of {score}")

# Find the document with the highest BM25 score.
best_doc_id = query_scores.index(max(query_scores))
print(f"Document with id {best_doc_id} has the highest BM25 score.")