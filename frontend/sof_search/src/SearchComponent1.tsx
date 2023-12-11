import React, { useState } from 'react';

const SearchComponent: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<string[]>([]);  // 更改为字符串数组

  const handleSearch = async () => {
    try {
      const requestOptions: RequestInit = {
        method: 'GET',
        redirect: 'follow',
      };
      
      fetch(`http://127.0.0.1:8000/search/inverted_index?query=${query}`, requestOptions)
        .then(response => response.json())  // 假设后端返回的是JSON格式的数组
        .then(result => {
            console.log(result);
            // 使用正则表达式进行替换，并且仅取前十个
            const updatedResults = result.map((item: string) => {
              const pattern = /\d+_\$(\w+)_questions_(\d+)_([a-zA-Z0-9-]+)\.html/;
              const replacement = "https://stackoverflow.com/questions/$2/$3.html";
              return item.replace(pattern, replacement);
            }).slice(0, 10);  // 仅保留前十个结果
            setResults(updatedResults);
        })
        .catch(error => console.log('error', error));
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

  return (
    <div>
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)}
        placeholder="输入搜索内容..."
      />
      <button onClick={handleSearch}>搜索</button>
      <div>
        {results.length > 0 && (
          <ul>
            {results.map((result, index) => (
              <li key={index}><a href={result} target="_blank" rel="noopener noreferrer">{result}</a></li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
export default SearchComponent;
