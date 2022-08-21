import random
import subprocess
import psycopg2
import os
from flask import (
    Flask,
    render_template,
    request,
    flash,
    jsonify,
    session,
    Blueprint,
    current_app,
    redirect,
)
import redis
from datetime import datetime, timedelta
from serpapi import GoogleSearch
from checkAnswers import CheckAnswers
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required, JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_session import Session
from flask_bcrypt import Bcrypt

from sc import Data_scraper
import json

import base64
import re
import requests
from isodate import parse_duration

from fpdf import FPDF
from dotenv import load_dotenv
from get_text import ExtractText
from formatting import splitter

from bart_sum import PreProcessor, Summarization
from questiongenerator import QuestionGenerator

from uuid import uuid4

app = Flask(__name__)
load_dotenv()


class ApplicationConfig:
    SECRET_KEY = "automatedkeytutor"

    DB_USERNAME = "postgres"
    DB_PASSWORD = "tutorfyp"

    # SESSION_TYPE = "redis"
    # SESSION_TYPE = "sqlalchemy"
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    # SESSION_SQLALCHEMY = "postgresql://<postgres>:<tutorFYP>@localhost:5432/FYP"
    # SESSION_SQLALCHEMY_TABLE = "sessions"


# app.config.from_object(ApplicationConfig)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:HalaOsama7@localhost/FYP"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = "automatedkeytutor"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:HalaOsama7@localhost/FYP"
# # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# # app.secret_key = "tutor"

# # db = SQLAlchemy(app)
# # ma = Marshmallow(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:HalaOsama710@localhost/FYP"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config["JWT_SECRET_KEY"] = "automatedtutorkey"
# jwt = JWTManager(app)
app.secret_key = 'automatedkeytutor'
app.config['SESSION_TYPE'] = 'filesystem'
DB_USERNAME = "postgres"
DB_PASSWORD = "tutorFYP"

# DB_USERNAME = "postgres"
# DB_PASSWORD = "tutorFYP"
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# app.secret_key = "tutor"

db = SQLAlchemy(app)
ma = Marshmallow(app)
# app.config["JWT_SECRET_KEY"] = "automatedtutorkey"
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# jwt = JWTManager(app)


# main = Blueprint('main', __name__)

db.init_app(app)
cors = CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)
server_session = Session(app)

# scraper = Data_scraper()
# topics = scraper.main()


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost", database="FYP", user=DB_USERNAME, password=DB_PASSWORD
    )
    return conn


# with app.app_context():
#     db.create_all()


def get_uuid():
    return uuid4().hex


def create_table(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    # print("Table created successfully in PostgreSQL ")


create_table(
    """CREATE TABLE IF NOT EXISTS domain
            (DOMAIN_ID SERIAL PRIMARY KEY     NOT NULL,
            DOMAIN_NAME           TEXT  UNIQUE    NOT NULL,
            DOMAIN_LINK         TEXT        NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS topics
            (TOPIC_ID SERIAL PRIMARY KEY     NOT NULL,
            DOMAIN_ID INT REFERENCES domain (DOMAIN_ID),
            TOPIC_NAME           TEXT  UNIQUE    NOT NULL,
            TOPIC_LINK         TEXT     NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS scraped_data
            (SCRAPED_ID SERIAL PRIMARY KEY     NOT NULL,
            TOPIC_ID INT REFERENCES topics (TOPIC_ID),
            SCRAPED_DATA           TEXT    NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS yt_topic_data
            (yt_id serial PRIMARY KEY NOT NULL,
            TOPIC_ID INT REFERENCES topics (TOPIC_ID),
            yt_data TEXT NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS user_data
            (USER_ID SERIAL PRIMARY KEY     NOT NULL,
            FULL_NAME           TEXT    NOT NULL,
            USER_NAME           TEXT    UNIQUE    NOT NULL,
            EMAIL           TEXT    UNIQUE    NOT NULL,
            PASSWORD           TEXT NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS quiz
            (QUIZ_ID SERIAL PRIMARY KEY     NOT NULL,
            TOPIC_ID INT REFERENCES topics (TOPIC_ID),
            QUESTIONS           JSON    NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS topics_data
            (TOPIC_ID SERIAL PRIMARY KEY     NOT NULL,
            TOPIC_NAME           TEXT  UNIQUE    NOT NULL); """
)
create_table(
    """CREATE TABLE IF NOT EXISTS summaries
            (SUMMARY_ID SERIAL PRIMARY KEY     NOT NULL,
            TOPIC_ID INT REFERENCES topics_data (TOPIC_ID),
            SUMMARY           TEXT    NOT NULL,
            DATA_LINK     TEXT[] NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS youtubedata
            (YT_ID SERIAL PRIMARY KEY     NOT NULL,
            TOPIC_ID INT REFERENCES topics_data (TOPIC_ID),
            YT_DATA           JSON    NOT NULL); """
)

create_table(
    """CREATE TABLE IF NOT EXISTS quiz_data
            (QUIZ_ID SERIAL PRIMARY KEY     NOT NULL,
            TOPIC_ID INT REFERENCES topics_data (TOPIC_ID),
            QUESTIONS           JSON    NOT NULL); """
)


# conn = get_db_connection()
# cur = conn.cursor()
# cur.execute('INSERT INTO domain(DOMAIN_NAME, DOMAIN_LINK) VALUES ( % s, % s)',
#             ('Computer Networks', 'https://www.javatpoint.com/computer-network-tutorial'))
# conn.commit()


def search_results_return(topic):

    try:
        params = {
            "engine": "google",
            "q": f"{topic} -www.codecademy.com -en.wikipedia.org -www.youtube.com -www.researchgate.net -www.sciencedirect.com -www.kdkce.edu.in -www.slideshare.net -ncert.nic.in",
            "api_key": "f823624fc4b339b44fd356d2548a4557c5db95388683bc0f307d3fa6f07e1ac5",
            "google_domain": "google.com",
            "gl": "pk",
            "hl": "en",
            "safe": "active",
        }
    except:
        try:
            params = {
                "engine": "google",
                "q": f"{topic} -www.codecademy.com -en.wikipedia.org -www.youtube.com -www.researchgate.net -www.sciencedirect.com -www.kdkce.edu.in -www.slideshare.net -ncert.nic.in",
                "api_key": "16c2974f9c0829e8bae69c97101e912969ec75a8b65932e41da0d403c327cb48",
                "google_domain": "google.com",
                "gl": "pk",
                "hl": "en",
                "safe": "active",
            }
        except:
            try:
                params = {
                    "engine": "google",
                    "q": f"{topic} -www.codecademy.com -en.wikipedia.org -www.youtube.com -www.researchgate.net -www.sciencedirect.com -www.kdkce.edu.in -www.slideshare.net -ncert.nic.in",
                    "api_key": "cf6e80973f4b3d9911536a831c1a3489a4cdc3c3f5d0f909e8ba6ef581249e26",
                    "google_domain": "google.com",
                    "gl": "pk",
                    "hl": "en",
                    "safe": "active",
                }

            except:
                try:
                    params = {
                        "engine": "google",
                        "q": f"{topic} -www.codecademy.com -en.wikipedia.org -www.youtube.com -www.researchgate.net -www.sciencedirect.com -www.kdkce.edu.in -www.slideshare.net -ncert.nic.in",
                        "api_key": "95088fcf6717f70722b9e1f3583628534fe8589e0c60b1065cb7b3418775f379",
                        "google_domain": "google.com",
                        "gl": "pk",
                        "hl": "en",
                        "safe": "active",
                    }
                except:
                    params = {
                        "engine": "google",
                        "q": f"{topic} -www.codecademy.com -en.wikipedia.org -www.youtube.com -www.researchgate.net -www.sciencedirect.com -www.kdkce.edu.in -www.slideshare.net -ncert.nic.in",
                        "api_key": "912e3c9f8522a458f5dd23be0de52d77920252e45682a7f7bcbb3018f88c1748",
                        "google_domain": "google.com",
                        "gl": "pk",
                        "hl": "en",
                        "safe": "active",
                    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

    final_search_results = []
    print(organic_results)
    for i in organic_results:
        try:
            result_output = []
            result_output.append(i["title"])
            result_output.append(i["link"])
            result_output.append(i["snippet"])
            final_search_results.append(result_output)
        except:
            pass

    return final_search_results


@app.route("/searchResult", methods=["GET", "POST"])
def searchResult():
    msg = ""
    print(request.json)
    obj = request.json["obj"]
    print(obj, type(obj))
    title = obj["search"]
    print(title)
    # desc = request.form['desc']
    # print(desc)
    # todo = Todo(title=title, desc=desc)
    # db.session.add(todo)
    # db.session.commit()
    allTodo = search_results_return(title)
    print(allTodo)
    return jsonify(allTodo)
    # return render_template('index.html', allTodo=allTodo, hasRun=hasRun)

    # allTodo = search_results_return

    # return render_template('index.html', allTodo=allTodo, hasRun=hasRun)


@app.route("/searchResultAuto", methods=["GET", "POST"])
def searchResultAuto():
    msg = ""
    print(request.json)
    obj = request.json["obj"]
    print(obj, type(obj))
    title = obj["search"]
    print(title)
    allTodo = search_results_return(title)
    print(allTodo)
    links = []
    for lists in allTodo:
        links.append(lists[1])
    print(links)
    summarized = scrape_sum(title, links)
    return jsonify(summarized)


@app.route("/getDomain", methods=["GET"])
# @jwt_required()
def getDomain():
    conn = get_db_connection()
    cur = conn.cursor()
    # print("aa")
    cur.execute("SELECT * FROM domain;")
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    # print(row_headers)
    rv = cur.fetchall()
    # print(rv)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    # print(json_data)
    return jsonify(json_data)


@app.route("/get", methods=["GET"])
# @jwt_required()
def get_topics():
    conn = get_db_connection()
    cur = conn.cursor()
    # print("aa")
    cur.execute("SELECT * FROM topics;")

    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)


@app.route("/getDomainName/<name>/", methods=["GET", "POST"])
# @jwt_required()
def getDomainName(name):
    print("fg", name)
    namee = request.get_json()
    print("hh", namee)
    name = namee["name"]
    print(name)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT domain_name FROM domain where domain_id=%s;", (name,))
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    print(rv)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)


