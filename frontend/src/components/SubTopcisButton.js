import React from "react";
import APIService from "./APIService";
import { Link } from "react-router-dom";

function SubTopicsButton(props) {
  const scrapeData = (i, name) => {
    alert(props.topics[i].domain_topics[name]);
    APIService.InsertData(props.topics[i].domain_topics[name])
      .then((resp) => resp.json())
      .catch((error) => console.log(error));
  };

  return (
    <div>
      {props.topics &&
        props.topics.map((topics) => {
          // console.log(Object.keys(props.topics).indexOf(topics.));
          if (topics.domain_name == props.heading1) {
            var i = props.topics.findIndex(
              (x) => x.domain_name === props.heading1
            );
            var topic = new Array(topics.domain_topics.length)
              .fill(0)
              .map((zero, index) => (
                <li key={index} onClick={() => scrapeData(i, index)}>
                  <Link
                    className="btn btn-primary topic_btn"
                    // onClick={() => scrapeData(index)}
                    to={{
                      pathname: `/HomePage`,
                      search: topics.domain_topics[index],
                    }}
                  >
                    {topics.domain_topics[index]}
                  </Link>
                </li>
              ));
          }
          return <div>{topic}</div>;
        })}
    </div>
  );
}

export default SubTopicsButton;
