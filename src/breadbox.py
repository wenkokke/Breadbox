"""
Created on Aug 22, 2014

@author: Pepijn Kokke
"""
import os
import sys

from composes.similarity.cos import CosSimilarity
from enchant                 import Dict
from enum                    import Enum
from random                  import choice


class CaptureIO(object):

    def __enter__(self):
        sys.stdout = open(os.devnull, 'w')
        return self

    def __exit__(self, *args):
        sys.stdout = sys.__stdout__


class Breadbox(object):
    """
    Implementation of the Breadbox game.
    """


    Reply = Enum('Reply', 'LessLike EquallyLike MoreLike ExactlyEqual')


    def __init__(self, semantic_space, similarity=None):
        """
        Constructor.

        Args:
            data: file containing a pickled semantic space

        Returns:
            An instance of the Breadbox game.
        """
        self._semantic_space = semantic_space
        self._similarity = similarity or CosSimilarity()
        self._rows = self.__rows()
        self.reset()


    # Compute the rowset based on the semantic space.
    def __rows(self):
        en_us = Dict('en_US')
        en_gb = Dict('en_GB')
        return [word for word in self._semantic_space.id2row
                if word.isalpha() and (en_us.check(word) or en_gb.check(word))]


    # Generate a new secret and use it internally.
    def __generate_secret(self):
        return choice(self._rows)


    # Compute the similarity between a guess word and the internal secret.
    def __secret_sim(self, guess):
        with CaptureIO():
            return self._semantic_space.get_sim(
                self._secret, guess, self._similarity)


    @property
    def current(self):
        """
        Get the current best guess.
        """
        return self._current


    def reset(self):
        """
        Reset the Breadbox game by generating a new secret word.
        """
        self._secret = self.__generate_secret()
        print "(Shh! The secret is %s)" % self._secret
        self._current = 'breadbox'
        self._current_sim = self.__secret_sim(self._current)


    def guess(self, guess):
        """
        Try to guess the word.

        Arguments:
            word: the word that the player guesses

        Return:
            A value from the Reply enumeration, indicating whether the guess is
            exactly equal to the secret word or less, equally or more like the
            secret word when compared to the current best guess.
        """

        # Check if the guess is correct.
        guess = guess.lower()
        if guess == self._secret:
            return Breadbox.Reply.ExactlyEqual

        # Check if the guess is less, equally or more like the secret
        # than the current guess.
        guess_sim = self.__secret_sim(guess)
        if guess_sim < self._current_sim:
            return Breadbox.Reply.LessLike

        elif guess_sim == self._current_sim:
            return Breadbox.Reply.EquallyLike

        elif guess_sim > self._current_sim:
            self._current = guess
            self._current_sim = guess_sim
            return Breadbox.Reply.MoreLike
