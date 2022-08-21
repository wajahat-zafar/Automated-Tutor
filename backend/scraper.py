from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from threading import Thread

import fpdf

dct = {}
topics = []


def main():

    ##
    # print("Data Communication and Computer Networks Topics\n")

    template_link = "computer-network-tutorial"

    javatpoint = "https://www.javatpoint.com/"

    new_link = javatpoint+template_link
# print(new_link,'\n')

    source = requests.get(new_link).text

    soup = BeautifulSoup(source, 'lxml')

    main_headings = soup.findAll('h2', {"class": "spanh2"})
    left_menu = soup.findAll('div', {"class": "leftmenu"})

    headings = []
    c = 1
    for heading in main_headings:

        for x in heading.find('span'):

            heading_n = x

            headings.append(heading_n)
            c += 1

    counter = 0
    for topics_links in left_menu:
        t = topics_links.findAll('a')
        lst = []
        for x in t:
            topic_name = x.text
            each_topic_link = javatpoint+x['href']
            lst.append([topic_name, each_topic_link])
        dct[headings[counter]] = lst
        counter += 1

    for k in list(dct):
        for x in dct[k]:
            if 'Tutorial' in x:
                dct[k].remove(x)
        if 'MCQ' in k:
            dct.pop(k)
        if 'Questions' in k:
            dct.pop(k)

    counter = 1
    new_dict = {}
    g = 1
    for k, v in dct.items():
        for x in v:
            new_dict[g] = [k+" "+x[0], x[1]]
            g += 1
    # for k, v in dct.items():
    #     print(counter, k)
    #     counter += 1

    # print(dct)

    for k, v in dct.items():
        topics.append([k, v[0][1]])
    # print(lst)
    return topics


# main()


def subtopics():
    # print("dct", dct)
    subs = {}
    for k, v in dct.items():
        new = []
        for i in v:
            new.append(i[0])
        subs[k] = new
    # print(subs)
    return subs


# subtopics()


def scrapedata(select):
    # nn_dct = {}
    ##
    # nn = 1
    # for k,v in dct.items():
    # nn_dct[nn] = [k,v]
    # nn += 1
    ##
    # nn_lst = {}
    # user_inp = input('\nEnter which topic do you want? ')
    ##
    # dd = nn_dct[int(user_inp)]
    # nc = 1
    # print(f'Which topic to do you want to learn about?\n ')
    ##
    # new_topic_names = []
    # lnks = []
    ##
    # for i in dd[1]:
    # print(nc, i[0])
    # new_topic_names.append(i[0])
    # lnks.append(i[1])
    # nc+=1
    ##
    # user_input_again = input('\nEnter which topic do you want? ')

    global output
    output = ""

    PATH = "F:/Desktop/fyp_code/backend/chromedriver.exe"
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
# driver = webdriver.Chrome(options=options, executable_path=PATH)

    print("\n\n\n NAME", select)

##    print("dct", dct)
##    print("\n\n slt", topics)
    for i in topics:
        print(i)
        if i[0] == select:
            new_topic_name = select
            new_page = i[1]
    # for k, v in dct.items():
    #     # print("out", v)
    #     for x in v:
    #         # print("x", x)
    #         if select == x[0]:
    #             print("yes", select)
    #             new_topic_name = select
    #             new_page = x[1]
##
# new_page = new_dict[int(user_inp)]
# new_page = new_page[1]
##
# new_topic_name = new_topic_names[int(user_input_again)-1]
# og_topic_name = new_topic_names[int(user_input_again)-1]
##
# new_page = lnks[int(user_input_again)-1]

# print(new_topic_name)
# print(new_page)
    og_topic_name = new_topic_name
    print("\n\n\n\nNAME", og_topic_name)
    source = requests.get(new_page).text

    soup = BeautifulSoup(source, 'lxml')

    big_template = soup.find('div', id='city')
    btn = soup.find('div', id="bottomnextup")
    btn1 = soup.find('div', id="bottomnext")
    btn2 = soup.find('div', class_="nexttopicdiv")
    btn.clear()
    btn1.clear()
    btn2.clear()

    fileopen2 = open('data4.txt', 'w')

# print(big_template.text)
    fileopen2.write(big_template.text)
    output += "\n" + big_template.text

##    print('\nNow for tutorialspoint')
##    new_topic_name = new_topic_name.split()
##    new_topic_name = "+".join(new_topic_name)
##    google_link = f'https://www.google.com/search?q={new_topic_name}+%3Atutorialspoint.com'
# print(google_link)
##
##    source = requests.get(google_link).text
##
##    soup = BeautifulSoup(source, 'lxml')
##
##    google_topic_link = soup.find('div', {"id": "search"})
# print(google_topic_link)
# print(soup.prettify())

    def tutorial_point():
        global output
        driver = webdriver.Chrome(
            options=options, executable_path=PATH)

        driver.get('https://www.google.com')
        search_kw = og_topic_name + ' :tutorialspoint.com'
        search = driver.find_element_by_name('q')
        search.send_keys(search_kw)
        search.send_keys(Keys.RETURN)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        google_topic_link = soup.find('div', {"class": "v7W49e"})
        # print(google_topic_link.prettify())
        # print(soup.prettify())
        try:
            link = google_topic_link.find('a')
            link = link['href']
