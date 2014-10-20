#!/usr/bin/env python
import socket, ssl

class NoNick(Exception):
    def __init__(self, message):
        super(NoNick, self).__init__(message)

class IRCRoom(object):
    def __init__(self, network, port, ssl=False):
        self.network = network
        if port:
            self.port = port
        else:
            if ssl is True:
                self.port = 6697
            else:
                self.port = 6667
        self.nickset=False
        self.nicktouse=None

    def connect(self):
        try:
            self.room.close()
        except:
            pass
        self.room = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.room.settimeout(250)
        if ssl is True:
            self.room = ssl.wrap_socket(self.room)
        self.room.connect((self.network, self.port))

    def setnick(self, nick):
        self.nicktouse = nick
        self.nickset=True
        self.sendraw('NICK {} \r\n'.format(self.nicktouse))

    def identify(self, password=None, msg='This is a bot'):
        if self.nickset is False:
            raise NoNick('Please specify a nick')
        self.msg = msg
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
        self.room.close()

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
                self.join(self.channel)
                continue
            yield data
