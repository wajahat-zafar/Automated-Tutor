import React from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { Container, Row, Col, Button, Navbar, Nav } from "react-bootstrap";
import httpClient from "./httpClient";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome } from "@fortawesome/free-solid-svg-icons";
import logo from "../images/logo.svg";

function Header(props) {
  let navigate = useNavigate();
  const routeChange = () => {
    let path = `Signup`;
    navigate(path);
  };

  const logoutUser = async () => {
    await httpClient.post("//localhost:5000/logout");
    window.location.href = "/";
  };
  const uploadDocument = async () => {
    navigate("/UploadDocument", { replace: false });
  };

  const element = <FontAwesomeIcon icon={faHome} />;

  return (
    <div className="header2">
      {props.user == "Logged In" ? (
        <Navbar bg="transparent" expand="md">
          <Container>
            <Navbar.Brand href="/">
              <img src={logo} alt="logo" width={70} height={70}></img>
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="justify-content-between">
                <h3 className="subhead">Automated Tutor</h3>
                <Nav.Link
                  className="header_btn"
                  // variant="outline-secondary"
                  onClick={uploadDocument}
                >
                  Upload Document
                </Nav.Link>
                <Nav.Link className="header_btn" onClick={logoutUser}>
                  Logout
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      ) : (
        // <nav className="navbar navbar-expand-md navbar-dark">
        //   {/* <a className="navbar-brand">
        //     <h1 className="logo">AT</h1>
        //   </a> */}
        //   {/* <a href="/">{element}</a> */}
        //   <a href="/">
        //     <img src={logo} alt="logo" width={70} height={70}></img>
        //   </a>

        //   <button
        //     className="navbar-toggler"
        //     type="button"
        //     data-toggle="collapse"
        //     data-target="#navbarSupportedContent"
        //     aria-controls="navbarSupportedContent"
        //     aria-expanded="false"
        //     aria-label="Toggle navigation"
        //   >
        //     <span className="navbar-toggler-icon"></span>
        //   </button>
        //   <div
        //     className="collapse navbar-collapse justify-content-end"
        //     id="navbarSupportedContent"
        //   >
        //     <ul className="navbar-nav">
        //       <h3 className="subhead">Automated Tutor</h3>
        //       <li className="nav-item">
        //         <a
        //           className="header_btn"
        //           // variant="outline-secondary"
        //           onClick={uploadDocument}
        //         >
        //           Upload Document
        //         </a>
        //       </li>
        //       <li className="nav-item">
        //         <a
        //           className="header_btn"
        //           // variant="outline-secondary"
        //           // data-toggle="modal"
        //           // data-target="#logoutModal"
        //           onClick={logoutUser}
        //         >
        //           Logout
        //         </a>
        //       </li>
        //     </ul>
        //     {/* <div
        //       className="modal fade"
        //       id="logoutModal"
        //       tabindex="-1"
        //       role="dialog"
        //       aria-labelledby="logoutModalLabel"
        //     >
        //       <div
        //         className="modal-dialog modal-dialog-centered"
        //         role="document"
        //       >
        //         <div className="modal-content">
        //           <div class="modal-header">
        //             <h5 class="modal-title" id="logoutModalLabel">
        //               Are you sure you want to logout?
        //             </h5>
        //             <button
        //               type="button"
        //               class="close"
        //               data-dismiss="modal"
        //               aria-label="Close"
        //             >
        //               <span aria-hidden="true">&times;</span>
        //             </button>
        //           </div>
        //           <div class="modal-body">
        //             <button
        //               className="select-btn"
        //               type="button"
        //               data-toggle="modal"
        //               data-target="#logoutModal"
        //               data-dismiss="modal"
        //               aria-label="Close"
        //             >
        //               No
        //             </button>
        //             <button
        //               className="select-btn"
        //               type="button"
        //               data-toggle="modal"
        //               data-target="#logoutModal"
        //               onClick={logoutUser}
        //             >
        //               Yes
        //             </button>
        //           </div>
        //         </div>
        //       </div>
        //     </div> */}
        //   </div>
        // </nav>
        // <nav className="navbar navbar-expand-md navbar-light">
        //   <a href="/">
        //     <img src={logo} alt="logo" width={70} height={70}></img>
        //   </a>
        //   {/* <a href="/">{element}</a> */}
        //   <div className="flex_center">
        //     <a href="/Login" className="header_btn">
        //       Login
        //     </a>
        //     <a href="/Signup" className="header_btn">
        //       Signup
        //     </a>
        //   </div>
        // </nav>
        <nav className="navbar navbar-expand-md navbar-light">
          <a href="/">
            <img src={logo} alt="logo" width={70} height={70}></img>
          </a>
          {/* <a href="/">{element}</a> */}
          <div className="flex_center">
            <a href="/Login" className="header_btn" id="loginBtn">
              Login
            </a>
            <a href="/Signup" className="header_btn" id="signupBtn">
              Signup
            </a>
          </div>
        </nav>
      )}
    </div>
  );
}

export default Header;
