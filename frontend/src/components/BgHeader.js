import React from "react";
import Header from "./Header";
import HomeBg from "../images/home_bg.png";
import PageBg from "../images/pages_bg.png";
import LoginBg from "../images/main_bg.png";

function BgHeader(props) {
  return (
    <>
      {props.page === "page" ? (
        <>
          <img
            src={PageBg}
            className="bg_image_resp3"
            style={{
              width: "100%",
              height: "100%",
              position: "absolute",
              left: "0",
            }}
          ></img>
          <Header user="Logged In" />
        </>
      ) : props.page === "home" ? (
        <>
          <img
            src={LoginBg}
            className="bg_image2"
            style={{
              width: "100%",
              height: "100%",
              position: "absolute",
              left: "0",
            }}
          ></img>
          <img
            src={PageBg}
            className="bg_image_resp2"
            style={{
              width: "100%",
              height: "100%",
              position: "absolute",
              left: "0",
            }}
          ></img>
          <Header user="Not Logged In" />
        </>
      ) : (
        <>
          <img
            src={HomeBg}
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
          <Header user="Logged In" />
        </>
      )}
    </>
  );
}

export default BgHeader;
