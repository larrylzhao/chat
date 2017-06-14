#!/usr/bin/python

import sys
import threading
import time
import re
import json
from socket import *
import os
import datetime
import shutil

mode = ""
nickname = ""
recipient = ""
serverip = ""
sPort = 0
cPort = 0
clientTable = {}
listensocket = socket(AF_INET, SOCK_DGRAM)
sSocket = socket(AF_INET, SOCK_DGRAM)

def client_listen():
    global listensocket
    global clientTable
    while True:
        data, sender = listensocket.recvfrom(1024)
        datasplit = data.split(";")
        if sender[0] == serverip and sender[1] == sPort:
            # messages from server
            try:
                clientTable = json.loads(datasplit[1])
            except:
                pass
            print datasplit[0]
            # print clientTable
        elif datasplit[0] == "CHAT":
            # chat messages from clients
            listensocket.sendto("ACK", (sender[0],sender[1]))
            find = re.search('^CHAT;'+datasplit[1]+';'+datasplit[2]+';(.*)', data)
            if find:
                message = find.group(1)
                print datasplit[1] + ": " + message
        sys.stdout.write(">>> ")
        sys.stdout.flush()


def offline_chat(message):
    # send offline message to server
    chatsocket = socket(AF_INET, SOCK_DGRAM)
    chatsocket.settimeout(.5)
    chatsocket.sendto(message, (serverip, sPort))
    tries = 0
    chattimeout = False
    while tries < 5:
        try:
            data, sender = chatsocket.recvfrom(1024)
        except timeout:
            tries += 1
            # print "try " + str(tries)
            if tries >= 5:
                print ">>> [Server not responding]"
                print ">>> [Exiting]"
                chattimeout = True
        else:
            print data
            break
    chatsocket.close()
    return chattimeout


def client_commands():
    global recipient
    while True:
        input = raw_input('>>> ')
        find = re.search('(\S*)', input)
        if find:
            command = find.group(1)
            if command == "send":
                if clientTable[nickname]['active'] is False:
                    print "You are not registered."
                else:
                    find = re.search('\S* (\S*)', input)
                    if find:
                        recipient = find.group(1)
                        if recipient == nickname:
                            print "Cannot send message to yourself."
                        elif recipient in clientTable.keys():
                            find = re.search('\S* \S* (.+)', input)
                            if find:
                                message = "CHAT;" + nickname + ";" + recipient + ";" + find.group(1)
                                if clientTable[recipient]['active'] is True:
                                    recipientip = clientTable[recipient]['ip']
                                    recipientport = clientTable[recipient]['port']
                                    chatsocket = socket(AF_INET, SOCK_DGRAM)
                                    chatsocket.settimeout(.5)
                                    chatsocket.sendto(message, (recipientip, recipientport))
                                    try:
                                        data, sender = chatsocket.recvfrom(1024)
                                    except timeout:
                                        print ">>> [No ACK from <" + recipient + ">, message sent to server.]"
                                        chattimeout = offline_chat(message)
                                        if chattimeout is True:
                                            break
                                    else:
                                        for name in clientTable:
                                            if sender[0] == clientTable[name]['ip'] and sender[1] == clientTable[name]['port']:
                                                print ">>> [Message received by <" + name + ">.]"
                                    chatsocket.close()

                                else:
                                    print ">>> <" + recipient + "> is offline, message sent to server."
                                    chattimeout = offline_chat(message)
                                    if chattimeout is True:
                                        break
                            else:
                                print "Please provide a message to the recipient."
                        else:
                            print "Invalid recipient name."
                    else:
                        print "Invalid recipient name."

            elif command == "dereg":
                find = re.search('\S* (\S*)', input)
                if find:
                    deregnickname = find.group(1)
                    if deregnickname == nickname:
                        deregsocket = socket(AF_INET, SOCK_DGRAM)
                        deregsocket.settimeout(.5)
                        deregsocket.sendto("DEREG;" + nickname, (serverip, sPort))
                        deregtimeout = False
                        tries = 0
                        while tries < 5:
                            try:
                                data, sender = deregsocket.recvfrom(1024)
                            except timeout:
                                tries += 1
                                # print "try " + str(tries)
                                if tries >= 5:
                                    print ">>> [Server not responding]"
                                    print ">>> [Exiting]"
                                    deregtimeout = True
                            else:
                                print data
                                break
                        deregsocket.close()
                        if deregtimeout is True:
                            break
                    else:
                        print "Invalid nickname. You can only deregister yourself."
                else:
                    print "Please provide a nickname for dereg."

            elif command == "reg":
                find = re.search('\S* (\S*)', input)
                if find:
                    regnickname = find.group(1)
                    if regnickname == nickname:
                        regsocket = socket(AF_INET, SOCK_DGRAM)
                        regsocket.settimeout(.5)
                        regsocket.sendto("REG;" + nickname, (serverip, sPort))
                        regtimeout = False
                        tries = 0
                        while tries < 5:
                            try:
                                data, sender = regsocket.recvfrom(1024)
                            except timeout:
                                tries += 1
                                # print "try " + str(tries)
                                if tries >= 5:
                                    print ">>> [Server not responding]"
                                    print ">>> [Exiting]"
                                    regtimeout = True
                            else:
                                print data
                                break
                        regsocket.close()
                        if regtimeout is True:
                            break
                    else:
                        print "Invalid nickname. You can only deregister yourself."
                else:
                    print "Please provide a nickname for dereg."

            else:
                print "<"+ command + "> is not a recognized command."

