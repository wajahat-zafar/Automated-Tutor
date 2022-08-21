import torch
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration


class Summarization:
    def __init__(self, text_ids, length):
        self.text_ids = text_ids
        self.length = length
        self.model = BartForConditionalGeneration.from_pretrained(
            'F:\\Desktop\\fyp_code\\backend\\model_cnn')

    def summarize(self):

        print('\n\n', self.text_ids)
        l = list(self.text_ids.size())[1]

        print(l)
        if self.length == "short":
            summ_ids = self.model.generate(self.text_ids, num_beams=4, length_penalty=2.0,
                                           max_length=int(float(l/2)), min_length=int(float(l/4)), no_repeat_ngram_size=3, early_stopping=False)
        elif self.length == "medium":
            summ_ids = self.model.generate(self.text_ids, num_beams=4, length_penalty=2.0,
                                           max_length=int(float(l-(l/4))), min_length=int(float(l/3)), no_repeat_ngram_size=3, early_stopping=False)
        elif self.length == "long" or self.length == "":
            summ_ids = self.model.generate(self.text_ids, num_beams=4, length_penalty=2.0,
                                           max_length=l, min_length=int(float(l/2)), no_repeat_ngram_size=3, early_stopping=False)

        return summ_ids


class PreProcessor:
    def __init__(self, text):
        self.text = text
        self.tokenizer = BartTokenizer.from_pretrained(
            'F:\\Desktop\\fyp_code\\backend\\model_cnn')

    def token(self):

        text = self.text.replace('\n', '')
        print(self.text)
        text_input_ids = self.tokenizer.batch_encode_plus(
            [text], return_tensors='pt', max_length=1024, truncation=True)['input_ids'].to(torch_device)
        return text_input_ids

    def decoder(self, summ_ids):
        summary_txt = self.tokenizer.decode(
            summ_ids.squeeze(), skip_special_tokens=True)
        return summary_txt


torch_device = 'cpu'

##tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
##model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

##tokenizer = BartTokenizer.from_pretrained('F:\\Desktop\\fyp_code\\backend\\model_cnn')
##model = BartForConditionalGeneration.from_pretrained('F:\\Desktop\\fyp_code\\backend\\model_cnn')