@app.route("/get/<name>/", methods=["GET", "POST"])
# @jwt_required()
def get(name):
    print("aa")
    print("fg", name)
    namee = request.get_json()
    print("hh", namee)
    name = namee["name"]
    print(name)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics where domain_id=%s;", (name,))

    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    print(rv)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    print(json_data)
    return jsonify(json_data)


@app.route("/getData", methods=["GET", "POST"])
# @jwt_required()
def getData():
    # print("get")
    namee = request.get_json()
    print(namee)
    topic = namee["name"]
    print(topic)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM topics s join topics on s.topic_id = topics.topic_id;")
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    # print(rv)
    json_data = []
    for result in rv:
        if topic in result:
            print(result)
            tid = result[0]

    cur.execute("SELECT * FROM scraped_data where topic_id=%s", (tid,))
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    print(row_headers)
    rv = cur.fetchall()
    print(rv)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    cur.close()
    conn.close()
    return jsonify(json_data)


@app.route("/getDataSum", methods=["GET", "POST"])
# @jwt_required()
def getDataSum():
    # print("get")
    namee = request.get_json()
    print(namee)
    name = namee["name"]
    print(name)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics_data where topic_name=%s", (name,))
    # print(cur.fetchone())
    topic_id = cur.fetchone()[0]
    print(topic_id)
    cur.execute("SELECT * FROM summaries where topic_id=%s", (topic_id,))
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    print(row_headers)
    rv = cur.fetchall()
    print(rv)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    cur.close()
    conn.close()
    return jsonify(json_data)


@app.route("/getquiz/<name>", methods=["POST"])
# @jwt_required()
def getquiz(name):
    # try:
    namee = request.get_json()
    print(namee)
    new = namee["name"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * from topics_data where topic_name=%s", (new,))
    topic_id = cur.fetchone()[0]
    cur.execute("SELECT questions FROM quiz_data where topic_id=%s", (topic_id,))
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    final_q = []
    final_quest = []
    json_data = []
    for result in rv:
        print('\ntooooo\n', result[0], '\n')
        for quest in result[0]:
            if quest['question'] not in final_q:
                print(quest)
                final_q.append(quest['question'])
                final_quest.append(quest)

    print(final_quest)
    json_data.append(dict(zip(row_headers, [final_quest])))
    print('\nout\n', json_data)
    return jsonify(json_data)


@app.route("/checkAnswers/<name>", methods=["GET", "POST"])
# @jwt_required()
def checkAnswers(name):
    # try:
    namee = request.get_json()
    # print(namee)
    mainQ = namee["mainQ"]
    data = namee["data"]
    # print(mainQ)
    # print(data)
    find = []
    for i in range(len(mainQ)):
        find.append([mainQ[i]["answer"], data[i][str(i)]])
    print(find)
    ch = CheckAnswers(find)
    result = ch.check_answers()
    print(result)
    return jsonify(result)
    # except:
    #     # print("sssss", request)
    #     namee = request.get_json()
    #     print(namee)
    #     # print(namee['name'])
    #     new = namee["name"]
    #     conn = get_db_connection()
    #     cur = conn.cursor()
    #     # print("aa")
    #     cur.execute("SELECT topic_id from topics where topic_name=%s", (new,))
    #     idd = cur.fetchone()
    #     # print(idd)
    #     cur.execute("SELECT * FROM quiz where topic_id=%s", (idd,))
    #     row_headers = [x[0] for x in cur.description]  # this will extract row headers
    #     rv = cur.fetchall()
    #     json_data = []
    #     for result in rv:
    #         json_data.append(dict(zip(row_headers, result)))
    #     return jsonify(json_data)


# @ app.route("/getUser", methods=["POST"])
# def get_user():
#     msg = ""
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         # Check if account exists using MySQL
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute(
#             'SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
#         # Fetch one record and return result
#         account = cur.fetchone()
#         # If account exists in accounts table in out database
#         if account:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id'] = account['UserID']
#             session['username'] = account['email']
#             # Redirect to home page
#             return 'Logged in successfully!'
#         else:
#             # Account doesnt exist or username/password incorrect
#             msg = 'Incorrect username/password!'
#     # Show the login form with message (if any)
#     # return render_template('index.html', msg=msg)
#     # conn = get_db_connection()
#     # cur = conn.cursor()
#     # cur.execute('SELECT * FROM users;')
#     # row_headers = [x[0]
#     #                for x in cur.description]  # this will extract row headers
#     # rv = cur.fetchall()
#     # json_data = []
#     # for result in rv:
#     #     json_data.append(dict(zip(row_headers, result)))
#     return jsonify(msg)


@app.route("/mc-topics", methods=["POST"])
# @jwt_required()
def add_topic():
    # result = topics
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT domain_id FROM domain where domain_name = %s", (
            "Computer Networks",)
    )
    dom_id = cur.fetchone()[0]
    cur.execute("SELECT * from topics where domain_id=%s", (dom_id,))
    exist = cur.fetchone()
    if exist:
        return "already"
    else:
        for out in result:
            cur.execute(
                "INSERT INTO topics(DOMAIN_ID, TOPIC_NAME, TOPIC_LINK) VALUES (%s, %s, %s)",
                (dom_id, out[0], out[1]),
            )
            conn.commit()
        cur.execute("SELECT * FROM topics;")

        # this will extract row headers
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        cur.close()
        conn.close()
        # domain_name = "Computer Networks"
        # domain_topics = result
        # print(domain_topics)

        # topics = Domains(domain_name, domain_topics)
        # db.session.add(topics)
        # db.session.commit()

        # for topic in result:
        #     domain_name = topic[0]
        #     domain_topics = topic[1]

        #     topics = Domains(domain_name, domain_topics)
        #     db.session.add(topics)
        #     db.session.commit()

        return jsonify(json_data)


