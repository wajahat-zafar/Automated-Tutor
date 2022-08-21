from bs4 import BeautifulSoup
import requests
import csv


def mc_topics():
    template_link = "mobile-computing"

    javatpoint = "https://www.javatpoint.com/"

    new_link = javatpoint + template_link
    source = requests.get(new_link).text

    soup = BeautifulSoup(source, "lxml")

    left_menu = soup.find("div", class_="leftmenu")

    dct = []
    for topics_links in left_menu.find_all("a"):
        topic_name = topics_links.text
        each_topic_link = javatpoint + topics_links["href"]
        dct.append([topic_name, each_topic_link, ""])

    return dct


mc_topics()
