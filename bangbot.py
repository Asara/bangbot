#!/usr/bin/env python
from IRCRoom import IRCRoom
import ConfigParser
from random import randint, choice

class BangBot(object):
    beenShot = False
    count = randint(0, 5)

    def __init__(self, profile='default', server_config=None, logfile=None,
    network=None, channel=None, nick=None, password=None, port=6667):
        self.profile = profile
        self.config = server_config
        self.network = network
        self.nick = nick
        self.channel = channel
        self.password = password
        self.port = port


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
                    print 'You forget to specify the {}'.format(e.key)


    def connect(self):
        self.room = IRCRoom(self.network, self.port)
        self.room.connect()
        self.room.identify(self.nick ,self.password, 'I am here!')
        self.room.join(self.channel)
        self.room.sendmsg('testing 123')


    # While connected
    def recieve(self):
        for data in self.room.read():
            try:
            # Buffer
                print data

                # Tells the bot to quit the self.channel
                if data.find('!botquit') != -1:
                    self.room.sendmsg('{} out'.format(self.nick))
                    self.room.quit()
                    exit()
            except KeyboardInterrupt:
                self.sendmsg('{} out!'.format(self.nick))
                self.quit()
                exit()


            # Help command
            if data.find('!help') != -1 or data.find('!bot') != -1:
                self.room.sendmsg(
                    'All commands begin with ! and are as follows: '
                    '!ask (Responds yes or no), !8ball (Responds as an 8ball), '
                    '!dice (Responds with the requested number of rolled die), '
                    '!flip (Flips a coin for you), '
                    'and !rr (Allows you to play Russian Roulette)')


            # Ask yes or no
            def ask(self):
                ask_responses = ['Yes.', 'No.']
                self.room.sendmsg('PRIVMSG {}: {}\r\n'.format(self.channel, choice(ask_responses)))
            # Magic 8ball responses
            def eightball(self):
                ball_responses = ['Yes.', 'Reply hazy, try again.', 'Without a doubt.', 'My sources say no.',
                                  'As I see it, yes.', 'You may rely on it.', 'Concentrate and ask again.',
                                  'Outlook not so good.', 'It is decidedly so.', 'Better not tell you now.',
                                  'Very doubtful.', 'Yes, definitely.', 'It is certain.', 'Cannot predict now.',
                                  'Most likely.', 'Ask again later.', 'My reply is no.', 'Outlook good.',
                                  'Don\'t count on it.']

                self.room.sendmsg('{}'.format(choice(ball_responses)))

            # Russian Roulette
            def russian_roulette(self):
                gun_responses = ['*Click*', '*Click*', '*Click*', '*Click*', '*Click*', '*BANG*']

                # Reload
                if self.beenShot:
                    self.room.sendmsg('*Reloading*')
                    self.count = randint(0, 5)
                    self.beenShot = False

                self.room.sendmsg(gun_responses[self.count])

                # Shoot
                if self.count == 5:
                    self.beenShot = True
                # If blank, click.
                else:
                    self.count += 1

            def semi_roulette(self):
                self.room.sendmsg('ClickClickClickClickClick *BANG!*')

            # Flip a coin
            def flip(self):
                flip_responses = ['Heads', 'Tails']
                self.room.sendmsg(choice(flip_responses))

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
                    irc.sendmsg(str(randint(1,6)))

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
                        t = i.split(':!dice')
                        dice = t[1].strip()
                        roll(dice)

if __name__ == '__main__':
    bot = BangBot(network='', channel='',
            nick='', password='',
            )
    bot.connect()
    bot.recieve()
