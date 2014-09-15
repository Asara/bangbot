#!/usr/bin/env python

import socket
from random import randint
from time import sleep

# Settings
network = 'chat.freenode.net'  
channel = ''
nick = 'bangbot'
password = ''
port = 6667



# Socket
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network, port))


# Login to server
irc.send('NICK ' + nick + '\r\n')
irc.send('USER ' + nick + ' ' + nick + ' ' + nick + ' ' + ':zotbot a simple IRC Bot\r\n')
irc.send('PRIVMSG ' + 'NICKSERV :identify ' + password + '\r\n')

sleep(20)

# Join Channel
irc.send('JOIN ' + channel + '\r\n')
irc.send('PRIVMSG ' + channel + ' : ' + nick + ' has arrived!\r\n')



# Globals Variables
beenShot = False
count = randint(0, 5)

# While connected
while True:
    # Buffer
    data = irc.recv(1024)

    # Verbose output
    print data

    # Respond to ping
    if data.find('PING') != -1:
        irc.send('PONG ' + data.split()[1] + '\r\n')

    # Auto rejoins to kicked
    if data.find('KICK') != -1:
        irc.send('JOIN ' + channel + '\r\n')

    # Tells the bot to quit the channel
    if data.find('!botquit') != -1:
        irc.send('PRIVMSG ' + channel + ' : ' + nick + ' out!\r\n')
        irc.send('QUIT\r\n')
        quit()

    # Help command
    if data.find('!help' or '!Help') != -1:
        irc.send('PRIVMSG ' + channel + ' :All commands begin with ! and are as follows: '
                                        '!ask (Responds yes or no), !8ball (Responds as an 8ball), '
                                        '!roll (Responds with the requested number of rolled die'
                                        'and !rr (Allows you to play Russian Roulette)\r\n')


    # Ask yes or no
    def ask():
        ask_responses = ['Yes', 'No']
        irc.send('PRIVMSG ' + channel + ' :' + choice(ask_responses) + '\r\n')

    # Magic 8ball responses
    def eightBall():
        ball_responses = ['Yes.', 'Reply hazy, try again.', 'Without a doubt.', 'My sources say no.',
                          'As I see it, yes.', 'You may rely on it.', 'Concentrate and ask again.',
                          'Outlook not so good.', 'It is decidedly so.', 'Better not tell you now.',
                          'Very doubtful.', 'Yes, definitely.', 'It is certain.', 'Cannot predict now.',
                          'Most likely.', 'Ask again later.', 'My reply is no.', 'Outlook good.',
                          'Don\'t count on it.']

        irc.send('PRIVMSG ' + channel + ' :' + choice(ball_responses)  + '\r\n')

    # Russian Roulette
    def russianRoulette():
        global count
        global beenShot
        gun_responses = ['*Click*', '*Click*', '*Click*', '*Click*', '*Click*', '*BANG*']

        # Reload
        if beenShot:
            irc.send('PRIVMSG ' + channel + ' :*Reloading*\r\n')
            count = randint(0, 5)
            beenShot = False

        irc.send('PRIVMSG ' + channel + ' ' + gun_responses[count] + '\r\n')

        # Shoot
        if count == 5:
            beenShot = True
        # If blank, click.
        else:
            count += 1

    # Roll up to 6 dice
    def roll(x):
        x = int(x)
        if x > 6:
            irc.send('PRIVMSG ' + channel + ' :Please ask for less than 6 die at a time.\r\n')
        elif x <= 0:
            irc.send('PRIVMSG ' + channel + ' :Give me a number of die to roll\r\n')
        else:
           r = []
           for i in range(0,x):
                r.append(str(randint(1,6)))
                dicelist = ' '.join(r)
           irc.send('PRIVMSG ' + channel + ' :' + dicelist +'\r\n')
             

# Getters
    if data.find('!ask' or '!a') != -1:
        ask()

    if data.find('!8b' or '!8ball') != -1:
        eightBall()

    if data.find('!rr' or '!russianRoulette') != -1:
        russianRoulette()

    if data.find('!roll') != -1:
        t = data.split(':!roll')
        dice = t[1].rstrip()
        roll(dice)