@app.route("/quiz/<name>/", methods=["GET", "POST"])
def quiz(name):
    # try:
    print("sdasd")
    namee = request.get_json()
    print(namee["name"])
    new = namee["name"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT topic_id FROM topics_data WHERE TOPIC_NAME=%s", (new,))
    topic_id = cur.fetchone()[0]
    print(topic_id, "topic_id")
    cur.execute("SELECT * FROM quiz_data WHERE topic_id=%s", (topic_id,))
    q = cur.fetchone()
    print(q)
    if q:
        cur.execute(
            "SELECT summary FROM summaries WHERE topic_id=%s", (topic_id,))
        out = cur.fetchone()
        print(out)

        qg = QuestionGenerator()
        qa_list = qg.generate(out[0], num_questions=20)
        question = qa_list
        print(question)
        # temp = []
        # res = dict()
        # for i in question:
        #     for key, val in i.items():
        #         if val not in temp:
        #             temp.append(val)
        #             res[key] = val
        # print('\nres\n', res)
        cur.execute(
            "UPDATE quiz_data SET QUESTIONS=%s WHERE TOPIC_ID=%s",
            (json.dumps(question), topic_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(question)
    else:
        cur.execute(
            "SELECT summary from summaries where topic_id=%s", (topic_id,))
        out = cur.fetchone()
        print(out)

        qg = QuestionGenerator()
        qa_list = qg.generate(out[0], num_questions=20)
        question = qa_list
        print("\n\n", question)
        cur.execute(
            "INSERT INTO quiz_data (TOPIC_ID, QUESTIONS) VALUES (%s, %s)",
            (
                topic_id,
                json.dumps(question),
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(question)

    # except:
    #     print("sdasd")
    #     namee = request.get_json()
    #     print(namee["name"])
    #     new = namee["name"]
    #     conn = get_db_connection()
    #     cur = conn.cursor()
    #     cur.execute("SELECT topic_id from topics_data where topic_name=%s", (new,))
    #     top_id = cur.fetchone()[0]
    #     print(top_id)
    #     cur.execute("SELECT * from quiz where topic_id=%s", (top_id,))

    #     # cur.execute("SELECT * from quiz where topic_id=%s", (top_id,))
    #     exists = cur.fetchone()
    #     if exists:
    #         return "already exists"
    #     else:
    #         cur.execute(
    #             "SELECT scraped_dataa from scraped_data where topic_id=%s", (top_id,)
    #         )
    #         out = cur.fetchone()
    #         print(out[0])
    #         output = InputProcess()
    #         question = output.preprocess_text(out[0])
    #         print(question)
    #         cur.execute(
    #             "INSERT INTO quiz (TOPIC_ID, QUESTIONS) VALUES (%s, %s)",
    #             (
    #                 top_id,
    #                 json.dumps(question),
    #             ),
    #         )
    #         conn.commit()
    #         cur.close()
    #         conn.close()
    #         return jsonify(question)


def scrape_sum(topic, links):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT topic_id FROM topics_data WHERE TOPIC_NAME=%s", (topic,))
    topic_id = cur.fetchone()

    print(topic_id)
    if topic_id:

        data_scraped = ExtractText(links)
        scraped = data_scraped.scrape_text_from_link()

        new = " ".join(scraped.splitlines())

        pre = PreProcessor(new)
        tokenized = pre.token()
        summarizer = Summarization(tokenized, "")
        summ_ids = summarizer.summarize()
        result = pre.decoder(summ_ids)
        print(result)

        cur.execute("SELECT * FROM summaries WHERE TOPIC_ID=%s", (topic_id,))

        exists2 = cur.fetchone()
        if exists2:

            cur.execute(
                "UPDATE summaries SET summary=%s, data_link=%s WHERE topic_id=%s",
                (result, links, topic_id),
            )
            conn.commit()

            search_url = "https://www.googleapis.com/youtube/v3/search"
            video_url = "https://www.googleapis.com/youtube/v3/videos"

            videos = []

            print("yt")
            search_params = {
                "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
                "q": topic,
                "part": "snippet",
                "maxResults": 9,
                "type": "video",
            }

            r = requests.get(search_url, params=search_params)

            results = r.json()["items"]

            video_ids = []
            for result in results:
                video_ids.append(result["id"]["videoId"])

            video_params = {
                "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
                "id": ",".join(video_ids),
                "part": "snippet,contentDetails",
                "maxResults": 9,
            }

            total_vid = video_params["maxResults"]
            # print(total_vid)

            r = requests.get(video_url, params=video_params)
            results = r.json()["items"]
            print(results)
            for result in results:
                video_data = {
                    "id": result["id"],
                    "url": f'https://www.youtube.com/watch?v={ result["id"] }',
                    "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
                    "duration": int(
                        parse_duration(
                            result["contentDetails"]["duration"]
                        ).total_seconds()
                        // 60
                    ),
                    "title": result["snippet"]["title"],
                }
                videos.append(video_data)
            try:
                cur.execute(
                    "UPDATE youtubedata SET YT_DATA=%s WHERE topic_id=%s",
                    (json.dumps(videos), topic_id),
                )
                conn.commit()

                new_lst = f"{videos}"
                print(new_lst)
                return topic

            except:
                cur.execute(
                    "INSERT INTO youtubedata (YT_DATA, TOPIC_ID) VALUES (%s, %s)",
                    (json.dumps(videos), topic_id),
                )
                conn.commit()

                new_lst = f"{videos}"
                print(new_lst)
                return topic

        else:

            cur.execute(
                "INSERT INTO summaries (SUMMARY, TOPIC_ID, DATA_LINK) VALUES (%s, %s,%s)",
                (result, topic_id, links),
            )
            conn.commit()

            search_url = "https://www.googleapis.com/youtube/v3/search"
            video_url = "https://www.googleapis.com/youtube/v3/videos"

            videos = []

            print("yt")
            search_params = {
                "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
                "q": topic,
                "part": "snippet",
                "maxResults": 9,
                "type": "video",
            }

            r = requests.get(search_url, params=search_params)

            results = r.json()["items"]

            video_ids = []
            for result in results:
                video_ids.append(result["id"]["videoId"])

            video_params = {
                "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
                "id": ",".join(video_ids),
                "part": "snippet,contentDetails",
                "maxResults": 9,
            }

            total_vid = video_params["maxResults"]
            # print(total_vid)

            r = requests.get(video_url, params=video_params)
            results = r.json()["items"]
            print(results)
            for result in results:
                video_data = {
                    "id": result["id"],
                    "url": f'https://www.youtube.com/watch?v={ result["id"] }',
                    "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
                    "duration": int(
                        parse_duration(
                            result["contentDetails"]["duration"]
                        ).total_seconds()
                        // 60
                    ),
                    "title": result["snippet"]["title"],
                }
                videos.append(video_data)
            cur.execute(
                "INSERT INTO youtubedata (YT_DATA, TOPIC_ID) VALUES (%s, %s)",
                (json.dumps(videos), topic_id),
            )
            conn.commit()

            new_lst = f"{videos}"
            print(new_lst)
            return topic

    else:
        cur.execute(
            "INSERT INTO topics_data (TOPIC_NAME) VALUES (%s)", (topic,))
        conn.commit()

        data_scraped = ExtractText(links)
        scraped = data_scraped.scrape_text_from_link()

        new = " ".join(scraped.splitlines())

        pre = PreProcessor(new)
        tokenized = pre.token()
        summarizer = Summarization(tokenized, "")
        summ_ids = summarizer.summarize()
        result = pre.decoder(summ_ids)
        print(result)

        cur.execute(
            "SELECT topic_id FROM topics_data WHERE topic_name=%s",
            (topic,),
        )
        idd = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO summaries (SUMMARY, TOPIC_ID, DATA_LINK) VALUES (%s, %s,%s)",
            (result, idd, links),
        )
        conn.commit()

        search_url = "https://www.googleapis.com/youtube/v3/search"
        video_url = "https://www.googleapis.com/youtube/v3/videos"

        videos = []

        print("yt")
        search_params = {
            "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
            "q": topic,
            "part": "snippet",
            "maxResults": 9,
            "type": "video",
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()["items"]

        video_ids = []
        for result in results:
            video_ids.append(result["id"]["videoId"])

        video_params = {
            "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
            "id": ",".join(video_ids),
            "part": "snippet,contentDetails",
            "maxResults": 9,
        }

        total_vid = video_params["maxResults"]
        # print(total_vid)

        r = requests.get(video_url, params=video_params)
        results = r.json()["items"]
        print(results)
        for result in results:
            video_data = {
                "id": result["id"],
                "url": f'https://www.youtube.com/watch?v={ result["id"] }',
                "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
                "duration": int(
                    parse_duration(result["contentDetails"]
                                   ["duration"]).total_seconds()
                    // 60
                ),
                "title": result["snippet"]["title"],
            }
            videos.append(video_data)
        cur.execute(
            "INSERT INTO youtubedata (YT_DATA, TOPIC_ID) VALUES (%s, %s)",
            (json.dumps(videos), idd),
        )
        conn.commit()

        new_lst = f"{videos}"
        print(new_lst)
        return topic


@app.route("/search", methods=["GET", "POST"])
def search():
    checked = request.get_json()
    topic = checked["obj"]["topic"]
    checked_list = checked["obj"]["checkedList"]
    print(topic, checked_list)

    result = scrape_sum(topic, checked_list)
    return jsonify(result)
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute("SELECT topic_id FROM topics_data WHERE TOPIC_NAME=%s", (topic,))
    # topic_id = cur.fetchone()

    # print(topic_id)
    # if topic_id:

    #     data_scraped = ExtractText(checked_list)
    #     scraped = data_scraped.scrape_text_from_link()

    #     new = " ".join(scraped.splitlines())

    #     pre = PreProcessor(new)
    #     tokenized = pre.token()
    #     summarizer = Summarization(tokenized)
    #     summ_ids = summarizer.summarize()
    #     result = pre.decoder(summ_ids)
    #     print(result)

    #     cur.execute("SELECT * FROM summaries WHERE TOPIC_ID=%s", (topic_id,))

    #     exists2 = cur.fetchone()
    #     if exists2:

    #         cur.execute(
    #             "UPDATE summaries SET summary=%s, data_link=%s WHERE topic_id=%s",
    #             (result, checked_list, topic_id),
    #         )
    #         conn.commit()

    #         search_url = "https://www.googleapis.com/youtube/v3/search"
    #         video_url = "https://www.googleapis.com/youtube/v3/videos"

    #         videos = []

    #         print("yt")
    #         search_params = {
    #             "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
    #             "q": topic,
    #             "part": "snippet",
    #             "maxResults": 9,
    #             "type": "video",
    #         }

    #         r = requests.get(search_url, params=search_params)

    #         results = r.json()["items"]

    #         video_ids = []
    #         for result in results:
    #             video_ids.append(result["id"]["videoId"])

    #         video_params = {
    #             "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
    #             "id": ",".join(video_ids),
    #             "part": "snippet,contentDetails",
    #             "maxResults": 9,
    #         }

    #         total_vid = video_params["maxResults"]
    #         # print(total_vid)

    #         r = requests.get(video_url, params=video_params)
    #         results = r.json()["items"]
    #         print(results)
    #         for result in results:
    #             video_data = {
    #                 "id": result["id"],
    #                 "url": f'https://www.youtube.com/watch?v={ result["id"] }',
    #                 "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
    #                 "duration": int(
    #                     parse_duration(
    #                         result["contentDetails"]["duration"]
    #                     ).total_seconds()
    #                     // 60
    #                 ),
    #                 "title": result["snippet"]["title"],
    #             }
    #             videos.append(video_data)
    #         try:
    #             cur.execute(
    #                 "UPDATE youtubedata SET YT_DATA=%s WHERE topic_id=%s",
    #                 (json.dumps(videos), topic_id),
    #             )
    #             conn.commit()

    #             new_lst = f"{videos}"
    #             print(new_lst)
    #             return topic

    #         except:
    #             cur.execute(
    #                 "INSERT INTO youtubedata (YT_DATA, TOPIC_ID) VALUES (%s, %s)",
    #                 (json.dumps(videos), topic_id),
    #             )
    #             conn.commit()

    #             new_lst = f"{videos}"
    #             print(new_lst)
    #             return topic

    #     else:

    #         cur.execute(
    #             "INSERT INTO summaries (SUMMARY, TOPIC_ID, DATA_LINK) VALUES (%s, %s,%s)",
    #             (result, topic_id, checked_list),
    #         )
    #         conn.commit()

    #         search_url = "https://www.googleapis.com/youtube/v3/search"
    #         video_url = "https://www.googleapis.com/youtube/v3/videos"

    #         videos = []

    #         print("yt")
    #         search_params = {
    #             "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
    #             "q": topic,
    #             "part": "snippet",
    #             "maxResults": 9,
    #             "type": "video",
    #         }

    #         r = requests.get(search_url, params=search_params)

    #         results = r.json()["items"]

    #         video_ids = []
    #         for result in results:
    #             video_ids.append(result["id"]["videoId"])

    #         video_params = {
    #             "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
    #             "id": ",".join(video_ids),
    #             "part": "snippet,contentDetails",
    #             "maxResults": 9,
    #         }

    #         total_vid = video_params["maxResults"]
    #         # print(total_vid)

    #         r = requests.get(video_url, params=video_params)
    #         results = r.json()["items"]
    #         print(results)
    #         for result in results:
    #             video_data = {
    #                 "id": result["id"],
    #                 "url": f'https://www.youtube.com/watch?v={ result["id"] }',
    #                 "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
    #                 "duration": int(
    #                     parse_duration(
    #                         result["contentDetails"]["duration"]
    #                     ).total_seconds()
    #                     // 60
    #                 ),
    #                 "title": result["snippet"]["title"],
    #             }
    #             videos.append(video_data)
    #         cur.execute(
    #             "INSERT INTO youtubedata (YT_DATA, TOPIC_ID) VALUES (%s, %s)",
    #             (json.dumps(videos), topic_id),
    #         )
    #         conn.commit()

    #         new_lst = f"{videos}"
    #         print(new_lst)
    #         return topic

    # else:
    #     cur.execute("INSERT INTO topics_data (TOPIC_NAME) VALUES (%s)", (topic,))
    #     conn.commit()

    #     data_scraped = ExtractText(checked_list)
    #     scraped = data_scraped.scrape_text_from_link()

    #     new = " ".join(scraped.splitlines())

    #     pre = PreProcessor(new)
    #     tokenized = pre.token()
    #     summarizer = Summarization(tokenized)
    #     summ_ids = summarizer.summarize()
    #     result = pre.decoder(summ_ids)
    #     print(result)

    #     cur.execute(
    #         "SELECT topic_id FROM topics_data WHERE topic_name=%s",
    #         (topic,),
    #     )
    #     idd = cur.fetchone()[0]

    #     cur.execute(
    #         "INSERT INTO summaries (SUMMARY, TOPIC_ID, DATA_LINK) VALUES (%s, %s,%s)",
    #         (result, idd, checked_list),
    #     )
    #     conn.commit()

    #     search_url = "https://www.googleapis.com/youtube/v3/search"
    #     video_url = "https://www.googleapis.com/youtube/v3/videos"

    #     videos = []

    #     print("yt")
    #     search_params = {
    #         "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
    #         "q": topic,
    #         "part": "snippet",
    #         "maxResults": 9,
    #         "type": "video",
    #     }

    #     r = requests.get(search_url, params=search_params)

    #     results = r.json()["items"]

    #     video_ids = []
    #     for result in results:
    #         video_ids.append(result["id"]["videoId"])

    #     video_params = {
    #         "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
    #         "id": ",".join(video_ids),
    #         "part": "snippet,contentDetails",
    #         "maxResults": 9,
    #     }

    #     total_vid = video_params["maxResults"]
    #     # print(total_vid)

    #     r = requests.get(video_url, params=video_params)
    #     results = r.json()["items"]
    #     print(results)
    #     for result in results:
    #         video_data = {
    #             "id": result["id"],
    #             "url": f'https://www.youtube.com/watch?v={ result["id"] }',
    #             "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
    #             "duration": int(
    #                 parse_duration(result["contentDetails"]["duration"]).total_seconds()
    #                 // 60
    #             ),
    #             "title": result["snippet"]["title"],
    #         }
    #         videos.append(video_data)
    #     cur.execute(
    #         "INSERT INTO youtubedata (YT_DATA, TOPIC_ID) VALUES (%s, %s)",
    #         (json.dumps(videos), idd),
    #     )
    #     conn.commit()

    #     new_lst = f"{videos}"
    #     print(new_lst)
    #     return topic


@app.route("/uploadDocSum", methods=["GET", "POST"])
# @jwt_required()
def uploadDocSum():
    data = request.get_json()
    text = data["obj"]["data"]
    length = data["obj"]["length"]
    print(text)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT topic_id FROM topics_data WHERE TOPIC_NAME=%s", ("fromText",))
    topic_id = cur.fetchone()

    print(topic_id)
    if topic_id:
        pre = PreProcessor(text)
        tokenized = pre.token()
        summarizer = Summarization(tokenized, length)
        summ_ids = summarizer.summarize()
        result = pre.decoder(summ_ids)
        print(result)

        cur.execute(
            "INSERT INTO summaries (SUMMARY, TOPIC_ID, DATA_LINK) VALUES (%s, %s,%s)",
            (result, topic_id, []),
        )
        conn.commit()
    else:

        cur.execute(
            "INSERT INTO topics_data (TOPIC_NAME) VALUES (%s)", ("fromText",))
        conn.commit()

        pre = PreProcessor(text)
        tokenized = pre.token()
        summarizer = Summarization(tokenized, length)
        summ_ids = summarizer.summarize()
        result = pre.decoder(summ_ids)
        print(result)

        cur.execute(
            "SELECT topic_id FROM topics_data WHERE topic_name=%s",
            ("fromText",),
        )
        idd = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO summaries (SUMMARY, TOPIC_ID, DATA_LINK) VALUES (%s, %s,%s)",
            (result, idd, []),
        )
        conn.commit()

    return jsonify(result)


@app.route("/cn-data/<name>/", methods=["POST"])
# @jwt_required()
def add_data(name):
    namee = request.get_json()
    print(namee["name"])
    new = namee["name"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT topic_id FROM topics where topic_name = %s", (new,))
    top_id = cur.fetchone()[0]

    cur.execute("SELECT * from scraped_data where topic_id=%s", (top_id,))
    exists = cur.fetchone()
    if exists:
        print("already exists")
    else:
        # print(request.json[name])
        scraper = Data_scraper()
        topics = scraper.main()

        scraper.scrapedata(new)
        data_scraped = f"{scraper.output1}\n{scraper.output2}\n{scraper.output3}\n{scraper.output4}\n{scraper.output5}\n{scraper.output6}\n"

        topic_n = new
        print(data_scraped)
        new = " ".join(data_scraped.splitlines())
        # preproc = PreProcessor(new)

        pre = PreProcessor(new)
        tokenized = pre.token()
        summarizer = Summarization(tokenized, "")
        summ_ids = summarizer.summarize()
        result = pre.decoder(summ_ids)
        # summary = preproc.token()
        print(result)

        cur.execute(
            "INSERT INTO scraped_data(TOPIC_ID, SCRAPED_DATAA) VALUES (%s, %s)",
            (top_id, result),
        )
        conn.commit()

        cur.execute("SELECT * from yt_topic_data where topic_id=%s", (top_id,))
        already = cur.fetchone()

        if already:
            print("already.")
        else:

            search_url = "https://www.googleapis.com/youtube/v3/search"
            video_url = "https://www.googleapis.com/youtube/v3/videos"

            videos = []

            if request.method == "POST":
                print("yt")
                search_params = {
                    "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
                    "q": topic_n + "Computer Network",
                    "part": "snippet",
                    "maxResults": 9,
                    "type": "video",
                }

                r = requests.get(search_url, params=search_params)

                results = r.json()["items"]

                video_ids = []
                for result in results:
                    video_ids.append(result["id"]["videoId"])

                # if request.form.get('submit') == 'lucky':
                #     return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

                video_params = {
                    "key": "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
                    "id": ",".join(video_ids),
                    "part": "snippet,contentDetails",
                    "maxResults": 9,
                }

                total_vid = video_params["maxResults"]

                r = requests.get(video_url, params=video_params)
                # print(r)
                results = r.json()["items"]
                # print(results)
                for result in results:
                    video_data = {
                        "id": result["id"],
                        "url": f'https://www.youtube.com/watch?v={ result["id"] }',
                        "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
                        "duration": int(
                            parse_duration(
                                result["contentDetails"]["duration"]
                            ).total_seconds()
                            // 60
                        ),
                        "title": result["snippet"]["title"],
                    }
                    videos.append(video_data)
                cur.execute(
                    "INSERT INTO yt_topic_data (TOPIC_ID, TOTAL_VID, YT_DATA) VALUES (%s, %s, %s)",
                    (top_id, total_vid, json.dumps(videos)),
                )
                conn.commit()

                print(type(videos))
                # new_lst = []
                new_lst = f"{videos}"
                print(new_lst)
                # for i in videos:
                # print(type(i))

    cur.close()
    conn.close()

    # data_s = DataScraped(topic_n, scraped_data)
    # db.session.add(data_s)
    # db.session.commit()
    return jsonify("a")


@app.route("/info")
def Get_Current_User():
    user_id = session.get("user_id")
    print(user_id)

    if not user_id:
        return jsonify({"error": "Unauthorized "}), 401

    if user_id != "9999":
        # Retrieve a user by email:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM user_data WHERE user_id = %s",
            (user_id,),
        )
        account = cur.fetchone()
        print(account)
        # user = User.query.filter_by(id=user_id).first()
        return jsonify({"id": account[0], "email": account[3], "type": "user"})
    else:
        return jsonify({"id": user_id, "email": "admin@gmail.com", "type": "admin"})


@app.route("/login", methods=["GET", "POST"])
def login():
    # Output message if something goes wrong...
    msg = ""
    print(request.json)
    obj = request.json["obj"]
    print(obj, type(obj))
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == "POST":
        # Create variables for easy access
        username = obj["user"]
        password = obj["password"]
        # Check if account exists using MySQL
        if username == "admin" and password == "admin":
            session["user_id"] = "9999"
            return jsonify(
                {
                    "id": "9999",
                    "email": "admin@gmail.com",
                    "Message": "Welcome Admin",
                }
            )
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM user_data WHERE user_name = %s",
                (username,),
            )
            # Fetch one record and return result
            account = cur.fetchone()
            print(account)
            # If account exists in accounts table in out database
            if account:
                # access_token = create_access_token(identity=username)
                # response = {"access_token": access_token}
                # return response
                # Create session data, we can access this data in other routes
                print(password)
                if bcrypt.check_password_hash(
                    account[-1],
                    password,
                ):

                    session["user_id"] = account[0]
                    # Redirect to home page
                    msg = "Login Successful"
                    return jsonify(
                        {
                            "id": account[0],
                            "email": account[3],
                            "Message": "you are Register Successfully",
                        }
                    )
                else:
                    return jsonify({"error": "Incorrect Password "}), 401
                # return 'Logged in successfully!'
            else:
                return jsonify({"error": "Incorrect Credentials "}), 401
            # Account doesnt exist or username/password incorrect
            # msg = "Incorrect username/password!"
            # return jsonify({'error': msg}), 401
    # Show the login form with message (if any)
    # return jsonify(msg)


# @app.route("/logout")
# # @jwt_required()
# def logout():
#     # Remove session data, this will log the user out
#     session.pop("loggedin", None)
#     session.pop("id", None)
#     session.pop("user_name", None)
#     # response = jsonify({"msg": "logout successful"})
#     # unset_jwt_cookies(response)
#     # return response


@app.route("/logout", methods=["POST"])
def User_Logout():
    session.pop("user_id")
    return "200"


@app.route("/signup", methods=["POST"])
def signup():
    # Output message if something goes wrong...
    msg = ""
    print(request.json)
    obj = request.json["obj"]
    print(obj, type(obj))
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == "POST":
        # Create variables for easy access
        username = obj["user"]
        password = obj["password"]
        email = obj["email"]
        fname = obj["name"]

        print(username, password, email, fname)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM user_data WHERE email = %s or user_name = %s",
            (
                email,
                username,
            ),
        )
        account = cur.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = "Account already exists!"
            return jsonify({"error": msg}), 401
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address!"
            return jsonify({"error": msg}), 401
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers!"
            return jsonify({"error": msg}), 401
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed_password = bcrypt.generate_password_hash(
                password).decode("utf8")
            print(hashed_password)
            cur.execute(
                "INSERT INTO user_data (FULL_NAME, USER_NAME, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s)",
                (fname, username, email, hashed_password),
            )
            conn.commit()
            cur.execute(
                "SELECT * FROM user_data WHERE user_name = %s AND email = %s",
                (
                    username,
                    email,
                ),
            )
            # Fetch one record and return result
            account = cur.fetchone()
            cur.close()
            conn.close()
            session["user_id"] = account[0]
            msg = "You have successfully registered!"

            return jsonify({"id": account[0], "email": account[3], "Message": msg})
    # elif request.method == 'POST':
    #     # Form is empty... (no POST data)
    #     msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    # return jsonify(msg)


@app.route("/addDomain", methods=["POST"])
def addDomain():
    # Output message if something goes wrong...
    msg = ""
    print(request.json)
    obj = request.json["obj"]
    print(obj, type(obj))

    if request.method == "POST":
        dname = obj["name"]

        print(dname)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM domain WHERE domain_name = %s",
            (dname,),
        )
        domain = cur.fetchone()
        # If account exists show error and validation checks
        if domain:
            msg = "Domain already there"
            return jsonify({"error": msg}), 401

        else:
            cur.execute(
                "INSERT INTO domain (DOMAIN_NAME, DOMAIN_LINK) VALUES (%s, %s)",
                (dname, ""),
            )
            conn.commit()
            return jsonify({"Message": msg})
    # elif request.method == 'POST':
    #     # Form is empty... (no POST data)
    #     msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    # return jsonify(msg)


@app.route("/addTopic", methods=["GET", "POST"])
def addTopic():
    # Output message if something goes wrong...
    msg = ""
    print(request.json)
    obj = request.json["obj"]
    print(obj, type(obj))

    if request.method == "POST":
        tname = obj["name"]
        tid = obj["id"]
        print(tname)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM topics WHERE topic_name = %s",
            (tname,),
        )
        domain = cur.fetchone()

        if domain:
            msg = "Topic already exists"
            return jsonify({"error": msg}), 401

        else:
            cur.execute(
                "INSERT INTO topics (DOMAIN_ID, TOPIC_NAME, TOPIC_LINK) VALUES (%s, %s, %s)",
                (tid, tname, ""),
            )
            conn.commit()
            return jsonify({"Message": "Topic Added"})


