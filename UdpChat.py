#!/usr/bin/python

import sys
import threading
import time
import re
import json
from socket import *

mode = ""
nickname = ""
serverip = ""
sPort = 0
cPort = 0
clientTable = {}

def client_listen():
    global clientTable
    listensocket = socket(AF_INET, SOCK_DGRAM)
    listensocket.bind(('', cPort))
    while True:
        data, server = listensocket.recvfrom(1024)
        datasplit = data.split(";")
        clientTable = json.loads(datasplit[1])
        print datasplit[0]
        print clientTable
        sys.stdout.write(">>> ")
        sys.stdout.flush()

def client_message():
    while True:
        input = raw_input('>>> ')
        find = re.search('(\S*)', input)
        if find:
            command = find.group(1)
            if command == "chat":
                find = re.search('\S* (\S*)', input)
                if find:
                    recipient = find.group(1)
                    if recipient == nickname:
                        print "Cannot send message to yourself."
                    elif recipient in clientTable.keys():
                        find = re.search('\S* \S* (.+)', input)
                        if find:
                            message = find.group(1)
                            print "message: " + message
                        else:
                            print "Please provide a message to the recipient."
                    else:
                        print "Invalid recipient name."
                else:
                    print "Invalid recipient name."
            else:
                print "<"+ command + "> is not a recognized command."

def server_clientTable_push():
    pushSocket = socket(AF_INET, SOCK_DGRAM)
    for client in clientTable:
        if clientTable[client]['active'] is True:
            pushSocket.sendto("[Client table updated.];" + json.dumps(clientTable), (clientTable[client]['ip'], clientTable[client]['port']))
    pushSocket.close()

"""
argument parser
./UdpChat.py -c client1 127.0.0.1 6000 6061
./UdpChat.py -c client2 127.0.0.1 6000 6062
./UdpChat.py -c client3 127.0.0.1 6000 6063
./UdpChat.py -s 6000
"""
goodArgs = True
if len(sys.argv) > 1:
    if sys.argv[1] == "-s":
        #server mode
        mode = "server"
        if len(sys.argv) > 2:
            sPort = int(sys.argv[2])
            if sPort >= 1024 and sPort <= 65535:
                print "server port number: ", sPort
            else:
                print "please give a server port number between 1024 and 65535"
                exit()
        else:
            print "please give a server port number between 1024 and 65535"
            exit()
    elif sys.argv[1] == "-c":
        #client mode
        mode = "client"
        if len(sys.argv) > 2:
            nickname = sys.argv[2]
            print "client nickname: ", nickname
        else:
            print "please give client nickname"
            exit()

        if len(sys.argv) > 3:
            serverip = sys.argv[3]
            #TODO check if server ip is valid string
            print "server ip: ", serverip
        else:
            print "please give a server ip"
            exit()

        if len(sys.argv) > 4:
            sPort = int(sys.argv[4])
            if sPort >= 1024 and sPort <= 65535:
                print "server port number: ", sPort
            else:
                print "please give a server port number between 1024 and 65535"
                exit()
        else:
            print "please give a server port number between 1024 and 65535"
            exit()

        if len(sys.argv) > 5:
            cPort = int(sys.argv[5])
            if cPort >= 1024 and cPort <= 65535:
                print "client port number: ", cPort
            else:
                print "please give a client port number between 1024 and 65535"
                exit()
        else:
            print "please give a client port number between 1024 and 65535"
            exit()
    else:
        goodArgs = False
else:
    goodArgs = False

if goodArgs is False:
    print "please set server or client mode!"
    print "\tfor server -s <port>"
    print "\tfor client -c <nick-name> <server-ip> <server-port> <client-port>"
    sys.exit


if mode == "server":
    sSocket = socket(AF_INET, SOCK_DGRAM)
    sSocket.bind(('', sPort))

    while True:
        data, client = sSocket.recvfrom(1024)
        print "client: ", client
        print "data: ", data

        dataSplit = data.split(":")
        action = dataSplit[0]
        nickname = dataSplit[1]
        if action == "reg":
            #check if nickname exists and is active
            if nickname in clientTable.keys():
                if clientTable[nickname]['active'] == True:
                    sSocket.sendto("[Client " + nickname + " exists!];" + json.dumps(clientTable), client)
                else:
                    clientTable[nickname]['active'] == True
            else:
                #add new client to table
                clientInfo = {
                    'ip':client[0],
                    'port':client[1],
                    'active':True
                }
                clientTable[nickname] = clientInfo
                sSocket.sendto("[Welcome, You are registered.];" + json.dumps(clientTable), client)
                server_clientTable_push()

elif mode == "client":
    cSocket = socket(AF_INET, SOCK_DGRAM)
    cSocket.settimeout(10)
    cSocket.bind(('', cPort))
    cSocket.sendto("reg:" + nickname, (serverip,sPort))
    try:
        data, server = cSocket.recvfrom(1024)
        cSocket.close()
        datasplit = data.split(";")
        clientTable = json.loads(datasplit[1])
        print ">>> " + str(datasplit[0])
        print ">>> [Client table updated.]"
        # print clientTable
    except timeout:
        print 'REGISTRATION REQUEST TIMED OUT AFTER 10 SECONDS'
        exit()

    try:
        clientListenThread = threading.Thread(target=client_listen, args = ())
        clientListenThread.daemon = True
        clientListenThread.start()

        client_message()

    except (KeyboardInterrupt, SystemExit):
        print "\nexiting"
        exit()