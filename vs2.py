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

# 节点标签与序号的映射
label_to_index = {}
index = 1

# 添加节点和边
for group in file_groups:
    for file_name in group:
        # 使用正则表达式提取特定部分
        match = re.search(pattern, file_name)
        node_label = match.group(1) if match else file_name[:10]  # 如果无法匹配，使用前10个字符

        # 检查标签是否已经映射到序号
        if node_label not in label_to_index:
            label_to_index[node_label] = index
            index += 1

        # 添加节点（使用序号）
        G.add_node(label_to_index[node_label])

    for i in range(len(group)):
        for j in range(i+1, len(group)):
            node_label_i = re.search(pattern, group[i]).group(1) if re.search(pattern, group[i]) else group[i][:10]
            node_label_j = re.search(pattern, group[j]).group(1) if re.search(pattern, group[j]) else group[j][:10]

            # 添加边（使用序号）
            G.add_edge(label_to_index[node_label_i], label_to_index[node_label_j])

# 绘制图形
# nx.draw(G, with_labels=True, node_color='lightblue', font_size=8, edge_color='gray')
# 绘制图形，隐藏边
pos = nx.spring_layout(G)  # 可以尝试不同的布局算法
nx.draw_networkx_nodes(G, pos, node_color='lightblue', alpha=0.9)  # 绘制节点
nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in G.nodes()}, font_size=8, font_color='black')

# 隐藏边和坐标轴
plt.axis('off')

# plt.show()
plt.savefig('network_visualization_similarity.png')

# 保存节点标签和序号的映射到txt文件
with open('label_to_index_mapping_similarity.txt', 'w') as mapping_file:
    for label, idx in label_to_index.items():
        mapping_file.write(f"{idx}: {label}\n")
