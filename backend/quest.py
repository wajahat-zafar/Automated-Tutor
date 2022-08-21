#!/usr/bin/env python
import os
import re
import json
import argparse
import pickle
import sys
import spacy
import PyPDF2
##import magic
import glob

from textblob import TextBlob
from nltk.stem.wordnet import WordNetLemmatizer


class Qgen:

##    def _isprp_it(self, tag):
##        """
##        Chhecks if the tag is PRP and the value is it
##        """
##        if tag[1] == 'PRP':
##            if tag[0] == 'it':
##                return True
##            else:
##                return False
##
##        elif tag[0] != 'PRP':
##            return True

    def __init__(self, sentence):
        self.all_possible_tags = set(['VBD', 'VBG', 'VBN', 'VB', 'VBZ']) # these are the verbs we will be using
        self.text = self._clean(sentence)
        self.tags = TextBlob(self.text).tags
        self.question = None
        self.question_tag = None
        self._tag_collection = list()  # to chek if the tags can form a question
        self.formated = str()
        self._new_sentences = list()
        self.genq()
        self._format_question()

##    def _clean(self, sentence):
##        text = re.sub(r'”|“|’|"', '', sentence)
##        return text.lower()
##
##    def _generate_quest(self, item, index):
##        """
##        Generates the question from the sentence.
##        """
##        flag = True
##        if len(item) <= index + 1:
##            return
##
##        elif item[index + 1][1] not in self.all_possible_tags:
##            return
##        self.question = 'Who '
##        if item[index + 1][1] in ['VBG']:
##            self.question = 'Who is '
##        if item[index][1] in ['PRP$']:
##            self.question = 'Whose '
##        if item[index][1] in ['NN'] and item[index][0] not in ['i', 'ive'] and item[index + 1][0] not in ['is']:
##            self.question = 'What '
##        if item[index][0] in ['it']:  # and item[index + 1][0] in ['is']:
##            self.question = 'What '
##        for i in range(index + 1, len(item)):
##            self.question += item[i][0] + ' '
##
##    def genq(self):
##        for index, item in enumerate(self.tags):
##            if item[1] in ['NN', 'NNS', 'PRP', 'NNP', 'NNPS', 'PRP$']:
##                self._generate_quest(self.tags, index)
##                break
##
##    def _format_question(self):
##        """
##        Convert the question to the required generalized form. (future sentence and remove names)
##        """
##        if self.question:
##            self.question_tags = TextBlob(self.question).tags
##        else:
##            return
##        for index, tag in enumerate(self.question_tags):
##            if tag[1] in ['VBD', 'VB', 'VBG', 'VBN', 'PRP', 'VBP', 'VBZ', 'VBP'] and self._can_preseed_verb(index):
##                self.formated += ' will ' + \
##                    WordNetLemmatizer().lemmatize(tag[0], 'v')
##            # Noune and personal pronoun: she, he, it, they
##            elif (tag[1] in ['NNP', 'PRP'] and index != 0 and self._isprp_it(tag)) or tag[0] == 'i':
##                self.formated += ' someone'
##            elif tag[1] in ['PRP$']:  # Possessive pronoun:  her, his , mine
##                self.formated += ' their'
##            elif tag[1] in ['POS']:
##                self.formated += tag[0]
##            elif tag[0] in ['this', 'these']:
##                continue       # determinor: these, this
##            else:
##                self.formated += ' ' + tag[0]
##
##
##    def _can_preseed_verb(self, index):
##        """
##        Checks what values can presead the verb
##        """
##        if index == len(self.question_tags) - 1 and len(self.question_tags) > 2:  # last word
##            return False
##        if index == 0:
##            return True
##        if self.question_tags[index][0] in ['ill', 'didnt', 'didnot', "did'nt"]:
##            return False
##        if len(self.question_tags) - 1 != index and self.question_tags[index + 1][1] in ['VBP']:
##            return False
##        else:
##            if self.question_tags[index - 1][1] in ['WP', 'PRP']:
##                return True
##        return False


