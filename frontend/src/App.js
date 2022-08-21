import React, { useState, useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import MainPage from "./components/MainPage";
import "../node_modules/react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import DomainBtn from "./components/DomainBtn";
import { Container, Row, Col, Button, Modal } from "react-bootstrap";
// import "../react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import httpClient from "./components/httpClient";
import { User } from "./type";
import AdminHome from "./components/AdminHome";
import { useNavigate } from "react-router-dom";
import { RevolvingDot } from "react-loader-spinner";
import "antd/dist/antd.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import BgHeader from "./components/BgHeader";

function App() {
  const [user, setUser] = useState(User);
  console.log(user);
  const [loggedIn, setLoggedIn] = useState();
  const [search, setSearch] = useState("");
  const [searching, setSearching] = useState(false);
  const [message, setMessage] = useState(false);
  let navigate = useNavigate();
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("//localhost:5000/info", {
          mode: "cors",
        });
        // resp.setHeader("Access-Control-Allow-Origin", "http://localhost:3000");
        // resp.setHeader("Access-Control-Allow-Credentials", "true");
        // resp.setHeader(
        //   "Access-Control-Allow-Methods",
        //   "GET,HEAD,OPTIONS,POST,PUT"
        // );
        // resp.setHeader(
        //   "Access-Control-Allow-Headers",
        //   "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
        // );
        console.log(resp?.data);
        setUser(resp?.data);
        setLoggedIn(true);
      } catch (error) {
        console.log("Not authenticated");
        setLoggedIn(false);
      }
    })();
  }, [loggedIn]);

  const searchResult = async () => {
    setSearching(true);
    setMessage("Searching Links");
    const modal = document.querySelector(".modal-backdrop");
    modal.classList.remove("show");
    modal.style.display = "none";
    const obj = { search: search };
    try {
      const resp = await httpClient.post("//localhost:5000/searchResult", {
        mode: "cors",
        obj,
      });
      console.log(resp.data);
      navigate(
        "/SearchResult",
        // { replace: false },
        { state: { data: resp.data, search: search } }
      );
    } catch (error) {
      if (error.response.status === 401) {
        console.log(error.response);
        alert(error.response.data.error);
      }
    }
  };

  const searchResultAuto = async () => {
    setSearching(true);
    setMessage("Searching Links");
    const modal = document.querySelector(".modal-backdrop");
    modal.classList.remove("show");
    modal.style.display = "none";
    setTimeout(() => {
      setMessage("Summarizing Data");
    }, 15000);
    const obj = { search: search };
    try {
      const resp = await httpClient.post("//localhost:5000/searchResultAuto", {
        mode: "cors",
        obj,
      });
      console.log(resp.data);
      setMessage("Gathering Youtube Data");
      const name = resp.data;
      navigate({
        pathname: "/HomePage",
        search: `?${name}`,
      });
    } catch (error) {
      if (error.response.status === 401) {
        console.log(error.response);
        alert(error.response.data.error);
      }
    }
  };

  const inputChange = () => {
    setSearch(document.querySelector("#title").value);
  };
  const handleKeypress = (e) => {
    //it triggers by pressing the enter key
    if (e.keyCode === 13) {
      searchResult();
    }
  };

  return (
    <div className="main">
      {searching ? (
        <div className="loader">
          <RevolvingDot
            ariaLabel="loading-indicator"
            radius="4"
            color="#0093ab"
            width="110"
            height="110"
          />
          <h6 className="subhead">{message}</h6>
        </div>
      ) : loggedIn ? (
        user.type === "user" ? (
          <div className="home">
            <BgHeader />
            <div className="container2">
              {/* <MainPage /> */}
              <div>
                <h1 className="main_heading">AUTOMATED TUTOR</h1>
                <p className="subhead">
                  Improve your learning in a single step!
                </p>
                <div className="search">
                  <form class="d-flex" id="myform" action="#">
                    <input
                      className="me-2 searchbar"
                      name="title"
                      id="title"
                      type="search"
                      placeholder="Search"
                      aria-label="Search"
                      value={search}
                      required
                      onKeyPress={handleKeypress}
                      // onChange={(e) => setSearch(e.target.value)}
                      onChange={inputChange}
                    />
                    {/* <button
                      className="select-btn"
                      id="search-btn"
                      type="button"
                      data-toggle="modal"
                      data-target="#exampleModal"
                    >
                      Search
                    </button> */}
                    <Button
                      className="select-btn"
                      id="search-btn"
                      type="button"
                      onClick={handleShow}
                    >
                      Search
                    </Button>
                  </form>
                  <Modal
                    show={show}
                    onHide={handleClose}
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                  >
                    <Modal.Header closeButton>
                      <Modal.Title>Select Type</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                      <button
                        className="select-btn"
                        type="button"
                        data-toggle="modal"
                        data-target="#exampleModal"
                        onClick={() => searchResult()}
                      >
                        Select Links
                      </button>
                      <button
                        className="select-btn"
                        type="button"
                        data-toggle="modal"
                        data-target="#exampleModal"
                        onClick={() => searchResultAuto()}
                      >
                        Auto Select Links
                      </button>
                    </Modal.Body>
                  </Modal>
                  {/* <div
                    className="modal fade"
                    id="exampleModal"
                    tabindex="-1"
                    role="dialog"
                    aria-labelledby="exampleModalLabel"
                  >
                    <div
                      className="modal-dialog modal-dialog-centered"
                      role="document"
                    >
                      <div className="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title" id="exampleModalLabel">
                            Select Type
                          </h5>
                          <button
                            type="button"
                            class="close"
                            data-dismiss="modal"
                            aria-label="Close"
                          >
                            <span aria-hidden="true">&times;</span>
                          </button>
                        </div>
                        <div class="modal-body">
                          <button
                            className="select-btn"
                            type="button"
                            data-toggle="modal"
                            data-target="#exampleModal"
                            onClick={() => searchResult()}
                          >
                            Select Links
                          </button>
                          <button
                            className="select-btn"
                            type="button"
                            data-toggle="modal"
                            data-target="#exampleModal"
                            onClick={() => searchResultAuto()}
                          >
                            Auto Select Links
                          </button>
                        </div>
                      </div>
                    </div>
                  </div> */}
                  {/* <DomainBtn user="Logged In" /> */}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <AdminHome />
        )
      ) : (
        // <div>
        <div className="App">
          <MainPage />
        </div>
        // </div>
      )}
    </div>
  );
}

export default App;
