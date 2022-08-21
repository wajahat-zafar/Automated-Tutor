import { Link, Route } from "react-router-dom";
import APIService from "./APIService";
import React, { useState, useEffect } from "react";
import { Alert } from "react-bootstrap";
import AdminTopic from "./AdminTopic";

function DomainBtn(props) {
  const [data, setData] = useState(null);

  const scrapeTopics = () => {
    APIService.InsertTopic()
      .then((resp) => resp.json())
      .catch((error) => console.log(error));
  };

  // const getTopics = (name) => {
  //   // alert(name);
  //   APIService.Topics(name)
  //     .then((resp) => resp.json())
  //     .catch((error) => console.log(error));
  // };

  const getTopics = async (name) => {
    alert(name);
    fetch("http://localhost:5000/get/<name>/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ name: name }),
    })
      .then((resp) => resp.json())
      .then((resp) => console.log(resp))
      .then((resp) => setData(resp))
      .catch((error) => console.log(error));
  };

  // const [domain, setDomains] = useState([]);

  // useEffect(() => {
  //   fetch("http://localhost:5000/getDomain", {
  //     method: "GET",
  //     headers: {
  //       "Content-type": "application/json",
  //     },
  //   })
  //     .then((resp) => resp.json())
  //     .then((resp) => console.log(resp[0].domain_name))
  //     .then((resp) => setDomains(resp))
  //     // .then((resp) => setTopics(resp))
  //     .catch((error) => console.log(error));
  // }, []);

  return (
    <div>
      {props.type != "admin" ? (
        <div className="domain">
          <Link
            // to="/MC"
            onClick={scrapeTopics}
            className="btn btn-primary domain_btn"
            // user={props.user}
            to={{
              pathname: `/MC`,
              search: props.user,
            }}
          >
            Computer Networks
          </Link>
        </div>
      ) : (
        <div className="domain">
          {props.domain &&
            props.domain.map((domain) => {
              var domains = new Array(domain.length)
                .fill(0)
                .map((zero, index) => (
                  <div
                    className="topics"
                    key={index}
                    // onClick={() => getTopics(domain.domain_id)}
                  >
                    <Link
                      className="btn btn-primary topic_btn"
                      // onClick={() => getTopics(domain.domain_id)}
                      to={{
                        pathname: `/AdminTopic`,
                        search: JSON.stringify(domain.domain_id),
                        // search: `?data=${data}`,
                        // state: {
                        //   user1: JSON.stringify({
                        //     id: 1,
                        //     name: "sabaoon",
                        //     shirt: "green",
                        //   }),
                        // },

                        // search: new URLSearchParams({
                        //   name: domain.domain_name,
                        //   dataa: { data },
                        // }),
                      }}
                      // state={{ data: data }}
                    >
                      {domain.domain_name}
                    </Link>
                  </div>
                ));
              return <div>{domains}</div>;
            })}
        </div>
      )}
    </div>
  );
}

export default DomainBtn;
