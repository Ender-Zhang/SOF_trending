text1 = 'Now Im back in the interpreter and I cant seem to import the module, because I dont understand how to import a relative (or absolute) path.'
text2 = 'I have a module that I want to import. The module is in the same directory as the script that wants to import it.'

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
# sentences = ["This is an example sentence", "Each sentence is converted"]
# sentences = [text1[0]['summary_text'], text2[0]['summary_text']]
sentences = [text1, text2]

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
embeddings = model.encode(sentences)
print(embeddings)

# 计算两个嵌入向量之间的余弦相似度
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
print(similarity)
print("Similarity: " + str(similarity[0][0]))