class InputProcess:

    def __init__(self):
        
        self.question_set = dict()
        self.counter = 0
        self.all_possible_tags = set(['VBD', 'VBG', 'VBN', 'VB', 'VBZ'])
        self.text = ""
        self.tags = []
        self.question = None
        self.question_tag = None
        self._tag_collection = list()  # to chek if the tags can form a question
        self.formated = str()
        self._new_sentences = list()
        

    def save_data(self):
        """
        Saves the metadata: text, questions, and formated questions as a json
        saves the output as csv
        """
        if self.counter > 0:
            print("Metadata saved successfully")

            with open('meta.json', 'w') as fp:
                    json.dump(self.question_set, fp, indent=4)
            return self.question_set

    def preprocess_text(self, text):
        quest = []
        for elem in re.split(r'\.|,\n|\?|—|,|:', text):
            sentence = elem.rstrip().lstrip()
            if sentence != '':
                self.text = self._clean(sentence)
                self.text = self.text.lower()
                self.tags = TextBlob(self.text).tags
                self.genq()
                self._format_question()
                if self.question:
                    self.question_set[self.formated] = [self.question, self.text]
                    self.counter += 1
                    print(f'processed {self.counter} questions')

                    if True:
                        print("Tags:", self.tags)
                        print("Text: ", self.text)
                        print("Question: ", self.question)
                        print("Formated:", self.formated)
                        print("Question tags:", self.question_tags)
                        print('-' * 20)
                        print('\n')
                        quest.append(self.question)
        return quest

    def _isprp_it(self, tag):
        """
        Chhecks if the tag is PRP and the value is it
        """
        if tag[1] == 'PRP':
            if tag[0] == 'it':
                return True
            else:
                return False

        elif tag[0] != 'PRP':
            return True

    def _clean(self, sentence):
        text = re.sub(r'”|“|’|"', '', sentence)
        return text.lower()

    def _generate_quest(self, item, index):
        """
        Generates the question from the sentence.
        """
        flag = True
        if len(item) <= index + 1:
            return

        elif item[index + 1][1] not in self.all_possible_tags:
            return
        self.question = 'Who '
        if item[index + 1][1] in ['VBG']:
            self.question = 'Who is '
        if item[index][1] in ['PRP$']:
            self.question = 'Whose '
        if item[index][1] in ['NN'] and item[index][0] not in ['i', 'ive'] and item[index + 1][0] not in ['is']:
            self.question = 'What '
        if item[index][0] in ['it']:  # and item[index + 1][0] in ['is']:
            self.question = 'What '
        for i in range(index + 1, len(item)):
            self.question += item[i][0] + ' '

    def genq(self):
        for index, item in enumerate(self.tags):
            if item[1] in ['NN', 'NNS', 'PRP', 'NNP', 'NNPS', 'PRP$']:
                self._generate_quest(self.tags, index)
                break

    def _format_question(self):
        """
        Convert the question to the required generalized form. (future sentence and remove names)
        """
        if self.question:
            self.question_tags = TextBlob(self.question).tags
        else:
            return
        for index, tag in enumerate(self.question_tags):
            if tag[1] in ['VBD', 'VB', 'VBG', 'VBN', 'PRP', 'VBP', 'VBZ', 'VBP'] and self._can_preseed_verb(index):
                self.formated += ' will ' + \
                    WordNetLemmatizer().lemmatize(tag[0], 'v')
            # Noune and personal pronoun: she, he, it, they
            elif (tag[1] in ['NNP', 'PRP'] and index != 0 and self._isprp_it(tag)) or tag[0] == 'i':
                self.formated += ' someone'
            elif tag[1] in ['PRP$']:  # Possessive pronoun:  her, his , mine
                self.formated += ' their'
            elif tag[1] in ['POS']:
                self.formated += tag[0]
            elif tag[0] in ['this', 'these']:
                continue       # determinor: these, this
            else:
                self.formated += ' ' + tag[0]


    def _can_preseed_verb(self, index):
        """
        Checks what values can presead the verb
        """
        if index == len(self.question_tags) - 1 and len(self.question_tags) > 2:  # last word
            return False
        if index == 0:
            return True
        if self.question_tags[index][0] in ['ill', 'didnt', 'didnot', "did'nt"]:
            return False
        if len(self.question_tags) - 1 != index and self.question_tags[index + 1][1] in ['VBP']:
            return False
        else:
            if self.question_tags[index - 1][1] in ['WP', 'PRP']:
                return True
        return False


