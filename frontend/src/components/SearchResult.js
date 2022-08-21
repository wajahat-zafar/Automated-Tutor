import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import httpClient from "./httpClient";
import { User } from "../type";
import { Container, Row, Col, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Header from "./Header";
import { message } from "antd";
import { RevolvingDot } from "react-loader-spinner";
import BgHeader from "./BgHeader";

function SearchResult(props) {
  // const [checked, setChecked] = useState(false);
  const checkedList = [];
  const [user, setUser] = useState(User);
  const [searching, setSearching] = useState(false);
  const [messagee, setMessage] = useState("Scraping Data");
  const [name, setName] = useState();
  const { state } = useLocation();
  // console.log(state);
  // const data = props.location.state.data;
  // console.log(state.data);
  const data = state.data;
  const search = state.search;
  console.log(data);
  // console.log(search);
  let navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("//localhost:5000/info");
        console.log(resp.data);
        setUser(resp.data);
      } catch (error) {
        console.log("Not authenticated");
        navigate("/", { replace: false });
      }
    })();
  }, []);

  const handleClick = (e, link) => {
    // console.log(e.target.attributes.for.value);
    e.preventDefault();
    const itemindex = checkedList.findIndex((item) => item === link);
    if (e.target.style.backgroundColor != "rgb(0, 60, 153)") {
      e.target.style.backgroundColor = "rgb(0, 60, 153)";
      e.target.style.color = "white";
      e.target.style.border = "none";
      checkedList.push(link);
    } else {
      e.target.style.backgroundColor = "white";
      e.target.style.color = "rgb(0, 60, 153)";
      e.target.style.border = "1px solid rgb(0, 60, 153)";
      checkedList.splice(itemindex, 1);
    }
    console.log(checkedList);
  };

  const findSummary = async () => {
    console.log(search);
    setName(search);
    if (checkedList.length == 0) {
      message.warning("please select at least one link.");
    } else {
      setSearching(true);
      console.log(document.getElementsByClassName("loader-text"));
      setTimeout(() => {
        setMessage("Summarizing Data");
      }, 15000);
      const obj = { checkedList: checkedList, topic: search };
      try {
        const resp = await httpClient.post("//localhost:5000/search", {
          mode: "cors",
          obj,
        });
        setMessage("Gathering Youtube Data");
        console.log(resp.data);
        const name = resp.data;
        // navigate(
        //   "/SearchResult",
        //   // { replace: false },
        //   { state: { data: resp.data, search: search } }
        // );
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
    }
  };

  return (
    <div className="main">
      {/* <nav className="navbar navbar-expand-md navbar-light">
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
                onClick={logoutUser}
              >
                Logout
              </Button>
            </li>
          </ul>
        </div>
      </nav> */}
      {searching ? (
        <div className="loader">
          <h3 className="main_heading">{name.toUpperCase()}</h3>
          <RevolvingDot
            ariaLabel="loading-indicator"
            radius="4"
            color="#0093ab"
            width="110"
            height="110"
          />
          <h6 className="subhead loader-text">{messagee}</h6>
        </div>
      ) : (
        <div className="links_page">
          {/* <Header user="Logged In" /> */}
          <BgHeader page="page" />
          <div className="main_data">
            <h1 className="main_heading">{search.toUpperCase()}</h1>
            <div className="links">
              {data &&
                data.map((result, index) => {
                  var results = new Array(1).fill(0).map((zero) => (
                    <div className="search-results">
                      <div className="link-result">
                        <div className="doamain-name">{result[1]}</div>
                        <div className="result-name">
                          <a href={result[1]} target="_blank">
                            {result[0]}
                          </a>
                        </div>
                        <div className="result-description">{result[2]}</div>
                      </div>
                      <div className="search-checkbox">
                        <input
                          type="checkbox"
                          className="btn-check"
                          id={index}
                          // checked={checked}
                        />
                        <button
                          className="select-btn"
                          for={index}
                          onClick={(e) => handleClick(e, result[1])}
                        >
                          Select
                        </button>
                      </div>
                    </div>
                  ));
                  return <div>{results}</div>;
                })}
            </div>
            <button className="mb-4 main_btn" onClick={() => findSummary()}>
              Get Summary
            </button>
          </div>
        </div>
      )}

      {/* <p>{data}</p> */}
      {/* <div className="search-results">
        <div className="doamain-name">ABCD</div>
        <input
          type="checkbox"
          className="btn-check"
          id="1"
          autocomplete="off"
        />
        <label
          className="btn btn-outline-primary"
          // style={{ marginLeft: "-100px" }}
          for="1"
        >
          Select
        </label>
        <div className="result-name">
          <a href="#">NAME</a>
        </div>
        <div className="result-description">Description</div>
      </div> */}
      {/* {data &&
        data.map((result, index) => {
          var results = new Array(1).fill(0).map((zero) => (
            <div className="search-results">
              <div className="link-result">
                <div className="doamain-name">{result[1]}</div>
                <div className="result-name">
                  <a href="#">{result[0]}</a>
                </div>
                <div className="result-description">{result[2]}</div>
              </div>
              <div className="search-checkbox">
                <input
                  type="checkbox"
                  className="btn-check"
                  id={index}
                  // checked={checked}
                />
                <button
                  className="select-btn"
                  for={index}
                  onClick={(e) => handleClick(e, result[1])}
                >
                  Select
                </button>
              </div>
            </div>
          ));
          return <div>{results}</div>;
        })} */}
      {/* <Link
        className="btn mb-4 signup_btn"
        to={{
          pathname: `/HomePage`,
          search: search,
        }}
        onClick={() => findSummary()}
      >
        search
      </Link> */}
    </div>
  );
}

export default SearchResult;
