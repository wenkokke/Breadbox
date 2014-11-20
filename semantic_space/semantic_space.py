"""
Created on Aug 23, 2014

@author: Pepijn Kokke
"""
from composes.similarity.cos  import CosSimilarity
from composes.utils           import io_utils
from enchant                  import Dict
from multiprocessing          import current_process
from multiprocessing.managers import BaseManager
from os.path                  import dirname, join, realpath
from random                   import choice


# Configuration.
DATA_DIR = realpath(join(dirname(realpath(__file__)), 'data'))
DATA_FILE = realpath(join(DATA_DIR, 'EN-wform.w.5.cbow.neg10.400.subsmpl.pkl'))
#DATA_FILE = realpath(join(DATA_DIR, 'ex01.pkl'))


# API implementation.
class SemanticSpace(object):
    """
    Simple API for accessing various natural language functions.
    """

    def __init__(self, semantic_space, similarity=None):
        self.semantic_space = semantic_space
        self.similarity = similarity or CosSimilarity()
        self.en_us = Dict('en_US')
        self.en_gb = Dict('en_GB')
        self.words = [word for word
                      in self.semantic_space.id2row
                      if self.is_english(word)]

    def is_english(self, word):
        """
        Check if a string is a valid English word.
        """
        return word.isalpha() and (
            self.en_us.check(word) or self.en_gb.check(word))

    def get_random_word(self):
        """
        Return a random word from the corpus.
        """
        word = choice(self.words)
        print "Chose %s" % word
        return word

    def get_sim(self, word1, word2):
        """
        Return the similarity between two words.
        """
        word1 = word1.strip()
        word2 = word2.strip()
        return self.semantic_space.get_sim(word1, word2, self.similarity)


# Main script serving the semantic space.
if __name__ == '__main__':

    print "Loading Semantic Space..."
    semantic_space = SemanticSpace(io_utils.load(DATA_FILE))

    print "Setting up process manager..."
    class SemanticSpaceManager(BaseManager): pass
    SemanticSpaceManager.register('is_english', semantic_space.is_english)
    SemanticSpaceManager.register('get_random_word', semantic_space.get_random_word)
    SemanticSpaceManager.register('get_sim', semantic_space.get_sim)

    print "Starting up server..."
    address = ('localhost', 6000)
    authkey = b'szxzcJVYgdZaN5PAqpp6fAKRmh4BvqT6mXLbAMuAQmHSpBAX'
    current_process().authkey = authkey
    manager = SemanticSpaceManager(address=address, authkey=authkey)

    server = manager.get_server()
    print "Server started."
    server.serve_forever()
