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
