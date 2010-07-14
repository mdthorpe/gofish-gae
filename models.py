import random

from google.appengine.ext import db

class Card(object):
  card_number = db.IntegerProperty()

  def __init__(self, card_number):
    self.card_number = card_number

class Deck(db.Model):
  cards = db.ListProperty(long)
  discards = db.ListProperty(long)

class Game(db.Model):
  human_player = db.StringProperty()
  in_progress = db.BooleanProperty()
  num_ai_opponents = db.IntegerProperty()
  game_deck = db.ReferenceProperty(Deck)

class AiPlayer(db.Model):
  nickname = db.StringProperty()
  game = db.ReferenceProperty(Game)
  hand = db.ListProperty(long)

