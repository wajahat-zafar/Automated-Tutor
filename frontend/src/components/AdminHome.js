import React, { useState, useEffect } from "react";
import "../App.css";
import MainPage from "./MainPage";
import "../../node_modules/react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import DomainBtn from "./DomainBtn";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Button } from "react-bootstrap";
import httpClient from "./httpClient";
import { User } from "../type";
import AdminDomain from "./AdminDomain";

function AdminHome() {
  const [user, setUser] = useState(User);
  const [show, setShow] = useState(false);
  const [name, setName] = useState("");
  let navigate = useNavigate();

  const logoutUser = async () => {
    await httpClient.post("http://localhost:5000/logout");
    window.location.href = "/";
  };

  //   const addDomain = async () => {};

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("http://localhost:5000/info");
        setUser(resp.data);
      } catch (error) {
        console.log("Not authenticated");
      }
    })();
  }, []);

  const addDomain = async () => {
    console.log(name);
    const obj = { name: name };

    try {
      const resp = await httpClient.post("http://localhost:5000/addDomain", {
        mode: "cors",
        obj,
      });
      // resp.setHeader("Access-Control-Allow-Origin", "//localhost:3000/signup");
      // window.location.href = "/";
      alert("Domain Added");
      navigate("/AdminHome", { replace: false });
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
            {/* <img
              src="/landing.png"
              style={{
                width: "100%",
                height: "100%",
                position: "absolute",
                left: "0",
              }}
            ></img> */}
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
                      Add Domain
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
            {/* <div className="header row">
              <div className="col-md-8">
                <h1 className="logo">AT</h1>
              </div>
              <div className="col-md-2">
                <Button
                  className="mt-2 btn signup_btn"
                  // variant="outline-secondary"
                  onClick={() => setShow(!show)}
                >
                  Add Domain
                </Button>
              </div>
              <div className="col-md-2">
                <Button
                  className="mt-2 btn signup_btn"
                  // variant="outline-secondary"
                  onClick={logoutUser}
                >
                  Logout
                </Button>
              </div>
            </div> */}
            {/* <MainPage /> */}
            <div className="admin-data">
              {/* <div className="row">
                <div className="col-md-10"></div>
                <div className="col-md-2">
                  <Button
                    className="btn signup_btn"
                    // variant="outline-secondary"
                    onClick={() => setShow(true)}
                  >
                    Add Domain
                  </Button>
                </div>
              </div> */}
              <h3
                style={{ position: "relative", paddingTop: "20px" }}
                className="main_heading"
              >
                Welcome Admin
              </h3>
              <p className="subhead">Below are the domains</p>

              {show ? (
                <div className="newDomain">
                  <form
                    class="form-detail"
                    action="#"
                    method="post"
                    // onSubmit={handleSubmit}
                  >
                    <h6 className="add-heading">Add New Domain</h6>
                    <input
                      type="text"
                      placeholder="Enter domain name"
                      className="add-domain"
                      name="name"
                      id="name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                    />
                    <button className="btn signup_btn" onClick={addDomain}>
                      Add
                    </button>
                  </form>{" "}
                </div>
              ) : (
                <div className="newDomain" style={{ display: "none" }}></div>
              )}
              <div>
                <AdminDomain />
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

export default AdminHome;