@app.route("/getrelated/<name>", methods=["POST"])
# @jwt_required()
def getrelated(name):
    # print("sssss", request)
    namee = request.get_json()
    # print(namee)
    # print(namee['name'])
    new = namee["name"]
    conn = get_db_connection()
    cur = conn.cursor()
    # print("aa")
    cur.execute("SELECT topic_id from topics where topic_name=%s", (new,))
    idd = cur.fetchone()
    # print(idd)
    cur.execute("SELECT * FROM yt_topic_data where topic_id=%s", (idd,))
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    # print(rv)
    # yt_d = rv[0]
    # print(yt_d)
    # print(yt_d[2])
    # new_l = list(yt_d[2].split(","))
    # print(new_l[0])
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)


@app.route("/getyt/<name>", methods=["POST"])
def getyt(name):
    namee = request.get_json()
    new = namee["name"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics_data where topic_name=%s", (new,))
    topic_id = cur.fetchone()[0]
    cur.execute("SELECT yt_data FROM youtubedata where topic_id=%s", (topic_id,))
    row_headers = [x[0]
                   for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    print(rv)
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    # data = json.loads(json_data[0]["yt_data"])
    # result = [{"yt_data": data}]
    print(json_data)
    return jsonify(json_data)


@app.route("/download/<name>/", methods=["POST"])
# @jwt_required()
def download(name):
    print("pdf")
    namee = request.get_json()
    print(namee["name"])
    new = namee["name"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM topics_data where topic_name=%s", (new,))
    topic_id = cur.fetchone()[0]
    cur.execute("SELECT summary FROM summaries where topic_id=%s", (topic_id,))
    summary = cur.fetchone()[0]
    print(summary)
    splitter(new, summary)
    return jsonify(["done"])
    # Python program to create
    # a pdf file

    # save FPDF() class into a
    # variable pdf
    # with open("output.txt", "w", encoding="utf-8") as f:
    #     f.write(new)
    #     f.write("\n")
    # pdf = FPDF()

    # # Add a page
    # pdf.add_page()

    # # set style and size of font
    # # that you want in the pdf
    # pdf.set_font("Arial", size=15)

    # # create a cell
    # pdf.cell(200, 10, txt=new,
    #          ln=1, align='C')

    # conn = get_db_connection()
    # cur = conn.cursor()

    # cur.execute("SELECT topic_id from topics where topic_name=%s", (new,))
    # out = cur.fetchone()

    # cur.execute("SELECT scraped_dataa from scraped_data where topic_id=%s", (out,))
    # data = cur.fetchone()
    # if data:
    #     print(data[0])
    #     with open("output.txt", "w", encoding="utf-8") as f:
    #         f.write(new)
    #         f.write("\n")
    #         f.write(data[0])
    # add another cell
    # pdf.cell(200, 90, txt=data[0],
    #          ln=2, align='C')

    # # save the pdf with name .pdf
    # pdf.output("{}.pdf".format(new))

    # pdf_file = open("GFG.pdf", "rb")
    # return base64.b64encode(pdf_file.read())


if __name__ == "__main__":
    db.create_all()
    app.run()


# import subprocess
# import psycopg2
# from flask import Flask, render_template, request, flash, jsonify, session, Blueprint, current_app, redirect
# from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
#     unset_jwt_cookies, jwt_required, JWTManager
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import ARRAY
# from flask_marshmallow import Marshmallow
# from flask_cors import CORS, cross_origin
# # from scraper import main, subtopics, scrapedata
# # from scraper_final import Data_scraper
# from sc import Data_scraper
# import json
# # from summarizer import Summarization, PreProcessor
# from bart_sum import PreProcessor, Summarization
# import base64
# import re
# import requests
# from isodate import parse_duration
# from genq import InputProcess
# from fpdf import FPDF
# app = Flask(__name__)

# cors = CORS(app, origins="*",  supports_credentials=True)

# scraper = Data_scraper()
# topics = scraper.main()
# # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:HalaOsama7@localhost/FYP"
# # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# # app.secret_key = "tutor"

# # db = SQLAlchemy(app)
# # ma = Marshmallow(app)
# app.secret_key = 'automatedkeytutor'
# app.config["JWT_SECRET_KEY"] = "automatedtutorkey"
# # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# jwt = JWTManager(app)

# DB_USERNAME = "postgres"
# DB_PASSWORD = "tutorFYP"
# # main = Blueprint('main', __name__)


# def get_db_connection():
#     conn = psycopg2.connect(host='localhost', database='FYP',
#                             user=DB_USERNAME, password=DB_PASSWORD)
#     return conn


# def create_table(query):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute(query)
#     conn.commit()
#     print("Table created successfully in PostgreSQL ")


# create_table('''CREATE TABLE IF NOT EXISTS domain
#             (DOMAIN_ID SERIAL PRIMARY KEY     NOT NULL,
#             DOMAIN_NAME           TEXT  UNIQUE    NOT NULL,
#             DOMAIN_LINK         TEXT        NOT NULL); ''')

# create_table('''CREATE TABLE IF NOT EXISTS topics
#             (TOPIC_ID SERIAL PRIMARY KEY     NOT NULL,
#             DOMAIN_ID INT REFERENCES domain (DOMAIN_ID),
#             TOPIC_NAME           TEXT  UNIQUE    NOT NULL,
#             TOPIC_LINK         TEXT     NOT NULL); ''')

# create_table('''CREATE TABLE IF NOT EXISTS scraped_data
#             (SCRAPED_ID SERIAL PRIMARY KEY     NOT NULL,
#             TOPIC_ID INT REFERENCES topics (TOPIC_ID),
#             SCRAPED_DATA           TEXT    NOT NULL); ''')

# create_table('''CREATE TABLE IF NOT EXISTS yt_topic_data
#             (yt_id serial PRIMARY KEY NOT NULL,
#             TOPIC_ID INT REFERENCES topics (TOPIC_ID),
#             yt_data TEXT NOT NULL); ''')

# create_table('''CREATE TABLE IF NOT EXISTS user_data
#             (USER_ID SERIAL PRIMARY KEY     NOT NULL,
#             FULL_NAME           TEXT    NOT NULL,
#             USER_NAME           TEXT    UNIQUE    NOT NULL,
#             EMAIL           TEXT    UNIQUE    NOT NULL,
#             PASSWORD           TEXT NOT NULL); ''')

# create_table('''CREATE TABLE IF NOT EXISTS quiz
#             (QUIZ_ID SERIAL PRIMARY KEY     NOT NULL,
#             TOPIC_ID INT REFERENCES topics (TOPIC_ID),
#             QUESTIONS           JSON    NOT NULL); ''')

# # conn = get_db_connection()
# # cur = conn.cursor()
# # cur.execute('INSERT INTO domain(DOMAIN_NAME, DOMAIN_LINK) VALUES ( % s, % s)',
# #             ('Computer Networks', 'https://www.javatpoint.com/computer-network-tutorial'))
# # conn.commit()


# @ app.route("/get", methods=["GET"])
# # @jwt_required()
# def get_topics():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     # print("aa")
#     cur.execute('SELECT * FROM topics;')

#     row_headers = [x[0]
#                    for x in cur.description]  # this will extract row headers
#     rv = cur.fetchall()
#     json_data = []
#     for result in rv:
#         json_data.append(dict(zip(row_headers, result)))
#     return jsonify(json_data)


# @ app.route("/getData", methods=["GET"])
# # @jwt_required()
# def get_data():
#     # print("get")
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         'SELECT * FROM scraped_data s join topics on s.topic_id = topics.topic_id;')
#     row_headers = [x[0]
#                    for x in cur.description]  # this will extract row headers
#     rv = cur.fetchall()
#     json_data = []
#     for result in rv:
#         json_data.append(dict(zip(row_headers, result)))

#     cur.close()
#     conn.close()
#     return jsonify(json_data)


# @ app.route('/getquiz/<name>/', methods=['POST'])
# # @jwt_required()
# def getquiz(name):
#     # print("sssss", request)
#     namee = request.get_json()
#     # print(namee)
#     # print(namee['name'])
#     new = namee['name']
#     conn = get_db_connection()
#     cur = conn.cursor()
#     # print("aa")
#     cur.execute("SELECT topic_id from topics where topic_name=%s", (new,))
#     idd = cur.fetchone()
#     # print(idd)
#     cur.execute(
#         'SELECT * FROM quiz where topic_id=%s', (idd,))
#     row_headers = [x[0]
#                    for x in cur.description]  # this will extract row headers
#     rv = cur.fetchall()
#     json_data = []
#     for result in rv:
#         json_data.append(dict(zip(row_headers, result)))
#     return jsonify(json_data)

# # @ app.route("/getUser", methods=["POST"])
# # def get_user():
# #     msg = ""
# #     # Check if "username" and "password" POST requests exist (user submitted form)
# #     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
# #         # Create variables for easy access
# #         username = request.form['username']
# #         password = request.form['password']
# #         # Check if account exists using MySQL
# #         conn = get_db_connection()
# #         cur = conn.cursor()
# #         cur.execute(
# #             'SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
# #         # Fetch one record and return result
# #         account = cur.fetchone()
# #         # If account exists in accounts table in out database
# #         if account:
# #             # Create session data, we can access this data in other routes
# #             session['loggedin'] = True
# #             session['id'] = account['UserID']
# #             session['username'] = account['email']
# #             # Redirect to home page
# #             return 'Logged in successfully!'
# #         else:
# #             # Account doesnt exist or username/password incorrect
# #             msg = 'Incorrect username/password!'
# #     # Show the login form with message (if any)
# #     # return render_template('index.html', msg=msg)
# #     # conn = get_db_connection()
# #     # cur = conn.cursor()
# #     # cur.execute('SELECT * FROM users;')
# #     # row_headers = [x[0]
# #     #                for x in cur.description]  # this will extract row headers
# #     # rv = cur.fetchall()
# #     # json_data = []
# #     # for result in rv:
# #     #     json_data.append(dict(zip(row_headers, result)))
# #     return jsonify(msg)


# @ app.route("/mc-topics", methods=["POST"])
# # @jwt_required()
# def add_topic():
#     result = topics
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "SELECT domain_id FROM domain where domain_name = %s", ('Computer Networks',))
#     dom_id = cur.fetchone()[0]
#     cur.execute("SELECT * from topics where domain_id=%s", (dom_id,))
#     exist = cur.fetchone()
#     if exist:
#         return "already"
#     else:
#         for out in result:
#             cur.execute(
#                 'INSERT INTO topics(DOMAIN_ID, TOPIC_NAME, TOPIC_LINK) VALUES (%s, %s, %s)', (dom_id, out[0], out[1]))
#             conn.commit()
#         cur.execute('SELECT * FROM topics;')

#         row_headers = [x[0]
#                        for x in cur.description]  # this will extract row headers
#         rv = cur.fetchall()
#         json_data = []
#         for result in rv:
#             json_data.append(dict(zip(row_headers, result)))
#         cur.close()
#         conn.close()
#         # domain_name = "Computer Networks"
#         # domain_topics = result
#         # print(domain_topics)

#         # topics = Domains(domain_name, domain_topics)
#         # db.session.add(topics)
#         # db.session.commit()

#         # for topic in result:
#         #     domain_name = topic[0]
#         #     domain_topics = topic[1]

#         #     topics = Domains(domain_name, domain_topics)
#         #     db.session.add(topics)
#         #     db.session.commit()

#         return jsonify(json_data)


# @ app.route("/quiz/<name>/", methods=["POST"])
# def quiz(name):
#     print("sdasd")
#     namee = request.get_json()
#     print(namee['name'])
#     new = namee['name']
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "SELECT topic_id FROM topics where topic_name = %s", (new,))
#     top_id = cur.fetchone()[0]
#     print(top_id)
#     cur.execute("SELECT * from quiz where topic_id=%s", (top_id,))

