import React, { useEffect } from "react";
import { Link } from "react-router-dom";

window.vh_sceneLoaded = function() {
  window.setStatus(0, 0, 0, 1);
  window.followCursor(0);
  window.sayText("I am", 2, 1, 1);
};

function Char2D() {
  useEffect(() => {
    function loadEmbedFile() {
      var sc = document.createElement("script");
      sc.type = "text/javascript";
      sc.src =
        "//vhss-d.oddcast.com/vhost_embed_functions_v4.php?acc=5626448&js=1";
      sc.onload = function() {
        callEmebedFunction();
      };

      document.head.appendChild(sc);
    }
    function callEmebedFunction() {
      var interval = setInterval(() => {
        if (typeof AC_VHost_Embed == "function") {
          clearInterval(interval);
          var script = document.createElement("script");
          script.type = "text/javascript";
          script.innerHTML =
            'AC_VHost_Embed(3432155,600,800,"",1,1,2722664,0,1,1,"WSGmJ3ScqO8d4Zop1cuILz7q4In5k6q2",0)';
          // "AC_VHost_Embed(3432155,400,700,'',1,1, 2722641, 0,1,1,'85bd6cc7c39b75b2094fd6c1d9b7175c',0)";
          document.getElementById("embed").appendChild(script);
        }
      }, 10);
    }
    const scripts = document.head.getElementsByTagName("script");
    if (scripts.length > 0) {
      var alreadyAdded = false;
      for (var i = 0; i < scripts.length; i++) {
        if (scripts[i].src.includes("vhost_embed_functions_v4.php")) {
          alreadyAdded = true;
          callEmebedFunction();
        }
        if (scripts.length === i + 1 && !alreadyAdded) {
          loadEmbedFile();
        }
      }
    } else {
      loadEmbedFile();
    }
  }, []);
  return (
    <div>
      <table
        id="tblContainer"
        cellSpacing="0"
        align="center"
        border="0"
        width="50%"
        style={{ minHeight: "73vh" }}
      >
        <tbody>
          <tr>
            <td id="tdContent">
              <table align="center" width="90%">
                <tbody>
                  <tr>
                    <td align="center">
                      <table
                        cellPadding="10"
                        cellSpacing="0"
                        border="0"
                        width="350"
                      >
                        <tbody>
                          <tr>
                            <td colSpan="2" align="center"></td>
                          </tr>
                          <tr>
                            <td colSpan="2" align="center">
                              <div id="embed" className="Comment"></div>
                            </td>
                          </tr>
                          <tr></tr>
                          <tr>
                            <td align="right">
                              <button
                                onClick={() =>
                                  window.sayAudio("sayAudioExample")
                                }
                                className="btn btn_child shadow"
                                type="button"
                                id="btn1"
                                value="SAYAUDIO"
                              >
                                sayAudio()
                              </button>
                            </td>
                            <td align="left">
                              <button
                                onClick={() => window.sayText("I am", 2, 1, 1)}
                                className="btn btn_child shadow"
                                type="button"
                                id="btn1"
                                value="SAYTEXT"
                              >
                                sayText()
                              </button>
                            </td>
                            {/* <td>
                              <a
                                class="selected_support"
                                href="javascript:setBackground('Daytime');"
                              >
                                setBackgroundColor('f0f0f0')
                              </a>
                            </td> */}
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
export default Char2D;
