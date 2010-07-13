import random

from google.appengine.ext import db

class Card(object):
  card_number = db.IntegerProperty()

  def __init__(self, card_number):
    self.card_number = card_number

class Deck(db.Model):
  cards = db.ListProperty(int)
  discards = db.ListProperty(int)

  def __init__(self):
    self.cards = range(0,52) 

class Player(db.Model):
  player_nick = db.StringProperty()

class Game(db.Model):
  human_player = db.StringProperty()
  in_progress = db.BooleanProperty()
  num_ai_opponents = db.IntegerProperty()
  #game_deck = db.ReferenceProperty(Deck)
