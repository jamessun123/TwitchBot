#defines some functions to be used in the bot
#prob won't use ban or timeout

import cfg
import socket
import re #used to devlove chat messages into readable form

def chat(sock, msg):
    """
	send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG #{} :{}".format(cfg.CHAN, msg))

def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))

#network functions

socket = socket.socket()
socket.connect((cfg.HOST, cfg.PORT))
socket.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
socket.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
socket.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))


#maintain the chat in the infinite loop, handle the ping
hello = False
while True:
    response = socket.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        
        CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        if hello == False:
            chat(socket, b'''4Head''')
            hello = True
        #sleep(0.1)
