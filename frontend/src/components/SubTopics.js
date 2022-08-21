import React from "react";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import SubTopicsButton from "./SubTopcisButton";
import Header from "./Header";

function SubTopics(props) {
  const [topics, setSubTopics] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/get", {
      method: "GET",
      headers: {
        "Content-type": "application/json",
      },
    })
      .then((resp) => resp.json())
      .then((resp) => setSubTopics(resp))
      .catch((error) => console.log(error));
  }, [topics.shift()]);

  const data = useLocation();
  const heading = data.search.slice(1);
  const heading1 = decodeURI(heading);

  return (
    <div>
      <div className="App1">
        <Header />
        <h1 className="main_heading">{heading1}</h1>
      </div>
      <SubTopicsButton topics={topics} heading1={heading1} />
    </div>
  );
}

export default SubTopics;
