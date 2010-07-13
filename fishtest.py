#!/usr/bin/env python

import random
import time
import hashlib
from datetime import date

class Card(object):
  CardNumber = None
  Suits = ['C','D','H','S']

  def  __init__(self,card_number):
    self.CardNumber = card_number
  
  def get_value(self):
    return (self.CardNumber%13)+1

  def get_suit(self):
    return self.Suits[(self.CardNumber/13)]

class Hand(object):
  pass

class Deck(Hand):
  Cards = list()

  def __init__(self):
    for i in range(0,52): 
      self.Cards.append(Card(i))
      random.shuffle(self.Cards)

  def shuffle(self):
    random.shuffle(self.Cards)

class GoFishGame(object):
  Deck = None

  def __init__(self):
    self.Deck = Deck()

  def Deck(self):
    Cards = []


def main():
  go_fish_game = GoFishGame()


if __name__ == "__main__":
  main()