get_q = InputProcess()
result = get_q.preprocess_text("""
Application layer includes the following functions:  Identifying communication partners for an application with data to transmit .
Determining resource availability: The application layer determines whether sufficient network resources are available for the requested communication .
Synchronizing communication requires cooperation which is managed by an application layer . An application allows a user to access files in a remote computer, to retrieve files from a computer and to manage files .
The application defines a hierarchical virtual file in terms of file structure, file attributes and the kind of operations performed on the files and their attributes . The network architecture is fixed and provides a set of services to applications .
The application architecture is of two types:  Client-server architecture .
A program that sends a request to another application program is known as a client . Client-server architecture is a single-server based architecture which is incapable of holding all the requests from the clients .
P2P (peer-to-peer) architecture: It has no dedicated server in a data center . The peers communicate with each other without passing the information through a dedicated server .
The applications based on P2P architecture includes file sharing and internet telephony .
P2P is cost-effective as it does not require significant server infrastructure and server bandwidth . Application layer is the top most layer in OSI and TCP/IP layered model .
It takes the help of Transport and all layers below it to communicate or transfer its data to the remote host . There is an ambiguity in understanding Application Layer and its protocol .
Not every user application can be put into Application Layer. except those applications which interact with the communication system .
For example, designing software or text-editor cannot be considered as application layer programs . The OSI Model defines network communication used by systems open to interconnection and communication with other systems .
The Open System Interconnection (OSI Model) also defines a logical network and effectively describes computer packet transfer by using various layers of protocols . History of OSI Model:    7 Layers of the OSi Model .
Layers should only be created where the definite levels of abstraction are needed .
OSI Model has some important characteristics . The function of each layer should be selected as per the internationally standardized protocols .
The number of layers should be large so that separate functions should not be put in the same layer .
In the OSI model, each layer relies on the next lower layer to perform primitive functions . Every level should be able to provide services to the next higher layer Changes made in one layer should not need changes in other lavers .
The ISO conducted a program to develop general standards and methods of networking .
In 1973, an Experimental Packet Switched System in the UK identified the requirement for defining the higher-level protocols . OSI model was initially intended to be a detailed specification of actual interfaces .
In 1984, OSI architecture was formally adopted by ISO as an international standard 7 Layers of the OSI Model OSI model is a layered server architecture system in which each layer is defined according to a specific function to perform . The Lower Layers handle activities related to data transport. The physical layer and datalink layers also implemented in software and hardware .
The Upper Layers deals with application issues and mostly implemented only in software . Upper and Lower layers further divide network architecture into seven different layers as below  Application Presentation Session Transport Network, Data-link Physical layers .
Physical Layer helps you define the electrical and physical specifications of the data connection .
Data Link Layer: Data link layer corrects errors which can occur at the physical layer . The data link layer is subdivided into two types of sublayers: Media Access Control (MAC) layer- It is responsible for controlling how device in a network gain access to medium and permits to transmit data .
Logical link control layer- This layer are responsible for identity and encapsulating network-layer protocols and allows you to find the error . The transport layer builds on the network layer to provide data transport from a process on a source machine to a destination machine .
It is hosted using single or multiple networks, and also maintains the quality of service functions . TTC is the best-known example of the transport layer .
It divides the message received from the session layer into segments and numbers them to make a sequence .
The transport layer also offers an acknowledgment of the successful data transmission . Transport layer makes sure that the message is delivered to the correct process on the destination machine .
The network layer provides the functional and procedural means of transferring variable length data sequences from one node to another connected in different networks . Session layer offers services like dialog discipline, which can be duplex or half-duplex. It is mostly implemented in application environments that use remote procedure calls .
Presentation Layer Presentation layer transforms data into the form which is accepted by the application . The function of Presentation Layers:  Character code translation from ASCII to EBCDIC.  Data compression: Allows to reduce the number of bits that needs to be transmitted on the network .
The application layer interacts with an application program, which is the highest level of OSI model . Application layer interacts with software applications to implement a communicating component .
The function of the Application Layers are:  Application-layer helps you to identify communication partners, determining resource availability, and synchronizing communication .
Application-layer allows users to log on to a remote host . Interaction Between OSI Model Layers Information sent from a one computer application to another needs to pass through each of the OSI layers .
Every layer within an OSI model communicates with the other two layers which are below it and its peer layer .
The data link layer of the first system communicates with two layers, the network layer and the physical layer . Protocols supported at various levels Differences between OSI & TCP/IP model .
Advantages of the OSI Model are:  It helps you to standardize router, switch, motherboard, and other hardware .
It is a standard model in computer networking. Supports connectionless and connectionless services . The OSI network layer model is a standard model in computer networking .
It helps you to standardize router, switch, motherboard, and other hardware .
Fitting of protocols is a tedious task . Application Layer is topmost layer in the Open System Interconnection (OSI) model .
It provides several ways for manipulating the data (information) which actually enables any type of user to access network with ease . Application Layer provides a facility by which users can forward several emails .
This layer allows users to access, retrieve and manage files in a remote computer .
It provides access to global information about various services . Application Layer provides access to global information about various services .
This layer provides services which include: e-mail, transferring files, distributing results to the user, directory services, network resources . Application Layer helps us to identify communication partners, synchronizing communication .
This layer allows users to interact with other software applications .
In the OSI model, this application layer is narrower in scope . The application layer in the OSI model generally acts only like the interface which is responsible for communicating with host-based and user-facing applications .
This is in contrast with TCP/IP protocol, wherein the layers below the application layer, which is Session Layer and Presentation layer, are clubbed together and form a simple single layer . The client sends an initiation connection request to server and when server receives request, it gives acknowledgement (ACK) to client through client .
The client has access to server through which it may either ask server to send any types of files or other documents . Application layer protocols are implemented the same on source host and destination host .
The Application Layer protocol defines process for both parties which are involved in communication . The application layer provides several protocols which allow any software to easily send and receive information .
The following are some of the protocols which are provided by the application layer .
TELNET: Telnet stands for Telecommunications Network . FTP stands for File Transfer Protocol. This protocol helps to transfer different files from one device to another .
FTP promotes sharing of files via remote computer devices with reliable, efficient data transfer . HTTP is a stateless protocol in which a client sends requests to server and server responses back as per the given state .
HTTP uses port 80.NFS: NFS stands for Network File System .
TELNET: Telnet stands for Telecommunications Network . The DNS service translates the domain name (selected by user) into the corresponding IP address .
The DNS protocol uses the port number 53. DHCP: DHCP stands for Dynamic Host Configuration Protocol. It provides IP addresses to hosts . SMTP stands for Simple Mail Transfer Protocol. It is used to transfer electronic mail from one user to another user .
HTTP is the foundation of the World Wide Web (WWW) SNMP is the top most layer of OSI Model .
It gathers data by polling devices from the network to the management station at fixed or random intervals .
The Application Layer contains a variety of protocols . Application Layer Mail Services: This layer provides the basis for E-mail forwarding and storage .
Network Virtual Terminal: It allows a user to log on to a remote host .
Remote host believes it is communicating with one of its own terminals . The application layer provides services for an application program to ensure that effective communication with another application program on a network is possible .
Patterns from several pattern languages can be addressed . The application layer is a component within an application that controls the communication method to other devices .
It's an abstraction layer service that masks the rest of the application from the transmission process .
At this stage, the data is presented in a visual form the user can understand . Ensures that the receiving device is identified, can be reached and is ready to accept data . Enables, if appropriate, authentication to occur between devices for an extra layer of security .
Determines protocol and data syntax rules at the application level .
""")
print(result)