# print(link)
            # v7W49e
            # driver.close()

            driver.get(link)

        except:
            link = google_topic_link.find_all('a')[1]
            link = link['href']
# print(link)
            # v7W49e
            # driver.close()

            driver.get(link)

# print(link)
        # v7W49e
        # driver.close()

        source = requests.get(link).text
        soup = BeautifulSoup(source, 'lxml')

        new_big_template = soup.find(
            'div', class_='mui-col-md-6 tutorial-content')
        btn3 = soup.find('div', class_="qa_category")
        try:
            btn3.clear()
        except:
            None

        btn4 = soup.find('div', class_="mui-panel profile-panel")
        try:
            btn4.clear()
        except:
            None

        btn5 = soup.find('ul', class_="toc chapters")
        try:
            btn5.clear()
        except:
            None

        btn6 = soup.find(
            'div', class_="mui-container-fluid button-borders show")
        try:
            btn6.clear()
        except:
            None

        btn7 = soup.find('div', class_="google-bottom-ads")
        try:
            btn7.clear()
        except:
            None

        btn8 = soup.find('div', id="ebooks_grid")
        try:
            btn8.clear()
        except:
            None

        fileopen9 = open('data2.txt', 'w', encoding="utf-8")

        srr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']
        for all_text in new_big_template.find_all(srr):
            # print(all_text.text)
            # print('\n')
            fileopen9.write(all_text.text)
            output += "\n" + all_text.text

        driver.close()

    def guru():
        global output
        driver2 = webdriver.Chrome(
            options=options, executable_path=PATH)

        driver2.get('https://www.google.com')
        search_kw = og_topic_name + ' :guru99.com'
        search = driver2.find_element_by_name('q')
        search.send_keys(search_kw)
        search.send_keys(Keys.RETURN)

        soup = BeautifulSoup(driver2.page_source, 'lxml')
        google_topic_link = soup.find('div', {"class": "v7W49e"})
        # print(google_topic_link.prettify())
        # print(soup.prettify())
        try:
            nlink = google_topic_link.find('a')
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver2.get(nlink)

        except:
            nlink = google_topic_link.find_all('a')[1]
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver2.get(nlink)

        time.sleep(5)

        # source = requests.get(nlink).text
        soup2 = BeautifulSoup(driver2.page_source, 'lxml')
        # print(soup2.prettify())

        new_big_template2 = soup2.find('div', class_='entry-content-wrap')

        try:

            summ = soup2.find_all('h2')[-3]
            summ1 = soup2.find(
                'div', class_='entry-content').find_all('ul')[-2]
            summ.clear()
            summ1.clear()

        except:
            None

        try:
            y = soup2.find('div', class_='yarpp')
            y.clear()
        except:
            None

        fileopen = open('data1.txt', 'w', encoding="utf-8")
        sr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']

        for all_text in new_big_template2.find_all(sr):
            # print(all_text.text)
            fileopen.write(all_text.text)
            # print('\n')
            output += "\n" + all_text.text

        driver2.close()
        # output += all_text.text

    def geeks():
        global output
        driver3 = webdriver.Chrome(
            options=options, executable_path=PATH)

        driver3.get('https://www.google.com')
        search_kw = og_topic_name + ' :geeksforgeeks.org'
        search = driver3.find_element_by_name('q')
        search.send_keys(search_kw)
        search.send_keys(Keys.RETURN)

        soup3 = BeautifulSoup(driver3.page_source, 'lxml')
        google_topic_link = soup3.find('div', {"class": "v7W49e"})

        # print(google_topic_link.prettify())
        # print(soup.prettify())
        try:
            nlink = google_topic_link.find('a')
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver3.get(nlink)

        except:
            nlink = google_topic_link.find_all('a')[1]
