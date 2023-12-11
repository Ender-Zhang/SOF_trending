import React, { useState, useEffect } from "react";
import "./image.css";

const PageRankComponent: React.FC = () => {
  const [imageSrc, setImageSrc] = useState("");
  const [textList, setTextList] = useState<string[]>([]);

  useEffect(() => {
    var requestOptions = {
      method: "GET",
      redirect: "follow",
    } as RequestInit;

    fetch("http://127.0.0.1:8000/pagerank", requestOptions)
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        if (result.image && result.text) {
          setImageSrc(`data:image/png;base64,${result.image}`);
          setTextList(result.text);
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
                {parts[0]}{" "}
                {parts[1] && (
                  <a href={parts[1]} target="_blank" rel="noopener noreferrer">
                    {parts[1]}
                  </a>
                )}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};


export default PageRankComponent;
