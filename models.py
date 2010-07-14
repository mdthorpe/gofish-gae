import random

from google.appengine.ext import db

class Deck(db.Model):
  cards = db.ListProperty(long)
  discards = db.ListProperty(long)

  def get_cards(self):
    return self.cards

class Game(db.Model):
  in_progress = db.BooleanProperty()
  game_deck = db.ReferenceProperty(Deck)

class Player(db.Model):
  nickname = db.StringProperty()
  game = db.ReferenceProperty(Game)
  hand = db.ListProperty(long)

  def get_cards(self):
    return self.hand

  def is_ai_player(self):
    return False

class AiPlayer(Player):
  """
  Will eventually contain actual game logic methods
  like "do_turn"
  """
  def is_ai_player(self):
    return True
