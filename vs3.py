import seaborn as sns
import matplotlib.pyplot as plt

# 假设 'similarity_matrix' 是您的相似度矩阵
sns.heatmap(similarity_matrix, annot=True, cmap='coolwarm')
plt.show()
