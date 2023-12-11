from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys
import base64



# 添加query.py所在的文件夹到sys.path
module_path = os.path.abspath(os.path.join('../search_engine/'))
if module_path not in sys.path:
    sys.path.append(module_path)

# 现在可以导入query模块
import search_module

# Load data once at startup
inverted_index = search_module.load_inverted_index('../search_engine/inverted_index.json')
tf_idf = search_module.load_scoring_data('../search_engine/tf_idf.json')
bm25 = search_module.load_scoring_data('../search_engine/bm25.json')


app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}



from fastapi import FastAPI

app = FastAPI()

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # return base64.b64encode(image_file.read()).decode('utf-8')
        return base64.b64encode(image_file.read()).decode()

def read_text_file(text_file_path):
    with open(text_file_path, "r", encoding="utf-8") as file:
        return file.read()

def save_to_json(image_base64, text_content, json_file_path):
    data = {"image": image_base64, "text": text_content}
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def load_urls_to_list(file_path):
    url_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            url_list.append(line.strip())
    return url_list


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# FastAPI端点
app = FastAPI()

@app.get("/groups")
def read_groups():
    # 读取分组信息
    with open('../file_groups.json', 'r') as infile:
        groups = json.load(infile)
    
    # 创建一个新的字典来存储文件名及其内容
    groups_with_content = {}
    
    # 对于每个组中的每个文件，读取其内容
    for group_id, file_list in groups.items():
        content_list = []
        for file_name in file_list:
            file_path = os.path.join('../data/summaries/', file_name)
            with open(file_path, 'r') as file:
                content = file.read()
                content_list.append({"file_name": file_name, "content": content})
        groups_with_content[group_id] = content_list
    
    return groups_with_content

@app.get("/similarity-results/")
async def read_similarity_results():
    with open('../similarity_results.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# 假设JSON文件和文本文件都在相同的目录中
summary_folder = '../data/summaries/'

@app.get("/similar-files/")
async def read_similar_files():
    # 读取JSON文件以获取相似文件组
    with open('../similar_files_groups.json', 'r', encoding='utf-8') as file:
        similar_files_groups = json.load(file)
    
    # 准备包含文件名和内容的响应数据
    response_data = []

    for group in similar_files_groups:
        group_data = []
        for file_name in group:
            file_path = os.path.join(summary_folder, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    group_data.append({"file_name": file_name, "content": content})
        response_data.append(group_data)

    return response_data

@app.get("/search/inverted_index")
async def search_inverted_index(query: str):
    return search_module.search_inverse_index(query, inverted_index)

@app.get("/search/tf_idf")
async def search_tf_idf(query: str):
    return search_module.search_tf_idf(query, inverted_index, tf_idf)

@app.get("/search/bm25")
async def search_bm25(query: str):
    return search_module.search_bm25(query, inverted_index, bm25)

@app.get("/search/bm25fuzzy")
async def search_bm25(query: str):
    return search_module.search_bm25_fuzzy(query, inverted_index, bm25)



@app.get("/pagerank")
async def read_pagerank():
    data = {
        "image": encode_image_to_base64("../search_engine/network_visualization.png"),
        "text": load_urls_to_list("../search_engine/node_index_mapping.txt")
    }
    return data

@app.get("/hits")
async def read_pagerank():
    data = {
        "image": encode_image_to_base64("../search_engine/network_visualization_hits.png"),
        "text": load_urls_to_list("../search_engine/node_index_mapping_hits.txt")
    }
    return data

@app.get("/llm")
async def read_pagerank():
    data = {
        "image": encode_image_to_base64("../network_visualization_similarity.png"),
        "text": load_urls_to_list("../label_to_index_mapping_similarity.txt")
    }
    return data


origins = ["http://127.0.0.1"]  #也可以设置为"*"，即为所有。
# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://192.168.1.167:3000","http://192.168.1.167:1"],  # 允许的来源列表
    allow_origins=["*"],  # 允许的来源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)