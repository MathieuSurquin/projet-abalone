import socket
import json
import sys
import random
import time
from optimizeAI import bigbrainmoves
from movementsAI import bestmove_unrepeated

def receiveJSON(socket):
    totalreceive = False
    message = ''
    while not totalreceive:
        message += socket.recv(512).decode('utf8')
        try:
            data = json.loads(message)
            totalreceive = True
        except json.JSONDecodeError:
            pass
    return data

def sendJSON(socket, data):
    data = json.dumps(data).encode('utf8')
    totalsend = 0
    while totalsend < len(data):
        sent = socket.send(data[totalsend:])
        totalsend += sent

def subscribe(port,name):
    port = int(port)
    message = {"request": "subscribe","port": port,"name": name,"matricules": ["195030", "195199"]}
    s = socket.socket()
    s.connect(( 'localhost' ,3000))
    sendJSON(s, message)
    s.close()

    listening = True
    while listening == True:
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.listen()
        client, address = s.accept()
        serverrequest = receiveJSON(client)
        if serverrequest['request'] == 'ping':
            sendJSON(client, {'response': 'pong'})
            listening = False

def SENDmove(server_request):

    playercolors = ['B','W']
    playerindice = server_request['state']['current']
    move = bestmove_unrepeated(server_request['state']['board'],playercolors[playerindice])
    if move == "giveup":
         return {"response": "giveup"}

    marbles = []
    for i in move[1]:
        if type(i) is tuple:
            marbles.append(list(i))
        else:
            direction = i
    moverequest = {"marbles": marbles,"direction": direction}
    return {"response": "move","move": moverequest}

defaultport = '5996'
defaultname = 'abaloneAI'

if len(sys.argv) == 2:
    try:
        isinteger = int(sys.argv[1])
        port = sys.argv[1]
        name = defaultname
    except ValueError:
        port = defaultport
        name = sys.argv[1]
elif len(sys.argv) == 3:
    port = sys.argv[1]
    name = sys.argv[2]
elif len(sys.argv) > 3:
    print('Invalid input')
    sys.exit()
else:
    port = defaultport
    name = defaultname
    
subscribe(port, name)

listening = True
while listening == True:
        s = socket.socket()
        s.bind(('0.0.0.0', int(port)))
        s.listen()
        client, address = s.accept()
        serverrequest = receiveJSON(client)

        if serverrequest['request'] == 'ping':
            sendJSON(client, {'response': 'pong'})
        if serverrequest['request'] == 'play':
            sendJSON(client, SENDmove(serverrequest))