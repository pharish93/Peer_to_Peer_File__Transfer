#################################################
# Internet Protocols Project 1 :- Peer to Peer Cleint server System
# Authors :-
# Harish Pulagurla :- hpullag@ncsu.edu
# Last Edited :- 17th April 2017
#################################################

import socket
import threading
import sys
import os
import shlex

RFC_Info = []
Peer_Dict = {}


class RFC_Information:
    def __init__(self, RFC_Number=-1, RFC_Title='None', RFC_Hostname='None'):
        self.RFC_Number = RFC_Number
        self.RFC_Title = RFC_Title
        self.RFC_Hostname = RFC_Hostname


def ReadInstruction(name, client_sock):
    instructions = client_sock.recv(1024)
    DecodeInstruction(instructions, client_sock)


def DecodeInstruction(instruction, client_sock):
    print 'Instruction Received is :'
    print instruction
    print
    split_instruction = shlex.split(instruction)
    # print split_instruction
    if split_instruction[0] == 'START':
        reply = Start_Peer_Connection(split_instruction)
    elif split_instruction[0] == 'END':
        reply = End_Peer_Connection(split_instruction)
    elif split_instruction[0] == 'ADD':
        reply = Add_RFC(split_instruction[2], instruction)
    elif split_instruction[0] == 'REMOVE':
        reply = Remove_RFC(split_instruction[2], instruction)
    elif split_instruction[0] == 'LOOKUP':
        reply = Lookup_RFC(split_instruction[2], instruction)
    elif split_instruction[0] == 'LIST':
        reply = List_All()
    else:
        reply = 'P2P-CI/1.0 400 BAD REQUEST \n'

    try:
        client_sock.send(reply)
    except:
        print 'File sending failed \n'
        sys.exit()


def Start_Peer_Connection(split_instruction):
    global Peer_Dict
    Peer_Dict[str(split_instruction[3])] = int(split_instruction[5]) # Client host name and clinet port number
    reply = 'P2P-CI/1.0 200 OK \n' + 'Peer added to list \n'
    return reply


def End_Peer_Connection(split_instruction):
    global Peer_Dict
    print split_instruction
    if len(RFC_Info) != 0:
        i = -1
        for element in RFC_Info:
            i += 1
            if (element.RFC_Number == str(split_instruction[5])) and (element.RFC_Hostname == str(split_instruction[3])):
                del RFC_Info[i]

    del Peer_Dict[str(split_instruction[3])]
    reply = 'P2P-CI/1.0 200 OK \n' + 'Peer removed from list \n'
    return reply


def Add_RFC(rfc_number, instruction):
    a = instruction.splitlines()
    host_name = str.strip(a[1].split(':')[1])
    port_number = str.strip(a[2].split(':')[1])
    RFC_Title = str.strip(a[3].split(':')[1])
    RFC_Info.append(RFC_Information(rfc_number, RFC_Title, host_name))
    reply = 'P2P-CI/1.0 200 OK \n'
    reply = reply + 'RFC ' + str(rfc_number) + ' ' + RFC_Title + ' ' + host_name + ' ' + port_number + '\n'
    return reply


def Remove_RFC(rfc_number, instruction):
    Error_Status = '404 Not Found'
    a = instruction.splitlines()
    RFC_Title = str.strip(a[3].split(':')[1])
    RFC_HostName = str.strip(a[1].split(':')[1])
    i = -1
    reply_1 = ''
    for element in RFC_Info:
        i += 1
        if (element.RFC_Number == rfc_number) and (element.RFC_Title == RFC_Title) and (
                    element.RFC_Hostname == RFC_HostName):
            del RFC_Info[i]
            reply_1 = 'RFC entry found and deleted \n'
            Error_Status = '200 OK'
    reply = 'P2P-CI/1.0' + Error_Status + '\n' + reply_1
    return reply


def Lookup_RFC(rfc_number, instruction):
    Error_Status = '404 Not Found'
    reply = ''
    Matched_RFC = []
    a = instruction.splitlines()
    RFC_Title = str.strip(a[3].split(':')[1])
    for element in RFC_Info:
        if ((element.RFC_Number == rfc_number) and (element.RFC_Title == RFC_Title)):
            Matched_RFC.append(element)
            Error_Status = '200 OK'

    if len(Matched_RFC) == 0:
        Error_Status = '404 Not Found'
        reply = 'P2P-CI/1.0 ' + Error_Status + '\n'
    else:
        for element in Matched_RFC:
            reply += "RFC " + element.RFC_Number + ' ' + element.RFC_Title + ' '
            print str(element.RFC_Hostname)
            print str(Peer_Dict[str(element.RFC_Hostname)])
            reply += element.RFC_Hostname + ' ' + str(Peer_Dict[str(element.RFC_Hostname)]) + '\n'

    return reply


def List_All():
    if (len(RFC_Info) == 0):
        Error_Status = '404 Not Found'
        reply = 'P2P-CI/1.0' + Error_Status + '\n'
    else:
        Error_Status = '200 OK'
        reply = 'P2P-CI/1.0 ' + Error_Status + '\n'
        for element in RFC_Info:
            reply += "RFC " + element.RFC_Number + ' ' + element.RFC_Title + ' '
            reply += element.RFC_Hostname + ' ' + str(Peer_Dict[str(element.RFC_Hostname)]) + '\n'

    return reply


def Main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(socket.gethostname())
    port = 5555
    print ip
    try:
        server.bind((ip, port))
    except socket.error as e:
        print (str(e))

    server.listen(5)
    print "Started listening on IP", ip, ' Port :', port

    while True:
        client, addr = server.accept()
        print "Clinet Connected is :" + str(addr[0]) + " Port : " + str(addr[1])
        t = threading.Thread(target=ReadInstruction, args=('ReadInstruction thread', client))
        t.start()

    server.close()


if __name__ == "__main__":
    Main()
