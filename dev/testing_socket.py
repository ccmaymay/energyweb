#!/usr/bin/env python


from random import randint, random
from time import sleep


AF_INET = None
SOCK_STREAM = None
PROB_SOCKET_DEATH = 0.001


error = Exception


class socket(object):

    def __init__(self, *args, **kwargs):
        self.chars_sent = 0

    def connect(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass

    def recv(self, *args, **kwargs):
        if random() < PROB_SOCKET_DEATH:
            return ''

        if self.chars_sent == 0:
            sleep(9.5 + random())
            r = ('RTSD' + chr(randint(0, 255))
                        + chr(2**5 + randint(0, 2**3)) + chr(randint(0, 255))
                        + chr(2**5 + randint(0, 2**3)) + chr(randint(0, 255))
                        + chr(2**5 + randint(0, 2**3)) + chr(randint(0, 255))
                        + ''.join([chr(randint(0, 255)) for i 
                                   in range(randint(1, 45 - 4 - 7))]))
        else:
            r = ''.join([chr(randint(0, 255)) for i 
                         in range(randint(1, 45 - self.chars_sent))])

        self.chars_sent += len(r)
        if self.chars_sent == 45:
            self.chars_sent = 0
        return r
