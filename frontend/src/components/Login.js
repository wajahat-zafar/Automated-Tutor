import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import httpClient from "./httpClient";
import { User } from "../type";
import { message } from "antd";
import loginImage from "../images/login.png";

function Login() {
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");
  const [userd, setUserD] = useState(User);
  let navigate = useNavigate();
  useEffect(() => {
    (async () => {
      try {
        const resp = await httpClient.get("http://localhost:5000/info", {
          mode: "cors",
        });
        console.log(resp.data);
        setUserD(resp.data);
        navigate("/", { replace: false });
      } catch (error) {
        console.log("Not authenticated");
      }
    })();
  }, []);

  const LogInUser = async () => {
    console.log(user, password);
    const obj = { user: user, password: password };
    try {
      const resp = await httpClient.post("http://localhost:5000/login", {
        mode: "no-cors",
        "Content-type": "application/json",
        obj,
      });

      // resp.setHeader("Access-Control-Allow-Origin", "http:http://localhost:5000");
      // resp.setHeader("Access-Control-Allow-Credentials", "true");
      // resp.setHeader(
      //   "Access-Control-Allow-Methods",
      //   "GET,HEAD,OPTIONS,POST,PUT"
      // );
      // resp.setHeader(
      //   "Access-Control-Allow-Headers",
      //   "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
      // );

      // window.location.href = "/";
      console.log(resp.data);
      // if (resp.data.Message == "Welcome Admin") {
      //   navigate("/AdminHome", { replace: false });
      // } else {
      //   navigate("/", { replace: false });
      // }
      message.success("Successfully Logged In.");
      navigate("/", { replace: false });
    } catch (error) {
      console.log(error);
      if (error.response.status === 401) {
        console.log(error.response);
        message.error(error.response.data.error);
      }
    }
  };

  return (
    // <div className="wrapper1 Login form-v6">
    <div className="form-v6">
      {/* <div className="backbtn">
        <Link to="/">
          <a href="#"> Back</a>
        </Link>
      </div> */}
      <div className="page-content login">
        <h3 className="main_heading">AUTOAMTED TUTOR</h3>
        <div className="form-v6-content">
          <div class="form-left">
            {/* <img src="/login.png" className="my_image" alt="form" /> */}
            <img src={loginImage} className="my_image" alt="form" />
          </div>
          <form
            class="form-detail"
            action="#"
            method="post"
            // onSubmit={handleSubmit}
          >
            {/* <header>Login Form</header> */}
            {/* <form method="post" onSubmit={handleSubmit}> */}
            <div className="field email form-row">
              {/* <div className="input-area"> */}
              <p>Username*</p>
              <input
                type="text"
                className="form-control input-text"
                placeholder="Enter username"
                name="username"
                id="username"
                value={user}
                onChange={(e) => setUser(e.target.value)}
                required
              />
              {/* </div> */}
            </div>
            <div className="field password form-row">
              {/* <div className="input-area"> */}
              <p>Password*</p>
              <input
                type="password"
                className="form-control input-text"
                placeholder="Enter password"
                name="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              {/* </div> */}
            </div>
            <div class="form-row-last">
              <input
                type="button"
                className="register"
                value="Login"
                onClick={() => LogInUser()}
              />
              {/* <p>{output}</p> */}
              {/* <div className="sign-txt"> */}
              <p>
                Not yet member?
                <Link to="/Signup">
                  <a href="#"> Signup now</a>
                </Link>
              </p>
            </div>
            {/* </div> */}
          </form>
        </div>
      </div>
    </div>
    /* <div className="Login">
      <form method="post" onSubmit={handleSubmit}>
        <h3 className="fomr-heading">Sign In</h3>

        <div className="form-group main-form">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            className="form-control"
            placeholder="Enter username"
            name="username"
            id="username"
            onChange={handleUser}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            className="form-control"
            placeholder="Enter password"
            name="password"
            id="password"
            onChange={handlePassword}
            required
          />
        </div> 
    
        <div className="form-group">
          <div className="custom-control custom-checkbox">
            <input
              type="checkbox"
              className="custom-control-input"
              id="customCheck1"
            />
            <label className="custom-control-label" htmlFor="customCheck1">
              Remember me
            </label>
          </div>
        </div>

    <button
          type="submit"
          className="btn btn-primary btn-block submit-btn"
          // onClick={signin}
        >
          Submit
        </button>
        <div class="bottom-links">
          <p>
            Don’t have account? <a href="#">Sign up</a>
          </p>
        </div>
        <p>{output}</p>
       </form>
     </div> */
  );
}

export default Login;
