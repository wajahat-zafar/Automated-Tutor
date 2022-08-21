import React, { useState, useEffect } from "react";
import DomainBtn from "./DomainBtn";
import TopicButtons from "./TopicButtons";

function AdminTopics(props) {
  const [topic, setData] = useState(null);
  const name = props.name;

  useEffect(() => {
    const fetchData = async () => {
      console.log(name);
      const response = await fetch("http://localhost:5000/get/<name>/", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify({ name: name }),
      });
      console.log(response);
      const newData = await response.json();
      setData(newData);
    };

    fetchData();
  }, []);

  if (topic) {
    return (
      <div>
        <TopicButtons user="Logged In" type="admin" topic={topic} />
      </div>
    );
  } else {
    return <div>JABBA</div>;
  }
}

export default AdminTopics;
