import React, { useState } from 'react';

const SearchComponent: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [searchType, setSearchType] = useState<string>('type1'); // 新增状态来管理搜索类型
  const [results, setResults] = useState<string[]>([]);

  const handleSearchType1 = async () => {
    // handleSearch 逻辑针对 Inverted index
    try {
        const requestOptions: RequestInit = {
          method: 'GET',
          redirect: 'follow',
        };
        
        fetch(`http://127.0.0.1:8001/search/inverted_index?query=${query}`, requestOptions)
          .then(response => response.json())  // 假设后端返回的是JSON格式的数组
          .then(result => {
              console.log(result);
              // 使用正则表达式进行替换，并且仅取前十个
              const updatedResults = result.map((item: string) => {
                const pattern = /\d+_\$(\w+)_questions_(\d+)_([a-zA-Z0-9-]+)\.txt/;
                const replacement = "https://stackoverflow.com/questions/$2/$3";
                return item.replace(pattern, replacement);
              }).slice(0, 10);  // 仅保留前十个结果
              setResults(updatedResults);
          })
          .catch(error => console.log('error', error));
      } catch (error) {
        console.error('Error:', error);
      }
  };

  const handleSearchType2 = async () => {
    // handleSearch 逻辑针对 TF-IDF
    try {
        const requestOptions: RequestInit = {
          method: 'GET',
          redirect: 'follow',
        };
        
        fetch(`http://127.0.0.1:8001/search/tf_idf?query=${query}`, requestOptions)
          .then(response => response.json())  // 假设后端返回的是JSON格式的数组
          .then((result: [string, number][]) => {  // 适当调整类型注解以匹配返回的数据结构
              console.log(result);
              // 使用正则表达式进行替换，并且仅取前十个
              const updatedResults = result.map(item => {
                const pattern = /\d+_\$(\w+)_questions_(\d+)_([a-zA-Z0-9-]+)\.txt/;
                const replacement = "https://stackoverflow.com/questions/$2/$3";
                return item[0].replace(pattern, replacement);
              }).slice(0, 10);  // 仅保留前十个结果
              setResults(updatedResults);
          })
          .catch(error => console.log('error', error));
      } catch (error) {
        console.error('Error:', error);
      }
    };

  const handleSearchType3 = async () => {
    // handleSearch 逻辑针对 BM25
    try {
      const requestOptions: RequestInit = {
        method: 'GET',
        redirect: 'follow',
      };
      
      fetch(`http://127.0.0.1:8001/search/bm25?query=${query}`, requestOptions)
        .then(response => response.json())  // 假设后端返回的是JSON格式的数组
        .then((result: [string, number][]) => {  // 适当调整类型注解以匹配返回的数据结构
            console.log(result);
            // 使用正则表达式进行替换，并且仅取前十个
            const updatedResults = result.map(item => {
              const pattern = /\d+_\$(\w+)_questions_(\d+)_([a-zA-Z0-9-]+)\.txt/;
              const replacement = "https://stackoverflow.com/questions/$2/$3";
              return item[0].replace(pattern, replacement);
            }).slice(0, 10);  // 仅保留前十个结果
            setResults(updatedResults);
        })
        .catch(error => console.log('error', error));
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleSearchType4 = async () => {
    // handleSearch 逻辑针对 BM25 Fuzzy
    try {
      const requestOptions: RequestInit = {
        method: 'GET',
        redirect: 'follow',
      };
      
      fetch(`http://127.0.0.1:8001/search/bm25fuzzy?query=${query}`, requestOptions)
        .then(response => response.json())  // 假设后端返回的是JSON格式的数组
        .then((result: [string, number][]) => {  // 适当调整类型注解以匹配返回的数据结构
            console.log(result);
            // 使用正则表达式进行替换，并且仅取前十个
            const updatedResults = result.map(item => {
              const pattern = /\d+_\$(\w+)_questions_(\d+)_([a-zA-Z0-9-]+)\.txt/;
              const replacement = "https://stackoverflow.com/questions/$2/$3";
              return item[0].replace(pattern, replacement);
            }).slice(0, 10);  // 仅保留前十个结果
            setResults(updatedResults);
        })
        .catch(error => console.log('error', error));
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

  const handleSearch = () => {
    if (searchType === 'type1') {
      handleSearchType1();
    } 
    else if (searchType === 'type2') {
        handleSearchType2();
        }
    else if (searchType === 'type3') {
      handleSearchType3();
    }
    else if (searchType === 'type4') {
      handleSearchType4();
    }
  };

  return (
    <div>
      <select value={searchType} onChange={(e) => setSearchType(e.target.value)}>
        <option value="type1">Inverted index</option>
        <option value="type2">TF-IDF</option>
        <option value="type3">BM25</option>
        <option value="type4">BM25 Fuzzy</option>
      </select>
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Content to search..."
      />
      <button onClick={handleSearch}>Search</button>
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
