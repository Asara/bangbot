#!/usr/bin/env python
import socket

class NoNick(Exception):
    def __init__(self, message):
        super(NoNick, self).__init__(message)

class IRCRoom(object):
    def __init__(self, network, port=6667):
        self.network = network
        self.port = port
        self.room = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.room.settimeout(250)
        self.nickset=False
        self.nicktouse=None

    def connect(self):
        self.room.connect((self.network, self.port))

    def setnick(self, nick):
        if nick is None and self.nicktouse is None:
            raise NoNick('Please specify a nick')

        if self.nicktouse is None:
            self.nicktouse = nick

        self.nickset=True
        self.sendraw('NICK {} \r\n'.format(self.nicktouse))

    def identify(self, nick=None, password=None, msg=''):
        self.msg = msg
        if not self.nickset:
            self.setnick(nick)

        self.password = password
        senduser = 'USER {0} {0} {0}:{1}\r\n'.format(
            self.nicktouse,
            self.msg
        )
        self.sendraw(senduser)
        self.sendpm('NICKSERV', 'identify {} {}'.format(
            self.nicktouse,
            self.password
            )
        )

    def join(self, channel):
        self.channel = channel
        self.sendraw('JOIN {} \r\n'.format(self.channel))
        arrival = 'PRIVMSG {}: {} has arrived!\r\n'.format(
            self.channel,self.nicktouse
        )
        self.sendraw(arrival)

    def sendmsg(self, text):
        self.msg = text
        self.sendraw('PRIVMSG {} :{}\r\n'.format(self.channel,self.msg))

    def sendpm(self, user, text):
        self.target = user
        self.msg = text
        self.sendraw('PRIVMSG {} :{}\r\n'.format(self.target, self.msg))

    def sendraw(self, text):
        self.msg = text
        self.room.send(self.msg)

    def quit(self):
        self.sendraw('QUIT\r\n')
        self.nickset = False

    def read(self):
        while True:
            try:
                data = self.room.recv(4096)
                # Respond to ping
                if data.find('PING') != -1:
                    self.sendraw('PONG {}\r\n'.format(data.split()[1]))

                # Auto rejoins to kicked
                if data.find('KICK') != -1:
                    self.sendraw('JOIN {}\r\n'.format(self.channel))
            except socket.error:
                self.room.close()
                self.connect()
                self.identify()
                self.join()
                continue
            yield data
>>>>>>> parent of 529c297... Working BangBot