FileContent = """
Application Layer
The application layer in the OSI model is the closest layer to the end user which means that the application layer and end user can interact directly with the software application. The application layer programs are based on client and servers.
The Application layer includes the following functions:

Identifying communication partners: The application layer identifies the availability of communication partners for an application with data to transmit.
Determining resource availability: The application layer determines whether sufficient network resources are available for the requested communication.
Synchronizing communication: All the communications occur between the applications requires cooperation which is managed by an application layer.

Services of Application Layers

Network Virtual terminal: An application layer allows a user to log on to a remote host. To do so, the application creates a software emulation of a terminal at the remote host. The user's computer talks to the software terminal, which in turn, talks to the host. The remote host thinks that it is communicating with one of its own terminals, so it allows the user to log on.
File Transfer, Access, and Management (FTAM): An application allows a user to access files in a remote computer, to retrieve files from a computer and to manage files in a remote computer. FTAM defines a hierarchical virtual file in terms of file structure, file attributes and the kind of operations performed on the files and their attributes.
Addressing: To obtain communication between client and server, there is a need for addressing. When a client made a request to the server, the request contains the server address and its own address. The server response to the client request, the request contains the destination address, i.e., client address. To achieve this kind of addressing, DNS is used.
Mail Services: An application layer provides Email forwarding and storage.
Directory Services: An application contains a distributed database that provides access for global information about various objects and services.
Authentication: It authenticates the sender or receiver's message or both.

Network Application Architecture
Application architecture is different from the network architecture. The network architecture is fixed and provides a set of services to applications. The application architecture, on the other hand, is designed by the application developer and defines how the application should be structured over the various end systems.
Application architecture is of two types:

Client-server architecture: An application program running on the local machine sends a request to another application program is known as a client, and a program that serves a request is known as a server. For example, when a web server receives a request from the client host, it responds to the request to the client host.

Characteristics Of Client-server architecture:

In Client-server architecture, clients do not directly communicate with each other. For example, in a web application, two browsers do not directly communicate with each other.
A server is fixed, well-known address known as IP address because the server is always on while the client can always contact the server by sending a packet to the sender's IP address.

Disadvantage Of Client-server architecture:
It is a single-server based architecture which is incapable of holding all the requests from the clients. For example, a social networking site can become overwhelmed when there is only one server exists.

P2P (peer-to-peer) architecture: It has no dedicated server in a data center. The peers are the computers which are not owned by the service provider. Most of the peers reside in the homes, offices, schools, and universities. The peers communicate with each other without passing the information through a dedicated server, this architecture is known as peer-to-peer architecture. The applications based on P2P architecture includes file sharing and internet telephony.


Features of P2P architecture

Self scalability: In a file sharing system, although each peer generates a workload by requesting the files, each peer also adds a service capacity by distributing the files to the peer.
Cost-effective: It is cost-effective as it does not require significant server infrastructure and server bandwidth.

Client and Server processes

A network application consists of a pair of processes that send the messages to each other over a network.
In P2P file-sharing system, a file is transferred from a process in one peer to a process in another peer. We label one of the two processes as the client and another process as the server.
With P2P file sharing, the peer which is downloading the file is known as a client, and the peer which is uploading the file is known as a server. However, we have observed in some applications such as P2P file sharing; a process can be both as a client and server. Therefore, we can say that a process can both download and upload the files.









Application Layer Introduction
Application layer is the top most layer in OSI and TCP/IP layered model. This layer exists in both layered Models because of its significance, of interacting with user and user applications.  This layer is for applications which are involved in communication system.
A user may or may not directly interacts with the applications.  Application layer is where the actual communication is initiated and reflects.  Because this layer is on the top of the layer stack, it does not serve any other layers.  Application layer takes the help of Transport and all layers below it to communicate or transfer its data to the remote host.
When an application layer protocol wants to communicate with its peer application layer protocol on remote host, it hands over the data or information to the Transport layer.  The transport layer does the rest with the help of all the layers below it.
There’is an ambiguity in understanding Application Layer and its protocol.  Not every user application can be put into Application Layer. except those applications which interact with the communication system.  For example, designing software or text-editor cannot be considered as application layer programs.
On the other hand, when we use a Web Browser, which is actually using  Hyper Text Transfer Protocol (HTTP) to interact with the network. HTTP is Application Layer protocol.
Another example is File Transfer Protocol, which helps a user to transfer text based or binary files across the network.  A user can use this protocol in either GUI based software like FileZilla or CuteFTP and the same user can use FTP in Command Line mode.
Hence, irrespective of which software you use, it is the protocol which is considered at Application Layer used by that software.  DNS is a protocol which helps user application protocols such as HTTP to accomplish its work.

OSI Model Layers and Protocols in Computer Network
What is OSI Model?
The OSI Model is a logical and conceptual model that defines network communication used by systems open to interconnection and communication with other systems. The Open System Interconnection (OSI Model) also defines a logical network and effectively describes computer packet transfer by using various layers of protocols.
In this tutorial, you will learn:

Characteristics of OSI Model    
Why of OSI Model?    
What is OSI Model?    		
History of OSI Model    
7 Layers of the OSI Model    
Physical Layer    
Data Link Layer    
Transport Layer    
Network Layer    
Session Layer    
Presentation Layer    
Application Layer    
Interaction Between OSI Model Layers    
Protocols supported at various levels    
Differences between OSI & TCP/IP    
Advantages of the OSI Model    
Disadvantages of the OSI Model    

Characteristics of OSI Model    
Why of OSI Model?    
What is OSI Model?    		
History of OSI Model    
7 Layers of the OSI Model    
Physical Layer    
Data Link Layer    
Transport Layer    
Network Layer    
Session Layer    
Presentation Layer    
Application Layer    
Interaction Between OSI Model Layers    
Protocols supported at various levels    
Differences between OSI & TCP/IP    
Advantages of the OSI Model    
Disadvantages of the OSI Model    
Characteristics of OSI Model
Here are some important characteristics of the OSI model:

A layer should only be created where the definite levels of abstraction are needed.
The function of each layer should be selected as per the internationally standardized protocols.
 The number of layers should be large so that separate functions should not be put in the same layer. At the same time, it should be small enough so that architecture doesn’t become very complicated.
In the OSI model, each layer relies on the next lower layer to perform primitive functions. Every level should able to provide services to the next higher layer
Changes made in one layer should not need changes in other lavers.

A layer should only be created where the definite levels of abstraction are needed.
The function of each layer should be selected as per the internationally standardized protocols.
 The number of layers should be large so that separate functions should not be put in the same layer. At the same time, it should be small enough so that architecture doesn’t become very complicated.
In the OSI model, each layer relies on the next lower layer to perform primitive functions. Every level should able to provide services to the next higher layer
Changes made in one layer should not need changes in other lavers.
Why of OSI Model?

Helps you to understand communication over a network
Troubleshooting is easier by separating functions into different network layers.
Helps you to understand new technologies as they are developed.
Allows you to compare primary functional relationships on various network layers.

Helps you to understand communication over a network
Troubleshooting is easier by separating functions into different network layers.
Helps you to understand new technologies as they are developed.
Allows you to compare primary functional relationships on various network layers.
History of OSI Model
Here are essential landmarks from the history of OSI model:

In the late 1970s, the ISO conducted a program to develop general standards and methods of networking.
In 1973, an Experimental Packet Switched System in the UK identified the requirement for defining the higher-level protocols.
In the year 1983, OSI model was initially intended to be a detailed specification of actual interfaces.
In 1984, the OSI architecture was formally adopted by ISO as an international standard

In the late 1970s, the ISO conducted a program to develop general standards and methods of networking.
In 1973, an Experimental Packet Switched System in the UK identified the requirement for defining the higher-level protocols.
In the year 1983, OSI model was initially intended to be a detailed specification of actual interfaces.
In 1984, the OSI architecture was formally adopted by ISO as an international standard
7 Layers of the OSI Model
OSI model is a layered server architecture system in which each layer is defined according to a specific function to perform. All these seven layers work collaboratively to transmit the data from one layer to another.

The Upper Layers: It deals with application issues and mostly implemented only in software. The highest is closest to the end system user. In this layer, communication from one end-user to another begins by using the interaction between the application layer. It will process all the way to end-user.
The Lower Layers: These layers handle activities related to data transport. The physical layer and datalink layers also implemented in software and hardware.

The Upper Layers: It deals with application issues and mostly implemented only in software. The highest is closest to the end system user. In this layer, communication from one end-user to another begins by using the interaction between the application layer. It will process all the way to end-user.
The Lower Layers: These layers handle activities related to data transport. The physical layer and datalink layers also implemented in software and hardware.
Upper and Lower layers further divide network architecture into seven different layers as below

Application
Presentation
Session
Transport
Network, Data-link
Physical layers

Application
Presentation
Session
Transport
Network, Data-link
Physical layers

Let’s Study each layer in detail:
Physical Layer
The physical layer helps you to define the electrical and physical specifications of the data connection. This level establishes the relationship between a device and a physical transmission medium. The physical layer is not concerned with protocols or other such higher-layer items.
Examples of hardware in the physical layer are network adapters, ethernet, repeaters, networking hubs, etc.

Data Link Layer:
Data link layer corrects errors which can occur at the physical layer. The layer allows you to define the protocol to establish and terminates a connection between two connected network devices.
It is IP address understandable layer, which helps you to define logical addressing so that any endpoint should be identified.
The layer also helps you implement routing of packets through a network. It helps you to define the best path, which allows you to take data from the source to the destination.
The data link layer is subdivided into two types of sublayers:
Media Access Control (MAC) layer- It is responsible for controlling how device in a network gain access to medium and permits to transmit data.
Logical link control layer- This layer is responsible for identity and encapsulating network-layer protocols and allows you to find the error.
Important Functions of Datalink Layer:

Framing which divides the data from Network layer into frames.
Allows you to add header to the frame to define the physical address of the source and the destination machine
Adds Logical addresses of the sender and receivers
It is also responsible for the sourcing process to the destination process delivery of the entire message.
It also offers a system for error control in which it detects retransmits damage or lost frames.
Datalink layer also provides a mechanism to transmit data over independent networks which are linked together.

Framing which divides the data from Network layer into frames.
Allows you to add header to the frame to define the physical address of the source and the destination machine
Adds Logical addresses of the sender and receivers
It is also responsible for the sourcing process to the destination process delivery of the entire message.
It also offers a system for error control in which it detects retransmits damage or lost frames.
Datalink layer also provides a mechanism to transmit data over independent networks which are linked together.
Transport Layer:
The transport layer builds on the network layer to provide data transport from a process on a source machine to a process on a destination machine. It is hosted using single or multiple networks, and also maintains the quality of service functions.
It determines how much data should be sent where and at what rate. This layer builds on the message which are received from the application layer. It helps ensure that data units are delivered error-free and in sequence.
Transport layer helps you to control the reliability of a link through flow control, error control, and segmentation or desegmentation.
The transport layer also offers an acknowledgment of the successful data transmission and sends the next data in case no errors occurred. TCP is the best-known example of the transport layer.
Important functions of Transport Layers:

It divides the message received from the session layer into segments and numbers them to make a sequence.
Transport layer makes sure that the message is delivered to the correct process on the destination machine.
It also makes sure that the entire message arrives without any error else it should be retransmitted.

It divides the message received from the session layer into segments and numbers them to make a sequence.
Transport layer makes sure that the message is delivered to the correct process on the destination machine.
It also makes sure that the entire message arrives without any error else it should be retransmitted.
Network Layer:
The network layer provides the functional and procedural means of transferring variable length data sequences from one node to another connected in “different networks”.
Message delivery at the network layer does not give any guaranteed to be reliable network layer protocol.
Layer-management protocols that belong to the network layer are:
routing protocols
multicast group management
network-layer address assignment.
Session Layer
Session Layer controls the dialogues between computers. It helps you to establish starting and terminating the connections between the local and remote application.
This layer request for a logical connection which should be established on end user’s requirement. This layer handles all the important log-on or password validation.
Session layer offers services like dialog discipline, which can be duplex or half-duplex. It is mostly implemented in application environments that use remote procedure calls.

Important function of Session Layer:

It establishes, maintains, and ends a session.
Session layer enables two systems to enter into a dialog
It also allows a process to add a checkpoint to steam of data.

It establishes, maintains, and ends a session.
Session layer enables two systems to enter into a dialog
It also allows a process to add a checkpoint to steam of data.
Presentation Layer
Presentation layer allows you to define the form in which the data is to exchange between the two communicating entities. It also helps you to handles data compression and data encryption.
This layer transforms data into the form which is accepted by the application. It also formats and encrypts data which should be sent across all the networks. This layer is also known as a syntax layer.
The function of Presentation Layers:

Character code translation from ASCII to EBCDIC.
Data compression: Allows to reduce the number of bits that needs to be transmitted on the network.
Data encryption: Helps you to encrypt data for security purposes — for example, password encryption.
It provides a user interface and support for services like email and file transfer.

Character code translation from ASCII to EBCDIC.
Data compression: Allows to reduce the number of bits that needs to be transmitted on the network.
Data encryption: Helps you to encrypt data for security purposes — for example, password encryption.
It provides a user interface and support for services like email and file transfer.
Application Layer
Application layer interacts with an application program, which is the highest level of OSI model. The application layer is the OSI layer, which is closest to the end-user. It means OSI application layer allows users to interact with other software application.
Application layer interacts with software applications to implement a communicating component. The interpretation of data by the application program is always outside the scope of the OSI model.
Example of the application layer is an application such as file transfer, email, remote login, etc.
The function of the Application Layers are:

Application-layer helps you to identify communication partners, determining resource availability, and synchronizing communication.
It allows users to log on to a remote host
This layer provides various e-mail services
This application offers distributed database sources and access for global information about various objects and services.

Application-layer helps you to identify communication partners, determining resource availability, and synchronizing communication.
It allows users to log on to a remote host
This layer provides various e-mail services
This application offers distributed database sources and access for global information about various objects and services.
Interaction Between OSI Model Layers
Information sent from a one computer application to another needs to pass through each of the OSI layers.
This is explained in the below-given example:

Every layer within an OSI model communicates with the other two layers which are below it and its peer layer in some another networked computing system.
In the below-given diagram, you can see that the data link layer of the first system communicates with two layers, the network layer and the physical layer of the system. It also helps you to communicate with the data link layer of, the second system.

Every layer within an OSI model communicates with the other two layers which are below it and its peer layer in some another networked computing system.
In the below-given diagram, you can see that the data link layer of the first system communicates with two layers, the network layer and the physical layer of the system. It also helps you to communicate with the data link layer of, the second system.
Protocols supported at various levels
Differences between OSI & TCP/IP
Here, are some important differences between the OSI & TCP/IP model:
Advantages of the OSI Model
Here, are major benefits/pros of using the OSI model :

It helps you to standardize router, switch, motherboard, and other hardware
Reduces complexity and standardizes interfaces
Facilitates modular engineering
Helps you to ensure interoperable technology
Helps you to accelerate the evolution
Protocols can be replaced by new protocols when technology changes.
Provide support for connection-oriented services as well as connectionless service.
It is a standard model in computer networking.
Supports connectionless and connection-oriented services.
Offers flexibility to adapt to various types of protocols

It helps you to standardize router, switch, motherboard, and other hardware
Reduces complexity and standardizes interfaces
Facilitates modular engineering
Helps you to ensure interoperable technology
Helps you to accelerate the evolution
Protocols can be replaced by new protocols when technology changes.
Provide support for connection-oriented services as well as connectionless service.
It is a standard model in computer networking.
Supports connectionless and connection-oriented services.
Offers flexibility to adapt to various types of protocols
Disadvantages of the OSI Model
Here are some cons/ drawbacks of using OSI Model:

Fitting of protocols is a tedious task.
You can only use it as a reference model.
Doesn’t define any specific protocol.
In the OSI network layer model, some services are duplicated in many layers such as the transport and data link layers
Layers can’t work in parallel as each layer need to wait to obtain data from the previous layer.

Fitting of protocols is a tedious task.
You can only use it as a reference model.
Doesn’t define any specific protocol.
In the OSI network layer model, some services are duplicated in many layers such as the transport and data link layers
Layers can’t work in parallel as each layer need to wait to obtain data from the previous layer.

Application Layer in OSI Model
Prerequisite : OSI Model
Introduction :The Application Layer is topmost layer in the Open System Interconnection (OSI) model. This layer provides several ways for manipulating the data (information) which actually enables any type of user to access network with ease. This layer also makes a request to its bottom layer, which is presentation layer for receiving various types of information from it. The Application Layer interface directly interacts with application and provides common web application services. This layer is basically highest level of open system, which provides services directly for application process.
Functions of Application Layer :The Application Layer, as discussed above, being topmost layer in OSI model, performs several kinds of functions which are requirement in any kind of application or communication process.Following are list of functions which are performed by Application Layer of OSI Model –
Application Layer provides a facility by which users can forward several emails and it also provides a storage facility.This layer allows users to access, retrieve and manage files in a remote computer.It allows users to log on as a remote host.This layer provides access to global information about various services.This layer provides services which include: e-mail, transferring files, distributing results to the user, directory services, network resources and so on.It provides protocols that allow software to send and receive information and present meaningful data to users.It handles issues such as network transparency, resource allocation and so on.This layer serves as a window for users and application processes to access network services.Application Layer is basically not a function, but it performs application layer functions.The application layer is actually an abstraction layer that specifies the shared protocols and interface methods used by hosts in a communication network.Application Layer helps us to identify communication partners, and synchronizing communication.This layer allows users to interact with other software applications.In this layer, data is in visual form, which makes users truly understand data rather than remembering or visualize the data in the binary format (0’s or 1’s).This application layer basically interacts with Operating System (OS) and thus further preserves the data in a suitable manner.This layer also receives and preserves data from it’s previous layer, which is Presentation Layer (which carries in itself the syntax and semantics of the information transmitted).The protocols which are used in this application layer depend upon what information users wish to send or receive.This application layer, in general, performs host initialization followed by remote login to hosts.
Application Layer provides a facility by which users can forward several emails and it also provides a storage facility.
This layer allows users to access, retrieve and manage files in a remote computer.
It allows users to log on as a remote host.
This layer provides access to global information about various services.
This layer provides services which include: e-mail, transferring files, distributing results to the user, directory services, network resources and so on.
It provides protocols that allow software to send and receive information and present meaningful data to users.
It handles issues such as network transparency, resource allocation and so on.
This layer serves as a window for users and application processes to access network services.
Application Layer is basically not a function, but it performs application layer functions.
The application layer is actually an abstraction layer that specifies the shared protocols and interface methods used by hosts in a communication network.
Application Layer helps us to identify communication partners, and synchronizing communication.
This layer allows users to interact with other software applications.
In this layer, data is in visual form, which makes users truly understand data rather than remembering or visualize the data in the binary format (0’s or 1’s).
This application layer basically interacts with Operating System (OS) and thus further preserves the data in a suitable manner.
This layer also receives and preserves data from it’s previous layer, which is Presentation Layer (which carries in itself the syntax and semantics of the information transmitted).
The protocols which are used in this application layer depend upon what information users wish to send or receive.
This application layer, in general, performs host initialization followed by remote login to hosts.
Working of Application Layer in the OSI model :In the OSI model, this application layer is narrower in scope. The application layer in the OSI model generally acts only like the interface which is responsible for communicating with host-based and user-facing applications. This is in contrast with TCP/IP protocol, wherein the layers below the application layer, which is Session Layer and Presentation layer, are clubbed together and form a simple single layer which is responsible for performing the functions, which includes controlling the dialogues between computers, establishing as well as maintaining as well as ending a particular session, providing data compression and data encryption and so on.
At first, client sends a command t server and when server receives that command, it allocates port number to client. Thereafter, the client sends an initiation connection request to server and when server receives request, it gives acknowledgement (ACK) to client through client has successfully established a connection with the server and, therefore, now client has access to server through which it may either ask server to send any types of files or other documents or it may upload some files or documents on server itself.
Features provided by Application Layer Protocols :To ensure smooth communication, application layer protocols are implemented the same on source host and destination host.The following are some of the features which are provided by Application layer protocols-
The Application Layer protocol defines process for both parties which are involved in communication.These protocols define the type of message being sent or received from any side (either source host or destination host).These protocols also define basic syntax of the message being forwarded or retrieved.These protocols define the way to send a message and the expected response.These protocols also define interaction with the next level.
The Application Layer protocol defines process for both parties which are involved in communication.
These protocols define the type of message being sent or received from any side (either source host or destination host).
These protocols also define basic syntax of the message being forwarded or retrieved.
These protocols define the way to send a message and the expected response.
These protocols also define interaction with the next level.
Application Layer Protocols: The application layer provides several protocols which allow any software to easily send and receive information and present meaningful data to its users.The following are some of the protocols which are provided by the application layer.
TELNET: Telnet stands for Telecommunications Network. This protocol is used for managing files over the Internet. It allows the Telnet clients to access the resources of Telnet server. Telnet uses port number 23.DNS: DNS stands for Domain Name System. The DNS service translates the domain name (selected by user) into the corresponding IP address. For example- If you choose the domain name as www.abcd.com, then DNS must translate it as 192.36.20.8 (random IP address written just for understanding purposes). DNS protocol uses the port number 53.DHCP: DHCP stands for Dynamic Host Configuration Protocol. It provides IP addresses to hosts. Whenever a host tries to register for an IP address with the DHCP server, DHCP server provides lots of information to the corresponding host. DHCP uses port numbers 67 and 68.FTP: FTP stands for File Transfer Protocol. This protocol helps to transfer different files from one device to another. FTP promotes sharing of files via remote computer devices with reliable, efficient data transfer. FTP uses port number 20 for data access and port number 21 for data control.SMTP: SMTP stands for Simple Mail Transfer Protocol. It is used to transfer electronic mail from one user to another user. SMTP is used by end users to send emails with ease. SMTP uses port numbers 25 and 587.HTTP: HTTP stands for Hyper Text Transfer Protocol. It is the foundation of the World Wide Web (WWW). HTTP works on the client server model. This protocol is used for transmitting hypermedia documents like HTML. This protocol was designed particularly for the communications between the web browsers and web servers, but this protocol can also be used for several other purposes. HTTP is a stateless protocol (network protocol in which a client sends requests to server and server responses back as per the given state), which means the server is not responsible for maintaining the previous client’s requests. HTTP uses port number 80.NFS: NFS stands for Network File System. This protocol allows remote hosts to mount files over a network and interact with those file systems as though they are mounted locally. NFS uses the port number 2049.SNMP: SNMP stands for Simple Network Management Protocol. This protocol gathers data by polling the devices from the network to the management station at fixed or random intervals, requiring them to disclose certain information. SNMP uses port numbers 161 (TCP) and 162 (UDP).
TELNET: Telnet stands for Telecommunications Network. This protocol is used for managing files over the Internet. It allows the Telnet clients to access the resources of Telnet server. Telnet uses port number 23.
DNS: DNS stands for Domain Name System. The DNS service translates the domain name (selected by user) into the corresponding IP address. For example- If you choose the domain name as www.abcd.com, then DNS must translate it as 192.36.20.8 (random IP address written just for understanding purposes). DNS protocol uses the port number 53.
DHCP: DHCP stands for Dynamic Host Configuration Protocol. It provides IP addresses to hosts. Whenever a host tries to register for an IP address with the DHCP server, DHCP server provides lots of information to the corresponding host. DHCP uses port numbers 67 and 68.
FTP: FTP stands for File Transfer Protocol. This protocol helps to transfer different files from one device to another. FTP promotes sharing of files via remote computer devices with reliable, efficient data transfer. FTP uses port number 20 for data access and port number 21 for data control.
SMTP: SMTP stands for Simple Mail Transfer Protocol. It is used to transfer electronic mail from one user to another user. SMTP is used by end users to send emails with ease. SMTP uses port numbers 25 and 587.
HTTP: HTTP stands for Hyper Text Transfer Protocol. It is the foundation of the World Wide Web (WWW). HTTP works on the client server model. This protocol is used for transmitting hypermedia documents like HTML. This protocol was designed particularly for the communications between the web browsers and web servers, but this protocol can also be used for several other purposes. HTTP is a stateless protocol (network protocol in which a client sends requests to server and server responses back as per the given state), which means the server is not responsible for maintaining the previous client’s requests. HTTP uses port number 80.
NFS: NFS stands for Network File System. This protocol allows remote hosts to mount files over a network and interact with those file systems as though they are mounted locally. NFS uses the port number 2049.
SNMP: SNMP stands for Simple Network Management Protocol. This protocol gathers data by polling the devices from the network to the management station at fixed or random intervals, requiring them to disclose certain information. SNMP uses port numbers 161 (TCP) and 162 (UDP).


Application Layer - OSI Model
It is the top most layer of OSI Model. Manipulation of data(information) in various ways is done in this layer which enables user or software to get access to the network. Some services provided by this layer includes: E-Mail, transferring files, distributing the results to user, directory services, network resources, etc.
The Application Layer contains a variety of protocols that are commonly needed by users. One widely-used application protocol is HTTP(HyperText Transfer Protocol), which is the basis for the World Wide Web. When a browser wants a web page, it sends the name of the page it wants to the server using HTTP. The server then sends the page back.
Other Application protocols that are used are: File Transfer Protocol(FTP), Trivial File Transfer Protocol(TFTP), Simple Mail Transfer Protocol(SMTP), TELNET, Domain Name System(DNS) etc.
Functions of Application Layer
Mail Services: This layer provides the basis for E-mail forwarding and storage. 
Network Virtual Terminal: It allows a user to log on to a remote host. The application creates software emulation of a terminal at the remote host. User's computer talks to the software terminal which in turn talks to the host and vice versa. Then the remote host believes it is communicating with one of its own terminals and allows user to log on.
Directory Services: This layer provides access for global information about various services.
File Transfer, Access and Management (FTAM): It is a standard mechanism to access files and manages it. Users can access files in a remote computer and manage it. They can also retrieve files from a remote computer.

Design Issues with Application Layer
There are commonly reoccurring problems that occur in the design and implementation of Application Layer protocols and can be addressed by patterns from several different pattern languages:

Pattern Language for Application-level Communication Protocols
Service Design Patterns 
Patterns of Enterprise Application Architecture
Pattern-Oriented Software Architecture

Pattern Language for Application-level Communication Protocols
Service Design Patterns 
Patterns of Enterprise Application Architecture
Pattern-Oriented Software Architecture

Sitting at Layer 7 -- the very top of the Open Systems Interconnection (OSI) communications model -- the application layer provides services for an application program to ensure that effective communication with another application program on a network is possible. The application layer should not be thought of as an application as most people understand it. Instead, the application layer is a component within an application that controls the communication method to other devices. It's an abstraction layer service that masks the rest of the application from the transmission process. The application layer relies on all the layers below it to complete its process. At this stage, the data, or the application, is presented in a visual form the user can understand.
Functions of the application layer

Ensures that the receiving device is identified, can be reached and is ready to accept data.
Enables, if appropriate, authentication to occur between devices for an extra layer of security.
Makes sure necessary communication interfaces exist. For example, is there an Ethernet or Wi-Fi interface in the sender's computer?
Ensures agreement at both ends about error recovery procedures, data integrity and privacy.
Determines protocol and data syntax rules at the application level.
Presents the data on the receiving end to the user application.

Ensures that the receiving device is identified, can be reached and is ready to accept data.
Enables, if appropriate, authentication to occur between devices for an extra layer of security.
Makes sure necessary communication interfaces exist. For example, is there an Ethernet or Wi-Fi interface in the sender's computer?
Ensures agreement at both ends about error recovery procedures, data integrity and privacy.
Determines protocol and data syntax rules at the application level.
Presents the data on the receiving end to the user application.
Two types of software provide access to the network within the application layer: network-aware applications, such as email, and application-level services, such as file transfer or print spooling.
"""
##new = " ".join( FileContent.splitlines())
##
##pre = PreProcessor(new)
##tokenized = pre.token()
##summarizer = Summarization(tokenized)
##summ_ids = summarizer.summarize()
##result = pre.decoder(summ_ids)
##
# print(result)


##print(bart_summarize(text,4, 2.0, 500, 120, 3))