#     # cur.execute("SELECT * from quiz where topic_id=%s", (top_id,))
#     exists = cur.fetchone()
#     if exists:
#         return "already exists"
#     else:
#         cur.execute(
#             "SELECT scraped_dataa from scraped_data where topic_id=%s", (top_id,))
#         out = cur.fetchone()
#         print(out[0])
#         output = InputProcess()
#         question = output.preprocess_text(out[0])
#         print(question)
#         cur.execute("INSERT INTO quiz (TOPIC_ID, QUESTIONS) VALUES (%s, %s)",
#                     (top_id, json.dumps(question),))
#         conn.commit()
#         cur.close()
#         conn.close()
#         return jsonify(question)


# @ app.route("/cn-data/<name>/", methods=["POST"])
# # @jwt_required()
# def add_data(name):
#     namee = request.get_json()
#     print(namee['name'])
#     new = namee['name']
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "SELECT topic_id FROM topics where topic_name = %s", (new,))
#     top_id = cur.fetchone()[0]

#     cur.execute("SELECT * from scraped_data where topic_id=%s", (top_id,))
#     exists = cur.fetchone()
#     if exists:
#         print("already exists")
#     else:
#         # print(request.json[name])
#         scraper.scrapedata(new)
#         data_scraped = f"{scraper.output1}\n{scraper.output2}\n{scraper.output3}\n{scraper.output4}\n{scraper.output5}\n{scraper.output6}\n"

