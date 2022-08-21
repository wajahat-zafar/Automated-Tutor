import React, { useState, useEffect } from "react";
// import APIService from "./APIService";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import httpClient from "./httpClient";
import { User } from "../type";
import { message } from "antd";
import signupImage from "../images/signup.png";

function Login() {
  // const [output, setOut] = useState([]);
  const [name, setName] = useState("");
  const [user, setUser] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userd, setUserD] = useState(User);
  let navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const resp = httpClient.get("http://localhost:5000/info");
        console.log(resp.data);
        setUserD(resp.data);
        // navigate("/", { replace: false });
      } catch (error) {
        console.log("Not authenticated");
      }
    })();
  }, []);

  const User_Registration = async () => {
    console.log(name, user, email, password);
    if (
      user.length > 0 &&
      name.length > 0 &&
      email.length > 0 &&
      password.length > 0
    ) {
      const obj = { user: user, password: password, email: email, name: name };

      try {
        const resp = await httpClient.post("http://localhost:5000/signup", {
          mode: "cors",
          obj,
        });
        // resp.setHeader(
        //   "Access-Control-Allow-Origin",
        //   "//localhost:3000/signup"
        // );
        // window.location.href = "/";
        message.success("You are Registered Successfully");
        navigate("/Login", { replace: false });
      } catch (error) {
        if (error.response.status === 401) {
          console.log(error.response.data.error);
          message.error(error.response.data.error);
        }
      }
    }
  };

  return (
    <div className="form-v6">
      {/* <div className="backbtn">
        <Link to="/">
          <a href="#"> Back</a>
        </Link>
      </div> */}
      <div className="page-content">
        <h3 className="main_heading">AUTOAMTED TUTOR</h3>
        <div className="form-v6-content">
          <div class="form-left">
            {/* <img src="/signup.png" className="my_image" alt="form" /> */}
            <img src={signupImage} className="my_image" alt="form" />
          </div>
          <form
            class="form-detail"
            action="#"
            method="post"
            // onSubmit={handleSubmit}
          >
            <div className="form-group field form-row">
              <p>Full Name*</p>
              <input
                type="text"
                className="form-control input-text"
                placeholder="Enter Full Name"
                name="fname"
                id="fname"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
              {/* </div> */}
            </div>
            <div className="form-group field form-row">
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
            <div className="form-group field form-row">
              {/* <div className="input-area"> */}
              <p>Email*</p>
              <input
                type="email"
                className="form-control input-text"
                placeholder="Enter email"
                name="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              {/* </div> */}
            </div>

            <div className="form-group field form-row">
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

            {/* <div className="form-group">
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
        </div> */}
            <div class="form-row-last">
              <input
                type="button"
                className="register"
                value="Signup"
                onClick={() => User_Registration()}
              />
              <p>
                Already a member?
                <Link to="/Login">
                  <a href="#"> Login</a>
                </Link>
              </p>
            </div>

            {/* <p className="forgot-password text-right">
          Forgot <a href="#">password?</a>
        </p>  */}
          </form>
          {/* <div className="sign-txt">
        <p>Already a member?{" "}
        <Link to="/Login">
          <a href="#">Login</a>
        </Link></p>
      </div> */}
        </div>
      </div>
    </div>
  );
}

export default Login;
