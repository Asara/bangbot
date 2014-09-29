#!/usr/bin/env python

import socket
from random import randint, choice

# Settings
network =
channel =
nick =
password =
port = 6667



# Socket
def connect():
    global irc
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.settimeout(255)
    irc.connect((network, port))


# Login to server

def identify():
    irc.send('NICK {} \r\n'.format(nick))
    irc.send('USER {0} {0} {0}:bangbot a simple IRC Bot\r\n'.format(nick))
    irc.send('PRIVMSG ' + 'NICKSERV :identify {}\r\n'.format(password))


# Join Channel
def join():
    irc.send('JOIN {} \r\n'.format(channel))
    irc.send('PRIVMSG {}: {} has arrived!\r\n'.format(channel,nick))



# Globals Variables
beenShot = False
count = randint(0, 5)


# While connected
def recieve():
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
            irc.send('JOIN {}\r\n'.format(channel))
    
        # Tells the bot to quit the channel
        if data.find('!botquit') != -1:
            irc.send('PRIVMSG {}:{} out!\r\n'.format(channel,nick))
            irc.send('QUIT\r\n')
            quit()
    
        # Help command
        if data.find('!help') != -1 or data.find('!bot') != -1:
            irc.send('PRIVMSG ' + channel + ' :All commands begin with ! and are as follows: '
                                            '!ask (Responds yes or no), !8ball (Responds as an 8ball), '
                                            '!dice (Responds with the requested number of rolled die), '
                                            '!flip (Flips a coin for you), '
                                            'and !rr (Allows you to play Russian Roulette)\r\n')
    
    
        # Ask yes or no
        def ask():
            ask_responses = ['Yes.', 'No.']
            irc.send('PRIVMSG {}: {}\r\n'.format(channel, choice(ask_responses)))
    
        # Magic 8ball responses
        def eightball():
            ball_responses = ['Yes.', 'Reply hazy, try again.', 'Without a doubt.', 'My sources say no.',
                              'As I see it, yes.', 'You may rely on it.', 'Concentrate and ask again.',
                              'Outlook not so good.', 'It is decidedly so.', 'Better not tell you now.',
                              'Very doubtful.', 'Yes, definitely.', 'It is certain.', 'Cannot predict now.',
                              'Most likely.', 'Ask again later.', 'My reply is no.', 'Outlook good.',
                              'Don\'t count on it.']
    
            irc.send('PRIVMSG :{}\r\n'.format(channel,choice(ball_responses)))
    
        # Russian Roulette
        def russian_roulette():
            global count
            global beenShot
            gun_responses = ['*Click*', '*Click*', '*Click*', '*Click*', '*Click*', '*BANG*']
    
            # Reload
            if beenShot:
                irc.send('PRIVMSG {} :*Reloading*\r\n'.format(channel))
                count = randint(0, 5)
                beenShot = False
    
            irc.send('PRIVMSG {} : {}\r\n'.format(channel, gun_responses[count]))
    
            # Shoot
            if count == 5:
                beenShot = True
            # If blank, click.
            else:
                count += 1
    
        def semi_roulette():
            irc.send('PRIVMSG {} :ClickClickClickClickClick *BANG!*\r\n'.format(channel))
    
        # Flip a coin
        def flip():
            flip_responses = ['Heads', 'Tails']
            irc.send('PRIVMSG {} :{}\r\n'.format(channel,choice(flip_responses)))
    
    
    
    
        # Roll up to 6 dice
        def roll(x):
            try:
                x = int(x)
                if x > 6:
                    irc.send('PRIVMSG {} :Please ask for less than 6 die at a time.\r\n'.format(channel))
                elif x <= 0:
                    irc.send('PRIVMSG {} :Give me a number of die to roll\r\n'.format(channel))
                else:
                    r = []
                    for i in range(0,x):
                        r.append(str(randint(1,6)))
                        dicelist = ' '.join(r)
                    irc.send('PRIVMSG {} :{}\r\n'.format(channel,dicelist))
    
            except ValueError:
                irc.send('PRIVMSG {} :{} \r\n'.format(channel,str(randint(1,6))))
    
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
        irc.send('PRIVMSG {} :{} out!\r\n'.format(channel,nick))
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

