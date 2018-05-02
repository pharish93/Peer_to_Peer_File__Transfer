#################################################
# Internet Protocols Project 1 :- Peer to Peer Cleint server System
# Authors :-
# Harish Pulagurla :- hpullag@ncsu.edu
# Last Edited :- 17th April 2017
#################################################



import socket
import threading
import os
import shlex
import datetime
import platform
import sys

UploadServer_Port = -1
Client_HostName = ''
UploadServer_IP = ''
RFC_Info = {}  # Dictionary to store RFC Numbers


def Message_CentralServer(message, central_server_address):  # Function to Talk to the Central Server
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(central_server_address)
        client.send(message)
        server_reply = client.recv(2048)
        print "Response from Central Server :"
        print server_reply
        client.close()
    except:
        print 'Couldnot create Socket to Send. Please Check and restart the progam'
        sys.exit()


def Upload_File(name, sock):  # Function to reply to GET command
    print 'Entered Upload Function'
    Peer_request = sock.recv(1024)
    print "Peer Request Received is " + Peer_request
    split_instruction = shlex.split(Peer_request)
    if split_instruction[0] == 'GET':
        if len(RFC_Info) == 0:
            reply = 'P2P-CI/1.0 404 FILE NOT FOUND \n'
            sock.send(reply)
        else:
            file_exists = -1
            if split_instruction[2] in str(RFC_Info.values()):
                filename = 'RFC' + str(split_instruction[2]) + '.txt'
                if os.path.isfile(filename):
                    file_exists += 1

            if file_exists == -1:
                reply = 'P2P-CI/1.0 404 FILE NOT FOUND \n'
                sock.send(reply)
            else:
                reply = 'P2P-CI/1.0 200 OK \n'
                reply += 'Date: ' + str(datetime.datetime.now()) + '\n'
                reply += 'OS: ' + str(platform.platform()) + '\n'
                try:
                    mtime = os.path.getmtime(filename)
                except OSError:
                    mtime = 0
                reply += 'Last-Modified: ' + str(datetime.datetime.fromtimestamp(mtime)) + '\n'
                reply += 'Content-Length: ' + str(os.path.getsize(filename)) + '\n'
                reply += 'Content-Type: text \n'
                sock.send(reply)
                with open(filename, 'rb')as f:
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
                    while bytesToSend != "":
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)

    else:
        reply = 'P2P-CI/1.0 400 BAD REQUEST \n'
        sock.send(reply)

    sock.close()


def UploadServer():  # Function to Create a listening upload server
    print 'Upload Server Thread Started'

    global UploadServer_Port
    UploadServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        UploadServer.bind((UploadServer_IP, UploadServer_Port))
    except socket.error as e:
        print (str(e))

    UploadServer.listen(5)
    print "Upload Server at Client Started listening at ", UploadServer_IP, " Port :", UploadServer_Port

    while True:
        peer, peer_address = UploadServer.accept()
        print "Peer Connected is :" + str(peer_address[0]) + " Port :" + str(peer_address[1])

        Peer_download_thread = threading.Thread(target=Upload_File, args=('Peer_download_thread', peer))
        Peer_download_thread.daemon = True
        Peer_download_thread.start()


def Download_File(RFC_Number, PeerServer_Address): # Function to download file from peer
    DownloadServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        DownloadServer.connect(PeerServer_Address)
        message = 'GET RFC ' + RFC_Number + ' P2P-CI/1.0 \n'
        message += 'Host : ' + Client_HostName + '\n'
        message += 'OS: ' + str(platform.platform()) + '\n'
        DownloadServer.send(message)
        peer_response = DownloadServer.recv(2048)
        print 'Message Received from the server' + peer_response
        split_instruction = shlex.split(peer_response)
        if split_instruction[1] == '200' and split_instruction[2] == 'OK':
            a = peer_response.splitlines()
            file_length = str.strip(a[4].split(':')[1])
            filename = 'RFC' + str(RFC_Number) + '.txt'
            f = open(filename, 'wb')
            data = DownloadServer.recv(1024)
            totalRec = len(data)
            f.write(data)
            while totalRec < int(file_length):
                data = DownloadServer.recv(1024)
                totalRec += len(data)
                f.write(data)
            print "Download Complete"
            return True
        else:
            print 'File not present at Peer \n'
            return False
        DownloadServer.close()
    except:
        print 'Client Not present in the given location'
        return False



