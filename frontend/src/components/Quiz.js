import React from "react";
import { useLocation } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import QuizQuestions from "./QuizQuestions";
import Header from "./Header";
import { RevolvingDot } from "react-loader-spinner";
import { User } from "../type";
import httpClient from "./httpClient";
import { useNavigate } from "react-router-dom";
import BgHeader from "./BgHeader";

function Quiz() {
  const [user, setUser] = useState(User);
  const data1 = useLocation();
  const heading = data1.search.slice(1);
  const heading1 = decodeURI(heading);
  const [fetchresult, setfetchresult] = useState("Generating Quiz");
  let navigate = useNavigate();

  const [quiz_data, setQuizData] = useState([]);

  useEffect(() => {
    setfetchresult("Creating Quiz");

    (async () => {
      try {
        const response = await httpClient.get("http://localhost:5000/info");
        setUser(response.data);
        const fetchquiz = async () => {
          const resp = await fetch("http://localhost:5000/getquiz/<name>", {
            method: "POST",
            headers: {
              "Content-type": "application/json",
            },
            body: JSON.stringify({ name: heading1 }),
          });
          console.log(resp);
          const newData = await resp.json();
          console.log(newData);
          setQuizData(newData);
          // console.log(quiz_data);
        };
        fetchquiz();
      } catch (error) {
        console.log("Not authenticated");
        navigate("/", { replace: false });
      }
    })();
  }, []);

  return (
    <div>
      {quiz_data.length === 0 ? (
        <div className="loader">
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
        <>
          <BgHeader page="page" />

          <div className="main_data">
            <h1 className="main_heading">QUIZ</h1>
            <QuizQuestions quiz_data={quiz_data} />
          </div>
        </>
      )}
    </div>
  );
}

export default Quiz;
