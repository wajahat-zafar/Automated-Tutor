import React, { useState, useEffect } from "react";
import Header from "./Header";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloudUpload, faFileAlt } from "@fortawesome/free-solid-svg-icons";
import httpClient from "./httpClient";
import { User } from "../type";
import { useNavigate } from "react-router-dom";
import { UploadOutlined } from "@ant-design/icons";
import { Button, message, Upload } from "antd";
import { Worker } from "@react-pdf-viewer/core";
import { Viewer } from "@react-pdf-viewer/core";
import { Buffer } from "buffer";
import "@react-pdf-viewer/core/lib/styles/index.css";
import BgHeader from "./BgHeader";
import { RevolvingDot } from "react-loader-spinner";
// import PDFViewer from "pdf-viewer-reactjs";
// import { PDFExtract, PDFExtractOptions } from "pdf.js-extract";
// import PDFJS from "pdfjs-dist";
// import PDFJSWorker from "pdfjs-dist/build/pdf.worker.js"; // add this to fit 2.3.0

function UploadDocument() {
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);
  const [sumamrizing, setSumamrizing] = useState(false);
  const [status, setStatus] = useState(0);
  const [status2, setStatus2] = useState("short");
  const [status3, setStatus3] = useState("short");
  const [mytext, setMyText] = useState("");
  const [summData, setSumData] = useState("");
  const [summData2, setSumData2] = useState("");
  const [user, setUser] = useState(User);
  let navigate = useNavigate();

  const [file, setFile] = useState();
  const [fileBase, setFileBase] = useState();
  const getFile = (event) => {
    console.log(event.target.files);
    setFile(event.target.files);
  };
  const pdfjs = window["pdfjs-dist/build/pdf"];
  async function getContent(src, file) {
    let data = [];
    let numPages = 0;
    await pdfjs.getDocument({ data: atob(src) }).then(function (doc) {
      numPages = doc.numPages;
      console.log("# Document Loaded");
      console.log("Number of Pages: " + numPages);
    });

    for (let page = 1; page <= numPages; page++) {
      const doc = await pdfjs.getDocument({ data: atob(src) }).promise;
      const pagee = await doc.getPage(page);
      console.log(await pagee.getTextContent());
      let items = await pagee.getTextContent();
      data.push(items);
      console.log(data);
    }
    console.log(data);
    return data;
  }
  async function getItems(src, file) {
    var text = "";
    const content = await getContent(src, file);
    console.log(content);
    content?.map((data) => {
      data?.items?.map((item) => {
        text = text + " " + item.str;
        // console.log(item.str)
      });
    });
    return text;
  }
  var fileBase64 = [];
  async function encodeBase64(file) {
    console.log(file);
    var reader = new FileReader();
    reader.readAsDataURL(file);
    return new Promise((resolve) => {
      reader.onload = async () => {
        var base64 = reader.result;
        console.log(base64);
        var getText = await getItems(
          base64.replace("data:application/pdf;base64,", ""),
          file
        );
        fileBase64.push({
          name: file.name,
          encrypt: base64,
          text: getText,
        });
        console.log(fileBase64);
        resolve(fileBase64);

        const obj = { data: getText, length: status3 };
        try {
          const resp = await httpClient.post("//localhost:5000/uploadDocSum", {
            mode: "cors",
            obj,
          });
          console.log(resp.data);
          setSumData2(resp.data);
          setSumamrizing(false);
        } catch (error) {
          if (error.response.status === 401) {
            console.log(error.response);
            alert(error.response.data.error);
          }
        }
      };
    });
  }

  const getSummary = async (type) => {
    console.log(selectedFile);
    setSumamrizing(true);
    if (type == "file") {
      if (file?.[0].type !== "application/pdf") {
        message.error("Please select only pdf files.");
      } else {
        var encodedPDF;
        for (var i = 0; i < file["length"]; i++) {
          encodedPDF = await encodeBase64(file[i]);
        }
        setFileBase(encodedPDF);
      }
    } else {
      const obj = { data: mytext, length: status2 };
      console.log(obj);
      try {
        const resp = await httpClient.post("//localhost:5000/uploadDocSum", {
          mode: "cors",
          obj,
        });
        console.log(resp.data);
        setSumData(resp.data);
        setSumamrizing(false);
      } catch (error) {
        if (error.response.status === 401) {
          console.log(error.response);
          alert(error.response.data.error);
        }
      }
    }
  };
  const radioHandler = (status) => {
    setStatus(status);
  };
  const radioSummHandler = (status2) => {
    setStatus2(status2);
  };
  const radioSummHandler2 = (status3) => {
    setStatus3(status3);
  };

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

  const element = <FontAwesomeIcon icon={faCloudUpload} />;
  const element1 = <FontAwesomeIcon icon={faFileAlt} />;

  const setTextArea = () => {
    setMyText(document.querySelector(".input_text").value);
  };

  return (
    <div className="main">
      <BgHeader page="page" />
      <div className="main_data">
        <div className="type-form">
          <h3 className="main_heading">GET SUMMARY</h3>
          <h5 className="subhead">SELECT INPUT TYPE</h5>
          <div id="debt-amount-slider">
            <input
              type="radio"
              name="debt-amount"
              id="1"
              value="1"
              checked={status === 1}
              onClick={(e) => radioHandler(1)}
            />
            <label for="1" data-debt-amount="RAW TEXT"></label>
            <input
              type="radio"
              name="debt-amount"
              id="2"
              value="2"
              checked={status === 2}
              onClick={(e) => radioHandler(2)}
            />
            <label for="2" data-debt-amount="PDF"></label>
            <div id="debt-amount-pos"></div>
          </div>
          {status === 1 && (
            <div className="upload-div">
              <textarea
                className="input_text"
                onChange={setTextArea}
              ></textarea>
              <div className="summary-options">
                <h6>Summary Length</h6>
                <div className="summ-option">
                  <div className="flex_center_start">
                    <div className="flex_center">
                      <input
                        type="radio"
                        name="summoption"
                        value="short"
                        required
                        checked={status2 === "short"}
                        onClick={(e) => radioSummHandler("short")}
                      />
                      <label>Short</label>
                    </div>
                    <div className="flex_center">
                      <input
                        type="radio"
                        name="summoption"
                        value="medium"
                        required
                        checked={status2 === "medium"}
                        onClick={(e) => radioSummHandler("medium")}
                      />
                      <label>Medium</label>
                    </div>
                    <div className="flex_center">
                      <input
                        type="radio"
                        name="summoption"
                        value="long"
                        required
                        checked={status2 === "long"}
                        onClick={(e) => radioSummHandler("long")}
                      />
                      <label>Long</label>
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <button
                  className="header_btn"
                  onClick={() => getSummary("text")}
                >
                  Summarize
                </button>
              </div>

              {sumamrizing ? (
                <div className="loader">
                  <RevolvingDot
                    ariaLabel="loading-indicator"
                    radius="4"
                    color="#0093ab"
                    width="110"
                    height="110"
                  />
                  <h6 className="subhead">Summarizing Text</h6>
                </div>
              ) : summData !== "" ? (
                <div className="summary_up">
                  <h3 className="subhead">Summary of your Text</h3>
                  <p>{summData}</p>
                </div>
              ) : (
                <></>
              )}
            </div>
          )}
          {status === 2 && (
            <div className="upload-div">
              <div>
                <div className="zone">
                  <div className="dropZ">
                    <div className="upload-info">
                      <i>{element}</i>
                      <div className="upload-data">
                        <h5>Drag and drop your file here</h5>
                        <p>File size limit : 10 MB</p>
                      </div>
                    </div>
                    <div class="selectFile">
                      {/* <label for="file">Browse File</label> */}
                      {/* <Upload {...props}>
                        <Button icon={<UploadOutlined />}>
                          Click to Upload
                        </Button>
                      </Upload> */}
                      {/* <Upload
                        accept=".txt, .pdf"
                        showUploadList={true}
                        beforeUpload={(file) => {
                          const reader = new FileReader();

                          reader.onload = (e) => {
                            console.log(e.target.result);
                          };
                          reader.readAsText(file);

                          return false;
                        }}
                      >
                        <Button icon={<UploadOutlined />}>Upload</Button>
                      </Upload> */}
                      <input
                        type="file"
                        name="file"
                        id="file"
                        accept="application/pdf"
                        onChange={getFile}
                      />
                    </div>
                  </div>
                  {isFilePicked ? (
                    <div className="file-info">
                      <i>{element1}</i>
                      <div className="file-data">
                        <p className="file-name">{selectedFile?.name}</p>
                        {/* <p className="file-type">{selectedFile.type}</p> */}
                      </div>
                      {/* <p className="file-size">{selectedFile.size} Bytes</p> */}
                    </div>
                  ) : (
                    ""
                  )}
                </div>
                <div className="summary-options">
                  <h6>Summary Length</h6>
                  <div className="summ-option">
                    <div className="flex_center_start">
                      <div className="flex_center">
                        <input
                          type="radio"
                          name="summoption"
                          value="short"
                          required
                          checked={status3 === "short"}
                          onClick={(e) => radioSummHandler2("short")}
                        />
                        <label>Short</label>
                      </div>
                      <div className="flex_center">
                        <input
                          type="radio"
                          name="summoption"
                          value="medium"
                          required
                          checked={status3 === "medium"}
                          onClick={(e) => radioSummHandler2("medium")}
                        />
                        <label>Medium</label>
                      </div>
                      <div className="flex_center">
                        <input
                          type="radio"
                          name="summoption"
                          value="long"
                          required
                          checked={status3 === "long"}
                          onClick={(e) => radioSummHandler2("long")}
                        />
                        <label>Long</label>
                      </div>
                    </div>
                  </div>
                </div>
                <div>
                  <button
                    className="header_btn"
                    onClick={() => getSummary("file")}
                  >
                    Summarize
                  </button>
                </div>
                {sumamrizing ? (
                  <div className="loader">
                    <RevolvingDot
                      ariaLabel="loading-indicator"
                      radius="4"
                      color="#0093ab"
                      width="110"
                      height="110"
                    />
                    <h6 className="subhead">Summarizing The File</h6>
                  </div>
                ) : summData2 !== "" ? (
                  <div className="summary_up">
                    <h3 className="subhead">Summary of your Text</h3>
                    <p>{summData2}</p>
                  </div>
                ) : (
                  <></>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default UploadDocument;