#         topic_n = new
#         print(data_scraped)
#         new = " ".join(data_scraped.splitlines())
#         # preproc = PreProcessor(new)
#         pre = PreProcessor(new)
#         tokenized = pre.token()
#         summarizer = Summarization(tokenized)
#         summ_ids = summarizer.summarize()
#         result = pre.decoder(summ_ids)
#         # summary = preproc.token()
#         print(result)

#         cur.execute('INSERT INTO scraped_data(TOPIC_ID, SCRAPED_DATAA) VALUES (%s, %s)',
#                     (top_id, result))
#         conn.commit()

#         cur.execute("SELECT * from yt_topic_data where topic_id=%s", (top_id,))
#         already = cur.fetchone()

#         if already:
#             print("already.")
#         else:

#             search_url = 'https://www.googleapis.com/youtube/v3/search'
#             video_url = 'https://www.googleapis.com/youtube/v3/videos'

#             videos = []

#             if request.method == 'POST':
#                 print("yt")
#                 search_params = {
#                     'key': "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
#                     'q': topic_n+"Computer Network",
#                     'part': 'snippet',
#                     'maxResults': 9,
#                     'type': 'video'
#                 }

#                 r = requests.get(search_url, params=search_params)

#                 results = r.json()['items']

#                 video_ids = []
#                 for result in results:
#                     video_ids.append(result['id']['videoId'])

