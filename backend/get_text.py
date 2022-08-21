import trafilatura


class ExtractText:
    def __init__(self, links_list):
        self.links_list = links_list

    def scrape_text_from_link(self):
        summary = ""
        for i in self.links_list:
            try:
                downloaded = trafilatura.fetch_url(i)
                text = trafilatura.extract(downloaded, include_links=False)

                summary += f"{text}\n\n\n\n"
            except:
                pass
        return summary


##lst_links = ['https://www.geeksforgeeks.org/data-communication-definition-components-types-channels/',
##             'https://www.tutorialspoint.com/data_communication_computer_network/index.htm',
##             'https://www.techopedia.com/definition/6765/data-communications-dc',
##             'https://ecomputernotes.com/computernetworkingnotes/communication-networks/what-is-data-communication',
##             'https://www.camiresearch.com/Data_Com_Basics/data_com_tutorial.html']


##lst_links = ['https://www.geeksforgeeks.org/data-communication-definition-components-types-channels/',
##             'https://www.tutorialspoint.com/data_communication_computer_network/index.htm'
##             ]
##get_text = ExtractText(lst_links)
##summary_result = get_text.scrape_text_from_link()
##print(summary_result)
