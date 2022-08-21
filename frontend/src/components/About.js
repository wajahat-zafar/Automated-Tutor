import React from "react";

function About(props) {
  return (
    <div className="about" id={props.id}>
      <h2 className="main_heading">ABOUT</h2>
      <p className="subhead">About Automated Tutor</p>
      <p className="datap">
        Everyone has gone through the arduous effort of conducting an online
        search and moving from one web page to another. The information is
        largely the same on numerous websites, with a few exceptions, and
        reviewing all of them takes extra time. As a result, a system was
        required that can acquire data from many websites and summarize it
        before presenting it to the user.<br></br>
        <br></br> The main objective of this project is to reduce the tedious
        effort of searching a topic and browsing through multiple web pages and
        to help the user by providing summarized information on that topic at a
        single platform through automation.<br></br>
        <br></br> This project addresses this issue and saves the user the time
        and effort of researching the topic online and navigating the
        difficulties of online searching. It is primarily targeted at students
        who require a website that saves them time when exploring the web and
        gives concise information on the topic they are looking for. Gathering
        information from many sources and then extracting valuable and relevant
        facts from such a large number of documents is a difficult undertaking.
        This objective is accomplished by combining web scraping technology with
        information summarizing before presenting it to the user. This project's
        purpose is to reduce the amount of time and effort required by people to
        grasp and analyze useful data.
      </p>
    </div>
  );
}

export default About;