#                 # if request.form.get('submit') == 'lucky':
#                 #     return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

#                 video_params = {
#                     'key': "AIzaSyATk2ehcXjfvJ4EB8Qk6BnsAfjECTBae1M",
#                     'id': ','.join(video_ids),
#                     'part': 'snippet,contentDetails',
#                     'maxResults': 9
#                 }

#                 total_vid = video_params['maxResults']

#                 r = requests.get(video_url, params=video_params)
#                 # print(r)
#                 results = r.json()['items']
#                 # print(results)
#                 for result in results:
#                     video_data = {
#                         'id': result['id'],
#                         'url': f'https://www.youtube.com/watch?v={ result["id"] }',
#                         'thumbnail': result['snippet']['thumbnails']['high']['url'],
#                         'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
#                         'title': result['snippet']['title'],
#                     }
#                     videos.append(video_data)
#                 cur.execute(
#                     "INSERT INTO yt_topic_data (TOPIC_ID, TOTAL_VID, YT_DATA) VALUES (%s, %s, %s)", (top_id, total_vid, json.dumps(videos)))
#                 conn.commit()

#                 print(type(videos))
#                 # new_lst = []
#                 new_lst = f'{videos}'
#                 print(new_lst)
#                 # for i in videos:
#                 # print(type(i))

