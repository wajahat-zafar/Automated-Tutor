// import React from "react";

export default class APIService {
  static InsertTopic() {
    return fetch("http://localhost:5000/mc-topics", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
    }).then((resp) => resp.json());
  }

  static InsertSubTopic() {
    return fetch("http://localhost:5000/cn-topics", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
    }).then((resp) => resp.json());
  }

  static signup() {
    return fetch("http://localhost:5000/signup", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
    }).then((resp) => resp.json());
  }

  static InsertData(name) {
    // alert(name);
    return fetch("http://localhost:5000/cn-data/<name>/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ name: name }),
    }).then((resp) => resp.json());
  }

  static GetRelated(name) {
    alert(name);
    return fetch("http://localhost:5000/getrelated/<name>/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ name: name }),
    }).then((resp) => resp.json());
  }

  static Quiz(name) {
    // alert(name);
    return fetch("http://localhost:5000/quiz/<name>/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ name: name }),
    }).then((resp) => resp.json());
  }

  static Topics(name) {
    alert(name);
    return fetch("http://localhost:5000/get/<name>/", {
      method: "GET",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ name: name }),
    }).then((resp) => resp.json());
  }

  static DownloadFile(name) {
    // alert(name);
    return fetch("http://localhost:5000/download/<name>/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({ name: name }),
    }).then((resp) => resp.json());
  }

  // static GetData() {
  //   // console.log(body.topic_name);
  //   return fetch("http://localhost:5000/<domain-name>", {
  //     method: "POST",
  //     headers: {
  //       "Content-type": "application/json",
  //     },
  //   }).then((resp) => resp.json());
  // }
}
