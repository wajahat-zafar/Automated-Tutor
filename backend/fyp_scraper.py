# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import json
# import time
#
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import csv

# chrome_options = webdriver.ChromeOptions()
# CHROMEDRIVER_PATH = "E:\ARSAL\Semesters\Semester VII\FYP\Scrapper\chromedriver.exe"
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)

def main():
    print("Mobile Computing Topics\n")

    template_link = "mobile-computing"

    javatpoint = "https://www.javatpoint.com/"

    new_link = javatpoint+template_link
    print(new_link,'\n')
    source = requests.get(new_link).text

    soup = BeautifulSoup(source,'lxml')


    left_menu = soup.find('div',class_='leftmenu')
    # print(left_menu.prettify())

    dct = {}
    counter = 1
    for topics_links in left_menu.find_all('a'):
        topic_name = topics_links.text
        each_topic_link = javatpoint+topics_links['href']
        dct[counter] = [topic_name,each_topic_link]
        counter+=1
        # print(each_topic_link)
        # print('\n')
    # print(dct)

    for k,v in dct.items():
        print(k,v[0],v[1])

    # user_inp = input('\nEnter which topic do you want? ')
    # new_page = dct[int(user_inp)]
    # new_page = new_page[1]

    # print(new_page)
    # source = requests.get(new_page).text

    # soup = BeautifulSoup(source,'lxml')

    # big_template = soup.find('div',class_='onlycontentinner')
    #     # print(big_template.text)
    # print(big_template.text)
    #     # print(big_template)
    #     #
    #     # for content in big_template.find_all('p'):
    #     #     print(1)
    #     #     print(content)

    # # for i in big_template.find
    # # new = big_template.find_all_previous('div',class_='nexttopicdiv')
    # # print(new)

    
main()