import os
import networkx as nx
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

# Original string
# original_string = "1_stackoverflow$com_questions_77564335_problem-loading-external-scripts-like-jquery"

# Regular expression pattern and replacement format
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
                        # print("filename: "+filename)
                        # print(file_name_regex)
                        graph.add_edge(file_name_regex, target)
    return graph

def compute_pagerank(graph):
    return nx.pagerank(graph)

def save_pagerank_results(page_ranks, filename):
    with open(filename, 'w') as file:
        for page, rank in page_ranks.items():
            file.write(f"{page}: {rank}\n")

def plot_graph(graph, page_ranks, filename):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=[v * 10000 for v in page_ranks.values()])
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos)
    plt.title("PageRank Network Visualization")
    plt.savefig(filename)

# 定义HTML文件所在的文件夹
html_folder = '../data/html_all'

# 构建链接图
link_graph = create_link_graph(html_folder)

# 计算PageRank
page_ranks = compute_pagerank(link_graph)

# 保存PageRank结果
save_pagerank_results(page_ranks, 'pagerank_results.txt')

# 绘制并保存网络图
plot_graph(link_graph, page_ranks, 'network_visualization.png')
