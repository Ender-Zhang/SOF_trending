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

def compute_pagerank(graph):
    return nx.pagerank(graph)

def save_pagerank_results(page_ranks, filename):
    with open(filename, 'w') as file:
        for page, rank in page_ranks.items():
            file.write(f"{page}: {rank}\n")

def create_index_mapping(graph):
    """为图中的每个节点分配一个序号，并返回序号到节点名的映射字典。"""
    return {node: i for i, node in enumerate(graph.nodes())}

def save_index_mapping(mapping, filename):
    """将序号与节点名的映射保存到文件。"""
    with open(filename, 'w') as file:
        for node, index in mapping.items():
            file.write(f"{index}: {node}\n")

def plot_graph(graph, page_ranks, index_mapping, filename):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=[v * 10000 for v in page_ranks.values()])
    nx.draw_networkx_edges(graph, pos)
    
    # 用序号代替节点名绘制标签
    labels = {node: index_mapping[node] for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels=labels)

    plt.title("PageRank Network Visualization")
    plt.savefig(filename)

# 定义HTML文件所在的文件夹
html_folder = '../data/html_all'

# 构建链接图
link_graph = create_link_graph(html_folder)

# 计算PageRank
page_ranks = compute_pagerank(link_graph)

# 生成节点序号映射
index_mapping = create_index_mapping(link_graph)

# 保存PageRank结果
save_pagerank_results(page_ranks, 'pagerank_results.txt')

# 保存序号与节点名的对应关系
save_index_mapping(index_mapping, 'node_index_mapping.txt')

# 绘制并保存网络图
plot_graph(link_graph, page_ranks, index_mapping, 'network_visualization.png')
