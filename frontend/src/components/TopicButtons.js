import React from "react";
import APIService from "./APIService";
import { Link } from "react-router-dom";

function TopicButtons(props) {
  const scrapeData = (name) => {
    APIService.InsertData(name)
      .then((resp) => resp.json())
      .catch((error) => console.log(error));
  };

  return (
    <div className="main">
      {props.type != "admin" ? (
        <div>
          {props.topics &&
            props.topics.map((topics) => {
              var topic = new Array(topics.length)
                .fill(0)
                .map((zero, index) => (
                  <div
                    className="topics"
                    key={index}
                    onClick={() => scrapeData(topics.topic_name)}
                  >
                    <Link
                      className="btn btn-primary topic_btn"
                      to={{
                        pathname: `/HomePage`,
                        search: topics.topic_name,
                      }}
                    >
                      {topics.topic_name}
                    </Link>
                  </div>
                ));
              // const topic = [];
              // // const name = [];
              // let i = 1;
              // for (var k in topics.domain_topics) {
              //   var name = topics.domain_topics[k];
              //   // name.push(name1);
              //   topic.push(
              //     <Link
              //       className="btn btn-primary topic_btn"
              //       onClick={() => scrapeData(i)}
              //       to={{
              //         pathname: `/HomePage`,
              //         search: topics.domain_topics[k],
              //       }}
              //     >
              //       {topics.domain_topics[k]}
              //     </Link>
              //   );

              //   i++;
              // }
              return <div>{topic}</div>;
            })}
        </div>
      ) : (
        <div>
          {props.topic &&
            props.topic.map((topic) => {
              var topics = new Array(topic.length)
                .fill(0)
                .map((zero, index) => (
                  <div
                    className="topics"
                    key={index}
                    // onClick={() => domainData(topic.topic_name)}
                  >
                    <Link
                      className="btn btn-primary topic_btn"
                      to={{
                        pathname: `/AdminTopic`,
                        search: topic.topic_name,
                      }}
                    >
                      {topic.topic_name}
                    </Link>
                  </div>
                ));
              return <div>{topics}</div>;
            })}
        </div>
      )}
    </div>
  );
}

export default TopicButtons;

// import React from "react";
// import APIService from "./APIService";
// import { Link } from "react-router-dom";

// function TopicButtons(props) {
//   const scrapeTopics = () => {
//     APIService.InsertSubTopic()
//       .then((resp) => resp.json())
//       .catch((error) => console.log(error));
//   };

//   return (
//     <div>
//       {props.topics &&
//         props.topics.map((topics) => {
//           const total_topics = topics.domain_topics.length;
//           const topic = [];
//           let i = 1;
//           for (var k in topics.domain_topics) {
//             topic.push(
//               <Link
//                 className="btn btn-primary topic_btn"
//                 // to={`/SubTopics/${"haha"}`}
//                 onClick={scrapeTopics}
//                 to={{
//                   pathname: `/SubTopics`,
//                   search: topics.domain_topics[k],
//                 }}
//               >
//                 {topics.domain_topics[k]}
//               </Link>
//             );

//             i++;
//           }
//           return <div>{topic}</div>;
//         })}
//     </div>
//   );
// }

// export default TopicButtons;