def server_clientTable_push():
    for client in clientTable:
        if clientTable[client]['active'] is True:
            sSocket.sendto("[Client table updated.];" + json.dumps(clientTable), (clientTable[client]['ip'], clientTable[client]['port']))

"""
argument parser
./UdpChat.py -c c1 127.0.0.1 6000 6061
./UdpChat.py -c c2 127.0.0.1 6000 6062
./UdpChat.py -c c3 127.0.0.1 6000 6063
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
            # check if server ip is valid string
            try:
                inet_aton(serverip)
            except:
                print "please provide a valid server ip"
                exit()
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
    try:
        sSocket.bind((serverip, sPort))
        offlinedir = "offline/"
        try:
            os.makedirs(offlinedir)
        except OSError:
            pass
        while True:
            data, client = sSocket.recvfrom(1024)
            print "client: ", client
            print "data: ", data

            datasplit = data.split(";")
            command = datasplit[0]
            nickname = datasplit[1]
            if command == "REG":
                #check if nickname exists and is active
                if nickname in clientTable.keys():
                    if clientTable[nickname]['active'] == True:
                        sSocket.sendto("[Client " + nickname + " exists!];" + json.dumps(clientTable), client)
                    else:
                        clientTable[nickname]['active'] = True
                        sSocket.sendto(">>> [Welcome back, you are re-registered.]", client)
                        server_clientTable_push()
                        # check if client has offline messages waiting
                        try:
                            with open(offlinedir+nickname) as f:
                                content = f.readlines()
                            os.remove(offlinedir+nickname)
                        except:
                            pass
                        else:
                            content = [x.strip() for x in content]
                            sSocket.sendto("[You have messages.]", (clientTable[nickname]['ip'], clientTable[nickname]['port']))
                            for message in content:
                                sSocket.sendto(message, (clientTable[nickname]['ip'], clientTable[nickname]['port']))
                else:
                    #add new client to table
                    clientInfo = {
                        'ip': client[0],
                        'port': client[1],
                        'active': True
                    }
                    clientTable[nickname] = clientInfo
                    sSocket.sendto("[Welcome, You are registered.];" + json.dumps(clientTable), client)
                    server_clientTable_push()
            elif command == "DEREG":
                clientTable[nickname]['active'] = False
                sSocket.sendto(">>> [You are Offline. Bye.]", client)
                server_clientTable_push()
            elif command == "CHAT":
                # save messages to files
                sSocket.sendto(">>> [Messages received by the server and saved.]", client)
                find = re.search('^CHAT;'+datasplit[1]+';'+datasplit[2]+';(.*)', data)
                if find:
                    message = nickname + ": <" + str(datetime.datetime.now()) + "> " + find.group(1)
                    f = open(offlinedir + datasplit[2], 'a+')
                    f.write(message + '\n')
                    f.close()

    except (KeyboardInterrupt):
        print "\n[exiting]"
        try:
            shutil.rmtree(offlinedir)
            os.remove(offlinedir)
        except OSError:
            pass
        exit()


elif mode == "client":
    cSocket = socket(AF_INET, SOCK_DGRAM)
    cSocket.settimeout(10)
    cSocket.bind(('', cPort))
    cSocket.sendto("REG;" + nickname, (serverip, sPort))
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
        # start thread to listen to inbound traffic
        listensocket.bind(('', cPort))
        clientListenThread = threading.Thread(target=client_listen, args=())
        clientListenThread.daemon = True
        clientListenThread.start()

        # start chat functionality
        client_commands()
        exit()
    except (KeyboardInterrupt):
        print "\n[exiting]"
        exit()
