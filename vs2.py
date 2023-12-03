import networkx as nx
import matplotlib.pyplot as plt
import json
import re

# 正则表达式模式
pattern = r"com_questions_(.+)\.txt$"

# 读取 JSON 文件来获取文件组
with open('similar_files_groups.json', 'r') as file:
    file_groups = json.load(file)

# 创建图
G = nx.Graph()

# 添加节点和边
for group in file_groups:
    for file_name in group:
        # 使用正则表达式提取特定部分
        match = re.search(pattern, file_name)
        node_label = match.group(1) if match else file_name[:10]  # 如果无法匹配，使用前10个字符
        G.add_node(node_label)

    for i in range(len(group)):
        for j in range(i+1, len(group)):
            node_label_i = re.search(pattern, group[i]).group(1) if re.search(pattern, group[i]) else group[i][:10]
            node_label_j = re.search(pattern, group[j]).group(1) if re.search(pattern, group[j]) else group[j][:10]
            G.add_edge(node_label_i, node_label_j)

# 绘制图形
nx.draw(G, with_labels=True, node_color='lightblue', font_size=8)
plt.show()
