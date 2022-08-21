import React from "react";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { RevolvingDot } from "react-loader-spinner";
import { message } from "antd";

function QuizQuestions(props) {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [answer, setAnswer] = useState(0);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e, i) => {
    const { value, name } = e.target;

    const newState = [...data];
    newState[i] = {
      ...newState[i],
      [name]: value,
    };

    setData(newState);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const undArr = [];
    if (data.length === 0) {
      message.error("answer all questions");
    } else {
      if (data.length == total) {
        for (let i = 0; i < data.length; i++) {
          if (typeof data[i] == "undefined") {
            undArr.push("undf");
          } else if (data[i][i] == "") {
            undArr.push("undf");
          }
        }
        console.log(undArr);
        if (undArr.length > 0) {
          message.error("answer all questions");
        } else {
          setSubmitting(true);
          const fetchAns = async () => {
            const resp = await fetch(
              "http://localhost:5000/checkAnswers/<name>",
              {
                method: "POST",
                headers: {
                  "Content-type": "application/json",
                },
                body: JSON.stringify({
                  mainQ: props.quiz_data[0].questions,
                  data: data,
                }),
              }
            );
            const newData = await resp.json();
            console.log(newData);
            setSubmitting(false);
            message.success("Answers are checked. Your score is at the end.");
            setAnswer(newData.output);
          };
          fetchAns();
        }
      } else {
        message.error("answer all questions");
      }
    }
  };
  useEffect(() => {
    setTotal(props.quiz_data[0].questions.length);
  }, []);

  return (
    <div className="">
      {submitting ? (
        <div className="loader">
          <RevolvingDot
            ariaLabel="loading-indicator"
            radius="4"
            color="#0093ab"
            width="110"
            height="110"
          />
          <h6 className="subhead">Checking Answers</h6>
        </div>
      ) : (
        <div className="QA">
          {props.quiz_data &&
            props.quiz_data.map((questions) => {
              console.log(questions);
              const numbers = questions["questions"];
              console.log(numbers.length);
              const listItems = numbers.map((number, index) => (
                <div key={index + 1}>
                  <h5 className="question">
                    Q.{index + 1} - {number.question}
                  </h5>
                  <textarea
                    name={index}
                    onChange={(e) => handleChange(e, index)}
                    className="ans_inp"
                  />
                </div>
              ));
              return (
                <div style={{ textAlign: "center", marginBottom: "20px" }}>
                  <form onSubmit={handleSubmit}>
                    {listItems}
                    <button type="submit" className="main_btn">
                      Submit
                    </button>
                  </form>
                  <br></br>
                  <h4 className="subhead">
                    Your Score: {answer}/{numbers.length}
                  </h4>
                </div>
              );
            })}
        </div>
      )}
    </div>
  );
}

export default QuizQuestions;
