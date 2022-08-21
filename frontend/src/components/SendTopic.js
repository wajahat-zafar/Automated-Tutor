import React from "react";

function sendTopic(props) {
  return (
    <div>
      {props.topics &&
        props.topics.map((topics) => {
          return (
            <button className="btn btn-primary topic_btn">
              {topics.domain_name}
            </button>
          );
        })}
    </div>
  );
}

export default sendTopic;
