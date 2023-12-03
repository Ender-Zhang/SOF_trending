from fastapi import FastAPI
import json
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



from fastapi import FastAPI

app = FastAPI()


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


app = FastAPI()

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
