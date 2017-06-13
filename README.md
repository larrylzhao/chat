Larry Zhao

LZ2479

#Simple UDP Chat App

###Running the app
There is no Makefile for this application.

#####server mode
`./UdpChat.py -s <server-port>`

#####client mode
`./UdpChat.py -c <nick-name> <server-ip> <server-port> <client-port>`

###Overview of the App
The application uses UDP to communicate between clients and server.

####Server operations
The server allows clients to register themselves. The client info is stored in a Python dictionary. The server pushes the table of clients to all registered clients whenever there is a change. The dictionary is serialized to JSON when it is sent using UDP. The client then deserializes the JSON into a Python dictionary.

The server also stores offline messages and sends them to clients when they come back online. The messages are stored in individual text files, one for each client. The text file is deleted when the client comes back online or when the client is shut down.

####Client operations
Once the clients register with the server, they will receive the table of available clients. The clients chat directly with each other and not through the server. 

Chat messages can be sent with the `send` command:

`send <recipient-name> <message>`

The client waits for an ACK from the recipient client. If it does not receive an ACK within 500ms, the message will be sent to the server for storage.

The client can go offline by sending a `dereg` command and return online with the `reg` command.