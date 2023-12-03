from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 打开文件
with open('data/content/content_webpage_c1.txt', 'r') as file:
    # 读取文件内容
    content = file.read()

# 打印内容
text1 = summarizer(content, max_length=130, min_length=30, do_sample=False)
print(text1[0]['summary_text'])

with open('data/content/content_webpage_c2.txt', 'r') as file:
    # 读取文件内容
    content = file.read()

# 打印内容
text2 = summarizer(content, max_length=130, min_length=30, do_sample=False)
print(text2[0]['summary_text'])


# sentences = ["This is an example sentence", "Each sentence is converted"]
sentences = [text1[0]['summary_text'], text2[0]['summary_text']]

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
embeddings = model.encode(sentences)
print(embeddings)

# 计算两个嵌入向量之间的余弦相似度
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
print(similarity)
print("Similarity: " + str(similarity[0][0]))