# print(nlink)
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver3.get(nlink)

        time.sleep(5)

        # source = requests.get(nlink).text
        soup3 = BeautifulSoup(driver3.page_source, 'lxml')
        # print(soup2.prettify())

        try:
            new_big_template3 = soup3.find('article')
            bb = soup3.find('div', class_='media')
            bb.clear()
        except:
            None
        # summ = soup2.find_all('h2')[-3]
        # summ1 = soup2.find('div', class_='entry-content').find_all('ul')[-2]
        # y = soup2.find('div', class_='yarpp')
        # summ.clear()
        # summ1.clear()
        # y.clear()

        fileopen = open('data3.txt', 'w', encoding="utf-8")
        sr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']
        for all_text in new_big_template3.find_all(sr):
            # print(all_text.text)
            fileopen.write(all_text.text)
            output += "\n" + all_text.text
            # print('\n')

        driver3.close()

    # STUDY TONIGHT

    def study_point():
        global output
        driver4 = webdriver.Chrome(
            options=options, executable_path=PATH)

        driver4.get('https://www.google.com')
        search_kw = og_topic_name + ' :studytonight.com'
        search = driver4.find_element_by_name('q')
        search.send_keys(search_kw)
        search.send_keys(Keys.RETURN)

        soup = BeautifulSoup(driver4.page_source, 'lxml')
        google_topic_link = soup.find('div', {"class": "v7W49e"})
        # print(google_topic_link.prettify())
        # print(soup.prettify())
        try:
            nlink = google_topic_link.find('a')
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver4.get(nlink)
        except:
            nlink = google_topic_link.find_all('a')[1]
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver4.get(nlink)

        # source = requests.get(nlink).text
        soup4 = BeautifulSoup(driver4.page_source, 'lxml')
        # print(soup2.prettify())

        fileopen = open('data5.txt', 'w', encoding="utf-8")
        try:
            clearr = soup4.find('ul', class_='pager')
            clearr.clear()
        except:
            None

        try:
            new_big_template4 = soup4.find('article')
            sr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']
            for all_text in new_big_template4.find_all(sr):
                # print(all_text.text)
                fileopen.write(all_text.text)
                output += "\n" + all_text.text
                # print('\n')
        except:
            None

        try:
            new_big_template4 = soup4.find('div', class_='p-2')
            sr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']
            for all_text in new_big_template4.find_all(sr):
                print(all_text.text)
                # print('\n')
                fileopen.write(all_text.text)
                output += "\n" + all_text.text

        except:
            None

        try:
            new_big_template4 = soup4.find('div', id='body-content')
            sr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']
            for all_text in new_big_template4.find_all(sr):
                # print(all_text.text)
                fileopen.write(all_text.text)
                output += "\n" + all_text.text

                # print('\n')
        except:
            None

        try:
            new_big_template4 = soup4.find('blockquote', class_='fs-5')
            sr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']
            for all_text in new_big_template4.find_all(sr):
                # print(all_text.text)
                # print('\n')
                fileopen.write(all_text.text)
                output += "\n" + all_text.text

        except:
            None

        driver4.close()

    def techtarget():
        global output
        driver7 = webdriver.Chrome(
            options=options, executable_path=PATH)

        driver7.get('https://www.google.com')
        search_kw = og_topic_name + ' :www.techtarget.com'
        search = driver7.find_element_by_name('q')
        search.send_keys(search_kw)
        search.send_keys(Keys.RETURN)

        soup3 = BeautifulSoup(driver7.page_source, 'lxml')
        google_topic_link = soup3.find('div', {"class": "v7W49e"})

        # print(google_topic_link.prettify())
        # print(soup.prettify())
        try:
            nlink = google_topic_link.find('a')
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver7.get(nlink)

        except:
            nlink = google_topic_link.find_all('a')[1]
            nlink = nlink['href']
# print(nlink)
            # v7W49e
            # driver.close()

            driver7.get(nlink)

        # time.sleep(5)

        # source = requests.get(nlink).text
        # fastrack = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))

        # try:
        #     element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="content-body"]/section[1]/h3'))
        #     WebDriverWait(driver7, 3).until(element_present)
        # except:
        #     print("Timed out waiting for page to load")

        # source = driver7.page_source
        #
        # driver7.close()

        soup3 = BeautifulSoup(driver7.page_source, 'lxml')
        # print(soup2.prettify())
        driver7.close()
        new_big_template3 = soup3.find('section', id='content-body')
        try:
            bb = soup3.find('h3', class_='section-title')
            bb.clear()
        except:
            None

        try:
            bbe = soup3.find('section', class_='contributors-block')
            bbe.clear()
        except:
            None
        # summ = soup2.find_all('h2')[-3]
        # summ1 = soup2.find('div', class_='entry-content').find_all('ul')[-2]
        # y = soup2.find('div', class_='yarpp')
        # summ.clear()
        # summ1.clear()
        # y.clear()

        try:

            bba = soup3.find
            bba.clear()
        except:
            None
        fileopen = open('data6.txt', 'w', encoding="utf-8")
        sr = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'li']
        for all_text in new_big_template3.find_all(sr):
            # print(all_text.text)
            fileopen.write(all_text.text)
            # print('\n')
            output += "\n" + all_text.text

        # driver7.close()
    a1 = Thread(target=tutorial_point)
    a2 = Thread(target=guru)
    a3 = Thread(target=geeks)
    a4 = Thread(target=study_point)
    a5 = Thread(target=techtarget)

    a1.start()
# a2.start()
# a3.start()
# a4.start()
# a5.start()
##
# a1.join()
# a2.join()
# a3.join()
# a4.join()
# a5.join()

    print('done')

    return output

    # tutorial_point()
    # guru()
    # geeks()
    # study_point()
    # print('all done')
##scrapedata("Network Layer")
