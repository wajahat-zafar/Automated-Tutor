import React from "react";
import { Link } from "react-router-dom";
import APIService from "./APIService";
import { Container, Col, Row, Button } from "react-bootstrap";
import Slider from "react-slick";
import LoginBg from "../images/main_bg.png";
import PageBg from "../images/pages_bg.png";
import About from "./About";
import Usage from "./Usage";
import Header from "./Header";
import BgHeader from "./BgHeader";

function MainPage() {
  var settings = {
    dots: false,
    infinite: false,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    className: "homeSlider",
  };

  return (
    <>
      <div className="splash">
        {/* <img
          // src="/landing.png"
          src={LoginBg}
          className="bg_image"
          style={{
            width: "100%",
            height: "100%",
            position: "absolute",
            left: "0",
          }}
        ></img>
        <img
          src={PageBg}
          className="bg_image_resp"
          style={{
            width: "100%",
            height: "100%",
            position: "absolute",
            left: "0",
          }}
        ></img>
        <Header user="Not Logged In" /> */}
        <BgHeader page="home" />

        <div className="newdata">
          <div className="all_data">
            <h1 className="main_heading">AUTOMATED TUTOR</h1>
            <p className="subhead">Improve your learning in a single step!</p>
            {/* <p className="datap">
          Welcome to the platform which gives you a precise information
          regarding any topic.
        </p> */}
            {/* <div className="nonlog"> */}
            <Slider {...settings}>
              <div>
                <div className="column_flex">
                  <p className="datap">
                    Welcome to the platform which gives you a precise
                    information regarding any topic.
                  </p>
                  <a href="#about" className="main_btn">
                    Read More
                  </a>
                </div>
              </div>
              <div>
                <div className="column_flex">
                  <p className="datap">
                    Learn How To Use Autotmated Tutor with the below steps...
                  </p>
                  <a href="#usage" className="main_btn">
                    How to use it?
                  </a>
                </div>
              </div>
              <div>
                <div className="column_flex">
                  <p className="datap">
                    Login to your account or signup if you are new here.
                  </p>
                  <div className="flex_center">
                    <a href="/Login" className="main_btn">
                      Login
                    </a>
                    <a href="/Signup" className="main_btn">
                      Signup
                    </a>
                  </div>
                </div>
              </div>
            </Slider>
          </div>
        </div>
      </div>
      <About id="about" />
      <Usage id="usage" />
    </>

    // {/* <div className="domain">
    //     <button className="btn btn-primary domain_btn">
    //       Computer Networks
    //     </button>
    //     <Link to="/CN" className="btn btn-primary domain_btn">
    //       ABC
    //     </Link>
    //   </div>
    //   <div className="domain">
    //     <button className="btn btn-primary domain_btn">Programming</button>
    //     <Link to="/Prog" className="btn btn-primary domain_btn">
    //       Programming
    //     </Link>
    //   </div> */}
    // </div>
  );
}

export default MainPage;
