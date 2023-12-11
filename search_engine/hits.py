import os
import networkx as nx
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

# 正则表达式模式和替换格式
pattern = r"\d+_\$(\w+)_questions_(\d+)_([a-zA-Z0-9-]+)\.html"
replacement = r"https://stackoverflow.com/questions/\2/\3.html"

def create_link_graph(html_folder):
    graph = nx.DiGraph()
    for filename in os.listdir(html_folder):
        if filename.endswith(".html"):
            file_path = os.path.join(html_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    target = link['href']
                    if target.endswith(".html"):
                        file_name_regex = re.sub(pattern, replacement, filename)
                        graph.add_edge(file_name_regex, target)
    return graph

def compute_hits(graph):
    return nx.hits(graph)

def save_hits_results(hub_scores, authority_scores, filename):
    with open(filename, 'w') as file:
        for page in hub_scores:
            file.write(f"{page}: Hub Score = {hub_scores[page]}, Authority Score = {authority_scores[page]}\n")

def create_index_mapping(graph):
    return {node: i for i, node in enumerate(graph.nodes())}

def save_index_mapping(mapping, filename):
    with open(filename, 'w') as file:
        for node, index in mapping.items():
            file.write(f"{index}: {node}\n")

def plot_graph(graph, hub_scores, index_mapping, filename):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=[v * 10000 for v in hub_scores.values()])
    nx.draw_networkx_edges(graph, pos)
    
    labels = {node: index_mapping[node] for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels=labels)

    plt.title("HITS Network Visualization")
    plt.savefig(filename)

# 定义HTML文件所在的文件夹
html_folder = '../data/html_all'

# 构建链接图
link_graph = create_link_graph(html_folder)

# 计算HITS分数
hub_scores, authority_scores = compute_hits(link_graph)

# 生成节点序号映射
index_mapping = create_index_mapping(link_graph)

# 保存HITS结果
save_hits_results(hub_scores, authority_scores, 'hits_results.txt')

# 保存序号与节点名的对应关系
save_index_mapping(index_mapping, 'node_index_mapping_hits.txt')

# 绘制并保存网络图
plot_graph(link_graph, hub_scores, index_mapping, 'network_visualization_hits.png')
