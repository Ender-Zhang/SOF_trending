import React, { useState } from 'react';
import './App.css';
import SearchComponent from './SearchComponent';
import PageRankComponent from './PageRankComponent';
import HitsComponent from './HitsComponent';
import {Test} from './test';
import HeatComponent from './HeatComponent';
import LlmComponent from './LlmComponent';

// React组件部分
function App() {
  const [activeTab, setActiveTab] = useState('hits');

  return (
    <div className="App">
      <header className="App-header">
        {/* 标签页切换按钮 */}
        {/* <Test/> */}
        {/* <HeatComponent/> */}
        <div className="tab-buttons">
         <button className={activeTab === 'search' ? 'active' : ''} onClick={() => setActiveTab('search')}>Search</button>
          <button className={activeTab === 'hits' ? 'active' : ''} onClick={() => setActiveTab('hits')}>Hits</button>
          <button className={activeTab === 'pagerank' ? 'active' : ''} onClick={() => setActiveTab('pagerank')}>PageRank</button>
          <button className={activeTab === 'heat' ? 'active' : ''} onClick={() => setActiveTab('heat')}>Hot Topic</button>
          <button className={activeTab === 'llm' ? 'active' : ''} onClick={() => setActiveTab('llm')}>LLM</button>
        </div>

        {/* 根据activeTab的值渲染对应的组件 */}
        {activeTab === 'hits' && <HitsComponent />}
        {activeTab === 'pagerank' && <PageRankComponent />}
        {activeTab === 'search' && <SearchComponent />}
        {activeTab === 'heat' && <HeatComponent />}
        {activeTab === 'llm' && <LlmComponent />}

      </header>
    </div>
  );
}


export default App;