def OperationSlection():
    print 'Operations Thread Started \n'
    CentralServerIP = raw_input('Enter IP Address of Central Server')
    CentralServerPort = raw_input('Enter Port Number of Central Server')
    central_server_address = (CentralServerIP, int(CentralServerPort))
    message = 'START P2P-CI/1.0 Host: ' + Client_HostName + ' Port: ' + str(UploadServer_Port) + '\n'
    Message_CentralServer(message, central_server_address)

    while (1):

        print "Choose from the operations list to Communicate with Central Server:- "
        print "1. Add RFC - To Add File with Client into Server List"
        print "2. Remove RFC - Remove the file from Server List"
        print "3. Lookup RFC - a specific RFC for download from other Peers"
        print "4. List All - available with Central Server"
        print "5. Exit Client Listing from Central Server"
        print
        print "To Communicate with Other Clients Present"
        print "6. GET RFC"

        choice = int(raw_input())

        if choice == 1:
            rfc_number = raw_input('Enter RFC Number')
            rfc_title = raw_input('Enter RFC Title')
            file_name = 'RFC' + rfc_number + '.txt'
            if os.path.isfile(file_name):
                RFC_Info[rfc_title] = rfc_number
                message = "ADD RFC" + " " + rfc_number + " P2P-CI/1.0" + "\n" + " Host: " + Client_HostName + "\n" \
                          + " Port: " + str(UploadServer_Port) + "\n" + " Title: " + rfc_title
                Message_CentralServer(message, central_server_address)
            else:
                print 'File Dosent exist in Folder . Please check \n'

        if choice == 2:
            rfc_number = raw_input('Enter RFC Number')
            rfc_title = raw_input('Enter RFC Title')
            file_name = 'RFC' + rfc_number + '.txt'
            if os.path.isfile(file_name):
                os.remove(file_name)
            message = "REMOVE RFC" + " " + rfc_number + " P2P-CI/1.0" + "\n" + " Host: " + Client_HostName + "\n" \
                          + " Port: " + str(UploadServer_Port) + "\n" + " Title: " + rfc_title
            Message_CentralServer(message, central_server_address)


        if choice == 3:
            rfc_number = raw_input('Enter RFC Number')
            rfc_title = raw_input('Enter RFC Title')
            message = "LOOKUP RFC" + " " + rfc_number + " P2P-CI/1.0" + "\n" + " Host: " + Client_HostName + "\n" \
                      + " Port: " + str(UploadServer_Port) + "\n" + " Title: " + rfc_title
            Message_CentralServer(message, central_server_address)

        if choice == 4:
            message = "LIST ALL P2P-CI/1.0" + "\n" + "Host: " + Client_HostName + "\n" + " Port: " + str(
                UploadServer_Port)
            Message_CentralServer(message, central_server_address)

        if choice == 5:
            message = "END P2P-CI/1.0 Host: " + Client_HostName + " Port: " + str(UploadServer_Port)
            Message_CentralServer(message, central_server_address)
            sys.exit()

        if choice == 6:
            rfc_number = raw_input('Enter RFC Number')
            peer_ip_address = raw_input('Enter Peer IP address')
            peer_port = raw_input('Enter Peer Port Address')
            Peer_address = (peer_ip_address, int(peer_port))
            status = Download_File(rfc_number, Peer_address)
            if status:
                response = raw_input('Add the Downloaded file to Central Server ? Y/N \n')
                if response == 'Y' or response == 'y':
                    rfc_title = raw_input('Enter RFC Title')
                    file_name = 'RFC' + rfc_number + '.txt'
                    if os.path.isfile(file_name):
                        RFC_Info[rfc_title] = rfc_number
                        message = "ADD RFC" + " " + rfc_number + " P2P-CI/1.0" + "\n" + " Host: " + Client_HostName + "\n" \
                                  + " Port: " + str(UploadServer_Port) + "\n" + " Title: " + rfc_title
                        Message_CentralServer(message, central_server_address)
                    else:
                        print 'File Dosent exist in Folder . Please check \n'

    return


def Main():
    global Client_HostName
    global UploadServer_IP
    global UploadServer_Port
    Client_HostName = raw_input('Enter Host Name : ')
    #UploadServer_IP = raw_input('Enter IP address of the present system / file :')
    UploadServer_IP = socket.gethostbyname(socket.gethostname())
    UploadServer_Port = int(raw_input("Enter a 4 digit Port number for Upload Server :"))

    UploasServer_Thread = threading.Thread(target=UploadServer)
    Operations_Thread = threading.Thread(target=OperationSlection)

    UploasServer_Thread.daemon = True
    Operations_Thread.daemon = True

    UploasServer_Thread.start()
    Operations_Thread.start()

    UploasServer_Thread.join()
    Operations_Thread.join()


if __name__ == '__main__':
    Main()
