import random
import logging

from google.appengine.ext import db

class Hand(db.Model):
  cards = db.ListProperty(int)
  discards = db.ListProperty(int)

  def get_cards(self): 
    return self.cards

  def set_cards(self,new_cards):
    self.cards = new_cards
    self.save()
    return self.cards

  def get_fancy_cards(self):
    fancy_cards = []
    for card in self.cards:
      card_value = self.get_card_value(card)
      card_suit = self.get_card_suit(card)
      fancy_cards.append(card_value+card_suit)
    return fancy_cards

  def get_card_value(self, card):
    return str((card/4)+1)

  def get_card_suit(self, card):
    suits = ["S","H","C","D"]
    index = card%4
    return suits[index] 

class Game(db.Model):
  in_progress = db.BooleanProperty()
  deck = db.ReferenceProperty(Hand)


class Player(db.Model):
  nickname = db.StringProperty()
  game = db.ReferenceProperty(Game)
  hand = db.ReferenceProperty(Hand)

  def is_ai_player(self):
    return False

  def take_cards(self, deck, num_cards):
    deck_cards = deck.get_cards()
    player_hand = self.hand.get_cards()

    for num in range(0,num_cards):
      player_hand.append(deck_cards.pop(-1))

    deck.set_cards(deck_cards)
    self.hand.set_cards(player_hand)


class AiPlayer(Player):
  """
  Will eventually contain actual game logic methods
  like "do_turn"
  """
  def is_ai_player(self):
    return True
