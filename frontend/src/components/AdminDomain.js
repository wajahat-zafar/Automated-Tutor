import React, { useState, useEffect } from "react";
import DomainBtn from "./DomainBtn";

function AdminDomain() {
  const [domain, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch("http://localhost:5000/getDomain");
      const newData = await response.json();
      setData(newData);
    };

    fetchData();
  }, []);

  if (domain) {
    return (
      <div>
        <DomainBtn user="Logged In" type="admin" domain={domain} />
      </div>
    );
  } else {
    return <div>JABBA</div>;
  }
  //   const [domain, setDomains] = useState(null);

  //   useEffect(() => {
  //     fetch("http://localhost:5000/getDomain", {
  //       method: "GET",
  //       headers: {
  //         "Content-type": "application/json",
  //       },
  //     })
  //       .then((resp) => resp.json())
  //       .then((resp) => console.log(resp))
  //       .then((resp) => setDomains(resp))
  //       .catch((error) => console.log(error));
  //   }, []);

  //   if (domain) {
  //     return <div>{domain}</div>;
  //   } else {
  //     return <div>JABBAAA</div>;
  //   }
  //   //   return (
  //   //     <div>
  //   //       <p>{domain}</p>
  //   //       <DomainBtn user="Logged In" type="admin" domain={domain} />
  //   //     </div>
  //   //   );
}

export default AdminDomain;
