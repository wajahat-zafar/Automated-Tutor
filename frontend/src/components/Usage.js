import React from "react";

function Usage(props) {
  return (
    <div className="usage" id={props.id}>
      <h2 className="main_heading">USAGE</h2>
      <p className="subhead">Learn How To Use Autotmated Tutor.</p>
      <p className="datap">
        Follow the below steps to use this paltform.
        <ul>
          <li>Login to your account. (Signup if you don't have an account)</li>
          <li>After Login you can search a topic from the homepage.</li>
          <li>
            Next you can select Links of your choice or let the system choose
            it.
          </li>
          <li>
            After selecting sites you would have to wait a little as scraping
            and summarizing is happening.
          </li>
          <li>
            Once summarization is performed, you will be presented with the
            final result page
          </li>
          <li>
            The result page will have the summarized text that can be
            downloaded.
          </li>
          <li>
            Youtube videos related to the topic you searched can also be seen
          </li>
          <li>
            A quiz will be generated that you can attempt to check your
            understanding after reading about the topic
          </li>
          <li>After attempting quiz you can also check your score.</li>
          <li>
            You can also input a simple text or upload a pdf to get the summary
            of it with the length of your choice i.e. small, medium, long.
          </li>
        </ul>
      </p>
    </div>
  );
}

export default Usage;
