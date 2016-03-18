"""
Created on Mar 18, 2016

@author: Pepijn Kokke
"""
from __future__                    import absolute_import, division, print_function
from future.builtins               import *
from composes.semantic_space.space import Space
from composes.similarity.cos       import CosSimilarity
from composes.utils                import io_utils
from enum                          import Enum
from getpass                       import getuser
from multiprocessing               import current_process
from multiprocessing.managers      import BaseManager
from names                         import get_first_name
from nltk.corpus                   import cmudict as cm
from nltk.corpus                   import wordnet as wn
from os.path                       import dirname, join, realpath
from random                        import choice
from re                            import compile as re


RE_PREFIX = re('^(\S+)\s')
AUTH_KEY  = b'szxzcJVYgdZaN5PAqpp6fAKRmh4BvqT6mXLbAMuAQmHSpBAX'
ADDRESS   = ('localhost', 6000)


def create_noun_only(ifile,ofile):
    with open (ofile, 'w') as ostream:
        with open (ifile, 'r') as istream:
            for l in istream:
                w = RE_PREFIX.match(l).group(1).decode('utf8','ignore')
                if len(w) > 1:
                    synsets = wn.synsets(w,pos=wn.NOUN)
                    if any([s.name().startswith(w + '.n.') for s in synsets]):
                        ostream.write(l)


def create_pickle(ifile,ofile):
    io_utils.save(Space.build(data = ifile, format = "dm"), ofile)


class NounSpace(object):

    def __init__(self, noun_space, similarity=None):
        self.noun_space = noun_space
        self.similarity = similarity or CosSimilarity()

    def get_random_word(self):
        word = choice(self.noun_space.id2row)
        print("Chose %s" % word)
        return word

    def get_sim(self, word1, word2):
        word1 = word1.strip()
        word2 = word2.strip()
        return self.noun_space.get_sim(word1, word2, self.similarity)


def serve(ifile):
    print("# loading NounSpace")
    noun_space = NounSpace(io_utils.load(ifile))

    print("# setting up process manager")
    class NounSpaceManager(BaseManager): pass
    NounSpaceManager.register('get_random_word', noun_space.get_random_word)
    NounSpaceManager.register('get_sim', noun_space.get_sim)

    print("# starting up server")
    current_process().authkey = AUTH_KEY
    manager = NounSpaceManager(address=ADDRESS, authkey=AUTH_KEY)
    server  = manager.get_server()

    print("# server started")
    server.serve_forever()


def a(word):
    if 'i give up'  == word:
        return 'I give up'
    elif startswith_vowel(word):
        return "an "+word
    else:
        return "a "+word

def startswith_vowel(word, pronunciations=cm.dict()):
    for syllables in pronunciations.get(word,[]):
        return syllables[0][-1].isdigit()
    return False


def play():

    Player      = getuser().title()
    Computer    = get_first_name()
    MaxLength   = max(map(len,[Player,Computer])) + 1

    def say(role,msg,filter=id,end="\n"):
        print((('{:<' + str(MaxLength) + '}: {}').format(role, msg)),end=end)

    class SemanticSpaceManager(BaseManager): pass
    SemanticSpaceManager.register('get_random_word')
    SemanticSpaceManager.register('get_sim')

    manager = SemanticSpaceManager(address=ADDRESS, authkey=AUTH_KEY)
    current_process().authkey = AUTH_KEY
    manager.connect()

    secret         = manager.get_random_word()._getvalue()
    next_guess     = 'breadbox'
    next_guess_sim = manager.get_sim(next_guess,secret)

    say(Computer , "I'm thinking of something!")
    say(Player   , "Is it a breadbox?")
    say(Computer , "No, it's not.")

    while True:

        say(Player , "Is it more like {} or more like ".format(a(next_guess)), end='')
        prev_guess     = next_guess
        next_guess     = input().strip().rstrip('?').lower()
        if next_guess.startswith('a '):
            next_guess = next_guess[2:]
        if next_guess.startswith('an '):
            next_guess = next_guess[3:]
        print(end="\033[F")
        say(Player , "Is it more like {} or more like {}?".format(a(prev_guess),a(next_guess)))
        prev_guess_sim = next_guess_sim
        next_guess_sim = manager.get_sim(next_guess,secret)

        if 'i give up' == next_guess:
            say(Computer, "I was thinking of %s!" % secret)
            for synset in wn.synsets(secret):
                if synset.name().startswith(secret + '.n.'):
                    say(Computer, "It's %s!" % synset.definition())
            break

        if ' ' in next_guess:
            next_guess     = prev_guess
            next_guess_sim = prev_guess_sim
            say(Computer, "I have to warn you, compound nouns scare me a little...")
            say(Computer, "Try to avoid words with spaces in them.")

        elif next_guess == secret:
            say(Computer, "That's exactly what I was thinking of!")
            break

        elif next_guess_sim > prev_guess_sim:
            say(Computer, "It's more like a %s..." % next_guess)

        elif next_guess_sim == prev_guess_sim:
            next_guess     = prev_guess
            next_guess_sim = prev_guess_sim
            say(Computer, "Eh. They're about equally like the thing I'm thinking of...")

        elif next_guess_sim < prev_guess_sim:
            next_guess     = prev_guess
            next_guess_sim = prev_guess_sim
            say(Computer, "It's more like a %s..." % next_guess)
