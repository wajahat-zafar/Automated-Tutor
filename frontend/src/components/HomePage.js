import React from "react";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import HomeData from "./HomeData";
import { RevolvingDot } from "react-loader-spinner";
import Header from "./Header";
import APIService from "./APIService";
import { Link } from "react-router-dom";
import Char2D from "./char2D";
import httpClient from "./httpClient";
import { User } from "../type";
import { useNavigate } from "react-router-dom";
import BgHeader from "./BgHeader";
import ReactTooltip from "react-tooltip";

function HomePage() {
  const data1 = useLocation();
  const heading = data1.search.slice(1);
  const heading1 = decodeURI(heading);
  console.log(heading1);
  const links = data1?.state?.links;
  let navigate = useNavigate();

  const [user, setUser] = useState(User);
  const [yt, setYt] = useState([]);
  const [data, setData] = useState("");
  const [canClick, setCanClick] = useState(false);
  const [fetchresult, setfetchresult] = useState("Summarizing Data");
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const response = await httpClient.get("http://localhost:5000/info");
        setUser(response.data);

        // const resp = await fetch("http://localhost:5000/getData", {
        //   method: "POST",
        //   headers: {
        //     "Content-type": "application/json",
        //   },
        //   body: JSON.stringify({ name: heading1 }),
        // });
        // console.log(resp);
        // const newData = await resp.json();
        // console.log(newData[0].scraped_dataa);
        // setData(newData[0].scraped_dataa);

        setfetchresult("Finalizing Data");
        const resp2 = await fetch("http://localhost:5000/getDataSum", {
          method: "POST",
          headers: {
            "Content-type": "application/json",
          },
          body: JSON.stringify({ name: heading1 }),
        });
        const newData2 = await resp2.json();
        console.log(newData2[0].summary);
        // setSummary(newData2[0].summary);

        // const regex = /(.[^:\s]+):([^:\s]+)/;
        // const regex2 = /(.[^:\s]+)+(?: \w+)*:/g;
        // const regex3 = /:\s*([^.]*)/;
        // const regex4 = /\w+(?: \w+)*:/;
        // const regex5 = /(?: \w+)+(?: \w+)*.\./;
        // const regex6 = /\w+:\s\w+/;
        // const regex7 = /\:([^.]*)./;
        const str = `. types abcd: sdi asnd. xyz: sads.`;

        var heading_data = [];
        var text_data = [];
        // console.log(regex.exec(str));
        // console.log(regex2.exec(str));
        // console.log(regex3.exec(str));
        // console.log(regex4.exec(str));
        // console.log(regex5.exec(str));
        // console.log(regex6.exec(str));
        // console.log(regex7.exec(str));

        // var re2 = /([\s\w]+)*:([^.]*)/gi;
        var headingregex = /(\w+-*[\w)+\s(]*):+/gi;
        var textr = /:\s+([^.]*.)/gi;
        let m;
        let newsum = newData2[0].summary.replace(/[\r\n]+/g, " ");
        let x = newsum.replace(/[\r-]+/g, " ");

        // var textregex = /([^:]*(?=\.))/gi;
        while ((m = headingregex.exec(x)) !== null) {
          // console.log(m[1].toUpperCase());
          heading_data.push(m[0]);
        }
        while ((m = textr.exec(x)) !== null) {
          // console.log(m[1]);
          let newdata = m[1].replace(/[\r:]+/g, " ");
          text_data.push(newdata);
        }
        // var str2 =
        //   "key_1: some text, maybe a comma, ending in a semicolon. key_2: text with no ending semicolon.";
        // while ((m = re2.exec(str)) !== null) {
        //   // document.body.innerHTML += m[1] + ": " + m[2] + "<br/>";
        //   console.log(m[1] + ": " + m[2]);
        // }

        // const c = 0;
        // const head = regex2.exec(str)[0];
        // console.log(head);
        // for (let m = 0; m < regex2.exec(str).length; m++) {
        //   console.log(m);
        //   before.push(regex2.exec(str)[m]);
        // }

        // while ((m = regex2.exec(str)) !== null) {
        //   // console.log(m);
        //   before.push(m[1]);
        //   // after.push(m[2]);
        // }
        console.log(heading_data);
        console.log(text_data);
        setSummary(x);

        //function accepts a string to look through and a string to look for
        function boldString(str, find) {
          find.forEach((word) => {
            console.log(word);
            str = str.replace(
              word,
              `<br><b class="summ-heading-text">${word}</b><br>`
            );
          });
          return str;
        }

        //calls boldString() function and passes in the old-text content and looks for the string "ch"
        var result = boldString(x, heading_data);
        console.log(result);

        //this is just for this example, but updates the new-text element with the result of the function
        document.getElementById("summary").innerHTML = result;

        const fetchvid = async () => {
          // alert(heading1);
          // const response = await fetch(
          //   "http://localhost:5000/getrelated/<name>",
          //   {
          //     method: "POST",
          //     headers: {
          //       "Content-type": "application/json",
          //     },
          //     body: JSON.stringify({ name: heading1 }),
          //   }
          // )
          //   .then((resp) => resp.json())
          //   // .then((resp) => alert(resp))
          //   .then((resp) => setYt(resp))
          //   .catch((error) => console.log(error));

          const resp = await fetch("http://localhost:5000/getyt/<name>", {
            method: "POST",
            headers: {
              "Content-type": "application/json",
            },
            body: JSON.stringify({ name: heading1 }),
          });
          console.log(resp);
          const newData = await resp.json();
          console.log(newData);
          setYt(newData);

          //   const response = await fetch("http://localhost:5000/getyt/<name>", {
          //     method: "POST",
          //     headers: {
          //       "Content-type": "application/json",
          //     },
          //     body: JSON.stringify({ name: heading1 }),
          //   })
          //     .then((response) => response.json())
          //     .then((response) => console.log(response))
          //     .then((response) => setYt(response))
          //     .catch((error) => console.log(error));
        };
        fetchvid();
        // APIService.Quiz(heading1)
        //   .then((resp) => resp.json())
        //   .catch((error) => console.log(error));
        console.log("for quiz", heading1);
        const resp = await fetch("http://localhost:5000/quiz/<name>/", {
          method: "POST",
          headers: {
            "Content-type": "application/json",
          },
          body: JSON.stringify({ name: heading1 }),
        }).then((resp) => resp.json());
        setCanClick(true);
      } catch (error) {
        console.log("Not authenticated");
        navigate("/", { replace: false });
      }
    })();
  }, []);

  // useEffect(() => {

  // const fetchdata = async () => {
  //   const resp = fetch("http://localhost:5000/getData", {
  //     method: "GET",
  //     headers: {
  //       "Content-type": "application/json",
  //     },
  //   })
  //     .then((resp) => resp.json())
  //     // .then((resp) =>
  //     //   console.log(resp.filter((t) => t.topic_name == heading1)[0])
  //     // )
  //     .then(
  //       (resp) =>
  //         // resp.filter((t) => t.topic_name == heading1)[0].scraped_dataa
  //         resp.filter((t) => t.topic_name == heading1)[0].topic_id
  //     )
  //     .then((resp) => setData(resp));
  // };
  // const fetchsummary = async () => {
  //   console.log(data);
  //   const resp2 = await fetch("http://localhost:5000/getDataSum", {
  //     method: "POST",
  //     headers: {
  //       "Content-type": "application/json",
  //     },
  //     body: JSON.stringify({ tid: data }),
  //   })
  //     .then((resp2) => resp2.json())
  //     .then((resp2) => console.log(resp2[0].scraped_dataa))
  //     // .then(
  //     //   (resp) =>
  //     //     resp.filter((t) => t.topic_name == heading1)[0].topic_id
  //     // )
  //     .then((resp2) => setData(resp2[0].scraped_dataa));
  // };
  // fetchdata();
  // fetchvid();
  // fetchsummary();
  // }, []);

  const showQuiz = (heading1) => {
    // alert(heading1);
    // navigate("/Quiz", { replace: false });
    navigate({
      pathname: "/Quiz",
      search: `?${heading1}`,
    });
  };

  const download_data = (heading1) => {
    // alert(heading1);
    setfetchresult("Downloading Data");
    APIService.DownloadFile(heading1)
      .then((resp) => resp.json())
      .catch((error) => console.log(error));
    setfetchresult("Data Downlaoded!");
  };

  return (
    <div className="main">
      {summary.length === 0 ? (
        <div className="loader">
          <h3 className="main_heading">{heading1.toUpperCase()}</h3>
          <RevolvingDot
            ariaLabel="loading-indicator"
            radius="4"
            color="#0093ab"
            width="110"
            height="110"
          />
          <h6 className="subhead">{fetchresult}</h6>
        </div>
      ) : (
        <div className="main">
          <BgHeader page="page" />
          <div className="main_data">
            <div className="container">
              <h1 className="main_heading">{heading1.toUpperCase()}</h1>
              <div className="home-data">
                <div className="pt-3 pb-2">
                  <h3 className="subhead">Summary</h3>
                  <div className="summary-data">
                    <h3 className="subhead text-center">{heading1}</h3>
                    <p className="summary" id="summary">
                      {summary}
                    </p>
                    <br></br>
                    <h4>
                      Reference Link(s) from where the summary is generated:{" "}
                    </h4>
                    <p>{links}</p>
                  </div>
                  {/* <textarea readOnly value={data}></textarea> */}
                </div>
                <div className="flex_center">
                  <a>
                    <button
                      className="main_btn"
                      onClick={() => download_data(heading1)}
                    >
                      Download
                    </button>
                  </a>
                  <div
                    data-tip={
                      !canClick
                        ? "Button will enable once the quiz is created."
                        : "click to attempt quiz"
                    }
                  >
                    <button
                      className="main_btn"
                      style={
                        !canClick
                          ? {
                              pointerEvents: "none",
                              backgroundColor: "#5eb3bc",
                            }
                          : null
                      }
                      onClick={() => showQuiz(heading1)}
                      to={{
                        pathname: `/Quiz`,
                        search: heading1,
                      }}
                    >
                      Attempt Quiz
                    </button>
                    {/* <button onClick={() => showQuiz(heading1)}>Quiz</button> */}
                  </div>
                </div>
                <ReactTooltip />
              </div>
              {/* <p>{yt}</p> */}
              {/* <div className="mycard">
              <div className="mycard-img">
                <img src="../../public/second.png"></img>
              </div>
              <div className="mycard-data">
                <h6>NAME</h6>
                <hr />
                <div className="mycard-sub-data">
                  <button className="select_btn">View</button>
                  <p>DURATION</p>
                </div>
              </div>
            </div> */}

              <HomeData yt={yt} heading1={heading1} />
              <div>{/* <Char2D /> */}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
