import React, { useState, useEffect } from "react";
import "./image.css";

const LlmComponent: React.FC = () => {
  const [imageSrc, setImageSrc] = useState("");
  const [textList, setTextList] = useState<string[]>([]);

  useEffect(() => {
    var requestOptions = {
      method: "GET",
      redirect: "follow",
    } as RequestInit;

    fetch("http://127.0.0.1:8001/llm", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      if (result.image && result.text) {
        setImageSrc(`data:image/png;base64,${result.image}`);
  
        // 更新正则表达式以匹配提供的格式
        const updatedResults1 = result.text.map((item:any) => {
          const pattern = /(\d+)_([a-zA-Z0-9-]+)/;
          const replacement = "https://stackoverflow.com/questions/$1/$2.html";
          console.log(item.split(" ")[1].replace(pattern, replacement));
          return item.split(" ")[1].replace(pattern, replacement);
        });
        console.log(updatedResults1);
        setTextList(updatedResults1);
      }
    })
    .catch((error) => console.log("error", error));
  }, []); // 空依赖数组意味着这个effect只会在组件挂载时运行一次
  

  return (
    <div >
      {imageSrc && <img src={imageSrc} alt="Hits Image" className="page-rank-image" />}
      <div className="text-list page-rank-component">
        <ul>
          {textList.map((text, index) => {
            const parts = text.split(" ");
            return (
              <li key={index}>
                {/* {parts[0]}{" "}
                {parts[1] && (
                  <a href={parts[1]} target="_blank" rel="noopener noreferrer">
                    {parts[1]}
                  </a>
                )
                } */}
                <a href={text} target="_blank" rel="noopener noreferrer">{parts}</a>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};


export default LlmComponent;
