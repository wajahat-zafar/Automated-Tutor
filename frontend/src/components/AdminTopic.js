import React, { useState, useEffect } from "react";
import "../App.css";
import MainPage from "./MainPage";
import "../../node_modules/react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import DomainBtn from "./DomainBtn";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Button } from "react-bootstrap";
import httpClient from "./httpClient";
import { User } from "../type";
import { useLocation } from "react-router-dom";
import AdminTopics from "./AdminTopics";
import TopicButtons from "./TopicButtons";

function AdminTopic(props) {
  const [user, setUser] = useState(User);
  const [show, setShow] = useState(false);
  const [name, setName] = useState("");
  const [data, setData] = useState("");

  //   const { user1 } = useLocation();
  //   console.log(user1);
  let navigate = useNavigate();
  //   const query = useLocation();
  //   console.log(query.data);
  const data1 = useLocation();
  console.log(data1);
  //   const { data } = data1.state;
  //   console.log(data);
  const heading = data1.search.slice(1);
  console.log(heading);
  //   const data = data1.search.slice(2);
  //   console.log(data);
  const heading1 = decodeURI(heading);

  const logoutUser = async () => {
    await httpClient.post("http://localhost:5000/logout");
    window.location.href = "/";
  };

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("http://localhost:5000/info");
        setUser(resp.data);

        const name = heading1;
        const response = await fetch(
          "http://localhost:5000/getDomainName/<name>/",
          {
            method: "POST",
            headers: {
              "Content-type": "application/json",
            },
            body: JSON.stringify({ name: name }),
          }
        );
        console.log(response);
        const newData = await response.json();
        console.log(newData[0].domain_name);
        setData(newData[0].domain_name);

        // const resp2 = await httpClient.get(
        //   "http://localhost:5000/getDomain/<name>/"
        // );
        // console.log(resp2.data);
        // setData(resp2.data);

        // console.log(name);
        // const resp2 = await httpClient.get("http://localhost:5000/get/<name>/");
        // console.location(resp2);
      } catch (error) {
        console.log("Not authenticated");
      }
    })();
  }, []);

  const addTopic = async () => {
    console.log(name);
    const obj = { id: heading, name: name };

    try {
      const resp = await httpClient.post("http://localhost:5000/addTopic", {
        mode: "cors",
        obj,
      });
      console.log(resp.data);
      // alert("Topic Added");
      // navigate("/AdminTopic", { replace: false });
    } catch (error) {
      if (error.response.status === 401) {
        console.log(error.response);
        alert(error.response.data.error);
      }
    }
  };

  return (
    <div className="main">
      {user != null ? (
        <div>
          <div className="App">
            <nav className="navbar navbar-expand-md navbar-light">
              <a className="navbar-brand">
                <h1 className="logo">AT</h1>
              </a>
              <button
                className="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
              >
                <span className="navbar-toggler-icon"></span>
              </button>
              <div
                className="collapse navbar-collapse justify-content-end"
                id="navbarSupportedContent"
              >
                <ul className="navbar-nav mr-auto">
                  <li className="nav-item">
                    <Button
                      className="mt-2 btn signup_btn"
                      // variant="outline-secondary"
                      onClick={() => setShow(!show)}
                    >
                      Add Topic
                    </Button>
                  </li>
                  <li className="nav-item">
                    <Button
                      className="mt-2 btn signup_btn"
                      // variant="outline-secondary"
                      onClick={logoutUser}
                    >
                      Logout
                    </Button>
                  </li>
                </ul>
              </div>
            </nav>

            <div className="admin-data">
              <h3
                style={{ position: "relative", paddingTop: "20px" }}
                className="main_heading"
              >
                {data}
              </h3>
              <p>Below are the Topics</p>

              {show ? (
                <div className="newDomain">
                  <form
                    class="form-detail"
                    action="#"
                    method="post"
                    // onSubmit={handleSubmit}
                  >
                    <h6 className="add-heading">Add New Topic</h6>
                    <input
                      type="text"
                      placeholder="Enter domain name"
                      className="add-domain"
                      name="name"
                      id="name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                    />
                    <button className="btn signup_btn" onClick={addTopic}>
                      Add
                    </button>
                  </form>{" "}
                </div>
              ) : (
                <div className="newDomain" style={{ display: "none" }}></div>
              )}
              <div>
                <AdminTopics name={heading} />
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="App">
          <img
            src="/landing.png"
            style={{
              width: "100%",
              height: "100%",
              position: "absolute",
              left: "0",
            }}
          ></img>
          <nav className="navbar navbar-expand-md navbar-light">
            <a className="navbar-brand">
              <h1 className="logo">AT</h1>
            </a>
            <button
              className="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target="#navbarSupportedContent"
              aria-controls="navbarSupportedContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div
              className="collapse navbar-collapse justify-content-end"
              id="navbarSupportedContent"
            >
              <ul className="navbar-nav mr-auto">
                <li className="nav-item">
                  <Button className="mt-2 btn signup_btn">About</Button>
                </li>
                <li className="nav-item">
                  <Button className="mt-2 btn signup_btn">Contact</Button>
                </li>
              </ul>
            </div>
          </nav>
          <MainPage />
          <p className="datap">LOGIN BEFORE YOU CONTINUE</p>

          <div className="nonlog">
            <Container>
              <Col className="mt-4">
                <Row md={6}>
                  <a href="/Login">
                    {" "}
                    <Button className="btn domain_btn">Login</Button>
                  </a>
                </Row>
                <Row md={6}>
                  <p className="orr">OR</p>
                </Row>
                <Row md={6}>
                  <a href="/Signup">
                    <Button className="btn domain_btn">Signup</Button>
                  </a>
                </Row>
              </Col>
            </Container>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminTopic;
