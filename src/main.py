"""
Created on Aug 22, 2014

@author: Pepijn Kokke
"""
import os, time

from breadbox       import Breadbox
from composes.utils import io_utils
from enum           import Enum
from getpass        import getuser
from names          import get_first_name


data_dir  = os.path.realpath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '../data'))
data_file = os.path.join(data_dir, 'EN-wform.w.5.cbow.neg10.400.subsmpl.pkl')
# data_file = os.path.join(data_dir, 'ex01.pkl')

class BreadboxCli(Breadbox):
    """
    Command-line client for the Breadbox game.
    """

    def __init__(self):
        semantic_space = io_utils.load(data_file)
        self.names = {
            'Player'   : getuser().title(),
            'Computer' : get_first_name()
        }
        max_length = max(map(len, self.names))
        self.names = {
            role: name.ljust(max_length, ' ') for role, name in self.names.items()}
        Breadbox.__init__(self, semantic_space)


    def __statement(self, msg, role='Computer'):
        time.sleep(1)
        print "%s: %s" % (self.names[role], msg)


    def __guess(self):
        # Get input from the user.
        time.sleep(1)
        msg = "%s: Is it more like a %s or more like a %s? "
        guess = raw_input(msg % (self.names['Player'], self.current, '[ ]'))

        # Reply.
        reply = self.guess(guess)
        if reply is Breadbox.Reply.ExactlyEqual:
            self.__statement(
                "It was EXACTLY a %s! YOU WIN!!1 :D" % guess)
            return True

        elif reply is Breadbox.Reply.LessLike:
            self.__statement(
                "It's more like a %s..." % self.current)

        elif reply is Breadbox.Reply.EquallyLike:
            self.__statement(
                "Eh. They're about equally like the thing I'm thinking of.")

        elif reply is Breadbox.Reply.MoreLike:
            self.__statement(
                "It's more like a %s..." % guess)
        return False


    def start(self):
        self.__statement("I'm thinking of something...")
        self.__statement("Is it a breadbox?", 'Player')
        self.__statement("No, it's not a breadbox.")
        while True:
            if self.__guess():
                break

if __name__ == "__main__":
    print 'Setting up Breadbox...'
    breadbox = BreadboxCli()
    breadbox.start()
