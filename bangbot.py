#!/usr/bin/env python

import socket
import ConfigParser
from random import randint, choice

class IRCRoom(object):
    def __init__(self, network=None, port=6667):
        if network:
            self.network = network
            self.port = port
            self.room = socket.socket(socket.AF_INET,socket.SOCKET_STREAM)
            self.room.timeout(255)
        else:
            print "Please provide a network"
            exit()

    def connect(self):
        self.room.connect((self.network, self.port))

    def identify(self, nick, password):
        if not nick || if not password:
            print "Please provide a nick and password"
            exit()
        else:
            self.nick = nick
            self.password = password
            self.room.send('NICK {} \r\n'.format(self.nick))
            self.room.send('USER {0} {0} {0}:bangbot a simple IRC Bot\r\n'.format(self.nick))
            self.sendpm(NICKSERV, 'identify {}'.format(self.password))

    def join(self, channel):
        self.channel = channel
        self.room.send('JOIN {} \r\n'.format(self.channel))
        self.room.send('PRIVMSG {}: {} has arrived!\r\n'.format(self.channel,self.nick))
    
   def sendmsg(self, text):
        self.msg = text
        self.room.send('PRIVMSG {} :{}\r\n'.format(self.channel,self.msg))

    def sendpm(self, user, text):
        self.target = user
        self.msg = text
        self.room.send('PRIVMSG {} :{}\r\n'.format(self.target, self.msg))

    def sendraw(self, text):
        self.msg = text
        self.room.send(self.msg)

    def read(self):
        while True:
            try:
                data = self.room.recv(1024)
                # Respond to ping
                if data.find('PING') != -1:
                    self.room.sendraw('PONG {}\r\n'.format(data.split()[1]))
        
                # Auto rejoins to kicked
                if data.find('KICK') != -1:
                    self.room.sendraw('JOIN {}\r\n'.format(self.channel))
                return data
            except KeyboardInterrupt:
                self.sendmsg('{} out!\r\n'.format(self.nick)
                self.room.sendraw('QUIT\r\n')
                quit()
            except socket.error:
                self.room.close()
                self.room.connect() 
                self.room.identify()
                self.room.join()
                self.room.recieve()

 


class BangBot(object):
    # Globals Variables
    beenShot = False
    count = randint(0, 5)
 
    def __init__(self, profile="default", server_config=None, logfile=None, network=None, channel=None, nick="bangbot", password=None, port=6667):
        if server_config:
            config = ConfigParser.RawConfigParser()
            config.read(server_config)

            config__room.keys_needed = [
                    'profile',
                    'logfile',
                    'network',
                    'channel',
                    'nick',
                    'password',
                    'port',
                    ]

            for config_key in config_keys_needed:
                try:
                    value = config.get(profile, config_key)
                    setattr(self, config_key, value)
                except ConfigParser.NoOptionError as e:
                    print "You forget to specify the {}".format(e.key)

    # While connected
    def recieve(self):
        while True:
          try:
            # Buffer
            data = room.recv(1024)
        
            # Verbose output
            print data
            
            # Tells the bot to quit the self.channel
            if data.find('!botquit') != -1:
                room.sendmsg('{} out'.format(self.nick))
                room.sendraw('QUIT\r\n')
                quit()
        
            # Help command
            if data.find('!help') != -1 or data.find('!bot') != -1:
                room.sendmsg('All commands begin with ! and are as follows: '
                            '!ask (Responds yes or no), !8ball (Responds as an 8ball), '
                            '!dice (Responds with the requested number of rolled die), '
                            '!flip (Flips a coin for you), '
                            'and !rr (Allows you to play Russian Roulette)')
        
        
            # Ask yes or no
            def ask(self):
                ask_responses = ['Yes.', 'No.']
                room.sendmsg('PRIVMSG {}: {}\r\n'.format(self.channel, choice(ask_responses)))
        
            # Magic 8ball responses
            def eightball(self):
                ball_responses = ['Yes.', 'Reply hazy, try again.', 'Without a doubt.', 'My sources say no.',
                                  'As I see it, yes.', 'You may rely on it.', 'Concentrate and ask again.',
                                  'Outlook not so good.', 'It is decidedly so.', 'Better not tell you now.',
                                  'Very doubtful.', 'Yes, definitely.', 'It is certain.', 'Cannot predict now.',
                                  'Most likely.', 'Ask again later.', 'My reply is no.', 'Outlook good.',
                                  'Don\'t count on it.']
        
                irc.send('PRIVMSG :{}\r\n'.format(self.channel,choice(ball_responses)))
        
            # Russian Roulette
            def russian_roulette(self):
                gun_responses = ['*Click*', '*Click*', '*Click*', '*Click*', '*Click*', '*BANG*']
        
                # Reload
                if beenShot:
                    irc.send('PRIVMSG {} :*Reloading*\r\n'.format(self.channel))
                    count = randint(0, 5)
                    beenShot = False
        
                irc.send('PRIVMSG {} : {}\r\n'.format(self.channel, gun_responses[count]))
        
                # Shoot
                if count == 5:
                    beenShot = True
                # If blank, click.
                else:
                    count += 1
        
            def semi_roulette(self):
                irc.send('PRIVMSG {} :ClickClickClickClickClick *BANG!*\r\n'.format(self.channel))
        
            # Flip a coin
            def flip(self):
                flip_responses = ['Heads', 'Tails']
                irc.send('PRIVMSG {} :{}\r\n'.format(self.channel,choice(flip_responses)))
        
            # Roll up to 6 dice
            def roll(self,x):
                try:
                    x = int(x)
                    if x > 6:
                        irc.send('PRIVMSG {} :Please ask for less than 6 die at a time.\r\n'.format(self.channel))
                    elif x <= 0:
                        irc.send('PRIVMSG {} :Give me a number of die to roll\r\n'.format(self.channel))
                    else:
                        r = []
                        for i in range(0,x):
                            r.append(str(randint(1,6)))
                            dicelist = ' '.join(r)
                        irc.send('PRIVMSG {} :{}\r\n'.format(self.channel,dicelist))
        
                except ValueError:
                    irc.send('PRIVMSG {} :{} \r\n'.format(self.channel,str(randint(1,6))))
        
        # Getters
            if data.find('!ask' or '!a') != -1:
                ask()
        
            if data.find('!8b' or '!8ball') != -1:
                eightBall()
        
            if data.find('!rr' or '!russianRoulette') != -1:
                russian_roulette()
        
            if data.find('!sr' or '!russianRoulette') != -1:
                semi_roulette()
        
            if data.find('!flip') != -1:
                flip()
            
            if data.find('!dice') != -1:
                t = data.split(':!dice')
                dice = t[1].strip()
                roll(dice)
        
          
