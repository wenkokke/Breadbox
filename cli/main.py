"""
Created on Aug 22, 2014

@author: Pepijn Kokke
"""
from __future__               import absolute_import, division, print_function
from future.builtins          import *
from enum                     import Enum
from getpass                  import getuser
from multiprocessing          import current_process
from multiprocessing.managers import BaseManager
from names                    import get_first_name
from time                     import sleep


Reply = Enum('Reply', 'LessLike EquallyLike MoreLike ExactlyEqual')


class Breadbox(object):
    """
    Implementation of a command-line version of the Breadbox game.
    """

    def __init__(self, semantic_space):
        self.names = Breadbox.setup_names()
        self.semantic_space = semantic_space
        self.secret = self.semantic_space.get_random_word()._getvalue()
        self.current_guess = 'breadbox'
        self.current_guess_sim = self.semantic_space.get_sim(
            self.current_guess, self.secret)._getvalue()


    def start(self):
        """
        Start the game.
        """
        self.say('Computer', "I'm thinking of something...")
        self.say('Computer', "(Pst! It's a '%s'!)" % self.secret)
        self.say('Player', "Is it a breadbox?")
        self.say('Computer', "No, it's not.")
        while True:
            new_guess = self.ask('Player', "Is it more like a %s or more like a %s? "
                                 % (self.current_guess, '_____'))
            new_guess = new_guess.strip().lower()

            reply = self.guess_secret(new_guess)

            if reply is Reply.ExactlyEqual:
                self.say('Computer',
                         "That's exactly what I was thinking of! Awesome show! Great job!")
                break

            elif reply is Reply.LessLike:
                self.say('Computer',
                         "It's more like a %s..." % self.current_guess)
            elif reply is Reply.EquallyLike:
                self.say('Computer',
                         "Eh. They're about equally like the thing I'm thinking of...")
            elif reply is Reply.MoreLike:
                self.say('Computer',
                         "It's more like a %s..." % new_guess)
            else:
                self.say('Computer',
                         "Error, error, does not compute!")
                break


    def say(self, role, statement):
        """
        Print a message.
        """
        print("%s: %s" % (self.names[role], statement))
        sleep(1)


    def ask(self, role, question):
        """
        Ask a question.
        """
        return input("%s: %s" % (self.names[role], question))


    def guess_secret(self, new_guess):
        """
        Try to guess the word.

        Arguments:
           new_guess: the word that the player guesses

        Return:
            A value from the Reply enumeration, indicating whether the guess is
            exactly equal to the secret word or less, equally or more like the
            secret word when compared to the current best guess.
        """

        # Check if new_guess is verbatim equal to the secret,
        # or if new_guess is closer or further away than the current guess.
        new_guess = new_guess.lower()
        new_guess_sim = self.semantic_space.get_sim(new_guess, self.secret)._getvalue()
        print(new_guess, new_guess_sim)

        if new_guess == self.secret:
            return Reply.ExactlyEqual

        elif new_guess_sim <  self.current_guess_sim:
            return Reply.LessLike

        elif new_guess_sim == self.current_guess_sim:
            return Reply.EquallyLike

        elif new_guess_sim  > self.current_guess_sim:
            self.current_guess = new_guess
            self.current_guess_sim = new_guess_sim
            return Reply.MoreLike


    @staticmethod
    def setup_names():
        """
        Setup the names dictionary for direct printing, by creating the player's
        name from the current user name and drawing the computer's name by
        randomly drawing from a large name corpus.
        """
        names = {
            'Player'   : getuser().title(),
            'Computer' : get_first_name()
        }
        maxlen = max([len(x) for x in names])
        return {
            role: name.ljust(maxlen, ' ')
            for role, name in names.items()
        }


# If Breadbox is run as a script.
if __name__ == "__main__":


    class SemanticSpaceManager(BaseManager): pass
    SemanticSpaceManager.register('is_english')
    SemanticSpaceManager.register('get_random_word')
    SemanticSpaceManager.register('get_sim')


    address = ('localhost', 6000)
    authkey = b'szxzcJVYgdZaN5PAqpp6fAKRmh4BvqT6mXLbAMuAQmHSpBAX'
    manager = SemanticSpaceManager(address=address, authkey=authkey)
    current_process().authkey = authkey
    manager.connect()


    Breadbox(manager).start()
