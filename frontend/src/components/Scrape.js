import React from "react";

function Scrape() {
  const data1 = useLocation();
  const heading = data1.search.slice(1);
  const heading1 = decodeURI(heading);
  alert(heading1);
  APIService.InsertData(heading1)
    .then((resp) => resp.json())
    .catch((error) => console.log(error));

  return (
    <div>
      <HomePage heading1={heading1} />
    </div>
  );
}

export default Scrape;
