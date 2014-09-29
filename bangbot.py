#!/usr/bin/env python

import socket
import ConfigParser
from random import randint, choice

class BangBot(object):

    def __init__(self, server_config=None, logfile=None, network=None, channel=None, nick="bangbot", password=None, port=6667):
        config = ConfigParser.RawConfigParser()
        config.read(server_config)





   # Socket
    def connect(self):
        global irc
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc.settimeout(255)
        irc.connect((self.network, self.port))
    
    
    # Login to server
    
    def identify(self):
        irc.send('NICK {} \r\n'.format(self.nick))
        irc.send('USER {0} {0} {0}:bangbot a simple IRC Bot\r\n'.format(self.nick))
        irc.send('PRIVMSG ' + 'NICKSERV :identify {}\r\n'.format(self.password))
    
    
    # Join Channel
    def join(self):
        irc.send('JOIN {} \r\n'.format(self.channel))
        irc.send('PRIVMSG {}: {} has arrived!\r\n'.format(self.channel,self.nick))
    
    
    
    # Globals Variables
    beenShot = False
    count = randint(0, 5)
    
    
    # While connected
    def recieve(self):
        while True:
          try:
            # Buffer
            data = irc.recv(1024)
        
            # Verbose output
            print data
        
            
        
            # Respond to ping
            if data.find('PING') != -1:
                irc.send('PONG {}\r\n'.format(data.split()[1]))
        
            # Auto rejoins to kicked
            if data.find('KICK') != -1:
                irc.send('JOIN {}\r\n'.format(self.channel))
        
            # Tells the bot to quit the self.channel
            if data.find('!botquit') != -1:
                irc.send('PRIVMSG {}:{} out!\r\n'.format(self.channel,self.nick))
                irc.send('QUIT\r\n')
                quit()
        
            # Help command
            if data.find('!help') != -1 or data.find('!bot') != -1:
                irc.send('PRIVMSG ' + self.channel + ' :All commands begin with ! and are as follows: '
                                                '!ask (Responds yes or no), !8ball (Responds as an 8ball), '
                                                '!dice (Responds with the requested number of rolled die), '
                                                '!flip (Flips a coin for you), '
                                                'and !rr (Allows you to play Russian Roulette)\r\n')
        
        
            # Ask yes or no
            def ask(self):
                ask_responses = ['Yes.', 'No.']
                irc.send('PRIVMSG {}: {}\r\n'.format(self.channel, choice(ask_responses)))
        
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
        
          except KeyboardInterrupt:
            irc.send('PRIVMSG {} :{} out!\r\n'.format(self.channel,self.nick))
            irc.send('QUIT\r\n')
            quit()
          except socket.error:
            irc.close()
            connect() 
            identify()
            join()
            recieve()
    
    
    connect()
    identify()
    join()
    recieve()
    
