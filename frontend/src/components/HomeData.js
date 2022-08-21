import React from "react";

function HomeData(props) {
  return (
    <div className="youtube">
      <h3 className="subhead">Youtube Videos Related To {props.heading1}</h3>
      {props.yt &&
        props.yt.map((data) => {
          console.log(data);
          const videos = [];
          console.log("s");
          for (var k in data.yt_data) {
            // console.log(data.yt_data[k]["thumbnail"]);
            videos.push(
              <div className="col-md-4">
                <div className="Card2 ph1">
                  <img
                    className="mycard-img"
                    src={data.yt_data[k]["thumbnail"]}
                    preserveAspectRatio="xMidYMid slice"
                    focusable="false"
                    role="img"
                    aria-label="Placeholder: Thumbnail"
                  ></img>
                  <div className="overlay">
                    <h4 className="title">{data.yt_data[k]["title"]}</h4>
                    <div className="view-info">
                      <small className="minutes">
                        {data.yt_data[k]["duration"]} mins
                      </small>
                      <a
                        className="link header_btn"
                        href="//s.codepen.io/ImagineAlex"
                        target="_blank"
                      >
                        View
                      </a>
                    </div>
                  </div>
                </div>
                {/* <div className="card mb-4">
                  <img
                    className="bd-placeholder-img card-img-top"
                    width="100%"
                    height="225"
                    src={data.yt_data[k]["thumbnail"]}
                    preserveAspectRatio="xMidYMid slice"
                    focusable="false"
                    role="img"
                    aria-label="Placeholder: Thumbnail"
                  ></img>
                  <div className="card-body">
                    <p className="card-title">{data.yt_data[k]["title"]}</p>
                    <hr></hr>
                    <div className="card-text d-flex justify-content-between align-items-center">
                      <div className="btn-group">
                        <a
                          type="button"
                          href={data.yt_data[k]["url"]}
                          className="select-btn"
                          target="_blank"
                        >
                          View
                        </a>
                      </div>
                      <small className="">
                        {data.yt_data[k]["duration"]} mins
                      </small>
                    </div>
                  </div>
                </div> */}
              </div>
            );
          }
          return (
            <div>
              <div className="album">
                <div className="container">
                  <div className="row">{videos}</div>
                </div>
              </div>
            </div>
          );
        })}
    </div>
  );
}

export default HomeData;
