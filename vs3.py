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

# Assemble nodes in the graph and track group membership
group_membership = {}
for group_id, group in enumerate(file_groups):
    for file_name in group:
        match = re.search(pattern, file_name)
        node_label = match.group(1) if match else file_name[:10]
        if node_label not in label_to_index:
            label_to_index[node_label] = index
            group_membership[index] = group_id
            index += 1
        G.add_node(label_to_index[node_label])

    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            node_label_i = re.search(pattern, group[i]).group(1) if re.search(pattern, group[i]) else group[i][:10]
            node_label_j = re.search(pattern, group[j]).group(1) if re.search(pattern, group[j]) else group[j][:10]
            G.add_edge(label_to_index[node_label_i], label_to_index[node_label_j])

# Generate a color for each connected component
connected_components = list(nx.connected_components(G))
color_map = []
for component in connected_components:
    color = plt.cm.jet(len(color_map) / len(connected_components))
    color_map.extend([color for _ in range(len(component))])

# Ensure the color map is correctly ordered according to node indices
sorted_color_map = [color_map[i - 1] for i in sorted(G.nodes())]

# 绘制图形
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color=sorted_color_map, alpha=0.9)
nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in G.nodes()}, font_size=8, font_color='black')
plt.axis('off')
plt.show()