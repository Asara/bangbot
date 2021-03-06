#!/usr/bin/env python
from IRCRoom import IRCRoom
from random import randint, choice
from sys import stderr, exit
from threading import Thread
import sys

class BangBot(object):

    def __init__(self, network, channel=None, nick=None,
                        password=None, port=None, ssl=False):
        if network is None:
            stderr.write('Please provide a network')
            exit()
        self.network = network
        self.nick = nick
        self.channel = channel
        self.password = password
        if ssl is True:
            self.port = 6697
            self.ssl = True
        else:
            self.port = 6667
            self.ssl = False
        if port:
            self.port = port
        self.beenShot = False
        self.count = randint(0, 5)
        self.wins = {}
        self.loss = {}
        self.connect()
        self.recieve()

    def connect(self):
        self.room = IRCRoom(self.network, self.port, self.ssl)
        self.room.connect()
        self.room.setnick(self.nick)
        self.room.identify(self.password,)
        self.room.join(self.channel)
        self.room.sendmsg('{} has arrived!'.format(self.nick))


    def ask(self):
        ask_responses = ['Yes.', 'No.']
        self.room.sendmsg('{}'.format(choice(ask_responses)))

# Magic 8ball responses
    def eightball(self):
        ball_responses = [
            'Yes.', 'Reply hazy, try again.', 'Without a doubt.',
            'My sources say no.', 'As I see it, yes.', 'You may rely on it.',
            'Concentrate and ask again.', 'Outlook not so good.',
            'It is decidedly so.', 'Better not tell you now.','Very doubtful.',
            'Yes, definitely.', 'It is certain.', 'Cannot predict now.',
            'Most likely.', 'Ask again later.', 'My reply is no.',
            'Outlook good.', 'Don\'t count on it.']

        self.room.sendmsg('{}'.format(choice(ball_responses)))

  # Russian Roulette
    def russian_roulette(self, nick):
        # Reload
        if self.beenShot:
            self.room.sendmsg('*Reloading*')
            self.count = randint(0, 5)
            self.beenShot = False
        # Shoot
        if self.count == 5:
            self.beenShot = True
            self.room.sendmsg('*BANG!*')
            self.loss[nick] = self.loss.get(nick, 0) + 1
        # If blank, click.
        else:
            self.count += 1
            self.room.sendmsg('*Click*')
            self.wins[nick] = self.wins.get(nick, 0) + 1

    def print_score(self):
        for k,v in self.wins.iteritems():
            self.room.sendmsg('{} has dodged {} bullets'.format(k,v))
        for k,v in self.loss.iteritems():
            self.room.sendmsg('{} has died {} times'.format(k,v))

    def semi_roulette(self, nick):
        self.room.sendmsg('ClickClickClickClickClick *BANG!*')
        self.loss[nick] = self.loss.get(nick, 0) + 1

    # Flip a coin
    def flip(self):
        flip_responses = ['Heads', 'Tails']
        self.room.sendmsg(choice(flip_responses))

    def quit(self):
        self.room.sendmsg('{} out'.format(self.nick))
        self.room.quit()

    # Roll up to 6 dice
    def roll(self,x):
        try:
            x = int(x)
            if x > 6:
                self.room.sendmsg('Please ask for less than 6 die at a time.')
            elif x <= 0:
                self.room.sendmsg('Give me a number of die to roll')
            else:
                r = []
                for i in range(0,x):
                    r.append(str(randint(1,6)))
                    dicelist = ' '.join(r)
                self.room.sendmsg(dicelist)

        except ValueError:
            self.room.sendmsg(str(randint(1,6)))


    # While connected
    def recieve(self):
        try:
            for data in self.room.read():
                # Buffer
                print data

                # Tells the bot to quit the self.channel
                if '!botquit' in data:
                    self.quit()
                    return

                # Help command
                elif '!help' in data or '!bot' in data:
                    self.room.sendmsg(
                        'All commands begin with ! and are as follows: '
                        '!ask (Responds yes or no), '
                        '!8ball (Responds as an 8ball), '
                        '!dice (Responds with the requested number of dice), '
                        '!flip (Flips a coin for you), '
                        '!rr (Allows you to play Russian Roulette), '
                        'and !score (Allows you to check !rr score) '
                    )

                # Ask yes or no            # Getters
                elif '!ask' in data:
                    self.ask()

                elif '!8b' in data or '!8ball' in data:
                    self.eightball()

                elif '!dice' in data:
                    t = data.split(':!dice')
                    dice = t[1].strip()
                    self.roll(dice)

                elif '!flip' in data:
                    self.flip()

                elif '!rr' in data:
                    name = data.split('!')[0].lstrip(':')
                    self.russian_roulette(name)

                elif '!sr' in data:
                    name = data.split('!')[0].lstrip(':')
                    self.semi_roulette(name)

                elif '!score' in data:
                    self.print_score()
        except:
            stderr.write('Connection lost')

class BotThread(Thread):
    def __init__(self, worker, args):
        super(BotThread, self).__init__()
        self.worker = worker
        self.args = args

    def run(self):
        self.worker(**self.args)
        print "Caught ^C, quitting"
        self.worker.quit()

def main():
    try:
        from config import bots
    except ImportError:
        stderr.write('Please provide a config\n')
        exit()

    threads = [ BotThread(BangBot, args=bot) for bot in bots ]

    def setup_thread(thread):
        thread.daemon = True
        thread.start()
        thread.join()

    try:
        map(setup_thread, threads)
    except KeyboardInterrupt:
        exit()

if __name__ == '__main__':
    main()