#     cur.close()
#     conn.close()

#     # data_s = DataScraped(topic_n, scraped_data)
#     # db.session.add(data_s)
#     # db.session.commit()
#     return jsonify("a")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Output message if something goes wrong...
#     print('a')
#     msg = ''
#     print('c')
#     print(request)
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST':
#         print('b')
#         # Create variables for easy access
#         print(request.form)
#         # username = request.json['user']
#         username = "osama123"
#         password = "osama123"
#         # password = request.json['password']
#         # Check if account exists using MySQL
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute(
#             'SELECT * FROM user_data WHERE user_name = %s AND password = %s', (username, password,))
#         # Fetch one record and return result
#         account = cur.fetchone()
#         print(account)
#         # If account exists in accounts table in out database
#         if account:
#             # access_token = create_access_token(identity=username)
#             # response = {"access_token": access_token}
#             # return response
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id'] = account[0]
#             session['user_name'] = account[2]
#             # Redirect to home page
#             msg = "Login Successful"
#             # return 'Logged in successfully!'
#         else:
#             # Account doesnt exist or username/password incorrect
#             msg = 'Incorrect username/password!'
#     # Show the login form with message (if any)
#     return jsonify(msg)


# @app.route('/logout')
# # @jwt_required()
# def logout():
#     # Remove session data, this will log the user out
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('user_name', None)
#     # response = jsonify({"msg": "logout successful"})
#     # unset_jwt_cookies(response)
#     # return response


# @app.route('/signup', methods=["POST"])
# def signup():
#     # Output message if something goes wrong...
#     msg = ''

#     # Check if "username", "password" and "email" POST requests exist (user submitted form)
#     if request.method == 'POST':
#         # Create variables for easy access
#         print(request.form)
#         username = request.json['user']
#         password = request.json['password']
#         email = request.json['email']
#         fname = request.json['name']

#         print(username, password, email, fname)

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute('SELECT * FROM user_data WHERE email = %s', (email,))
#         account = cur.fetchone()
#         # If account exists show error and validation checks
#         if account:
#             msg = 'Account already exists!'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address!'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers!'
#         else:
#             # Account doesnt exists and the form data is valid, now insert new account into accounts table
#             cur.execute(
#                 'INSERT INTO user_data (FULL_NAME, USER_NAME, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s)', (fname, username, email, password))
#             conn.commit()
#             cur.close()
#             conn.close()
#             msg = 'You have successfully registered!'
#     # elif request.method == 'POST':
#     #     # Form is empty... (no POST data)
#     #     msg = 'Please fill out the form!'
#     # Show registration form with message (if any)
#     return jsonify(msg)


# @app.route('/getrelated/<name>', methods=['POST'])
# # @jwt_required()
# def getrelated(name):
#     # print("sssss", request)
#     namee = request.get_json()
#     # print(namee)
#     # print(namee['name'])
#     new = namee['name']
#     conn = get_db_connection()
#     cur = conn.cursor()
#     # print("aa")
#     cur.execute("SELECT topic_id from topics where topic_name=%s", (new,))
#     idd = cur.fetchone()
#     # print(idd)
#     cur.execute(
#         'SELECT * FROM yt_topic_data where topic_id=%s', (idd,))
#     row_headers = [x[0]
#                    for x in cur.description]  # this will extract row headers
#     rv = cur.fetchall()
#     # print(rv)
#     # yt_d = rv[0]
#     # print(yt_d)
#     # print(yt_d[2])
#     # new_l = list(yt_d[2].split(","))
#     # print(new_l[0])
#     json_data = []
#     for result in rv:
#         json_data.append(dict(zip(row_headers, result)))
#     return jsonify(json_data)


# @ app.route("/download/<name>/", methods=["POST"])
# # @jwt_required()
# def download(name):
#     print("pdf")
#     namee = request.get_json()
#     print(namee['name'])
#     new = namee['name']
#     # Python program to create
#     # a pdf file

#     # save FPDF() class into a
#     # variable pdf
#     with open("output.txt", "w", encoding="utf-8") as f:
#         f.write(new)
#         f.write('\n')
#     # pdf = FPDF()

#     # # Add a page
#     # pdf.add_page()

#     # # set style and size of font
#     # # that you want in the pdf
#     # pdf.set_font("Arial", size=15)

#     # # create a cell
#     # pdf.cell(200, 10, txt=new,
#     #          ln=1, align='C')

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT topic_id from topics where topic_name=%s", (new,))
#     out = cur.fetchone()

#     cur.execute(
#         "SELECT scraped_dataa from scraped_data where topic_id=%s", (out,))
#     data = cur.fetchone()
#     if data:
#         print(data[0])
#         with open("output.txt", "w", encoding="utf-8") as f:
#             f.write(new)
#             f.write('\n')
#             f.write(data[0])
#         # add another cell
#         # pdf.cell(200, 90, txt=data[0],
#         #          ln=2, align='C')

#         # # save the pdf with name .pdf
#         # pdf.output("{}.pdf".format(new))

#         # pdf_file = open("GFG.pdf", "rb")
#         # return base64.b64encode(pdf_file.read())


# if __name__ == "__main__":
#     # db.create_all()
#     app.run()
