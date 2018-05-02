
Project 1 :- Peer to Peer System with Central Server 

Name : Harish Pullagurla ( 200178872 )
Name :	Venkatasuryasubrahmanyam Nukala 

Code tested on Python 2.7 version

How to use the Code :- 

1.	Run the Central server file – Server.py 
It starts listening on a TCP Socket Stream on a well-known Port Number ‘5555’
It prints a message “Started listening on IP 192.168.179.1  Port : 5555” upon successfully creating a socket. 

2.	Run the client file - Client.py 
It prompts the user to enter the Host Name which is the Name by which this host is to be registered with the Server. 
It is expected to give unique names for each of the client that is registering with the Centralized Server. 
The user is expected to enter the upload server details, the socket at which the client 
would be open, listening to other clients for registering. Upload TCP socket stream is started.

3.	Operations Thread is initialized in the Client file, which is responsible for communicating with other sockets that are listening. This happens through a set of pre-defined commands that are decoded by each of the corresponding files for decoding the operations.  

4.	Select from the set of operations that are available at the client side. This generates commands to communicate with the server 

5.	Suggested usage sequence :- 

	a.	Add a file with Client into the centralized server, by giving the RFC number and title of files present in the Client folder 
	b.	Try to Lookup for the reference by querying the RFC number available with the Central Server. 
	c.	Try to Get the list of all RFC’s present with the Central Server 
	d.	Get RFC’s present with other clients 
	e.	Remove File from RFC
	f.	Exit from the system – removes entry from the Central Server  

6.	Server prints each of messages it receives and makes note in the backend about the available files with each of the peers 
=======
Project 1 :- Peer to Peer System with Central Server 

Name : Harish Pullagurla ( 200178872 )
Name :	Venkatasuryasubrahmanyam Nukala 

Code tested on Python 2.7 version

How to use the Code :- 

1.	Run the Central server file – Server.py 
It starts listening on a TCP Socket Stream on a well-known Port Number ‘5555’
It prints a message “Started listening on IP 192.168.179.1  Port : 5555” upon successfully creating a socket. 

2.	Run the client file - Client.py 
It prompts the user to enter the Host Name which is the Name by which this host is to be registered with the Server. 
It is expected to give unique names for each of the client that is registering with the Centralized Server. 
The user is expected to enter the upload server details, the socket at which the client 
would be open, listening to other clients for registering. Upload TCP socket stream is started.

3.	Operations Thread is initialized in the Client file, which is responsible for communicating with other sockets that are listening. This happens through a set of pre-defined commands that are decoded by each of the corresponding files for decoding the operations.  

4.	Select from the set of operations that are available at the client side. This generates commands to communicate with the server 

5.	Suggested usage sequence :- 

	a.	Add a file with Client into the centralized server, by giving the RFC number and title of files present in the Client folder 
	b.	Try to Lookup for the reference by querying the RFC number available with the Central Server. 
	c.	Try to Get the list of all RFC’s present with the Central Server 
	d.	Get RFC’s present with other clients 
	e.	Remove File from RFC
	f.	Exit from the system – removes entry from the Central Server  

6.	Server prints each of messages it receives and makes note in the backend about the available files with each of the peers 

