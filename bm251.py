import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from math import log

# Example documents
docs = ["the cat sat on the mat", "the dog sat on the log", "dogs and cats living together"]

# Initialize CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)

# Convert X to a dense array and calculate document frequency
X_array = X.toarray()
df = np.sum(X_array > 0, axis=0)
N = X_array.shape[0]
avgdl = np.mean(np.sum(X_array, axis=1))

# BM25 parameters
k1 = 1.5
b = 0.75

# Function to calculate BM25 for each document-term pair
def bm25_individual(tf, df, n, avgdl, doc_len, k1=1.5, b=0.75):
    """
    Compute the BM25 score for a single term in a document.
    """
    # Calculate IDF using the given formula
    idf = log((n - df + 0.5) / (df + 0.5) + 1)
    
    # Apply the BM25 formula
    score = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avgdl)))
    return score

# Calculate BM25 score for each term in each document
bm25_scores = np.zeros_like(X_array, dtype=float)
for i in range(N):  # For each document in the corpus
    doc_len = np.sum(X_array[i])  # Length of the document
    for j in range(X_array.shape[1]):  # For each term in the vocabulary
        tf = X_array[i][j]  # Term frequency in the document
        df_val = df[j]  # Document frequency of the term
        bm25_scores[i][j] = bm25_individual(tf, df_val, N, avgdl, doc_len)


print(bm25_scores)

# Let's modify the code to include a function that finds the document with the highest BM25 score for a given term.

# First, we will calculate the BM25 scores as before
# def bm25_individual(tf, df, n, avgdl, doc_len, k1=1.5, b=0.75):
#     # Calculate IDF using the given formula
#     idf = log((n - df + 0.5) / (df + 0.5) + 1)
    
#     # Apply the BM25 formula
#     score = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avgdl)))
#     return score

# Function to find the document with the highest BM25 score for a given term
def find_highest_bm25_for_term(term, bm25_scores, feature_names):
    """
    Find the document with the highest BM25 score for a given term.
    
    :param term: the term to search for
    :param bm25_scores: the matrix of BM25 scores
    :param feature_names: list of feature names (vocabulary)
    :return: tuple of (highest scoring document index, highest score)
    """
    # Find the column index for the term
    try:
        term_index = feature_names.index(term)
    except ValueError:
        return None, None  # Term not in the vocabulary

    # Get the column of scores corresponding to the term
    term_scores = bm25_scores[:, term_index]

    # Find the index of the highest score for this term
    highest_doc_index = np.argmax(term_scores)
    highest_score = term_scores[highest_doc_index]

    return highest_doc_index, highest_score


feature_names = vectorizer.get_feature_names_out()
term = 'cat'  # Example term
highest_doc_index, highest_score = find_highest_bm25_for_term(term, bm25_scores, list(feature_names))

print(highest_doc_index, highest_score)
