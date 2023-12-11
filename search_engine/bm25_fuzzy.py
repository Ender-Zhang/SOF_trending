import json
from collections import defaultdict
from fuzzywuzzy import process

# Function to compute BM25 score for a query
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

# Load inverted index from JSON file
with open('inverted_index.json', 'r', encoding='utf-8') as file:
    inverted_index = json.load(file)

# Load BM25 scores from JSON file
with open('bm25.json', 'r', encoding='utf-8') as file:
    bm25_json = json.load(file)
bm25_scores = {tuple(key.split('::')): value for key, value in bm25_json.items()}

# Example query
query = "python"

# Perform search using BM25 with fuzzy matching
search_results = search_bm25(query, inverted_index, bm25_scores)

# Print top N results
N = 10
for doc_id, score in search_results[:N]:
    print(f"Document ID: {doc_id}, Score: {score}")

