#!/usr/bin/python

import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

mode = ""
nickname = ""
serverip = ""
sPort = 0
cPort = 0

goodArgs = True

#Client: UdpChat.py -c hello 1.1.1.1 1234 1235
#Server: UdpChat.py -s 1234
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
    #TODO
    print "do something in server mode"
elif mode == "client":
    print ">>> "