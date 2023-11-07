import os
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    # 找到所有具有 's-prose js-post-body' 类的元素
    prose_contents = soup.find_all(class_='s-prose js-post-body')
    # 对每个 's-prose js-post-body' 元素进行处理
    for prose in prose_contents:
        # 在每个 's-prose js-post-body' 元素中，找到所有 'lang-py s-code-block' 类的 <pre> 块
        code_blocks = prose.find_all('pre', class_='lang-py s-code-block')
        # 从 prose 元素中移除这些代码块
        for code_block in code_blocks:
            code_block.decompose()
            
    # 获取剩余文本内容并返回
    texts = [element.get_text(separator=' ', strip=True) for element in prose_contents]
    return ' '.join(texts)

# 文件夹路径
folder_path = 'data/html'
target_folder_path = 'data/preprocessed'

# 停用词和词干提取器
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# 遍历文件夹中的每个文件
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):  # 检查文件扩展名
        file_path = os.path.join(folder_path, filename)

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 使用函数提取并清洗文本
        text = text_from_html(html_content)

        # 分词
        tokens = word_tokenize(text)

        # 标准化：转小写并过滤停用词
        tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

        # 词干提取
        tokens = [stemmer.stem(word) for word in tokens]

        # 创建一个新文件名
        preprocessed_filename = 'preprocessed_' + filename.replace('.html', '.txt')
        preprocessed_file_path = os.path.join(target_folder_path, preprocessed_filename)

        # 写入预处理后的文本
        with open(preprocessed_file_path, 'w', encoding='utf-8') as preprocessed_file:
            preprocessed_file.write(' '.join(tokens))

print("Preprocessing complete and files are saved.")
