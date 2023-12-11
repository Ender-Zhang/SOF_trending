import React, { useState, useEffect } from "react";

export const HeatComponent: React.FC = () => {
  const [data, setData] = useState<{ file_name: string; content: string }[][]>([]);

  useEffect(() => {
    var requestOptions = {
      method: 'GET',
      redirect: 'follow'
    } as RequestInit;
    
    fetch("http://127.0.0.1:8000/similar-files/", requestOptions)
      .then(response => response.json())
      .then(result => setData(result))
      .catch(error => console.log('error', error));
  }, []); // 空依赖数组，确保仅在组件挂载时运行

  function convertFilenameToUrl(filename: string): string {
    // 正则表达式匹配并构建URL
    const pattern = /summary_content_\d+_\$com_questions_(\d+)_(.+)\.txt/;
    const match = filename.match(pattern);
  
    if (match) {
      const questionId = match[1];
      const title = match[2].replace(/_/g, '-'); // 将下划线替换为破折号
      return `https://www.stackoverflow.com/questions/${questionId}/${title}`;
    }
  
    return ''; // 如果不匹配，返回空字符串或适当的默认URL
  }

  function extractFileNames(data: { file_name: string; content: string }[][]): string[] {
    // 找到元素数量最多的子数组
    const maxList = data.reduce((a, b) => (a.length > b.length ? a : b), []);

    return maxList.map(item => convertFilenameToUrl(item.file_name));
  }

  const fileNames = extractFileNames(data);

  return (
    <div>
      <h1>Hot Topics</h1>
      <ul>
        {fileNames.map((fileName, index) => (
          <li key={index}><a href={fileName} target="_blank" rel="noopener noreferrer">{fileName}</a></li>
        ))}
      </ul>
    </div>
  );
}

export default HeatComponent;
