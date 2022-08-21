import React from "react";
import { useLocation } from "react-router-dom";
import TopicButtons from "./TopicButtons";
import { useState, useEffect } from "react";
import Header from "./Header";
import { Container, Row, Col, Button } from "react-bootstrap";
import httpClient from "../components/httpClient";

function MC(props) {
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/get", {
      method: "GET",
      headers: {
        "Content-type": "application/json",
      },
    })
      .then((resp) => resp.json())
      .then((resp) => setTopics(resp))
      // .then((resp) => setTopics(resp))
      .catch((error) => console.log(error));
  }, []);
  // alert(topics);
  const data1 = useLocation();
  const user = data1.search.slice(1);
  const info = decodeURI(user);
  console.log(info);

  const logoutUser = async () => {
    await httpClient.post("http://localhost:5000/logout");
    window.location.href = "/";
  };
  return (
    <div className="">
      {info == "Logged In" ? (
        <div>
          <div className="text-center">
            {/* <div className="header row">
              <div className="col-md-9">
                <h1 className="logo">AT</h1>
              </div>
              <div className="col-md-3">
                <Button
                  className="mt-2 btn signup_btn"
                  // variant="outline-secondary"
                  onClick={logoutUser}
                >
                  Logout
                </Button>
              </div>
            </div> */}
            <Header user="Logged In" />

            <h1 className="main_heading">Computer Networks</h1>
          </div>
          <TopicButtons user="Logged In" type="user" topics={topics} />
        </div>
      ) : (
        <div></div>
      )}
    </div>
  );
}

export default MC;
